# V2 — I3 public reader / exact REQUEST integration backcheck

2026-10-05. **READY for bounded manager fan-in** at the seals below. No unresolved blocking, major or minor finding in the scoped shared read/writer/UI flow or narrow REQUEST guard. This is own-code/source validation, not native human-act proof, Group D adoption, whole AUM review or I3 closure. TASK `/root/group_a_execution/aac_contract_review`, parent WORKING_ITEMS `/root/group_a_execution`, delegated-harness-native; no delegation/model-diversity claim.

## Exact candidate

| Subject | SHA-256 |
|---|---|
| changes/I3-READER-INTEGRATION.md | b4477a32e2035b17c142f9d5222e61a27a8addb433b6c8cc830f1e1469bfcb9d |
| lib.rs | c86894e541a4925a3581873d99ee0632eae0333768b06dbe21120f1d6bce6cbe |
| runtime_session.rs | 1055c7930afba5e970cc5912cfb8ff11edf9683d115704193388c3ea59e3c2d7 |
| act_control.rs, narrow private REQUEST guard | 27beab5887fc9235dc9da09e30c879be54abe8eb3d868ff10c1a4fb16a7e9fac |
| App.tsx | cc6a6cf2c2bd7e280ac59329e395e1bee8850ec485d03b88d7db138ee9ae7078 |
| tests/reader_integration.rs | 79a7a3970671e50336800e0ec73f9bc98ea904b5813a9f0b49a691bb52647878 |
| decision_view.rs, reviewed Core input | ed417172630d6b2833da76134eb184e77112374c738a98b26241772aaa7ddc17 |

All source hashes checked before and after independent focused checks. Inputs include named RS/DV warranted-order definition and concurrence; final Core's independent review is reused rather than broad substantive repetition.

## Source conclusions

Public `decision_view` calls `read_decision_packages`, which only derives the Core view and adds workspace/readOnly metadata; copying cached writerStatus mutates only the returned JSON. No control/writer enters that helper, no append/recovery/ownership/backlink operation runs. UI refresh and host polling cannot call the writer. Actual test census compares directory/file names, bytes and modification times, rather than treating readOnly:true as proof.

The separate startup/explicit command calls existing `refresh_recording`: native recovery first, ordinary package recorder only if writer_ready; absent native state returns a visible hold without fallback. Startup and command use the same act mutex/continuation; reader holds no act state. Trusted native pending ordinals, late-write facts and durable capture/recovery boundaries are preserved; reads neither clear pending state nor manufacture a capture. UI presents cached writer outcomes and limits separately from source-derived decision standing.

OfferSlot privately clones the complete validated request at compose. The renderer cannot supply or replace this field. Compose's original complete-set/duplicate refusal remains stricter than reader presentation of identical copies. Both confirmation_text (before native dialog) and confirm (after affirmative native dialog, before capture-ID mint/durable capture or record) require the offered reference to equal that original recordId, exactly one validated readable matching entry, and complete parsed Value equality. Missing target, changed sole record or multiple bound-ID entries refuse and mark stale. Matching by all kinds prevents a same-ID different-kind entry being silently ignored. Structural equality includes every record/body/header fact; this is not a weakened requestRef-only/body-subset comparison.

Unrelated post-compose read limits are not a blanket human-act veto. An unchanged readable target plus unrelated partial final append tail may still capture the native-confirmed facts, retaining them pending under existing writer guards. An unreadable/removed/changed actual target yields no equal matching entry and refuses. Prior ACT ambiguity never becomes a fresh authorization rule. This preserves source meanings of capture/observation/written time, native source/actor/frozen offer/choice/digest/package checks and pending writer admission order. The unchanged lib native path still freezes Host-built text, uses the native dialog and rechecks actor/owning-host context before confirm; synthetic test calls do not prove physical confirmation.

UI receives Core requestResolution/sources and contenders without selecting a path/clock winner. Ambiguous current standing is explicitly not pending human-act standing. Equivalent agreeing capture copies retain original sources/times without arbitrary alias. CurrentContentComparison, historyResolution/historyIncomplete and raw source/history details separate known current bytes from incomplete past observations; no origin, grant, role or witness upgrade is implied.

## Actual evidence and proportionate independent checking

Original actual REQUEST reproductions **0/3, exit101** remain historical failures: complete conflicting identity before presentation, after native presentation, and changed sole valid request. Initial fixtures' incidental sequence failures were separately corrected to complete schema/sequence-valid logs; they did not prove REQUEST safety. First broad read-limit repair's **19/24, exit101** was a real source regression against five unchanged hot-pending/late-write controls and is retained. Neither a passing unrelated suite nor those invalid fixture attempts releases the original missing checks.

Final owner evidence: reader10 plus affected32 **42/42**; separately credited Core **54/54** on combined source; TypeScript/Vite build and static SSR pass. These are author/source-owner results, not independent reruns here. Initial npm wrong-cwd exit254 and initial reader fixture/setup failures remain recorded. No criterion, schema or P0 pending oracle was relaxed.

Parent granted a serialized narrow Cargo slot. Reviewer ran with `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CARGO_NET_OFFLINE=true CHIRALITY_SKIP_CODEX=1`, offline/locked in app/src-tauri:

- `cargo test --offline --locked --test reader_integration actual_offer_request_binding_`: **3/3 PASS**, exit0, compile0.74s/run0.46s; all three original refusal assertions, with valid complete input and no-write census.
- `cargo test --offline --locked --test reader_integration explicit_writer_preserves_hot_pending_flush_before_ordinary_requests_and_read_stays_pure -- --exact`: **1/1 PASS**, exit0, compile0.15s/run0.44s; real scratch permission failure, hot retention/hold, pure reads, explicit retry and pending act before ordinary second request.

Existing unused common evidence_output warning retained. Cargo released promptly. No broad42/54 repeat or live/native/model/Auth execution. Missing-target rejection is source-established by empty-match equality; no independent new missing-target case is claimed. Remaining native/custody/physical crash/source-authenticity qualification obligations stay at their owners.

## Method

Applied software-code-review skill ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca; Root/TASK/v4 LOOP provenance retained in earlier assigned reviews and this run. Only this report written; product/Design/schema/Git unchanged. Review scope is related shared integration plus private REQUEST repair, not a blanket act-control security audit. Preservation comparison is recorded below.

Full bounded delta compared with Parent-provided immutable 523408 archive at `/var/folders/0s/50y7rb796d1bqdxmpcz6qg800000gn/T/chirality-v4-523408-urg_p53g/projects/chirality-app-v4/app`. Baseline lib4ab7de274ac32b661d1af1c540a30680c699597e22da07bca700fa5a3b79a989 and runtimeed2e61b60828a2cd39510e919cc00bff733185e68120fa5726684ae11a940601 match the existing READY V3-I1-HISTORY-INTEGRATION-R1 source association. lib changes only read/writer status, pure read delegation, separate command, startup invocation and command registration; runtime only appends the two helpers. Actor/Host/history start/cleanup/ROLE receiving paths are otherwise unchanged. ActControl baseline1d55ff94ad08cf17673dfdae9a16e5ca7d9a98f52a1fe99a9f6101ea30a8876e delta is only private REQUEST field/clone/helper/two rechecks, plus the separately manager-owned comment from App Refresh to explicit startup/command writer; pending/recovery/native implementation is unchanged.

Archive App3e509ea07de283fc4dfd9ca8ea67d1196457a165bbc3e247990fb02dcec3f672 predates already-reviewed HistoryPanel/role display. To verify those carry-forward bytes without re-review or pretend historical file recovery, reviewer removed only the new DecisionPackagesPanel declaration/invocation in memory and reinstated the archived prior decision section. The resulting complete App SHA is exactly **316cd7b31c5d8b8857380779a02936e766c71374eebb12d406baebca2f4e1d4a**, the prior READY history frontend seal. No reconstruction was written or treated as an actual historical artifact. Thus the actual current frontend preserves that reviewed predecessor outside the exact decision-panel delta. New maintained reader tests inspected in full; no unrelated test oracle changes. Baseline/full source comparisons used file reads only, no Git operations. **Final bounded READY remains at the exact candidate above.**
