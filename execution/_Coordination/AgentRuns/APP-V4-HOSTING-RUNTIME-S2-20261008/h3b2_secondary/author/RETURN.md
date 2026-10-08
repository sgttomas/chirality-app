# H3B-NAMESPACE-01 author return

Standing: bounded implementation candidate, no commit or implementation acceptance. Exact source/contract identities are in AUTHOR_BASIS and CANDIDATE_FILES. Initial f23997 basis received nonrewriting8d887605 (B graph only) then7fd670cc (C3 additive modules/commands/frontend); C3 semantics and B code/pins are untouched. Independent source/claim review remains required.

The implementation supplies the reviewed shared live namespace authority, whole-operation Store leases, epoch-pinned attachment refusal, private prepared REC commitment and Root account/key setup. Root installs capabilities before constructing a key Host; the new Host receives the retained Store. No new storage, JSON capability hydration, H5 allocation, S3 issuer or native supplier/auth act. NAMESPACE_ADMISSION.md states exact behavior and remaining limits.

## Validation

- Default broad Host:153 passed,3 intentionally ignored fixture entrypoints. This preceded only two new test cases/hooks, not a behavioral repair.
- Combined distribution-successor/custom-protocol broad Host:155 passed,3 intentionally ignored.
- Final default namespace schedules:12 passed,1 ignored worker (exercised by its bounded watchdog). Combined final integrated schedules:12 passed,1 ignored. The final default integrated check is separately retained.
- Combined distribution/Store/Unicode reader regression:28 passed. Existing access_integration:9 passed.
- Offline frontend build passed at both integration bases. No downloads; one shared Cargo target, no duplicate build tree.

Earlier diagnostics are preserved verbatim. First test compile required explicit lease arguments and avoiding Debug-bound unwrap_err on native capabilities; then fixtures needed an existing runtime parent and0700 private directories. A later liveness test needed its Instant import. Repairs changed test setup/imports, not production authorization. Final tests cover the repaired source; failed logs are not hidden.

## Exact read/hot-join repair

Self-review found that holding a lease only inside resolve_cold would release protection before Host.resolve_attachment_submission performs its Arc::ptr_eq hot overlay. The initial candidate still called custody.resolve_cold(submission) directly; no executed exploit was claimed. Repair adds resolve_cold_leased and retains the outer lease across the entire cold-read/hot-join operation. Deterministic namespace_admission_cannot_enter_between_cold_read_and_hot_join injects admission exactly after cold read: it is busy while that lease exists and can acquire after return. It also verifies the original genuine hot source join remains available before admission. This specific backcheck, not the broad suite alone, supports closure.

## Covered schedules and limits

Tests cover stale clones/prepared packets, old late AttachmentLink persistence with actual write/response retained, fresh cold pointer mismatch/no replay, checked epoch overflow, operation/writer busy with unchanged state, final geometry failure, valid/invalid unavailable REC, pre-materialization Store overlap, required Store absence/error, postcommit failure classification plus actual new Host refusal after App session end, no prospective registration, active Store read contention, two actual synthetic Host homes preserving account reference bytes and distinct H5, expanded key-link drift, blocked pipe admission refusal and Stop/EOF liveness under a watchdog.

The test-only worker uses invented local processes. No App/supplier launch, credential submission, signing or qualification. Physical preparation may survive precommit refusal; that is not rollback. Namespace/file observations remain bounded, not an atomic snapshot. Old attachment epochs deliberately lose read/dispatch/persistence availability; original live facts remain visible and fresh reads remain historical, never hot restoration. Restart hydration and other lifecycle/S3 residuals are unchanged.

B1147 source pins deliberately remain at their accepted bytes. This candidate changes bound Host/Store sources and adds namespaceAuthoritySourceSha256. Manager must commit only after independent review, run fresh exact-source exports, and receive B's named adoption on that same candidate before final CI; author did not repin or claim those checks passed.

## Independent blocking finding and repair

The initial candidate was NOT READY despite its passing broad checks. Independent review reproduced replacement of the publication directory after preflight_binding and before guard's second physical_root: publish_attempt eventually refused, but the substituted0700 directory already contained .pending-attempt writes. Initial report, original candidate hash packet, raw failure logs and exact instrumentation patch are retained in review_initial, together with the author's original manifest.

Repair: validated_root now returns the opened descriptor after all namespace/vendor/source/private/root-ID checks. preflight_binding discards that validated descriptor only for geometry-only admission; guard keeps and returns that same descriptor and never reopens a different object. The reviewer hook remains at the exact after-validation/before-return boundary. The original reviewer test body/name is byte-identical to the independent copy and now proves the substituted root receives no writes. A rename can still make the genuine old directory unreachable by its original name; later guards refuse, without a snapshot or rollback claim.

Repair validation: default and distribution-successor/custom-protocol each68 passed,2 intentionally ignored fixture entrypoints for the union of distribution_, namespace_admission and hosting::successor. Both runs explicitly execute reviewer_root_replacement_before_returned_descriptor_must_not_receive_writes, plus S1 publication/readback and namespace schedules. These affected reruns cover the repaired bytes; the original broad passes are historical and did not detect this defect. A patch transplantation initially omitted a context closing brace; the resulting compile failure is retained and repaired without changing the review test body. No new external exchange, B adoption, commit or pin change occurred.
