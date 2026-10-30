# S4 signing facts and package receiving join

`S4-INSTALLED-INTEGRITY-01`, 2026-10-30, supplies a runtime observation boundary
under DEL-01-01 [technical clause](../../DEL-01-01/Work/INSTALLED_INTEGRITY_S4.md).
Its selected basis is distribution-s1/README.md and original pre-flattening
DISTRIBUTION_IDENTITY SHA-256
`d51c1130f5a1356fcc2a6100f1486e8ee3a0728de59f4fe69d4ac6a1580e5290`.
This supplement leaves PACKAGING_AND_DISTRIBUTION's signing/FP obligations,
legacy producer and frozen schema/consumer identities unchanged.

The compiled publisher requirement remains None until the owner independently
selects publisher/team and production bundle identifier. No real identity is
selected or inspected, no signing/notary/account act occurs, and no package is
qualified. SIGN-1 Option B preserves the stock supplier bytes/signatures;
FP-0/FP-1 check those signatures. The runtime uses exact full reference equality,
not a second supplier signature trust anchor. Dynamic no-network validation needs
macOS 11.3+; unsupported API/flag failures refuse. The base configuration has no
explicit minimum, and the unsigned development overlay is not a production
minimum selection.

## Exact joining obligation

The S4 observation is outside the installer and is process evidence only. It
joins full generation, full supplier inventory and the compiled build-selection/
reference/attestation association. Its App facts are static/dynamic cdhash,
identifier, team identifier, signature flags, get-task-allow:false, requirement
digest, exact validation flags and resolved own-bundle/executable/resources/
parent paths. Translocation and App Management protection remain unestablished.
The custody assumption and residual check-to-exec/hostile mutation limits travel
with the evidence. The S4 reader verifies exact artifact bytes and these joins;
serialized records never grant live process authority.

A later packaged witness must independently bind the actual App revision,
build identity/version and production bundle identifier to those App signing
facts and compiled selection. It must also join the pkg-identity.s1 logical
`package_record_id`, exact package envelope, and pre-notarization installer
digest, retaining the separate post-staple digest and actual install subject.
Those package facts are not inferable from current_exe, a cdhash or the resource
mapping and are not fabricated by the runtime observation. Every supplier
Mach-O, entitlements, signing configuration digest and FP-0/1/3 evidence remain
OUT-002 responsibilities. Archive custody.json is acquisition evidence, not
installed custody.

The static-distribution checker continues requiring verification_artifact:null;
legacy EXP/SQ package links are not S4 runtime joins. Activating an S4-aware
package producer/receiver needs its own explicit version and candidate-bound
qualification evidence. Source fixture passes do not pass FP-2/W-4, signed or
quarantined install/launch, or terms/publication decisions. Packaging owns those
remaining acts and evidence; App Agent 0 owns technical adoption/integration and
the owner retains publisher, acceptance and release choices.

Signing information returned for the dynamic process is disk-backed (including
Security.framework kSecCodeInfoFlags); matching static/dynamic fields are a
consistency join, not independent runtime integrity proof. Running-process
assurance comes from SecCodeCheckValidity against the same compiled requirement.
Optional kernel guest-requirement matching can be assessed with the later exact
publisher requirement; it is not claimed here. The trusted stable parent-path
assumption and unestablished translocation/App Management protections remain
explicit limits, not observed access controls.
