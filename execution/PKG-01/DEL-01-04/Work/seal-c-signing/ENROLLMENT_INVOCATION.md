# Minimal native-host enrollment invocation design

Status: reviewable source design for the later admitted signing stage, **not
implemented, not activated**. KEYCHAIN_SELECTION remains None. This design adds
no new enduring governance mechanism and does not change SEAL-C/SEAL-2 scope.
The offline preparation is usable now; executing SC-1/SC-3 requires this bounded
source work and actual owner signing-stage authority first.

## Existing source and the exact gap

- `capture_seal_keychain.rs::enroll_initial(app_data)` takes an AppData path and
  uses the compiled provider authority. It is not called by product code. It
  returns `Result<(), String>` and does not distinguish newly created, already
  enrolled or completed-pending outcomes.
- `lib.rs::app_menu` / `on_menu_event` already dispatch native menu actions to
  Rust; `request_quit` retains the original configured window and runs the work
  off the main thread. No renderer invocation is necessary for this action.
- `native_lifecycle_confirmation::confirm` provides the existing parent-bound,
  safe-cancel native question method. Its body belongs to the native owner and
  is reused, not forked or replaced.
- `AppState.app_user_data_root` holds the host-owned installation location.
  `AppState.key_setup` excludes concurrent key setup, and `request_quit` uses
  a nonblocking acquisition of it before proceeding. Quit state is also exposed
  through `AppState.app_quit.busy()/proceeding()`.

Calling the existing path-only `enroll_initial` directly after a dialog would
not by itself bind the operation to the marker state the operator confirmed.
That is an actual gap, not an assumed existing capability. The implementation
below must add the small provider-owned prepared-intent join before invocation.

## One action, no new authority input surface

Propose one native App-menu action, **Prepare capture sealing**, enabled only in
an explicitly admitted signing-stage build with both compiled publisher and
keychain selections available. No `#[tauri::command]`, renderer event, MCP tool,
URL, CLI flag, persisted boolean or environment variable can invoke it or supply
its root/namespace. Ordinary startup continues only installing the existing
location; it never invokes enrollment.

This is an administrative setup action, not an A4/A6/A7 personal act or proof
that a human rather than an authorized accessibility operator pressed a button.
Actual actor/control attribution is retained for the signing witness; no new
personal identity or agent-exclusion guarantee is inferred.

## Prepared subject and ownership

Add a private, non-Deserialize `PreparedSealEnrollment` in the provider module,
created only from the running host's checked compiled selection and installed
AppData root. It contains no secret material. Its frozen subject is:

- exact publisher-binding digest, bundle/team and compiled provider policy hash;
- exact service/primary account/access-group and allow_first_enrollment;
- physical AppData/continuity-directory identity, or checked nearest existing
  parent plus the expected absent child for an uncreated directory;
- exact existing marker digest and committed/pending key IDs, or explicit marker
  absence; the observed legacy-directory presence/absence;
- one in-process attempt identity and original native-window handle/custody.

It is not a public constructor from JSON and not a namespace picker. Disk marker
bytes remain evidence only. Preview reads no key material and performs no SecItem
call. It may describe that the provider's own fresh namespace/readback checks
still occur after confirmation; it must not label an unqueried keychain empty.

The native host retains the prepared intent while showing its exact nonsecret
namespace and effects using the existing native-statement machinery. Cancel is
the safe default. If a marker has pending material, show the exact proposed
completion of that reserved subject; do not present it as a brand-new empty
namespace. If legacy data, malformed scope or ambiguous state is found, report
its existing refusal instead of offering migration/reset.

## Confirmation-to-operation join

1. Retain the configured original App window at native menu dispatch. Refuse a
   missing/replaced original; never choose a focused/replacement window later.
2. Freeze the provider-owned prepared subject. Do not hold an App writer,
   keychain continuity lock or key_setup mutex across the native dialog.
3. After affirmative native result, acquire `AppState.key_setup` nonblocking.
   A competing explicit key operation returns busy with no keychain work. Check
   `app_quit.busy()` and `proceeding()` while holding that gate. If Quit already
   won, refuse. A later Quit finds key_setup held and follows the existing retry
   behavior; App-initiated Quit must not proceed under enrollment. External
   termination/logout remains possible and is covered by crash recovery, not
   prevented by this gate. The existing Quit notice should
   say an explicit key operation is in progress, not falsely claim an API-key
   home change. This one wording hunk needs native-owner coordination.
4. Revalidate original window and AppData/compiled selection. Refresh the
   authority through `process_authority(recheck=true)` **before taking provider
   locks**. Require the refreshed identity and `allow_first` to equal the frozen
   prepared policy; a mismatch refuses, never updates the intent to new policy.
   Move the intent once into a provider-owned consume operation.
5. Preserve the **existing enrollment → continuity lock order** with two distinct
   comparisons. Immediately after acquiring the enrollment lock, compare frozen
   AppData/parent/directory identity and expected absence **before** computing
   `observed_absent` or calling `fresh_namespace` (which may perform a SecItem
   read). A fresh continuity directory and lock do not yet exist: never create
   them early just to perform this comparison. After taking the continuity lock
   and loading the marker, compare its exact digest and committed/pending IDs
   before any pending readback or add. Changed subjects refuse; no reconstruction
   from newer disk/window state. Reuse existing storage/entropy/reservation logic.
   Lock order remains host key_setup → authority refresh → enrollment lock →
   continuity lock; verification never reverses it. No marker/secret work runs
   on the main thread.
6. Retain key_setup until the actual call returns and evidence is settled.
   Failure/panic/termination never manufactures successful enrollment. The
   provider's reservation/readback semantics remain the recovery authority.
   Release guards on every return. Normal Seal/Verify/Rotate still cannot create
   a first key, and no failure path silently repeats Enroll.

The existing provider uses blocking writer locks with no timeout. Holding
key_setup during such a wait can delay App-initiated Quit indefinitely; this is a
known liveness limit, not a successful enrollment. External termination can still
interrupt it. The minimal invocation design retains that limit explicitly rather
than claiming a bounded wait; any later bounded/nonblocking writer policy needs
its own source tests and must preserve durable pending-state semantics.

If integration cannot reuse key_setup without an actual lock-order or native
ownership conflict, return that specific source conflict before adding another
broad global lock. This design proposes reuse; it does not assert an implemented
Quit/enrollment race check today.

## Result evidence, not a new permission record

The signing witness receives a bounded nonsecret observation of this attempt:
App source/build/executable/cdhash and publisher binding; prepared policy/root/
marker digests; native presentation/choice/control attribution; before/after
committed and pending key IDs; actual result category; and exact observation
artifacts. No key bytes, HMAC secret, Apple credentials or full keychain query
result are logged.

With today's `Result<(), String>` API the only success claim is **the provider
returned success for this checked subject**. Do not call it "new key created"
without an implementation-owned phase/outcome report proving an add occurred.
A later small typed `EnrollmentOutcome` can distinguish `already-committed`,
`committed-after-add` and `committed-existing-pending`; it must come from the
actual provider branches, not marker comparison or caller-provided flags.
The minimal implementation may retain the narrower success claim instead.
Records never grant future invocation authority or select the namespace.

## Later-stage validation, without native work now

Before this action is integrated/activated, source tests must exercise injected
native choice and backend to establish: cancel/missing parent no operation;
marker/root/policy drift during confirmation no operation; a second attempt does
not duplicate add; Quit winning before admission refuses; enrollment winning
keeps the App alive until result; guard release on refusal; and confirmation
subject checked inside provider locks. Reuse existing mock SecItem hard-disable
in test builds and preserve file-key regressions.

Only after source review and exact candidate signing may the actual SC-0…SC-6
witness observe profile entitlement membership, native no-UI behavior, explicit
fresh enrollment/readback/restart and failure/recovery. An actual locked/denied
control must use its separately admitted disposable namespace/session, not
change the owner's normal login keychain. Pending-only missing material remains
a retained failed subject, not authority to reset/delete/reseed it. A concrete
continuity disposition can admit a distinct namespace later.

## Bounded prospective files and ownership

Runtime owner: `capture_seal_keychain.rs` prepared-intent/consume join and tests;
no storage algorithm rewrite. Native owner: `lib.rs` App menu/dispatch and the
single key-operation Quit notice; reuse `native_lifecycle_confirmation` unchanged
unless a concrete interface gap appears. Packaging: exact selected entitlement/
profile/signature and fresh namespace/witness inputs. Parent: integration and
reserved namespace/signing-stage choices. No such runtime/native edits are made
by this preparation PR, and their overlaps must be disclosed again before work.
