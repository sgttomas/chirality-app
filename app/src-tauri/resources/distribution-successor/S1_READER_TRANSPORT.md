# Staged S1 reader and transport receipt

This implementation preserves the selected observed-verification.s1 and lifecycle-event.s1 shapes. Its semantic method is explicitly observed-lifecycle-reader.s3, including the separately reviewed lifecycle-label-join.s2 correction. It is not silent adoption of the historical Python reader. Production selection remains None; no installed integrity/custody issuer exists, and custody pass or verified claims refuse. Synthetic tests establish implementation behavior only.

## Receiving interface

The existing native distributionEvidence adapter returns state read only after current protected namespace, exact generation, original source association, digest, shape, semantic, and final inventory checks. Its evidence contains reference, artifact, lifecycle (nullable), transport, outcome, standing, readStanding and unsupportedEnvelopes. Failure returns unavailable with the existing reason dispatch; malformed or contradictory nonnull references never become missing-success.

reference has format distribution-s1-reference.s3, publication, generation, observed {path,sha256}, lifecycle nullable {path,sha256}, transport {path,sha256}, and reader. publication is relative to app_data/runtime/distribution. Native-held expected bytes and publication device/inode are deliberately not serialized: this projection is not a restart-hydratable authority token. Reading a foreign generation or replaced publication refuses.

transport has format distribution-closure-transport.s3, method selected-s1-contract-closure.s3, sourceAssociation, mirrorLocator, generation, entries, reader and limit. sourceAssociation is null without selection; otherwise it contains method, originalSource, compiledAnchor {path,sha256}, expectedReference and adoptionAttestation. originalSource remains the bundle source; mirrorLocator is the distinct full publication location. Paths and selected bytes are unchanged. The manifest binds all other members; its own exact digest is held by reference, avoiding a self-digest cycle. Creation correspondence does not assert future integrity.

reader exposes semanticRevision; readerSourceSha256, closureReaderSha256, storeReaderSha256, storeGuardsSha256, preflightReaderSha256; factsSchemaSha256 and transportSchemaSha256; exact S1 schema digests; labelJoin identity; transition table digest and exact historical source provenance; and stringIdentity. Receivers must explicitly adopt these method/digest identities. Stable JSON shapes do not imply compatibility with an older semantic reader. Store identity binds both the S1 module and parent physical/atomic helper source. This method receipt is not an exhaustive application build identity: native namespace/runtime dependencies and compiler/library versions still require the separate exact App revision/build joins.

## Exact declared closure

The sealed capability starts at the compiled build-selection.s2 path/digest. Runtime callers, environment and records cannot supply it; only private cfg(test) constructors accept synthetic fixtures. It includes selection itself, its expected and attestation files, and these declared references:

- expected: label_evidence, generation_correspondence, generated.provenance, generated.version_advance, archive.acquisition_authorization, archive.custody, archive.extraction_procedure.
- attestation: review_evidence, adoption.through_help_human, adoption.evidence.

Evidence targets are opaque exact bytes. Incidental nested path/sha256 JSON objects are not dependencies or authority. Duplicate paths with differing bytes/digests, file/ancestor collisions and reserved .chirality-s1 collisions refuse. The private fixture has thirteen distinct selected members. No selected historical example bytes are rewritten; private fixtures align their own pin and rehash their own dependency chain.

Publication rejects physical source/vendor overlap before writes, preserves no-follow traversal and private namespace checks, uses durable no-overwrite publication, and rechecks source association on creation and every read. Final inventory compares names, kinds, modes, sizes and digests after reads. These are bounded observations, not an atomic filesystem snapshot; the remaining check-to-exec race is not claimed solved.

## Semantic and Host sequence

The reader checks closed schemas; strict inventory method, members, parents, manifest and expected correspondence; declared artifact digests; generated/reference/attestation bindings; reviewer independence; label/pin correspondence; executable/root/PATH prefix, separate homes and removed wrapper environment names; mismatch-before-gap result derivation; all transition tuples; envelope observation/generation/result/standing/phase joins; and unchanged legacy event schemas. Known distribution-preflight-facts.s3 evidence must match observation generation, inventory, raw label and configuration. Unknown evidence retains opaque semantics.

Host publishes and reads back the truthful pre-spawn observation before the final revalidation and short custody guard. Prospective H5 is not live custody. Missing generated provenance/reference/attestation remain null or missing with unverifiable outcome; no missing fact is fabricated. The actual unchanged LT-09 event is enveloped after it occurs, in a new immutable publication with identical observation bytes. Late completion cannot replace a newer attempt reference. A same-attempt post-event publication error makes evidence unavailable while preserving actual legacy history.

Only actual LT-09 envelopes are produced. Other envelope production, restart reference hydration/indexing, and secondary-home store initialization remain implementation residuals. Previous nonnull legacy H5 on restart LT-24 is not rewritten or paired with a new prospective tuple. Real S3 selection/acquisition/extraction/probe/generated provenance/version advance and installed custody issuer remain qualification inputs, separate from implemented selected-closure machinery. Native App UI and Group B consumer adoption are outside this slice.

## Pinned Python identity compatibility

Reviewer independence implements Python str.strip().casefold() on Unicode scalar strings using a generated immutable table pinned by a separate literal expected digest. The table records exact Python 3.13.7 interpreter digest/version, unicodedata 15.1.0, generator digest and oracle outputs. generate_python_identity.py --check reproduces its bytes with that interpreter. Actual Rust tests compare every valid Unicode scalar and mixed strings with the Python oracle, including boundary controls, expansions and Unicode same-identity cases; source author/reviewer strings remain unchanged. Mapping tampering even under unchanged metadata and metadata/version drift refuse. This is the named pinned basis, not a claim about arbitrary future Python/Unicode versions or lone surrogate JSON strings.
