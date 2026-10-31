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
is provided. Cache users reverify provider availability on each read.

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
