# I3-READER-ORDER-IMPLEMENTATION — actual decision-view CI12 repair

2026-10-05. TASK `/root/group_a_execution/design_records_exec`, parent WORKING_ITEMS `/root/group_a_execution`; no delegation. Status FROZEN FOR INDEPENDENT BACKCHECK; targeted offline validation passed; shared public-read wiring still owned by its separate lane. Writes only app/src-tauri/src/decision_view.rs, new tests/decision_reader.rs and this record. Existing records/storage/writer code, canonical fixtures, schemas, lib/App/runtime_session and other Designs unchanged. Source interpretation and DV concurrence independently READY; Root publication hold remains until exact product backcheck.

Actual derive now retains owning-log source/seq metadata, distinguishes identical copies from conflicting record IDs, and resolves target identities without last-map precedence. Explicit same-kind/reason correction links and applicable complete-stream correction observation order are validated; cycles/missing/ambiguous/wrong-kind targets cannot erase originals. Explicit compatible distinct-capture supersession links warrant a recorded relation; writer seq, capturedAt, observedAt, writtenAt, filenames and UUIDs never become a human performance chronology. No new external schema/kind/store/native admission or authorization policy.

Incomparable claims produce ambiguous current standing/decision null while every contender retains its own attributed capture, timing, content standing, lapse/restoration history and native-origin-unverified provenance. Matching records of one agreeing capture are one claim, not multiple later performances; aggregate history uses exact attributed record links, all source projections remain. With no unique direct-capture record the aggregate has no arbitrary scalar act-ID/recorder/timestamp winner; equivalentCaptureRecords identifies all records. Same-capture disagreements stay visible and unresolved. Correction versus later decision remains distinct. No writes from derive.

Request resolution is separate from prior ACT uncertainty: differing facts under one request ID are unresolvable request identity; identical copies resolve the same unchanged claim with all sources, not a request selection policy. Existing storage/native-offer/replay admission limits remain untouched, including conservative duplicate handling; prior ACT ambiguity alone adds no fresh-act veto.

Consumer interface (derived JSON, not a governed RS format): row.requestResolution/requestSources, contenders/currentCandidates, existing row.decision only when warranted. Each projection retains existing attribution/lapse fields plus recordSources, recordedAt, observedAt, orderingMeaning, correctionTarget/correctedBy, relationUnresolved and claimLimits. Shared owner wires lib/App/runtime_session public read purity and separate existing writer continuation; this TASK does not edit shared files. ActControl's stale Refresh comment is outside fence and returned to manager for comment-only follow-through.

Targeted executable tests prepared: actual AB/BA discovery for independent claims and competing same-target corrections, exact contender lapse/restoration preservation, valid single-stream correction, distinct capture with explicit causal supersession, same-capture disagreement, late-record seq not capture order, missing/wrong-kind/self/cyclic correction target, identical versus conflicting request IDs, conflicting act IDs under explicit read paths, missing correction reason and agreeing same-capture history aggregation. Fixtures are invented claims; no person performed a native act. Old canonical history/oracles unchanged. Expected future serial command covers decision_reader, decision_standing, decide_flow and relevant act_storage writer/custody regressions. No all-future-R1–R8/version/general standing completion claim.

## Source inputs

| Source | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-RS-READER-ORDER.md` | `df7e4be855faa1adf8894c88265a81b4a9af58ba3da4b0c5c4442d231eb7ed1f` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-RS-READER-ORDER.md` | `2d86256a03df3fdd6435e29f7e248936331a25d9fd80ef2bc8dcda2d70b7767e` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-DV-READER-ORDER-CONCURRENCE.md` | `9674af0e0d6e19de9b4ceb06a97bbfd4aac6b3f1fe0bd9f9d0d1a09f9b0c8ff1` |

Current preparation hashes are intentionally not a final product freeze; they will be recorded with actual test results after the serial slot.

## Actual validation and repair history

First offline/locked full run compiled the prepared core and returned act_storage 23/24: unchanged P0 pending-before-fresh confirmation oracle expected ALT-2 but reader returned null. This failure is preserved separately from final success; no test/reference/producer criterion changed. Added bounded reported-native-admission-stream consumption under the source supplement in CC-RS-READER-ORDER (fields alone are forgeable; no native verification/grant/admission). One mistaken Cargo invocation from repository root reported no Cargo.toml and executed no tests; corrected only workdir.

Final locked offline command in app/src-tauri: `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --test decision_reader --test decision_standing --test decide_flow --test act_storage` → exit0, act_storage24/24, decide_flow4/4, decision_reader12/12, decision_standing9/9. After adding missing/mismatched-marker and cross-stream forged-marker negatives, affected `--test decision_reader` rerun →13/13. Thus 50 distinct focused tests pass. Only existing shared tests/common unused evidence_output warning emitted; no source repair for that unrelated warning.

Exact ORIGINAL synthetic 18-entry AB/BA scratch reproduction inputs (embedded in the named source-definition evidence) were replayed through the actual repaired derive/storage path using the original Rust path-dependency driver, offline/locked: all four outputs now `ambiguous current standing`, no filename-selected scalar act/alternative/correction winner. A's lapse/restoration remains in its own contender in the actual decision_reader tests, B's history remains empty. No input/oracle/actor provenance changed. Old historical RV8 remains historical reused-capture evidence; new distinct-capture explicit-link positive and same-capture disagreement negative establish the receiving distinction without recasting that old fixture.

No actual human/native/model/provider witness was performed. No schema/record-format, original fixture or production lock update. Full future version-aware/general R1–R8 reader work is not claimed complete by this targeted CI12 fix. Existing strict writer/replay/legacy discovery remain unchanged. Cargo slot released before shared public-reader consumer tests.

## Source warrant and derived interface

Explicit correction/compatible distinct-capture supersession links and correction-only applicable stream order warrant recorded relation projection. P0's declared native writer queue may supply source-reported captured observation order for same complete stream with original matching observedAt/captureTime; reader never treats the forgeable header as native proof, parses time chronology, feeds AdmittedAct or changes control grants. Projection orderingEvidence identifies that limited warrant. Missing/mismatched markers, unrelated streams, repeated same capture and incomparable branches do not acquire this order.

row.requestResolution is `unique claim`, `unique claim (identical copies)` or `conflicting identity`; row.requestSources retains every log/seq. Conflicting request facts yield `unresolvable request identity`, not a path-picked offer. ACT ambiguity remains separate with state `ambiguous current standing`, decision null, contenders and currentCandidates. Agreeing repeated capture is one claim with equivalentCaptureRecords and aggregate attributed history; no arbitrary scalar ID/recorder/time chosen when direct record is not unique. All per-record metadata persists in contenders. Actual/native origin remains unverified. Shared owner received exact fields and keeps read purity/compose policy separate; prior ACT uncertainty is not a new act prohibition.

## Frozen outputs and retained input evidence

| Output/input | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/decision_view.rs` | `15d0c9b0faad082636db9366009f3b58bdef99e66af0b0f5e7588a5f00f5c65e` |
| `projects/chirality-app-v4/app/src-tauri/tests/decision_reader.rs` | `25db7fa83823bac4dfae81a056483b510bffe827026eda99ba5122af2c3132f0` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-RS-READER-ORDER.md` | `5d65ec503c78cad5ebc1706bd98539dab2eaae11ada2ebc032d6c37fd49940ae` |
| `/tmp/chirality-rs-order-i6z7odqv/outcomes.repaired.jsonl` | `abc6a1759ab2d092c41bb289a965d0fcb74243f59766a5b885c56d43b34e2072` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.lock` | `2fad2d658b3ffaf7b3973d5ab7da693788613f7462eaeca9d4b6b9ad826f7012` |

Actual repaired raw replay:

```jsonl
{"alternative":null,"earlierActs":null,"lapseHistory":null,"limits":[],"rowLimits":["lapse history is a recorded observation claim; native origin not verified","ambiguous/unresolved current recorded claims; no warranted total order or later human performance"],"scenario":"acts-ab","selectedClaim":null,"state":"ambiguous current standing"}
{"alternative":null,"earlierActs":null,"lapseHistory":null,"limits":[],"rowLimits":["lapse history is a recorded observation claim; native origin not verified","ambiguous/unresolved current recorded claims; no warranted total order or later human performance"],"scenario":"acts-ba","selectedClaim":null,"state":"ambiguous current standing"}
{"alternative":null,"earlierActs":null,"lapseHistory":null,"limits":[],"rowLimits":["lapse history is a recorded observation claim; native origin not verified","recorders disagree: one capture has incompatible readable claims, not later performances","ambiguous/unresolved current recorded claims; no warranted total order or later human performance"],"scenario":"corrections-ab","selectedClaim":null,"state":"ambiguous current standing"}
{"alternative":null,"earlierActs":null,"lapseHistory":null,"limits":[],"rowLimits":["lapse history is a recorded observation claim; native origin not verified","recorders disagree: one capture has incompatible readable claims, not later performances","ambiguous/unresolved current recorded claims; no warranted total order or later human performance"],"scenario":"corrections-ba","selectedClaim":null,"state":"ambiguous current standing"}
```

## CI12 residual R1 repair and original-probe backcheck candidate

Independent reviewer found original frozen decision_view15d0 still scanned raw lapse observations without global identity resolution. In its actual control, valid lapse-a produced matches-c0-again; adding a schema-valid different act_lapsed body under the SAME recordId (c1=c0) left restoration resolved despite the global duplicate conflict. Original candidate and 50-test pass remain historical, not repaired evidence. Do not treat a test rerun as proof that this defect was fixed without the original trigger.

Successor resolved-history lookup excludes globally conflicting/invalid/cyclic observation IDs. Every raw observation claim retains its exact parsed RS record and owning log/seq; no map-last body is selected. Per-contender historyResolution and lapse show unknown/unresolvable past dependency, while currentContentComparison and existing current identity remain separate. Same agreeing capture aliases and aggregate propagate that dependency; identical copies deduplicate the resolved observation ID but retain both source claims. No unknown past is silently mapped to not-lapsed. Existing malformed unique observation/method/scope controls, raw content, actor provenance, P0 source-reported admission order and native/cold admission rules remain unchanged.

New exact regressions: conflicting lapse-ID trigger versus unchanged valid control; identical lapse copies versus conflicting bodies; agreeing same-capture alias/aggregate propagation and current-content separation. All three new cases supplement the original 13 reader tests. Full offline locked command with decision_reader, decision_standing, decide_flow, act_storage → exit0: 16+9+4+24=53 distinct tests passed. Existing historical fixtures/oracles retained; no writer/shared/schema/production-lock edits. Cargo slot released after exact probe replay.

Actual independent probe driver/source/inputs remained unchanged and reran against repaired current crate:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CARGO_TARGET_DIR=/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/app/src-tauri/target cargo run --offline --locked --manifest-path /private/tmp/chirality-reader-review-_ppu0fu_/Cargo.toml -- /private/tmp/chirality-reader-review-_ppu0fu_/inputs
```

Exit0. valid-lapse remains decided ALT1/matches-c0-again/resolved history; conflicting-lapse remains a recorded ALT1 claim but past lapse is unknown/unresolvable, no resolved lapse ID, current content separately matches c0. Complete source-reported stream still ALT2; incomplete stream ambiguous with no chosen decision. A summary script initially attempted .get on the expected null incomplete-stream decision; raw actual driver exit/output were unchanged and correct (reporting-script error only).

Current derived additions for shared receiver: historyResolution, lapseObservationClaims [{record,source:{log,seq},resolution}], historyRecordRefs (same agreeing capture aliases), currentContentComparison. These are ephemeral view diagnostics, not new governed RS types or proof of origin. Shared source owner receives the exact successor hashes for affected consumer backcheck.

Prior implementation record SHA-256 `32925b0f71ed69d2db8e7dfeec352ddf7e26a6b916668e8eeb61b2bb73b723c1` remains associated with original15d0 candidate. Successor seals:

| File/evidence | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/decision_view.rs` | `c76c85f2c6e1f961c0ef43b765f1e3cbfbbec377c55d25f696607932b45ca6b0` |
| `projects/chirality-app-v4/app/src-tauri/tests/decision_reader.rs` | `74bf305c3f54d478cca52738ba19a11fb159064c21fb4a658b592fd69d8ea0fe` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-RS-READER-ORDER.md` | `e77d8b20947e9bafdea2bcc4fe396a2628e67eeed6eeac283727e23dcbeeb7f6` |
| `/private/tmp/chirality-reader-review-_ppu0fu_/src/main.rs` | `0c28e184395d794c4ba071bcdf653ee5672078ce956ec08cb3b8720e2fa74387` |
| `/tmp/ci12-lapse-repaired-outcomes.jsonl` | `34aec17455d65e33d645064135e462471beabaf7b4eae70fb06f4e704b42f87c` |

Actual probe summary:

- `valid-lapse`: state `decided`, alternative `ALT-1`, lapse `matches c0 again after observed lapse`, past `resolved recorded history`, current `matches bound content`, resolved IDs `['rec:synthetic:lapse-a']`.
- `conflicting-lapse`: state `decided`, alternative `ALT-1`, lapse `unknown (lapse history unresolved)`, past `unknown/unresolvable past observation`, current `matches bound content`, resolved IDs `[]`.
- `complete-stream`: state `decided`, alternative `ALT-2`, lapse `not lapsed`, past `resolved recorded history`, current `matches bound content`, resolved IDs `[]`.
- `incomplete-stream`: state `ambiguous current standing`, alternative `None`, lapse `None`, past `None`, current `None`, resolved IDs `None`.

## R1 independent-witness preservation successor

Reviewer source backcheck raised a precise remaining over-conservative behavior in c76: any unresolved history observation forced unknown, even when another globally unique qualifying observation already independently established a prior lapse. c76/53-pass and the original residual findings remain preserved, not silently relabelled as this successor's evidence. Criterion unchanged: unusable/conflicting bodies cannot establish restoration, but independently warranted good observation must not be erased merely because total history is incomplete.

Successor tracks historyIncomplete separately from whether at least one resolved qualifying prior-lapse witness exists. Duplicate-only original trigger remains unknown/unresolvable past with current identity separately matching. Separate good-ID witness plus a different conflicted ID yields matches-c0-again with `historyResolution: established prior lapse; history incomplete` and historyIncomplete true. Only good ID enters lapseHistory; every conflicted body/source/limit remains visible. This applies per contender and same agreeing capture aggregate/aliases, without native verification, read writes, new act gate, timestamp order or source rewrite.

Added exact `independent_good_lapse_witness_survives_other_conflicting_id_without_claiming_complete_history` consumer test with singleton and agreeing-alias variants; prior duplicate-only/valid/identical-copy controls unchanged. Locked offline combined current-source suites after shared slot release: decision_reader17/17, decision_standing9/9, decide_flow4/4, act_storage24/24, total54 distinct, exit0. Shared native request guard source was included in this actual combined compile and existing storage oracle passed; no shared/writer edits by this TASK. Cargo released promptly. Shared consumer will rerun its own affected interface checks on this exact seal.

Parent authorized preparation while shared guard tests held Cargo; on-disk core changed from c76 during that lane's run. Shared owner was informed to qualify the earlier guard-specific initiated basis, not claim unchanged on-disk c76 or final successor coverage. This final combined run establishes the actual successor core tests; shared consumer evidence remains its own responsibility. No product source mutation occurred during this final run.

Prior implementation record SHA-256 `a191147a759fec2256047e47638f8a234f05b0202da98d069783a29cb84d7a51` remains associated with c76. Final successor seals:

| Output/source | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/decision_view.rs` | `ed417172630d6b2833da76134eb184e77112374c738a98b26241772aaa7ddc17` |
| `projects/chirality-app-v4/app/src-tauri/tests/decision_reader.rs` | `7fbd2ab9b271f2fda5c02d87d2306ca223122f1a0fc16ae9632a9583d9f778fe` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-RS-READER-ORDER.md` | `e471f2d11814e395f37328b73f8ad2cfc51860c722fa4784cd793e230e765557` |
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `27beab5887fc9235dc9da09e30c879be54abe8eb3d868ff10c1a4fb16a7e9fac` |
| `projects/chirality-app-v4/app/src-tauri/Cargo.lock` | `2fad2d658b3ffaf7b3973d5ab7da693788613f7462eaeca9d4b6b9ad826f7012` |
