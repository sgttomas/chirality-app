# H3B next residual readiness assessment

Basis: merged Git revision `f25ba6887d85904ebef2a6321c222809d47cfabd`. Read-only assessment; no build, product edit, native execution, or qualification. Source bytes were read from this exact Git object, not the frozen author's working diff.

## Recommendation

Implement actual **LT-23 after a completed same-H5 Stop**, initially for a successor generation with successfully published LT-09. This is a real Host-to-Store-to-native-read slice. Defer restart hydration, other transition rows, and collection/index design. Scope does not require S3 authority to exercise invented offline fixtures; production compiled selection remains absent and verified standing remains refused.

`Host::stop_inner` emits actual LT-17 (`ready/stop-requested/stopping`), LT-18 for handshaking, otherwise LT-19; after input close, process-group handling, EOF wait and generation recheck it emits LT-23 (`stopping/tree-ended/stopped`). LT-23 contains actual exitFacts, descendants and closedGeneration. Capture that entire unchanged event, its start_attempt and full generation at emission. Only an eligible ready/LT-09 predecessor is covered in this slice; do not claim the generic LT-19 branch is semantically valid for every pre-spawn state or repair unrelated legacy transitions here.

The existing full S1 reader permits LT-23 to reference the original immutable **pre-spawn** observation: artifact generation and verification_generation must agree, and nonnull legacy generation must equal them. It checks the original closed event schema, transition tuple, derived result/standing and version label joins when present. It does not demand a terminal observation phase. Preserve observation bytes/phase exactly; this envelope records a later event's association, not terminal integrity, a new probe, or renewed installed custody. Review this named producer support extension with the S1/RS owner; no schema or canonical meaning change proposed.

## Publication and race boundary

Retain current single-lifecycle-per-publication format. Publish a fresh immutable closure containing unchanged observation plus the actual LT-23 envelope; select it as the current reference only on successful readback. Previously issued LT-09 publications/references remain immutable and readable by their existing live holders. Do not introduce an envelope collection, claim discoverable historical indexing, or promise a new public LT-09-history interface. Explicitly update the native projection's supported-row statement and named producer/read-method identities; Group B must assess changed source identities, not silently repin.

Capture source facts under Inner, then release it before all Store work. No artifact I/O before close-input/kill/EOF handling, or under attachment/source/REC writer guards. Preserve Stop's operational success even if evidence fails. The simplest bounded implementation publishes synchronously **after cleanup and legacy LT-23 emission**, so artifact hashing may add return latency but cannot delay input closure/process handling or hold those global guards. Review that disclosed tradeoff; async publication would need a new pending/job lifetime interface and is not part of this recommendation.

Same attempt+generation alone is insufficient: existing LT-09 publication occurs outside locks and can finish after Stop. Introduce a narrowly scoped lifecycle-publication ordering token (actual event sequence plus attempt/full H5) for installation and errors. A late LT-09 cannot replace LT-23 or mark a newer terminal receipt unavailable. Eligibility requires an already successfully published LT-09 when Stop captures its source; a Stop racing initial LT-09 publication remains explicitly unsupported in the first slice. If restart/new attempt wins during terminal publication, discard installation/error mutation; preserve the old immutable artifact without assigning it to the new source. On same-source terminal publication failure, retain previous receipt internally but expose terminal evidence unavailable, never label LT-09 as LT-23 success. Test these exact schedules.

`Host::distribution_evidence` checks generation/attempt, not ready state; it therefore supports same-generation stopped readback already. Read must continue through current shared namespace lease, same validated Store descriptor, original compiled-anchor association and complete closure audit. Native adapter must expose actual terminal receipt without converting a stored JSON reference into native authority.

## Other rows and restart comparison

- LT-12 is emitted by `on_eof` for ready child end without a stop record (`ready/child-ended-without-stop-record/exited-unexpectedly`). It is a sensible following same-H5 slice, but has its own EOF/Stop ordering and source gates; exclude it from the smallest LT-23 change.
- LT-17/18/19 are intermediate stop events; LT-18 may lack published LT-09 and LT-19 includes unresolved pre-spawn mapping. LT-10/11 handshake failures and LT-04/24 prospective-H5 events need their own observation/source eligibility. Do not manufacture LT-13/14 merely because the transition table contains them; the inspected current Host has no matching emission path.
- Restart clears current successor reference at start. `S1Reference` deliberately skips native Files and publication identity in serialization. There is no accepted durable current-index discovery/hydration path. A cold historical reader could be implemented offline, but requires an explicit locator/index, corruption/ambiguity, namespace/anchor revalidation and historical-only standing contract. It cannot deserialize old JSON into current H5, current process custody, or live reference capability. This is larger and less ready than LT-23.
- S3 acquisition/extraction/probe/generated version-advance and installed integrity/custody issuer remain absent authority inputs, not excuses to omit synthetic producer machinery. SEAL-2/CI-10 concerns trustworthy persistent capture-origin replay and remains deferred; it is not established merely by distribution digests, and should not be asserted as an automatic prerequisite for every historical byte read. Any restored native/capture authority claim must separately satisfy its owner contract.

## Fence and acceptance

Proposed fence: hosting.rs successor publication/capture helpers and Stop completion; distribution_store_s1.rs narrowly generalized actual-event publisher with explicit supported rows; distribution_s1.rs only named method/support identity if needed; successor synthetic tests, maintained support documentation, and native reference projection wording. Preserve legacy event bytes, legacy dispatch, namespace/REC/attachment semantics, setup/UI/roles/workflow code, canonical schemas/pins and Group B source. No new restart API.

Deterministic tests in both default and distribution-successor+custom-protocol states: actual synthetic child ready→Stop→LT-23 full-event equality; same observation bytes/full H5; stopped native read; LT-09 immutability; wrong tuple/transition/subject and closure tamper refusal; namespace busy/rebind/replaced-root controls; publication failure after child cleanup; late LT-09 vs terminal installation; restart during terminal publication with no newer-source mutation; unsupported handshaking/pre-spawn cases truthful. Exercise graceful and forced synthetic termination without real supplier use. Independent source/contract review must inspect locks, actual event schema, publication ordering and original controls; then exact-head affected checks and Group B named receiving adoption. No broad build performed for this assessment.

## Exact source SHA-256

| Git path | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `2952406eeab874252de18fe3a263bd77c6e70f808d91c6cefdf2df4e4ee1cf52` |
| `projects/chirality-app-v4/app/src-tauri/src/distribution_store_s1.rs` | `e78664f9b422344f246099062c9247e484277095d8df2e570f247a02d469c8de` |
| `projects/chirality-app-v4/app/src-tauri/src/distribution_store.rs` | `9a5fd0308c80bc73b5fc4ca772f9aa13f3e0a73ca8dd271a9a87bc82205ba903` |
| `projects/chirality-app-v4/app/src-tauri/src/distribution_s1.rs` | `408302b9942b1a2eec8e08ab8f81f28700d4e40f69a049dba08ede62f1198ad1` |
| `projects/chirality-app-v4/app/src-tauri/src/distribution_selection.rs` | `b1e3ce5069c254ade3a8e73b9047f61076d48e483ba0ad8fe2013496dd856ff9` |
| `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` | `15425f6a48b31570447ab498b2a7c92f7870b2700d75fc9de1aef891af221f97` |
| `projects/chirality-app-v4/app/src-tauri/src/native_items.rs` | `05b2840fc07e8027ab9490395422663eb82da35dd3fa0d11ef106ce3540e5e7b` |
| `projects/chirality-app-v4/app/CONTRACT_ISSUES.md` | `d69721f2e5224bf98ceee5eb7d33bc0b6e0e20de3c44fd2de025d94cf0989311` |
