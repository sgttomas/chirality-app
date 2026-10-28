# B-S4-NAMESPACE-ADOPTION-v1

Named technical receiving successor for the bounded S4 EXP/PKG file cohort.
Selected Host source: `b7e9639d87b84af9a218e05f9e4f3c85fe00ebc0`.
Predecessor export source: `f2671306a3e167a5a858b11d04b6b1090771139a`.
This contribution selects the reviewed Host namespace implementation for this
consumer; its integration is recorded by the owning manager. It does not claim
canonical S1 adoption, an owner gate, namespace authentication or qualification.

## Exact identity selection

`pins.namespace-v1.json` fixes the entire new reader receipt and selected source
hashes, records the old pin-file digest, and maps each previous/new reader field
under `reader_changes`. `receive.py` selects that file through a literal digest.
The previous `pins.json`, historical f267 exports/provenance and run evidence
retain their original bytes. No caller choice or automatic fallback is offered.

The semantic revision string remains `observed-lifecycle-reader.s3`; that string
alone never establishes equal implementations. Five reader identities change:

| Receipt field | Source | Change relied on |
| --- | --- | --- |
| readerSourceSha256 | distribution_s1.rs | Exposes namespace authority dependency in the full receipt. |
| closureReaderSha256 | distribution_selection.rs | Separates selected root identity checking from full closure recheck. |
| storeReaderSha256 | distribution_store_s1.rs | Holds a current namespace lease across publication/read and nested readback. |
| storeGuardsSha256 | distribution_store.rs | Uses shared authority, current geometry/generation and the validated descriptor; admission preflight avoids full hashing under REC writer. |
| namespaceAuthoritySourceSha256 (added) | attachment_custody.rs | Names the live nonserialized namespace authority/epoch and leases shared with custody. |

New pins also bind hosting/runtime_session/recovery/lib integration sources,
exporter and NAMESPACE_ADMISSION.md. These are selected source correspondence,
not an exhaustive build digest or a replay of their runtime behavior. The
semantic schemas, transitions, string identity, preflight and label-join receipt
identities remain unchanged. The existing canonical EXP/PKG checker is unchanged.

## Active cohort and evidence

New selected/unselected fixtures are actual exports from a recompiled synthetic
Host test at the selected source, retained byte-for-byte under
`tests/group_b_distribution_receiving_namespace_fixtures`. Its provenance records
exact exchange hashes, source revision, command/features and executable digest.
The producer test executable is separately identified from the explicitly
invented application candidate used by the EXP/PKG fixtures. B passively checked
the executable digest and raw copies; no B Rust build or native action occurred.

Positive receiving uses the same complete canonical six-record join. Tests
refuse old producer identity, old receipt relabelled to the new source, mixed
reference/transport receipts, missing or false namespace source digest, added
namespace authority claims, changed namespace source and prior byte/generation/
LT09/verified/custody violations. No historical acceptance is rewritten.

## Authority and limits

NamespaceAuthority is native-held and nonserialized. Store operations use its
current lease; attachment capabilities pin issuing epochs and may refuse after
admission. Exported JSON does not restore either. A file-consistency pass does
not show that namespace admission happened or prove current geometry/epoch,
attachment liveness, original source custody or actual App build. The report
explicitly sets namespace_authority_authenticated=false.

The reviewed Host design keeps admission contention fail-fast, selected closure
hashing outside the REC writer, bounded filesystem observations, and explicit
partial protective-admission outcomes. These behaviors remain Host evidence;
B does not implement another semantic or native namespace reader. S3, installed
custody, real native examination, M1 qualification, package witnesses and release
remain separate. This cohort adds no SQ packaging gate.
