# I2 WR private publication implementation

2026-10-05. Type2 native TASK `/root/group_a_execution_astra/wr_publication_design`; parent `/root/group_a_execution_astra`. No descendants. Private snapshot `/private/tmp/wr-publication-astra/app`; all manager b44 tracked files matched the precopy manifest, zero differences. Maintained App/Design untouched. Reviewed source basis V6 SHA-256 `5737d6e4ad444415904ab14c214677e7a082dbf89c97aec8ebf726933de8740f`, WR §16.8 proposal; no acceptance or release inferred.

## First compilation freeze

Private files: workflow_workspace.rs only adds nested publication module; new workflow_record_store.rs and tests; exact reviewed envelope resource and SOURCE_MAP pin to eventual maintained Design source (no dated-run include). Registry uses locally bundled WD/WR, offline only. No shared records/lib/runtime/storage edits. Parent granted sole private offline Cargo lane after source drafting; first run pending cache-path confirmation. No supplier/native/auth/network/download/Git operations authorized or performed.

## Implemented boundary and API

`workflow_workspace::publication::ProjectRecords::open(&Path)` requires explicit absolute existing project and pins its directory descriptor; openat/O_NOFOLLOW traversal refuses symlinks. `publish(&PendingRecord)` validates envelope and basis, writes/syncs staging, no-replace link publishes, directory sync precedes success. Original immutable pending bytes survive failures; equal-byte retry resolves same identity, unequal collision never overwrites. `resolve(&str)` returns historical `ResolvedRecord` with reference/body/envelope/project_root/same_project/bytes accessors. No Deserialize, send or native-authority method exists on a resolved record. UUID references are opaque, filenames are only their mapping.

`PreparedRunPublication::new` requires original typed registered Selection and PreparedRunText, preserves source scope, refuses development-to-registered relabelling, and retains original typed prepared text. `publish` resolves exact linked revision again, writes selection then run_text, returns PublishedRunText with original prepared object and durable records. Existing Root dispatch untouched: before-send integration remains required. This constructor currently describes explicit selection only; proposal-confirmed selection provenance requires its owning selection event seam rather than guessed fields.

`PreparedEndPublication::new` consumes existing typed OwnerRunEnd check through PreparedRunText::end_notice; publish returns typed PublishedEndNotice. This does not implement EXEC lifecycle or make a cold record an end callback.

`CompletedSupplyCheck` has private body/source-reference fields and NO production constructor or Deserialize. PendingRecord::supply_check requires that token and resolved run_text. This intentionally leaves an unsupplied Root producer seam: Root must assemble comparison from the actual PreparedRunText and source-owned accepted pages under the current original home/generation/thread/turn/client scope, finish genuine all-page coverage, retain exact observed item/content and original read time/source receipt references, then produce the typed completed check. A coverage seal alone must not authorize arbitrary comparison JSON. Native turn remains opaque. Cold historical re-read cannot create this token. No live R3 append readiness is claimed. RS sibling consumes historical ResolvedRecord correspondence only, with no append-from-resolved path.

## Checks and limitations

Initial rustfmt failed because its declared new tests file had not yet been created; after creating it, rustfmt parsing passed. Six private tests cover immutable reopen/retry/collision/wrong-project; absent-project/symlink refusal; partial/unsupported/escaping references; forbidden payload/original time; uncertainty after durable-file link and same-identity retry; distinct rereads and wrong check correspondence. Cargo execution pending. Typed prepared/end path, genuine check producer, connected pre-send/no-resend integration and final Root/RS receiving tests remain required; whole publication readiness is not claimed.

## Custody

Private patch and manifest are adjacent `I2-WR-PUBLICATION-IMPLEMENTATION-ASTRA.patch` and `.manifest.json`. Baseline copy manifest lives at `/private/tmp/wr-publication-astra/basis-manifest.json`. Source freeze hashes and exact Cargo results follow as appended evidence. Existing exact832 delivery witness and b44 archive remain Parent-owned; no broader lifecycle, native qualification or adopted source standing is asserted.

## Final frozen validation return

Parent granted sole private Cargo lane, then released after checks. Commands used installed Cargo, `--offline --locked`, `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home`, shared `CARGO_TARGET_DIR=/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/app/src-tauri/target`, `CARGO_NET_OFFLINE=true`, `CHIRALITY_SKIP_CODEX=1`. No supplier execution. Private source location stationary throughout each invocation.

1. First compilation: `cargo test --offline --locked --lib workflow_workspace::publication -- --nocapture`: 6 passed, zero failed.
2. First affected suite: `cargo test --offline --locked --lib workflow_workspace:: -- --nocapture`: 55 passed, zero failed.
3. Added meaningful typed preparation/source-loss/development-refusal/end-notice test. First compile failed E0432 because test used one excess `super` in imports. Original failure preserved in cargo-final.log. Corrected only the test import to crate::workflow_workspace. No production repair was hidden by rerun.
4. Final same affected-suite command: 56 passed, zero failed (7 publication tests).
5. Ordinary-build negative probe added an unguarded sibling-module attempt to construct CompletedSupplyCheck from JSON. `cargo check --offline --locked --lib` failed E0451 specifically because body/sources fields are private. This demonstrates more than an external private-module import refusal. Probe then removed by restoring exact workflow_workspace bytes.
6. Restored ordinary `cargo check --offline --locked --lib`: passed. Existing and unwired-new-code warnings remain; no warning suppression added. Source patch hash returned to exact final frozen value after negative probe removal.

Final implementation patch SHA-256: `84f238d583c8fd25a4ac71abb2c68541dc68773e30295bddb0134bd43528f784`.
Frozen test executable copied before shared target release: `/private/tmp/wr-publication-astra/frozen-wr-tests`, SHA-256 `4ef64772ec2a08ed8b5687f1929f972e5581e3451729f8c355c37f0759969ce5`. Source per-file hashes are in the adjacent manifest; tests cover this private candidate, not maintained adoption.

## Root producer assembly contract still required

The concrete CompletedSupplyCheck type intentionally has no production factory, so this slice cannot claim completed native publication. One Root owner must integrate within the existing check_native_supply path while actual accepted pages and PreparedRunText remain in custody: establish original project/home/full generation/conversation/turn/client; preserve all page source receipts; compare those exact accepted page bytes against original prepared text and selected workflow body (same methods/scopes, no digest-only fallback); finish/revalidate coverage at the actual final boundary; form complete WR body with original read_at, opaque turn, selected item/located_by and limits; mint the private token inside an owning source function that performs this comparison, not a JSON-field setter. Unreadable/negative results must retain only actual known scope and limits. Every reread mints new check identity; pending publication retry keeps original token-derived body/bytes. The later producer patch requires its own source-bound negative and ordinary-build privacy tests.

Root then supplies the token to PendingRecord::supply_check with matching durable run_text, retains the pending object on failure, and publishes. RS's historical mapper may inspect resolved records but must not append new native supply from that alone; its future live route needs actual completed-check provenance plus durable references. If end-notice sourceIdentity requires a workflow tuple not present in that WR body, resolve the original owning run/source record; do not invent one. Sender gating remains separate and must consume PublishedRunText/PublishedEndNotice without treating publication retry as resend. Exact pre-send integration, current selection event provenance, source-bound live check, post-send no-resend and lifecycle/recovery joins remain Parent/Root work.

## Preserved check evidence

- `/private/tmp/wr-publication-astra/cargo-first.log` — SHA-256 `131442f346223b42212b600e0219ac4758d31ea26832e51ce9b03457b4c40f47`
- `/private/tmp/wr-publication-astra/cargo-workspace.log` — SHA-256 `5f6d4305faa5141e836fc4521d39f183c4d373642319daf94ef20ca4923b782d`
- `/private/tmp/wr-publication-astra/cargo-final.log` — SHA-256 `5736f201817dd6b71360a13f5db1afd58f19e2f1d471a80b9940c69d037fad35`
- `/private/tmp/wr-publication-astra/cargo-repaired.log` — SHA-256 `0070407037fc02cf19f54a928ac418bff55b57870c62bcf4f2c3665faacbdab5`
- `/private/tmp/wr-publication-astra/cargo-privacy-negative.log` — SHA-256 `6c95cca94c85a71b7fd6e3fed924c16a1318e97b69ca9bcd6422b19cad50fbee`
- `/private/tmp/wr-publication-astra/cargo-ordinary-restored.log` — SHA-256 `156be4d90ee42ee647fc9cab47fb34637507e0b75b7eafa15890f2bb1546a4ae`
- `/private/tmp/wr-publication-astra/basis-manifest.json` — SHA-256 `ac2967324b8ad1541a78de1ce79629ea8e573d9dc49bc3dc8032c4bdd620d096`

## End-notice source-authorized successor

Parent adopted independently READY CC-WR-END-NOTICE source patch
`ea56c20cdba35013a8a48689d4b4099c19781d8ed1749c27e0ed2367af49b5df`, recorded in
`CC-WR-END-NOTICE-SOURCE-ADOPTION.json` (WR source
`094602acb5e1ba8b68bffc7475da8a80557749d134eddb60c8c4d4a676019656`).
This authorized the following private repair; maintained code remained untouched.

- End-notice publisher now requires `original_start: &ResolvedRecord` between
  end callback and writer arguments. It checks same physical project, re-resolves
  the start and its selection lineage, and compares its complete body with the
  actual retained PreparedRunText record before publishing the actual unchanged
  end_notice body with that sole basis reference.
- Resolver follows end→same run/conversation start→selection. Check→text still
  compares same purpose/run/conversation and expected text. Optional
  expected_workflow on start checks still compares the full method/value object
  with start.workflow_file.content. No field is imposed on genuine end notices.
- Actual producer fixture asserts workflow/workflow_file absent and exact
  end_notice body unchanged. The original zero-basis case remains a refusal
  control. Wrong run, thread, project, missing start and start expected-workflow
  method mismatch are negative cases. The actual producer succeeds on cold
  reopen through original start. No fixture renames a start into an end notice.
- Previous implementation source is retained at
  `/private/tmp/wr-publication-astra/pre-end-repair-src`; earlier failed proposal
  and its source-review repair remain preserved in changes/. Existing live token
  constructor absence, Root sender/check custody limits and no-adoption claims
  remain unchanged.

Sole Cargo lane granted after REC release, then released to Parent after these
checks. Same explicit offline/locked/skip-supplier environment as above.
`cargo test --offline --locked --lib workflow_workspace:: -- --nocapture`:
**57 passed, 0 failed** (8 publication tests), first attempt.
`cargo check --offline --locked --lib`: **passed**, first attempt.
No further Cargo or source writes are running. RS sibling received the exact
frozen files/API for joined receiving validation.

Successor full implementation patch SHA-256:
`b7e5248a87e390bd048a3a408f997a69ec26688c736b9abf4a4091cd88dd34fd`.
Immutable test executable `/private/tmp/wr-publication-astra/frozen-wr-endnotice-tests`,
SHA-256 `f782d979009b0fa9e4ddf8cfefbcda4dfa31432a4e5319b22ca3309ed43d4840`.
Adjacent manifest now binds this successor; prior hashes above remain historical.

- `/private/tmp/wr-publication-astra/cargo-endnotice-first.log` — SHA-256 `730eba22f4472e52019955d34ed917fac14723a52548fcfe795b687e38723575`
- `/private/tmp/wr-publication-astra/cargo-endnotice-ordinary.log` — SHA-256 `ac11ea521c2a0393b4d972cccd52acfb6d6aab2e59e3c7d0955f1843b7e6b86e`
