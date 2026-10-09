# Constructed R2 carrier comparison

PROPOSED measurement result, not a selected carrier or production storage.
Receiving basis: resource-envelope PR #1195, exact reviewed source
3e905261fcbdfc9d4072c7db419baedc53bedb0d, merged
9031b63ef62282145bfd6949bad2e7b35348773d after required CI and independent full-range
READY. That merge selects no N/S/D/T/Q, retention policy or implementation.

## Method and interpretation

Use the same definition-valid exact 0.4 base, constructed answer and proposed
message0.2 content-only review. Compare illustrative compact JSON encodings:
inline all three; references to all three exact raw artifacts; and a hybrid that
references the base and embeds answer/review. The fixed hybrid partition makes
the comparison reproducible; it is not a product threshold or policy. Referenced
objects are counted once by exact bytes in this in-memory demonstration, not
assumed free or durably retained. Actor/custody identities are not deduplicated
into a content hash. No actual artifact store, journal or Host producer runs.

A smaller snapshot can move rather than remove costs. The result separately
counts snapshot bytes and retained referenced artifact bytes. The two-slot
illustration doubles one snapshot representation and adds its referenced bytes;
it is not a reservation formula for changing generations. Distinct old/new
critical sets, descriptors, temporary/control/admission files, failed leftovers,
terminal identity retention and reference-store metadata require additional
accounting. Actual Host custody, operation intent/outcome, target observations
and unresolved attempts are missing from this three-artifact corpus, not zero.

## Measured partial logical bytes

[Exact results](C3_R2_CARRIER_MEASUREMENTS.json) and
[read-only replay script](compare_c3_r2_carriers.py) retain 16 committed source
pins and 66 demonstrator checks: exact roundtrip, missing/rebound bytes, mutable
locator and self-consistent changed-subject refusal. These checks exercise the
illustrative codec, not a production resolver or immutable filesystem store.
Run `python3 compare_c3_r2_carriers.py <repository>` with existing offline
validators. Schema-only four-byte Unicode overflow remains a refused negative,
excluded from the six admissible cases below.

Totals include one illustrative current snapshot plus its exact external raw
artifact pool, in bytes. They exclude the costs named above.

| Constructed case | Inline | All referenced | Hybrid base reference |
|---|---:|---:|---:|
| normal | 11,266 | 10,521 | 10,469 |
| 1MiB_space_base_rebound | 1,051,339 | 1,050,595 | 1,050,542 |
| 1MiB_LF_base_rebound | 2,091,411 | 1,050,595 | 1,050,542 |
| ASCII_review65536 | 76,624 | 75,880 | 75,827 |
| quote_review65536 | 273,233 | 141,417 | 272,436 |
| LF_review65536 | 207,697 | 141,417 | 206,900 |

These encodings add per-artifact hashes/lengths, so their totals differ from the
previous three-string minimal envelope. The reference and hybrid savings depend
on exact content and escaping; quote-heavy review favors referencing the review
as well, while the fixed hybrid still embeds it. No ranking establishes a
production choice. Retaining multiple different generations or terminal records
can grow the external pool even when individual snapshots remain small.

## Resource gaps and source consequences

| Dimension | Available warrant | Still missing |
|---|---|---|
| Serialized sizes | Exact UTF-8 and escaping of explicit demonstration encodings; source-valid corpus and refusal counterexample | Adopted complete critical-set carrier, protocol metadata and changing-generation worst case |
| Resident memory | None from this Python encoding comparison; earlier dormant Rust proof applies only to its own test budgets | Actual Host handoff retention, parser/serializer/resolver lifetime and simultaneous allocations; C/OS/RSS |
| Logical project quota | Snapshot and counted reference bytes provide partial arithmetic | Cross-process reservation, evidence lifetime, orphan/terminal accounting, concurrent generations and project aggregate bounds |
| Physical disk | No disk store or allocated-block measurement performed | Filesystem metadata, copy-on-write retention, staging, sync latency, free-space/ENOSPC and crash qualification |
| Product use | Constructed boundary cases expose possible refusal pressure | Actual fleet workloads, acceptable refusal/storage/history bargain and separate CAM64 capacity suitability |

The reference demonstration does not establish immutable custody merely by
naming a hash. A production source must define exact locator/kind/claimed
identity/method/write-read resolution, bounded acquisition and retention longer
than every referring record. A reference into either mutable snapshot slot is
not sufficient. Cold bytes cannot recreate original acknowledgment, authorship,
permission, role lease or act. Current0.5 cold acquisition and answer-only subset
limits remain unchanged; message0.2 still needs its own adopted outer carrier.

## Next reviewable source result

- PROPOSAL: Specify a complete critical-set/reference carrier before production sizing.
  - Evidence: R2-S reference-survival rules, CCE-A2, content-review source §2 and the resource-envelope matrix.
  - Change: C3 source owner defines every required exact artifact and unresolved state; compare all-inline with retained references on identical complete generations, including replacement and finalization. Keep hybrid only as an explicit comparator until evidence supports a choice.
  - Why: Three message bodies cannot establish recoverable current status or a full quota.
  - Risk: A new carrier affects version dispatch, cold readers, source standing and evidence lifetime.
  - Status: PROPOSED

Required owning reviews: C3/CCE for semantic critical-set closure and consumer
version; Host/role for actual supplied/emitted evidence and absent producer
limits; DEL-04-03 RS for kind/identity/method/recorder/resolution; storage owner
for immutable retention, shared quota, replacement and bounded reader; CRP/CAM
for final-account/pre-final snapshot references and independent outcomes.
Project/fleet identity/placement concurrence is an interface review, not a GroupD
implementation prerequisite. Existing HELP_HUMAN RS receiving assessment is not
an actual RS source-owner adoption. Reuse existing reviewers where available;
missing ownership is returned explicitly rather than invented.

MISSING: complete critical-set carrier, generation-transition/resource and
platform evidence listed above. This result does not justify product numeric
caps or a claim that references are always smaller or safer.
NEEDS_HUMAN_RULING: none requested now; prepare the measured workload/retention
tradeoff before asking for product suitability choices.
DEPENDENCY_NOTES: no new producer, graph write, native/supplier action, storage
implementation or policy adoption. R2 journal is not a blanket prerequisite to
independent answer/review work. C2/C4/C5 holds remain separate. Deferral still
leaves pre-freeze recovery/PM05 and whole-product90 unfinished; CAM64 is unchanged.
