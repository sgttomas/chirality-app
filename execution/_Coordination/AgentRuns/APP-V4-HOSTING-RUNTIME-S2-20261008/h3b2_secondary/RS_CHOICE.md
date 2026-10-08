# H3B-2 retained attachment namespace use — RS source-owner choice

Recommendation: prepare named **CC-H3B2-NAMESPACE-USE-REVOCATION** as a narrow implementation-consequence clarification of the existing complete namespace/use guard. Extend the proposed admission fence to retained AttachmentCustody uses only after affected owners and independent design review. **No expanded implementation is authorized by this report.** Existing code hold remains.

TASK `/root/hosting_runtime_manager/rs_concurrence` under WORKING_ITEMS `/root/hosting_runtime_manager` under HELP_HUMAN `/root`; harness-native delegated source-owner assessment, no delegation. Read-only, 2026-10-08. No source/Design/pin/MEMORY/native/credential operations. This report prepares a concrete choice for the parent; it is neither human acceptance nor implementation review.

## Existing requirement and actual gap

The final R1 definition of CC-NIR-KEY-HOME-CUSTODY-FIT explicitly requires the complete known account/key/probe home and declared native-resource closure, checked after directory preparation, **when bindings change and at use before metadata reads/publication and the dispatch barrier**. It explicitly says a cached constructor or intended link alone proves no future closure. Its final definition/concurrences retain fixed S/C/L paths, no native content scan, and affected attachment unavailability without a blanket native plaintext veto. CC-REC-NATIVE-NAMESPACE-GUARD separately protects the ledger and requires prospective admission before changing healthy current bindings.

This is an already documented protective invariant, not a new user goal. The later V2 guard review identifies these final definition packets as accepted input. That review's separate NG-1 blocker is historical and does not establish an overall current pass; this assessment borrows no implementation verdict from it. Current canonical Design alone does not spell out an epoch/lease mechanism. The named packet is the specific source of the complete-scope use requirement.

The new audit identifies a source-reachable violation: lib submit_attachments clones an AttachmentCustody before slot replacement, and the clone retains its immutable old namespace Arc. Later new-key admission expands protected scope but cannot update that clone. The clone can resume after new-key drift without checking the newly admitted domain. Destinations remain fixed; this is not a reproduced arbitrary-write exploit. It is a stale protective-scope defect against the existing at-use requirement. Slot replacement or a Store-only lease cannot close it.

## Proposed exact bounded contract statement

> After a namespace expansion is committed, every retained native attachment capability must either obtain the committed complete namespace for its guarded use or fail closed before metadata read/publication and dispatch. An operation already admitted under the previous namespace must finish its guarded use before the expansion commits, or detect invalidation and refuse before the dependent effect. Native reference/record identities and bytes are unchanged. Admission failure leaves the previous committed authority usable at its existing standing; successful namespace admission is distinct from later setup failure. Missing or drifted current closure preserves the existing precise attachment/REC availability limits and does not itself cancel turns, mutate credentials or prohibit unrelated safe plaintext operations.

This clarifies implementation consequences without changing S/C/L/ledger/distribution paths, record schemas, methods, human-act classes, home ownership, source roles or protection domains. A canonical semantic amendment is needed only if the parent instead chooses to weaken those existing guards, change failure scope, grant new authority from JSON/history, or change owning storage/record meaning. No such change is recommended. If the project's documentation convention places this clarification in owning Design, perform it as a named reviewed propagation; do not relabel historical bytes as though they specified the new mechanism.

## Concrete choices for design review

**Recommended: one stable native-owned namespace authority, operation leases and coordinated commit.** Retained attachment capabilities and Stores reference the same replaceable authoritative binding/epoch rather than old immutable snapshots. Each protected operation leases one coherent binding for its complete guarded reliance through the relevant metadata/dispatch barrier. Admission acquires exclusive authority nonblockingly, checks the prepared full-scope candidate and REC conditions, and changes the namespace once at the defined Store/attachment/REC commitment. Old clones share this authority and cannot resume on a superseded reduced set. Preserve existing native reference objects/root IDs/selection bytes; no serialized authority factory. Avoid recursive lease acquisition: nested helpers accept the held lease. Review actual Host attachment_gate, REC writer and source lock order before choosing the exact ordering; this report does not assume the Store→REC argument automatically covers attachments.

**Alternative: revocable attachment epoch plus coordinated operation gate.** Retain capability identity but require an authoritative epoch/use gate around every attachment read/publication/dispatch reliance. Admission excludes such operations, updates scope and epoch with Store/REC, and old capabilities fail closed or explicitly rebind under native custody. A check only at function entry/exit is insufficient if a write or dispatch can occur after epoch change. A lone atomic epoch with no effect coordination is therefore not an adequate alternative. This option may produce more user-visible attachment unavailability and has broader coverage risk than a shared holder.

Both choices require a concrete synchronization and linearization point. Neither proves atomicity against external filesystem mutations; existing fresh metadata checks and race limits persist. Nonblocking admission failure during active operations must preserve them, with an honest busy/setup limit, not interrupt or discard them. No all-App transaction or restart hydration claim is justified merely by this narrow native-authority transaction.

## Required owners and release conditions

- DEL-01-04 NIR/attachment owner: confirm supply/client association, prewrite readback, dispatch barrier, retained capability and failure semantics; own attachment-custody change.
- DEL-01-01 hosting/distribution and Root setup owners: coordinate Store use, key admission sequencing, complete actual namespace inputs and required capability installation before exposing new key work.
- DEL-01-02 REC owner: confirm sole-ledger/writer binding, queued source facts, lock ordering, failed versus committed admission and mandatory-reply/liveness limits.
- DEL-01-05 ACCESS/home owner: confirm unchanged account/key/probe and linked-resource custody; no credential/read/setup action outside existing authorization.
- DEL-04-03 RS: **concur with the proposed contract statement and evidence-preserving scope**, not an unreviewed synchronization implementation. Exact source references, standing and human-act distinction remain unchanged.

Parent selects and records the precise mechanism/fence after attachment and affected owner return; independent design review checks it before any code. The existing stale-clone trace should become a deterministic test: pause an old account capability, admit or contend with new-key binding, mutate the declared new-key resource relationship synthetically, and show no stale guarded use/dispatch succeeds. Add failed admission preservation, no mixed binding, old-reference readability, post-admission failure truthfulness and actual lock-order checks. No tests performed in this assessment.

## Evidence and currency

Read the audit at `/private/tmp/H3B_SECONDARY_LOCK_ATTACHMENT_AUDIT.md` (hash below) and the selected historical source packets/current source at `37feb501bbb23cc2932e0101a51a2ae63edbd489`. Parent reports receiving main has since advanced to fa71; this report does not claim those newer bytes were re-reviewed. Parent/design reviewer must check affected-source currency on the chosen candidate. No use of predecessor READY or source concurrence substitutes for that review.

| Source | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-NIR-KEY-HOME-CUSTODY-FIT.md` at `37feb501` | `5df0554883cb4ff7d89b0b480733b197f11ac03e0a02d3a2163aa3a820e9831e` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-REC-NATIVE-NAMESPACE-GUARD.md` at `37feb501` | `8f348991da3f927910bea3bdeb13391bfc4b2ee49b5459a0d4a81c35320847ad` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-NIR-KEY-HOME-CUSTODY-FIT.md` at `37feb501` | `8659df7131ed956e321115fc21c9c21c30aea8e771a0d61c5a90a99870bb464b` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V2-I1-NATIVE-NAMESPACE-GUARD.md` at `37feb501` | `734e8a9684b3469790ccecff0c7dd9cd0dacf639f489a7cc1068de5e13982949` |
| `projects/chirality-app-v4/app/src-tauri/src/attachment_custody.rs` at `37feb501` | `04f82cbd64fe5a9c40b57556a804c063740019d584f0cf68aeab9172a2d58082` |
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` at `37feb501` | `0d28e14e58827b47f94a453885709ecba8e8002ce1bf5cf1223dc18c68b2e50a` |
| `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` at `37feb501` | `1cf78544f67bf552eab3c3b62d6d0e4a2f07492cf6f3b5610acdc0d72c435a01` |
| `/private/tmp/H3B_SECONDARY_LOCK_ATTACHMENT_AUDIT.md` | `cfb20ea6bcbb429c02ea7417919f138c2c7a3f1c097afdc90d2fc0deadeded21` |
