# Production publisher and App identity — owner decision preparation

2026-10-30; proposed, not selected. This follows integrated S4 at
`3cb060164ec8544bdd7ef700d9e095314d63a7e1`. It does not authorize signing,
notarisation, publication, v3.0.1 replacement, credentials or account access.
SIGN-1 Option B remains selected: supplier bytes/signatures stay unchanged.

## Decision to obtain through App Agent 0

Select the **exact production bundle identifier and expected Developer ID
Application publisher/team binding**, and whether that identity is intended to
continue an existing shipped App identity or establish a separate v4 identity.
The expected requirement will use an independently specified Apple Developer ID
Application certificate-chain template; the owner selects the identifier/team,
not arbitrary requirement logic or a self-derived designated requirement.
This selects a team and bundle identifier, not a particular signing certificate.
CF-1's certificate/signing-identity name is a separate signing-configuration
input supplied for the owner's later signing act; certificate renewal is not
itself a new team/identifier selection. Exact template constraints remain
reviewed implementation work.

Two concrete identity routes are available for the owner to choose:

- **Separate v4 identity:** an exact owner-controlled reverse-DNS identifier,
  distinct from the development identifiers and any shipped v3 identifier.
  This separates identifier-selected App-data/cache/WebKit namespaces and is
  compatible with retaining v3.0.1 as fallback. It does not itself implement
  data migration, guarantee side-by-side installation naming, or perform the
  owner's later replacement act. Package/app naming must also avoid replacing
  the fallback during qualification.
- **Existing identity continuity:** the owner supplies the exact prior shipped
  identifier and publisher/team basis. Verify that continuity before relying
  on it; the skeleton identifier is not proof of the existing shipped identity.
  Sharing identity can also share identity-selected storage/launch associations;
  prior-version data compatibility is not established by retaining a name.
  Package I-4's stable team/identifier and DEL-01-04's proposed SEAL-2 key-store
  relationship must be reconciled before claiming continuity or key access.

On **both routes**, the chosen team and identifier become the stable I-4 identity
for later v4 releases. SEAL-C's existing App-data key, its move to the OS keychain
at signing under OI-011, and any G-8/SEAL-2 entitlement or provisioning-profile
needs must be reconciled with that identity. Neither route carries development-
namespace keys or capture history into production without separately designed
migration; selecting a name does not perform that migration.

No prior production team or bundle identifier has been selected or inspected in
this lane. The local `v3.0.1` tag is retained; its inspected `runtime/package.json`
is a runtime workspace manifest, not a production signing identity. It supplies
no basis to guess the v4 identity. Current source uses
`dev.chirality.app-v4.skeleton`, and the native candidate uses a fresh
`dev.chirality.app-v4.candidate.…` namespace; neither is a proposed production
default. Public release and replacement remain distinct owner decisions.
An existing-identity continuity choice needs evidence from an actually shipped,
signed v3 artifact or its authoritative release identity account, not an inferred
identifier/team from that workspace manifest. No such artifact or identity is
inspected by this preparation.

Suggested decision wording, with values provided privately only after selection:

> Select [separate v4 identity / existing identity continuity] and the exact
> production bundle identifier and Developer ID Application publisher/team I
> provide through the secure input route. Use those values only to prepare and
> review the independently anchored production build requirement and matching
> package configuration. Keep ordinary builds unselected and retain the fallback.
> This is identity selection, not signing, credential use, release or replacement.

## Supported minimum-OS and version choices

The narrow publisher decision does not require guessing these values. If the
owner wishes to decide them together, the concrete proposals are:

- **Minimum macOS 15.0 for the current complete-stock composition.** The
  unsigned development overlay already declares 15.0. A read-only
  `xcrun vtool -show-build` inspection of all 31 Mach-O objects in unchanged
  candidate `fdcf608fb5-23c6c3f22f5e` found P-0 and stock bundled zsh declaring
  15.0, 26 voice objects declaring 14.0, and three other supplier objects
  declaring 11.0. Exact paths/digests/results are in
  [`successor-deployment-targets.json`](successor-deployment-targets.json).
  No object lacked a reported target and no command failed. Therefore 11.3,
  although the S4 no-network API floor, is not a supported whole-candidate
  minimum proposal. A lower minimum needs a separately assessed composition/
  build and qualification basis; no supplier change is selected here. Metadata
  is not an actual run on macOS 15.0 or proof that all relevant behavior works.
- **Release version 4.0.0 for the eventual initial v4 publication**, if the
  owner chooses to set it now. PRD V4-CST-02 names v4.0 on macOS Apple Silicon;
  current Tauri `0.0.0` and Cargo `0.0.0-skeleton` are development values.
  The proposal follows that product designation, not a previously approved
  release number. Set package/Info.plist/version evidence consistently in a
  separately identified production build. Selecting the number neither
  publishes a release nor replaces exact source/build identities. Deferring
  this choice until package construction does not prevent publisher selection.

## Secure input and build-selection route to implement after selection

This is a reviewable implementation proposal, **not an existing feature**.
`installed_custody.rs::COMPILED_PUBLISHER_REQUIREMENT` is currently literal
`None`; `build.rs` currently calls `tauri_build` only. No real values are read
or requested by this draft.

1. App Agent 0 obtains the decision once. For exact identifier/team values,
   use `request_secret` with file delivery to private task scratch, never chat,
   command-line literals, public PR text or logs. The input contains identity
   selection only, not a certificate private key, password, signing credential
   or notary login. No keychain enumeration or certificate extraction is needed.
2. The runtime/build owner implements a reviewed deterministic generator with
   strict identifier/team validation and requirement-string escaping, using an
   independently specified Apple Developer ID Application chain template. Do
   not accept arbitrary supplied requirement logic or derive the trust anchor
   from the candidate's own signature. Template/API correctness and negative
   tests are implementation work before reliance, not established by this draft.
3. Require explicit production-build selection. A build-time private locator
   may supply selected bytes to the generator, but no runtime environment,
   configuration, resource, UI flag or caller path can choose authority.
   Ordinary offline builds remain `None`; debug stays refused. Missing or changed
   private inputs and stale `OUT_DIR` must never silently reuse an earlier
   generated `Some`. The actual generated requirement is compiled into the
   exact candidate and used for both static and running-process validation.
4. Retain exact selected-input and requirement bytes, generator/template/recipe
   identity and resulting App build identity in controlled build evidence. The
   existing supplier S2/S3 anchor alone does **not** bind this new publisher
   selection. Do not repin frozen supplier artifacts. If private generated source
   contributes to the build, identify that input separately from the Git source;
   never claim a bare public revision completely identifies the built selection.
5. Keep public reports free of real identity/key material. Retain original exact
   signing/S4 evidence privately if required; a redacted public projection is a
   separately identified derivative, never an in-place replacement under the
   original digest. This handling does not make the eventual team/identifier
   secret: compiled requirement strings and shipped signing identities are
   inspectable, and S4 evidence carries identifier/team/path facts.
6. Coordinate the package/offline receiver with the runtime owner: S4 currently
   checks evidence against its **own compiled requirement**. An unconfigured
   `None` build cannot consume a real installed observation. A future receiver
   therefore needs explicit trusted matching publisher selection and exact
   package/S4 joins, while remaining unable to grant live-start authority.
   The package producer must also bind the independently selected identifier to
   actual Info.plist, signing facts, CF-1…8 and installed subject.

The expected next result after selection is the scoped generator/compiled-input
and matching receiver-selection implementation, independently reviewed with
invented identities before any real package act. App Agent 0 allocates that
runtime/build boundary and technical adoption; packaging owns configuration and
package joins. Signing/notary credentials and execution remain separate owner
acts. No such act, private value, or implementation is supplied by this draft.

## Evidence and review boundary

The deployment-target inspection used only static Mach-O metadata, not signature
display or supplier execution. Its full output remains at the digest-bound
scratch locator in the checked-in report; preserve it until consumers release
it. Native App/account state and the saved A/B inputs were not read or changed.
The source tuple and complete bundle identity remain those of the retained
development candidate, not the integrated S4 build or a future signed package.

This preparation does not change PK-R4, §9, the approved terms record, any
selected documentary projection, CI step, runtime constant or package config.
