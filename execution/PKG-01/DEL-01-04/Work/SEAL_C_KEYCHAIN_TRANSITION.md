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
  continuity directory without its marker also refuses; it is never reset.
- A private temporary marker is written, synced, atomically renamed and its
  directory synced BEFORE add. An uncertain marker write stops before add.
  A crash before reservation leaves no key operation and does not automatically
  reset an existing incomplete namespace.
- Add is followed by exact data readback. Only then is pending committed. Add
  error, duplicate, timeout/unknown outcome or readback failure leaves reservation
  intact; none proves success. No add is retried while pending.
- A later seal/enrollment/rotation write path may commit pending only after
  matching actual key ID/full digest readback and retained prior items.
  Missing/malformed/denied/locked pending items block new sealing/rotation.
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
