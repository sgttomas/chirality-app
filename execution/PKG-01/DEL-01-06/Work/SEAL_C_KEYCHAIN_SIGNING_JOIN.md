# SEAL-C signing-stage key provider receiving join

The runtime [SEAL-C-KEYCHAIN-01 clause](../../DEL-01-04/Work/SEAL_C_KEYCHAIN_TRANSITION.md)
implements AAC §6.3/U-AAC-3's adopted keychain-at-signing obligation. It does not
adopt deferred SEAL-2, entry seals, exclusive signed-App/agent exclusion or
native-origin/personal-act guarantees. PACKAGING I-4/G-8 stable identity and
SIGN-3/U-PKG-8 remain actual signing-stage dependencies, not proven configuration.

## Exact runtime inputs and source

`capture_seal_keychain.rs` retains `KEYCHAIN_SELECTION=None`. Future reviewed
source selection must explicitly name bundle_identifier, team_identifier,
service, primary account, exact access_group and allow_first_enrollment. The
three-field publisher-build-selection.s1 JSON is unchanged. A private typed
KeychainAuthority requires checked compiled publisher subject and S4 own-App
installed integrity. Namespace strings/markers/UI/env cannot create that authority.
`capture_seal_keychain_macos.rs` is the Security.framework boundary; its exact
source digest and selected policy belong in the eventual signing evidence.

Policy is Data Protection generic-password, explicit service/account/group,
non-synchronizable, WhenUnlockedThisDeviceOnly, authentication UI fail, exact
returned attributes and bounded key data. Operations are read and add only.
The primary account is the chosen exact value; immutable rotation items append
`.rotation.<16-lowerhex-keyId>`. The selected access group is never guessed from
the team. The public SDK requires actual application membership through
application-identifier and/or keychain-access-groups; no empty-entitlement or
provisioning-exemption claim is made by source implementation.

Packaging must retain exact selected namespace/policy, actual signed App
application-identifier and keychain-access-groups values, the entitlement source
and exact signed entitlement artifact digest, and provisioning-profile necessity
and compatibility (profile identifier/digest if applicable), joined to App
revision/build/cdhash and publisher binding. This document authorizes no profile
acquisition, entitlement edit, identity inspection or signing. Actual field
values remain pending their owner/signing-stage input and secure handling.

## Continuity and witness

Host-only `enroll_initial(app_data)` is separate from ordinary startup/capture/
verification/rotation and is not exposed by IPC/UI. Explicit signing-stage
selection and invocation are still required. The source never imports development
keys or reseals historical captures. Existing unsigned/dev file provider and
keys remain unchanged; selected production without admitted keychain retains
truthful unsealed/unverifiable behavior and cannot fall back to file keys.

The nonsecret continuity record is
`<AppData>/capture-seal-keychain/continuity.s1.json`, format
`capture-seal-keychain-continuity.s1`: scope_sha256, ordered committed keys
(id/full SHA-256), pending reserved key or null. It supplies continuity evidence,
not a keychain namespace authorization or signed platform receipt. Durable
reservation precedes add; exact key readback precedes commit. Unknown outcome,
missing/locked/denied item and duplicate add never imply success or permit
replacement. Rotation retains earlier items/IDs; no delete/reset/migration path
is provided. Cache users reverify the requested committed key on each read, even while a
pending rotation remains blocked. Authority is process-local, initially validated
and rechecked for enrollment/rotation; failed recheck revokes it. Seal waits for
concurrent verification readers instead of recording an unsealed act due only
to ordinary lock contention. First-use denial is checked before namespace
creation so enrollment can retry without deletion/reset.

A future signed-candidate witness must establish admitted membership/no-UI item
access, explicit fresh enrollment/restart/readback, retained-key rotation and
historical capture verification, denial/lock/missing failure and no fallback,
and unchanged relevant capture/records behavior. These facts join the selected
service/account/group and App build, not another signed App or development
namespace. Both marker loss and keychain loss require explicit continuity
handling; ordinary capture never regenerates a first key.

The mock source fixtures and CF attribute fixtures are not this actual witness.
All real SecItem calls are disabled in test builds. Keys remain readable by the
App process and do not prove person identity or exclusion of all same-user/admin
actors. Same-user marker tampering/rollback and external deletion remain stated
limits. Packaging owns the runbook/configuration/profile/witness inputs; runtime
owns the provider and failure semantics; parent owns integration and reserved
owner choices remain reserved.

Native qualification notes from SDK review: dictionaries now use CFType equality/
retain callbacks; returned non-sync accepts boolean false or exact numeric zero,
never absent/unknown values. The no-UI query flags are deprecated on current SDKs;
actual suppression/support must be observed before signing-stage activation.
This source preparation does not establish successful no-UI operation. A modern
authentication-context implementation, if required by the actual candidate,
needs reviewed source behavior before reliance. PACKAGING I-4/G-8/SIGN-3's
historical SEAL-2 wording must be read with this adopted SEAL-C signing obligation;
SEAL-2 remains deferred and no broader guarantee is inferred.

Final bounded source disposition: normal Seal reads only the committed current
key, so a lost historical item or unavailable pending rotation cannot by itself
make every new act unsealed. Verify still reads its requested committed key and
never mutates the marker. Explicit Enroll may resume markerless unreserved setup
only after checking legacy/primary absence under both locks; normal paths never
initialize, and directory recreation cannot follow an observed-present race.
Pending-only first enrollment with a missing item remains unavailable with its
reservation retained. Because the exact reserved secret cannot safely be
regenerated, the later runbook must retain that failure and obtain a concrete
continuity disposition/new independently admitted namespace if required. Do not
silently reset/delete the marker or retry add with different bytes. This is a
signing-stage recovery boundary, not a new generic approval prerequisite for
ordinary source work.

## Executable signing-stage preparation (lane3, 2026-11-01)

The source-owned [offline preparation](../../DEL-01-04/Work/seal-c-signing/README.md)
now consumes the integrated production_inputs completed plan and reuses the
existing package successor publisher checker. It emits a private metadata/gap
report, an unsigned entitlement proposal only when complete supplied profile/
certificate metadata agrees, and an exact SC-0…SC-6 witness/recovery plan. It
does not authenticate CMS, sign, call SecItem or alter KEYCHAIN_SELECTION=None.

The concrete proposed authorization route is an explicit macOS App ID for the
selected `com.chirality.app` (superseding earlier separate-v4-ID wording) and
Apple-issued Developer ID Application distribution profile including the existing
signer. The SDK spells the macOS entitlement com.apple.application-identifier as
AppIdentifierPrefix + bundle identifier; the prefix is obtained from the actual
profile, never guessed from the recovered team. The own-application group is
the smallest proposed namespace. Without a signed keychain-access-groups list,
SecItem documents that application identifier as the default group; with an
explicit list, the exact own-App group must be an authorized member. The helper
prepares either the default own-App route or one explicit own-App group, never
cross-App sharing or arbitrary profile entitlements. This conservative profile-
backed route is not a claim that every Developer ID app universally needs a profile.
For data protection keychain access groups specifically, Apple's public TN3137
and TN3125 (consulted 2026-11-02; cited in the helper README) document that the
entitlements must be authorized by a provisioning profile, and that Developer ID
profiles are supported. That is documentary evidence, not a signed witness.

Parent need not request team/private-key data again. Remaining actual actions are
owner confirmation of bundle/service/account and profile-derived own-App group,
Apple account operator obtaining the matching explicit App ID/profile, then
authenticated signer intake and separately authorized signing/enrollment witness.
A real profile's CMS/decode correspondence, certificate class/chain/validity and
signed entitlement membership remain independent checks, not facts proven by
plist shape. Existing v3 allow-jit-only metadata supplies none of these grants.

Inputs/outputs: existing completed tauri.package-inputs config/recipe/inventory;
exact publisher input and, when built, original binding/public projection/
requirement/effective config with independent original-binding digest; explicit
CMS, decoded plist, public certificate references and independent signer
fingerprint. Outputs are signing-plan.json, optional entitlements.proposed.plist,
witness-sequence.json and digest-bound COMPLETE.json. No new publisher picker
or new packaging config format is introduced. The helper cannot be used as an
authority input to the runtime. Original/private evidence and public derivatives
retain distinct exact digests.

The integrated host-only enroll_initial has no production caller. A reviewed
controlled native host invocation for the admitted signing stage remains an
explicit source prerequisite, not a hidden CLI/renderer bypass or startup act.
The witness plan identifies that prerequisite before any actual signing/
enrollment result may be claimed. Native qualification and existing packaging
FP/notary/install owners retain their respective execution scope.

The [concrete invocation design](../../DEL-01-04/Work/seal-c-signing/ENROLLMENT_INVOCATION.md)
narrows that source prerequisite: one native-menu administrative action, original
window and private prepared enrollment subject, no renderer/MCP/CLI constructor,
inside-lock marker/root/policy revalidation, and existing key_setup/Quit exclusion.
It specifies exact prospective runtime/native file ownership and cancellation/
staleness/concurrency tests. It is design for a later admitted implementation,
not a claim that the caller or native witness already exists.

## Inactive provider confirmation-subject join

SEAL-C-PREPARED-01 replaces the path-only entry with
`prepare_enrollment()` and `enroll_initial(PreparedSealEnrollment)`. The
private non-Clone/non-Deserialize intent freezes checked publisher/provider
policy, physical AppData/ancestor/directory identity, expected absence, exact
marker bytes/identity and committed/pending key IDs. Read-only preparation makes
no SecItem call or state write and holds no advisory lock across confirmation.
The consuming call refreshes authority and refuses changed policy before locks,
then performs the reviewed absence/directory join under enrollment lock before
fresh query and marker join under continuity lock before readback/add. Direct
path-only/dispatch enrollment is unavailable in production.

This is an inactive provider prerequisite, not the native operator action. The
original-window, affirmative confirmation, key_setup and Quit duties remain with
the future native host caller. Preview/attempt data cannot reconstruct authority;
dropping an intent cancels without effects. The compiled None gate, exact signer
inputs, original/private evidence and separate actual signed witness are unchanged.
No profile/namespace choice, entitlement/signing change or real SecItem access
is established by the source fixtures.

The prepared provider now derives AppData from the installed capture-seal folder
through a read-only accessor and accepts no enrollment path argument. A changed
installed root or a post-join presence/absence change refuses before backend
effects. No installation/legacy behavior changes. Path-based open races against
hostile same-user mutation remain explicitly bounded; this is not a claim of
atomic namespace integrity or completed native-caller confirmation.

## Native caller now wired in source, still None-gated

[The native caller implementation](../../DEL-01-04/Work/SEAL_C_NATIVE_CALLER.md)
closes the source invocation gap: one native-menu worker retains the original
window and private prepared intent, uses the unchanged safe-cancel confirmation,
then try-acquires key_setup, checks Quit, rechecks the original on the main thread
and checks Quit again before consume. Key_setup remains held until the provider
returns. No direct SEAL-C IPC/MCP/CLI/path/startup endpoint is added. Availability is a
pure compiled query; None hides the menu and rejects dispatch before preparation.

Packaging should now distinguish implemented source custody from the still-unrun
SC-0…SC-6 native/signed witness. No real namespace/profile/entitlement values are
selected by this join; no SecItem/signing action was executed. Success reports
only provider-returned success, not new-key creation or personal-act proof.
The final window check is not a lifetime lease, blocking provider waits may delay
App-initiated Quit, and external termination retains existing crash limits.

Menu-origin precision from caller review: existing core:default/core:menu permits
web content to construct a matching-ID menu whose click requests the native
question. The ID does not authenticate its origin. That route cannot confirm
the native sheet or grant provider authority; None rejects dispatch. Agent 0
must disposition the request-origin limit or separately authorize capability
narrowing before activation. No permission change is made by this contribution.
Provider/final-admission unwind is reported as outcome-unknown/not-retried inside
a boundary that preserves the shared key_setup lock from poisoning; existing
Quit logic is unchanged and real native/signing evidence remains separate.

## Current owner identity and v4-focused testing correction (2026-11-02)

The owner selected **production `com.chirality.app`**, retaining the existing App
ID, and expressly replaced a broad v3 comparison plan with **testing v4 itself**.
Earlier separate-v4-ID proposals in historical evidence are superseded for this
choice; no historical artifact is rewritten. Planned version4.0.0/minimum15 remain.
The recovered Developer ID team remains the parent/signer basis, not a question
that needs to be asked again. No real profile/group/signing/enrollment activation
follows from the App ID decision, and KEYCHAIN_SELECTION remains None.

`lib.rs` obtains AppData through `app.path().app_data_dir()` and installs that
same root for capture sealing and installation attribution. Reusing the ID can
therefore target an existing same-ID namespace; source inspection does not say
which files actually exist in the owner's v3 data, nor that v3 used the same
storage layout. Do not launch a new same-ID build against the owner's state to
find out. The narrow required precaution is to establish the selected test root/
account/configuration before use and avoid unintended existing-state access.

The adopted SEAL-C provider rejects preparation/enrollment when its legacy
`capture-seal` directory is present. It does not read/import that key material,
reseal captures, reset/delete the directory or silently make a new key. Existing
`capture-seal-keychain` marker/item state likewise needs its existing exact
continuity semantics. Retaining the App ID does not authorize reusing any old
key, group, installation.json or other stored authority. A same-ID future owner-
state test that meets such a refusal needs a concrete disposition; failure is
not a mandate for a v3 migration campaign or an automatic cleanup operation.

Service/account are independent compiled strings, not required to equal the
bundle identifier. Agent 0 then selected (2026-11-02, ordinary implementation selection, no
repeated owner string choice): service `com.chirality.app.v4.capture-seal`,
primary account `installation-keyring`, and `allow_first_enrollment=true` for the
explicit native enrollment action only. `v4` names a stable namespace generation
kept across later App versions; it is not bumped with the App version, because a
changed service would leave earlier keys unread and their captures "not verified
here". The selection is not enrollment or any key operation:
`KEYCHAIN_SELECTION` stays None until authorized signer facts and source
activation. The suffix lowers the chance of meeting a pre-existing item; it does
not prove the namespace is empty. Observed metadata of one installed v3 bundle
is bounded evidence, not an account of every historical installation. The exact access group
still derives from actual signer/profile authorization (AppIdentifierPrefix is
not guessed from team), bound to the selected `com.chirality.app` identity.
Rotation continues `<primary>.rotation.<keyId>`; normal paths never reenroll.

Practical sequence stays v4-focused:

1. Offline source/mock and isolated unqualified test-namespace/default-None
   builds exercise v4 functionality using fresh AppData/Codex/project fixtures.
   They do not establish the production identity or signing/keychain grants.
2. For the actual selected same-ID signed/installed v4 witness, use an explicitly
   admitted isolated macOS user/session with its own AppData/keychain and fresh
   v4 fixture projects, or another concretely reviewed isolation route. Merely
   changing HOME, choosing another project or copying the app bundle is not
   assumed to isolate OS AppData/keychain. No new account/session is created or
   requested by this source work. Packaging/native owners retain the later
   precise setup and actual-operation authority.
3. The owner tests v4's functional experience and the actual signed subject.
   Retain v3 artifacts only as fallback/aesthetic reference; no v3 equivalence,
   regression, migration or rollback qualification is a publication gate.

The owner also approved exactly the webview core:menu narrowing described in
[CORE_MENU_CAPABILITY_NARROWING.md](../../DEL-01-04/Work/CORE_MENU_CAPABILITY_NARROWING.md).
It preserves Rust menus and ordinary UI/Accessibility routes while denying
webview menu-object construction/mutation. It is neither universal agent/human
parity nor a grant for person-reserved acts. It changes no signing or keychain
permission and requires no immediate new owner act in this source lane.
