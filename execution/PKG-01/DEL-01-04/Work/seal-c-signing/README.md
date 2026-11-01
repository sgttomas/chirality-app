# Offline SEAL-C signing preparation

This is executable preparation for the integrated SEAL-C provider, not an
activation tool. It never invokes a build, codesign, Security's SecItem APIs,
Apple accounts, networking or a credential/keychain reader. Default runtime
`KEYCHAIN_SELECTION=None` is unchanged. All committed tests use invented data.

## Concrete proposed route and source basis

The installed public macOS SDK supplies two relevant facts (exact source hashes
and observations are in `sdk-basis.json`):

1. SDK `Entitlements.plist` spells the macOS application-identifier entitlement
   `com.apple.application-identifier`, with value
   `$(AppIdentifierPrefix)$(CFBundleIdentifier)`. **AppIdentifierPrefix is not
   assumed equal to Developer ID TeamIdentifier.** Obtain it from the actual
   independently authenticated profile/signing authorization.
2. `SecItem.h` documents application-identifier as the default keychain access
   group unless a `keychain-access-groups` entitlement is present. If that list
   is present, the calling App must belong to the queried group. Data Protection
   selection enables these access-group/accessibility rules on macOS without
   synchronizable items.

The smallest proposed namespace is therefore the **own-application group**, not
cross-App sharing: exact profile prefix + selected separate v4 identifier. This
is a proposal until the owner/signing stage adopts the actual value. The helper
never substitutes the recovered team for the prefix. Where the profile grants
an explicit group list, it checks an exact own-App group against those grants
and emits only that one group. Where there is no group-list grant, it prepares
only the profile-authorized application identifier and team entitlements; SecItem's
documented default-group route is the intended candidate. Neither is
"entitlement-free": the exact application-identifier must be authorized and
actually signed into the correct App.

For a conservative reviewable authorization route, the existing Apple Developer
account operator should register/use the **explicit v4 macOS App ID**, then obtain
an **Apple-issued Developer ID Application distribution provisioning profile**
that includes the already identified signing certificate and grants that exact
application identifier (and the own-App group if a group list is used). Retain
the original CMS and decoded metadata. This is a proposed profile-backed route;
it does not assert that every Developer ID app universally needs a provisioning
profile. No new certificate/private key, new account, purchase, cross-App sharing,
or repeated team-input request is part of the minimum proposal.

The executable handles a conservative metadata shape: `Platform=["OSX"]`,
`ProvisionsAllDevices=true`, no device list, valid creation/expiration interval,
matching single TeamIdentifier, single explicit AppIdentifierPrefix, exact
macOS application-identifier grant, matching team entitlement, no enabled
get-task-allow, and selected public certificate bytes in DeveloperCertificates.
Other/ambiguous shapes refuse for review rather than expanding permissions.
Terminal `prefix.*` group grants may cover the exact own-App group; arbitrary
wildcard/glob matching and cross-App groups are not supported.

**These are metadata-consistency checks.** The helper does not authenticate CMS,
prove that the plist was decoded from that CMS, parse/validate the certificate
chain/class, or establish OS entitlement acceptance. Those are exact signer
intake checks before relying on the output. Supplied CMS bytes, decoded plist,
public DER certificate, signer fingerprint and resulting signed entitlements
must be independently joined. The existing v3 App's allow-jit-only entitlement
and absent embedded profile establish neither a v4 access group nor authorization.
The old default-None unsigned candidate is not a production publisher binding.

## Minimal remaining owner/operator actions

1. Parent receives the owner's exact **bundle/service/account choice** and
   existing-team use. The proposed separate-v4 names are already in the parent
   decision context; this tool contains no real default choice and asks for no
   team or private key again. The existing closed three-field publisher input
   remains unchanged.
2. The Apple account operator obtains the explicit App ID/profile authorization
   described above for the existing Developer ID Application certificate. The
   actual AppIdentifierPrefix/profile grants settle the group recommendation.
   A signer authenticates the CMS/decode and certificate correspondence. No
   credential, password or private key is given to this helper.
3. After source/metadata review, the owner authorizes the concrete signing and
   fresh-namespace enrollment witness. A reviewed source activation/invocation
   must exist first; this preparation does not turn on the gate or perform it.
   The profile/entitlement group and first enrollment scope are approved as exact
   artifacts, not as a generic extra approval on every ordinary source action.

Absent those inputs the output lists precise missing artifacts and actions. It
does not merely report "profile unknown", and it never manufactures a qualified
or authenticated result from synthetic fixtures.

## Run with existing packaging and publisher outputs

Use `app/packaging/production_inputs/prepare.py` first. Its `check_plan` must
accept the selected plan directory. This helper does not create another config
picker: it consumes the exact 4.0.0/minimum15 unsigned config and its completed
input account. The plan must bind the exact publisher input digest; a default-None
test namespace is refused as a production subject.

The request is a closed JSON object:

```json
{
  "format": "seal-c-signing-preparation/1",
  "namespace": {"service": "invalid.example.seal", "account": "installation-keyring", "access_group": null},
  "publisher_input": {"path": "publisher.json", "sha256": "<exact digest>"},
  "publisher_artifacts": null,
  "profile_plist": null,
  "profile_cms": null,
  "signer_certificate": null
}
```

All reference paths are relative to one explicit evidence root; use standard
`{path,sha256}` references for supplied profile plist/CMS and public DER certificate.
`access_group:null` requests the profile-derived own-App group proposal, not an
unrestricted group. If a group string is supplied it must equal that exact own-App
group. Missing profile/certificate bytes produce a gap report, without an
entitlement plist. Supplied contradictions still refuse even when another
companion is missing.

Before a real publisher-selected build is authorized, `publisher_artifacts` may
be null and the report retains the missing build binding. Once available, supply
exact references named `publisher_binding`, `publisher_projection`,
`publisher_requirement`, and `tauri_config` (the **effective build configuration**,
not merely the packaging overlay). The existing package successor's
`Context.publisher` performs schema, exact-byte, requirement/template/recipe,
private-original/public-derivative and effective-config joins. Its separate
trusted original-binding digest is required for a complete consistency account;
missing independent trust remains missing. A public derivative digest never
substitutes for the original. The resource mappings and minimum must agree with
the completed packaging plan. No final App or source revision is authenticated
by that value checker.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 execution/PKG-01/DEL-01-04/Work/seal-c-signing/prepare.py \
  /private/evidence/request.json --evidence-root /private/evidence \
  --package-plan /private/completed-package-plan --output /private/new-seal-plan \
  --trusted-signer-sha1 <independently-selected-public-certificate-fingerprint> \
  --assessed-at <explicit-UTC-time-Z> \
  --trusted-publisher-sha256 <original-binding-digest-if-available>
```

The fingerprint is public certificate metadata, not a password; it is nevertheless
kept out of committed source and routine output. Actual values/references stay
in the private input/output closure. `assessed_at` is the stated assessment time,
not a trusted time source. Preparation outputs must be rechecked against current
profile/signing validity when used. No account sign-in or profile acquisition is
performed by this command.

Private evidence and the packaging plan must be outside this repository worktree.
CMS, decoded plist and certificate references must name distinct byte digests;
this separation is not cryptographic proof of CMS/decode correspondence.

The output must be a new directory, outside the repository, evidence root and
package plan, with an existing physical parent. Files are private (0600 in 0700).
`signing-plan.json` binds exact inputs/plan/code/SDK basis and lists remaining
conditions. `entitlements.proposed.plist` is emitted only when complete supplied
metadata passes the conservative route. It never copies v3 allow-jit or arbitrary
profile entitlements. `witness-sequence.json` is an exact copy of the source-owned
plan. `COMPLETE.json` binds each output digest, and `INCOMPLETE.txt` remains on
failed/interrupted publication. Require `check_output(directory)` before review;
completion means output integrity, not permission to sign or activate. Extra
output members are refused. A profile-only proposal with missing publisher
artifacts/trust is labelled `profile-proposal-publisher-gaps`; the report separately
states `publisher_closure`, metadata gaps and the always-outstanding activation
conditions. A supplied trusted original-binding digest must be lowercase SHA-256
and cannot be supplied without its artifacts. The effective build identifier and
version must equal the completed packaging plan, not just each other.

## Signed witness and recovery

`witness-sequence.json` gives SC-0…SC-6: exact subject/profile, source-controlled
invocation, actual signing/S4, explicit enrollment+restart, isolated locked/denied/
missing behavior, rotation/history/cache/concurrency, and final package joins.
The sequence is data, not a shell script or automated runner. Existing packaging
owns Option B, signing/notary/install/FP operations; native qualification remains
its separate undertaking.

The native source caller is now wired by
[SEAL-C-NATIVE-CALLER-01](../SEAL_C_NATIVE_CALLER.md), with the menu absent and
dispatch refused under None. Actual signing-stage policy admission and native
witness remain outstanding. The [concrete invocation design](ENROLLMENT_INVOCATION.md) defines a private
prepared subject, native-menu/original-window confirmation, inside-provider-lock
revalidation and reuse of the existing key_setup/Quit exclusion. The minimal
recommended invocation is a reviewed native host action for the admitted signing-stage fresh namespace,
using the existing private authority—not a generic renderer/MCP/CLI override,
and not silent enrollment at startup. The runtime/native owners implemented that source join under the unchanged
None gate; this metadata tool does not bypass or activate it. A signed/native
result still requires the exact admitted subject and actual witness.

Normal Seal uses the committed current key and Verify its requested committed
key; neither commits pending rotation. A locked/denied unreserved enrollment may
retry explicitly after admission checks. Pending with matching actual item can
be committed only through explicit enrollment/rotation. Pending-only missing
first-key material stays unavailable: its digest cannot reconstruct the secret.
Preserve the failed subject and reservation; a later explicit continuity decision
may admit a distinct namespace, never reset/delete or add different bytes under
the old reservation. Normal paths never reenroll after total loss. No migration,
old-capture reseal, SEAL-2 entry seal, agent exclusion or person authenticity is
introduced.

## Tests

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s execution/PKG-01/DEL-01-04/Work/seal-c-signing -p 'test_prepare.py' -v
```

Fixtures use invented certificate/CMS bytes and the existing synthetic publisher
fixture. They test only metadata and representation, not genuine profiles or
certificates. Tests cover distinct prefix/team, default versus explicit own-App
group, metadata failures, exact-byte tamper/symlink refusal, incomplete outputs,
default-None refusal and existing publisher original/public joins. No real
SecItem, key, certificate, profile, native candidate, signing or build is used.

Independent Claude Opus 5.5/high reviewed f25f99aa: no blockers after bounded
metadata corrections and two invocation-design precision fixes. The manager
added exact effective version/identifier joins, explicit publisher-gap status,
validated non-orphan trusted digest, exact output membership, distinct profile
artifacts, full UTC timestamp syntax and private-input location guards. Invocation
comparison points now precede fresh_namespace under the enrollment lock and
follow marker load under the continuity lock, with refreshed authority compared
to frozen policy first. App-initiated Quit exclusion is distinct from external
termination and the known blocking-wait liveness limit. No runtime code changed.
