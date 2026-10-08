# Host attempt transport, staged s2 development subset

The named payload `distribution-evidence-transport.s2` is validated against the
adjacent closed schema. This first implementation supports only explicitly
unqualified development attempts: originalSource and sourceSelection are null,
and the closure is exactly attempt.json plus transport.json. It refuses a
production/qualified mode. Extending the payload to selected-source transport
requires a named semantic/schema revision and reviewed reader adoption.

The native setup derives app_data/runtime/distribution from Tauri's App-data
root and actual Root NativeNamespaceBindings. Each publication/read reobserves
the protected native homes/fixed sources. Vendor overlap is refused by comparing no-follow-opened device/inode ancestor
chains in both containment directions, including case aliases and a prospective
root whose suffix does not exist. The check precedes each directory creation and
repeats at use; named App-data/runtime descriptors are rechecked before writes.
The store root's physical identity is held.
The store creates a private staging directory, exclusive regular single-link
files, fsyncs files/directory, renames with no-overwrite, and fsyncs the parent.
No reference is returned before exact readback succeeds. Each attempt receives
a new opaque directory even when a refused attempt leaves the same prospective
H5 counter available. Files from failed publication may remain as unpublished
pending evidence; no reference is issued and no automatic pruning is provided.

The reference binds the generation, relative publication name and both SHA-256
digests; native memory additionally binds the publication directory identity.
At use, the reader rechecks protected namespaces, generation/home, file type,
link count, private ownership/mode, named descriptor, exact digest and bounded
size, then audits the entire closure against expected names/types/modes/sizes/
digests. This is a bounded filesystem observation, not an atomic snapshot or a
future integrity guarantee. The creation manifest asserts no future checks.

Host.start publishes before final vendor revalidation and before the short
writer/source gates. It never allocates live custody to publish evidence. Native
setup marks successor configurations as requiring artifacts: missing/failed
store initialization refuses before spawn, including secondary home paths that
have not yet received store setup. Existing source-only fixture configurations
retain their explicit in-memory route. Production still refuses at the compiled
missing selection/custody check, with no supplier execution or trust override.

Host.observe reads outside Inner/source/ledger locks, then rechecks H5 and attempt
before projecting distributionEvidence. RuntimeSession/NativeView display that
separate field without changing closed legacy version/lifecycle data or standing.
A later failed read replaces the display with unavailable; a stored reference
is not itself a successful current read. No App UI is included.

## Remaining H3B-2 work

This is durable Host attempt evidence, not observed-verification.s1 or
lifecycle-event.s1. Full selected closure transport is an implementation
residual, not blocked merely by absent real S3: private synthetic selection
fixtures may exercise it while production selection remains None. It must copy
all original selection/reference/attestation/dependency bytes and original
relative paths, separately identify source/mirror locators, refuse collisions,
and recheck the original compiled association at creation and every reliance.

Full S1 production still needs truthful configuration/launcher/check evidence,
nullable generated/reference/attestation/candidate fields where absent, complete
shape and semantic checking, phase/outcome checks, exact envelope/reference
publication, and generation equality across restart/pre-spawn events without
rewriting legacy bytes. The reviewed lifecycle-label-join.s2 method addresses
only its named label join. It does not supply these remaining checks.

Persisted reference indexing/reopening after an App restart, selected closure
export, retention/pruning, secondary-home native store setup, and full S1 native
reference presentation remain separate work. The in-memory directory binding
is not claimed reconstructible from an arbitrary external reference. No package,
installer, qualification, current live custody or rendered UI witness is claimed.
