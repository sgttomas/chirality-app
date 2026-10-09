# Published-entry direct recheck: reviewed source and release interface

PROPOSED technical selection; production code remains held for HELP_HUMAN's
explicit bounded release. Current source basis9a82cbcf29c46bb6f722c074b5854de7ef470450.
Exact proposal `a10db615a16575f78c74d12b2f3c74ebc3b1e25d01f2bae5b2a0b0cf893725bc`,
24 designed cases `6d6166f1ee2ec668c3ba80fb6dad4f07375477c1aa1904e67a58704c7ca8ecb4`,
basis `6338665dc8ace3b9596a11c99008285cd20085c520e671c13d6a504df9cc47c9`.

## Actual reviews

Existing DEL-07-02 TASK cfb_design_owner prepared the source. Independent TASK
cfb_design_review returned READY on exact a10db615 as a source/fence proposal,
not code release. It verified six source pins and24 designed cases, actual loss
of success-path store custody today, narrow direct-read semantics and resource/
concurrency limits. Proportionality is justified by the existing draft UI and
actual publication input; no new framework or standalone exporter is needed.

Host/storage returned conditional CONCUR on555d, then exact a10db615 backcheck
with no remaining source blocker. Both actual reports are retained byte-exact:
C3_PUB_RECHECK_HOST_STORAGE_REVIEW.md SHA256
`5e79966f995cdee0d5ed6b7f51ef5ca894ff165b6925989c5535feca8e8fea95`;
HOST_STORAGE_BACKCHECK.md SHA256
`ef46772265a4b0856ebfb1f8036fa65006663519fd098e8fa797c6e4b167e868`.
Existing route_persistence implementation owner returned CRP/CAM receiving CONCUR
on exact a10db615, verifying case/basis hashes. This is receiving compatibility,
not retrospective Design authorship or implementation approval.

The555d→a10db615 clarification records actual App context rather than Git/source
liveness; per-entry immutable custody revision rather than unrelated global
revision; precise errno/unsafe/missing and known-replacement status; separate
busy/stale admission refusals; nonblocking acquisition and lease/drop ordering;
all coexisting prepared/recovery/read resource costs; and no fabricated custody
on post-writer installation failure. Original hashes remain in BASIS.json.
No designed case has yet been executed as implementation evidence.

## Recommended single production contribution

After release, join actual constructed local source/Git observation through
existing0.3/0.4 prepare and successful publication, typed same-entry custody,
token-only command, actual direct exact-file inspection and current draft panel.
That is the production path to implement/test; injected selection and constructed
Git are explicit test boundaries, not a native witness. Original outcome remains
unchanged; inspection reports current_match/missing/changed/unsafe/unavailable,
with separate busy/stale/custody command refusals and no namespace uniqueness.

The new private PublishedCustody retains the successful writer's original
Arc<ProjectRouteStore> and BoundReference, not a reconstructed JSON capability.
One transient inspection lease bounds concurrent backend reads; no new CAM slot,
full readback cache, second registry or source/TASK mint is introduced. Existing
resolve/discovery/reconcile and read-only0.5 remain unchanged. Existing generic
cold allocation gap is not repaired or hidden by this direct known-input path.

## Exact proposed implementation write fence

All paths below are under projects/chirality-app-v4/app/:

- src-tauri/src/connector_materialization.rs — typed success custody, immutable
  per-entry cut, transient lease/admission and return recheck.
- src-tauri/src/connector_route_store.rs — distinct no-enumeration known0.3/0.4
  direct bounded reader, preserving original error causes and old resolver.
- src-tauri/src/lib.rs — additive token/generation-only command and its actual
  AppState project guard/command registration/connected handler tests only.
- src/ConnectorSourcePanel.tsx — existing published-entry action, compact status,
  request/selection stale-result guard and narrowly scoped local helper exports.
- src-tauri/src/connector_materialization_tests.rs — writer-to-custody/lease/
  outcome preservation and constructed connected cases.
- src-tauri/src/connector_route_store_tests.rs — actual-file identity/bounds/
  nonblocking/error cases and no sibling open/enumeration instrumentation.
- tests/connector-source-presentation.test.mjs — real handler/panel transition
  and escaped compact status/late-response checks.

No Cargo/package changes, Host/role/RS changes, new carrier/parser/store, generic
resolver rewrite, other panel or new test framework. If an additional production
file or semantic change becomes necessary, return it before widening this fence.
Git evidence/graph updates remain manager-owned, separate from Type2 code edits.

## Required execution boundary and remaining decisions

Run only authorized offline constructed tests after release, serially with other
lanes' Rust windows. Verify default/distribution affected Rust behavior, actual
command+frontend path and existing legacy/0.5 checks; retain first failures and
obtain independent exact-code review. Account actual FD ownership and simultaneous
read/parse/frozen-payload allocations; do not claim global1MiB or runtime deadline.
No App/supplier launch, sign-in, native picker or person act is authorized.

No new owner-reserved meaning choice is identified for this source cut. Any need
to change registry lifetime/capacity, App project authority, publication meaning,
unique resolution or current Host behavior returns for named source treatment.
The connected Host request exporter assessment is retained as a later alternative
only (SHAca593d604383882e20ea5b052ab3fd60f65b2976b3a05267dbd9fa9426f8a801);
no standalone export seam is selected. Critical-set grammar, actual source exports,
immutable retention, R2/product policies and CAM64 suitability remain separate.
C2/C4/C5 external holds and no whole-product90 claim remain unchanged.
