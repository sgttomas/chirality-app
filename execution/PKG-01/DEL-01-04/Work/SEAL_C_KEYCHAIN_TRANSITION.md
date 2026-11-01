# SEAL-C signing-stage keychain transition

Named implementation `SEAL-C-KEYCHAIN-01`, 2026-10-31, under App Agent 0's
bounded runtime assignment. [AAC §6.3](APP_ACT_CONTROL.md) selects the SEAL-C
host-key fix and says the key moves to the OS keychain at signing (OI-011);
U-AAC-3 repeats that point of need. This is the adopted signing obligation.
SEAL-2 remains deferred/proposed: no RS entry seal, exclusive-agent exclusion,
cold native-origin proof, verified personal identity or personal-act guarantee
is adopted or established by this change.

## Actual source and narrow allocation

Before this change `capture_seal.rs` used `<AppData>/capture-seal/keys.json`,
HMAC-SHA-256, a current key and retained earlier keys. File loss caused a new key
at next capture; file metadata formed the verification-cache basis. The existing
unsigned/development route and historical seal method/bytes remain unchanged.
`lib.rs` still calls `capture_seal::install(data)` in its original order beside
`installation::install(data)`. This change adds provider dispatch and a separate
platform boundary; it does not migrate live AppData or change native startup,
Quit, process custody, capture semantics or the supplier route.

A checked selected production publisher cannot use the development file provider.
`KEYCHAIN_SELECTION: Option<Selection> = None` is a separate compiled gate in
`capture_seal_keychain.rs`. Missing/incompatible selection or publisher/installed
validation failure makes sealing unavailable; AAC's existing unsealed-capture
limit remains truthful and such a capture is not counted. It never falls back
to file keys. Ordinary builds without publisher selection remain usable with
the unchanged file provider. No real identity or keychain operation is activated.

Future signing-stage Selection must explicitly name `bundle_identifier`,
`team_identifier`, `service`, primary `account`, exact `access_group` and
`allow_first_enrollment`. No field is inferred from the publisher team, copied
from an arbitrary marker or read from a runtime override. The existing closed
three-field publisher input is unchanged. Private `KeychainAuthority` construction
requires that exact compiled selection, checked publisher subject match and the
running App's S4 installed-integrity observation. It is not deserializable.
The native backend borrows it and rejects service/group or account outside its
admitted primary/rotation namespace. Successful authority is held only in process
memory and reused for ordinary seal/verify operations. Enrollment and rotation
revalidate the own-App authority; failed refresh revokes the held authority.
Revocation here clears the held capability for subsequent acquisitions; an
already in-flight operation holding its prior Arc may finish. There is no
asynchronous cancellation or continuous kernel-signature monitoring claim.
No key bytes or provider availability are cached by this authority cache. The
stable installed-bundle/parent assumption and S4 residual limits remain explicit;
this is not continuous signature monitoring or an immutable installation claim.

## Platform policy and signing dependency

The backend uses Security.framework's Data Protection keychain generic-password
class, `kSecUseDataProtectionKeychain=true`, explicit service/account/access-group,
`kSecAttrSynchronizable=false`, `kSecAttrAccessibleWhenUnlockedThisDeviceOnly`,
and `kSecUseAuthenticationUIFail`. These no-UI query constants are deprecated
on current SDKs (replacement: authentication context with interactionNotAllowed);
source use is retained as an explicit compatibility policy, not an observed no-UI
guarantee. Actual no-UI behavior must be qualified on the signed candidate before
activation; unsupported or unavailable results refuse. Reads request one matching item's attributes
and data; returned namespace, accessibility, non-sync and bounded data must match.
The queried class is fixed; any returned class must agree. Standard CFType
dictionary callbacks retain values and compare keys by value. Returned non-sync
accepts CFBoolean false or exact CFNumber zero; missing expected attributes
still refuse. Actual returned attribute shape remains native qualification. The API is read/add only: no update, delete, enumeration,
legacy keychain fallback or authentication prompt. A duplicate add is a failure,
not permission to overwrite. Native errors are categorical and omit key bytes,
identity values and paths.

The installed public SDK's SecItem.h documents Data Protection selection on
macOS 10.15+, with access-group membership governed by `application-identifier`
and/or `keychain-access-groups`. This does NOT establish entitlement-free access,
a guessed team-prefix mapping, provisioning-profile exemption or permission to
alter entitlements. Packaging must supply the selected signed identity, actual
entitlement/profile compatibility and candidate evidence before activation; see
[the signing join](../../DEL-01-06/Work/SEAL_C_KEYCHAIN_SIGNING_JOIN.md).
The selected App minimum macOS 15 is outside this module's API-floor statement.

## Enrollment, crashes and continuity

First enrollment is a separate host-only `enroll_initial(app_data)` operation.
There is no startup call, IPC command or UI request that performs it. It requires
both the checked authority and explicit compiled `allow_first_enrollment`.
Actual invocation belongs to the reviewed signing stage, not this source work.
Normal seal, verify and rotate never create an initial namespace, including
after simultaneous loss of all local continuity and keychain items.

The nonsecret `capture-seal-keychain-continuity.s1` record lives at
`<AppData>/capture-seal-keychain/continuity.s1.json`, separate from historical
file keys. Closed fields are `format`, `scope_sha256`, `keys` and `pending`.
`scope_sha256` binds exact service/primary account/access-group and the fixed
provider policy. `keys` is the ordered committed `{id, sha256}` list; the last
key is current. `pending` is null or the reserved new key's `{id, sha256}`. IDs
retain SEAL-C's existing domain/key-id derivation; the full digest checks
readback. Neither keys nor HMAC values are stored in this marker. It is a
continuity guard, not namespace authority, a platform receipt or origin proof.

- Private owned folder/file checks and no-follow opens guard participating-App
  coordination. Verify holds a shared nonblocking lock and reads only the requested
  committed key. Seal/enrollment/rotation wait for the exclusive lock, so an
  ordinary concurrent verification cannot cause a newly captured act to be
  permanently unsealed just because the reader held the lock. An unavailable
  provider still produces its truthful failure limit; no timeout means success.
- Fresh admission takes a separate parent enrollment lock and checks legacy
  namespace absence and primary-item absence BEFORE creating the continuity
  directory. Transient first-use denial/lock failure leaves no poisoned empty
  namespace and can retry under the same lock. The lock file is not evidence of
  successful enrollment. Fresh explicit enrollment refuses if any legacy capture-seal directory exists;
  only presence is checked, with no legacy key read/import/reseal. A new v4
  production namespace gets its own key, not implicit development continuity.
- A fixed primary keychain account is checked before enrollment. Existing or
  unavailable primary items refuse a purported fresh namespace. An existing
  continuity directory without its marker refuses normal operations. Explicit
  host-only Enroll may resume an unreserved setup only after rechecking both
  legacy and primary-item absence under both locks; no directory is deleted.
  This explicit act is not triggered by capture/verify/rotation, including after
  loss. If both old key and marker were externally deleted, their prior existence
  cannot be inferred: invoking Enroll must be an independently admitted fresh
  namespace act, not automated loss recovery.
- A private temporary marker is written, synced, atomically renamed and its
  directory synced BEFORE add. An uncertain marker write stops before add.
  A crash before reservation leaves no key operation; ordinary paths never
  reset it. Explicit Enroll can retry after fresh absence checks. Directory
  creation is allowed only when the same admission observed absence; a directory
  disappearing after an observed-present result causes refusal, not recreation.
- Add is followed by exact data readback. Only then is pending committed. Add
  error, duplicate, timeout/unknown outcome or readback failure leaves reservation
  intact; none proves success. No add is retried while pending.
- A later explicit enrollment/rotation write path may commit pending only after
  matching actual key ID/full digest readback and retained prior items.
  Missing/malformed/denied/locked pending items block completing enrollment or
  rotation. Ordinary Seal continues under the already committed current key,
  reading that key only and never reading/committing pending or older rotated
  items. If no key is committed, sealing remains unavailable.
  Verify never reads or commits pending: it may still verify a capture using its
  committed historical key. Pending-only first enrollment has no usable key.
- Rotation first validates all retained keys, reserves one new key, adds an
  immutable item with account `<primary>.rotation.<16-lowerhex-keyId>`, and
  commits after readback. Prior items/IDs remain held. Duplicate IDs and the
  retained-key bound (128) refuse without replacement. Pending rotation cannot
  discard or overwrite earlier key material.

No automatic migration, marker reset, key deletion, fallback, old capture reseal
or destructive repair is implemented. A lost provider/key reads "not verified
here"; an unsealed capture is recorded with the existing limit and not counted.
Changing team, bundle, service, account or access group requires an explicit
continuity disposition and new qualification, never a silent new key.

## Reader/cache behavior and limits

HMAC method/domain/canonical capture facts are unchanged; `recordId` remains
outside the seal as before. Retained keys verify prior captures without reseal.
Keychain selection changes the verification-cache basis to a new per-call
reobservation token. File timestamps cannot cache a keychain success: every
consumer read must reverify its required key's provider availability, including
lock/denial/missing/rotation changes. It does not repeat a full bundle validation
per capture or read every historical key for a single verification. This deliberately trades caching for truthful availability. It does
not make reads atomic with later user actions or with external keychain changes.

The key bytes are delivered to process memory for HMAC. A process/agent that
obtains those bytes can seal; keychain storage alone proves no exclusion of a
hostile same-user/admin process, authorized Accessibility actor or code running
inside the App. Marker replacement/rollback and external keychain deletion by
such actors remain outside participating-App coordination; no tamper-proof
continuity or rollback counter is claimed. The fixed primary item and explicit
enrollment prevent ordinary silent regeneration, not all loss or malicious reset.
A successful seal still shows only possession of the held key, not that a person
acted, their verified identity, or authentic native origin for replay.

## Source assurance and remaining evidence

`capture_seal_keychain_tests.rs` uses invented fixed keys and an in-memory backend.
Tests cover explicit enrollment, first-use/total-loss refusal, rotation retaining
prior keys, crash-before-reservation, durable pending before add, completed add
before commit, unknown/duplicate add outcomes, exact readback, unavailable/locked/
denied/malformed items, wrong scope, participating writer contention, legacy
namespace refusal, actual capture dispatch and cache reobservation. CF attribute
fixtures exercise native returned-policy checks. In cfg(test), even the native
SecItem wrappers hard-return unavailable without calling Security's item APIs.
No real SecItem query/add/delete, identity/keychain inspection, entitlement/profile
change, signing or existing native AppData access is part of these tests.

Later actual signed-stage evidence must establish identity/profile compatibility,
no-UI availability/failure behavior, explicit first enrollment and restart,
rotation/history continuity, unavailable-provider behavior and integration with
the specific App candidate. Source fixtures are not that witness. Independent
Claude Opus 5.5/high review, focused checks and exact-head CI are retained in the
PR before integration; final App merge and signing-stage activation remain with
Agent 0 and the owner at their respective points of need.

Initial guarded offline source checks: capture_seal cohort 20 passed; checkpoint
recorder cohort 65 passed; file-act cohort 52 passed with one existing opt-in
ignored. CI-selection tests passed 62 and deliverable validation reported no
errors. These checks include synthetic protocol fixtures only and do not inspect
or operate the retained native candidate/AppData or any real keychain. Later
review repairs and exact-head check results remain in the reviewed PR.

Independent review of 5d42f4dd found no merge blocker behind None, but identified
activation-relevant concurrency, refused-enrollment retry, pending historical
verification and repeated full-bundle-validation defects. They were repaired in
this PR rather than left as activation debt. Source regressions cover concurrent
shared verification/Seal, transient initial denial then successful enrollment,
requested-key-only historical verification during failed rotation, and cached
authority refresh failure revocation. A bounded independent repair recheck and
exact-head checks are recorded in the PR. Real no-UI/returned-attribute/access-group
qualification remains separate; no SecItem call was made by source tests.

The repaired provider cohort passed 25 tests before the final concurrent initial
enrollment assertion; the broader seal filter passed 23 and installed-observer
ABI regression cohort passed four. The added SDK comparison corrected the existing
CFNumberGetValue parameter from i32 to CFIndex/isize in installed_custody.rs,
without changing its policy. Final concurrency and exact-head hosted results
are recorded in the PR; no native keychain behavior is inferred.

Bounded independent recheck of db587175 confirmed the original four repairs and
found no merge blocker behind None. Follow-up source refinements make Seal use
only the committed current key (including during pending rotation), let explicit
Enroll resume unreserved markerless setup after fresh absence checks, and tie
creation to observed directory absence. Missing pending-only first-key material
is deliberately NOT regenerated: exact reserved bytes cannot be reconstructed
safely. The record and items are retained for a later explicit signing-stage
continuity disposition (for example, a separately admitted new namespace).
This limitation remains visible, not converted to successful enrollment or
silent key replacement. No destructive recovery action is implemented here.

## Inactive prepared enrollment boundary (SEAL-C-PREPARED-01)

The path-only production enrollment entry is replaced by
`prepare_enrollment(app_data) -> PreparedSealEnrollment` and
`enroll_initial(prepared) -> Result<(), String>`. The intent has private fields,
no Clone/Deserialize implementation and no persisted reconstruction path. Direct
`dispatch(..., Operation::Enroll)` refuses; production enrollment cannot enter
the raw provider engine without the intent. Existing test-only raw provider
fixtures remain synthetic and cannot compile into production authority. No
product caller/menu/IPC/startup registration is added. KEYCHAIN_SELECTION stays
None; default builds refuse preparation before installation reads or SecItem.

Preparation uses the checked process-local authority and freezes its exact
compiled publisher subject, namespace and allow_first policy. It retains read-
only descriptors for AppData and its physical ancestor chain, the existing
continuity directory if present, and the exact marker if present. Directory
identity/ownership/mode and marker identity/times/size/mode/exact-byte hash are
bound; descriptor retention prevents inode reuse masquerading as the original
held object. Legacy namespace absence is required. The marker's committed and
pending key IDs are exposed only as a nonsecret preview. Preparation takes no
advisory lock, writes no state and performs no SecItem query/add. Dropping it is
a side-effect-free cancellation. The attempt ID/preview is evidence/display data,
not a constructor or proof of operator confirmation.

Consumption moves the intent once, refreshes installed authority and compares
the whole refreshed policy to the frozen policy before taking provider locks.
The source joins are repeated at the reviewed effect boundaries:

1. Under the enrollment lock, recheck AppData/ancestor identity, the original
   directory presence/absence, and legacy absence before fresh_namespace or its
   first keychain read. A newly appeared directory is not silently adopted.
2. Under the continuity lock, recheck held directory/root facts and the exact
   marker identity/bytes before pending readback or add. Marker parsing reads
   compare opened-before/after and named metadata, refusing changed reads. The
   provider guard retains its directory descriptor while the operation runs.

New directory/lock creation is the existing provider's own consumption effect,
not a stale-source exception permitting a different pre-existing directory.
Directory timestamps are not frozen: the provider's own lock-file creation must
not invalidate its AppData subject. Directory device/inode/owner/mode and the
marker's full stamp/bytes remain checked. This is bounded cooperating-App
custody, not atomic filesystem integrity against hostile same-user/admin mutation
after a check; the previously stated residual limits remain.

Competing absent or pending intents cannot duplicate an add/commit: the first
operation changes the namespace or marker, making the second stale before its
backend call. Existing committed state can legitimately produce another
idempotent observation under a separately prepared intent, without mutation.
Failed consumption does not reconstruct/retry an intent. A missing pending item
retains the original marker and cannot generate replacement bytes. Ordinary
Seal/Verify/Rotate keep their original no-enrollment rules.

The provider does NOT establish the original native window, affirmative choice,
AppState.key_setup admission or Quit exclusion. The future native caller must
hold those duties around this intent/consume API as described in
[ENROLLMENT_INVOCATION.md](seal-c-signing/ENROLLMENT_INVOCATION.md). No native or
signing authority is inferred from this inactive slice. Source tests use the
existing invented-key/mock backend, including stale policy/root/marker/absence,
cancel/drop, exact pending recovery, competing intents and unchanged file-key
regressions. Independent persistence/authority review and exact-head CI are
required before integration; real activation remains separate.

Prepared-intent source assurance: the guarded offline/locked `capture_seal`
cohort passed 40 tests with serial execution and a fresh scratch home. This
includes unchanged file-key/provider regressions and eleven prepared-intent
cases; native SecItem wrappers remain disabled in tests. Deliverable validation
reported zero errors. Independent review and exact-head hosted checks are retained
in the contribution PR; these source results are not native confirmation or
signed enrollment qualification.
