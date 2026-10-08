# C3-S4 concrete materialization candidate

CAM-v0.1 / C3-S4-MAT-01 and separate schema format 0.3 produce durable
source-evidence drafts from current private CGP observations. They preserve
old 0.1/0.2 and every prior Design file. No facts, supported conclusions,
performed or not-required duties are emitted. Caller roles/interpretations/
duty statuses remain explicit assertions; unassigned gap responsibility is
represented by typed null, never a guessed actor.

Receipt is compact: exact path/commit/hash, object identities, selected excerpts,
observation times and association/engine/traversal digests with explicit
non-replay/non-authority limits. No raw config/tree/commit/full blob duplication.
Non-UTF-8 materialization refuses; question/CGP commit mismatch refuses. Partial
gaps remain; stale/historical observations do not mint new accounts.

Prepare/publish/cancel/uncertain semantics and same-opened-root binding are
specified in CAM §6. Existing CRP has no account cap; the proposed 1 MiB composer
cap and post-identification cold refusal do not claim bounded generic cold
read allocation or silently restrict older versions. Store/reader 0.3 adoption
must be explicitly implemented; no external receiving adoption occurs here.

Independent source/schema review is required before implementation release.
Maintained schema checks exercise positive/negative shapes only; semantic
cross-field/source binding, root/lifecycle and connected tests remain required
implementation evidence. Actual native witness and full reconstruction remain
obligations. This proposal does not close Group C or alter group order.

Performed definition validation: maintained schema check ran offline, 31/31
constructed shape cases passed. No semantic/producer/native test pass is
inferred. Exact candidate artifact hashes are recorded in the basis.

## CAM-R1 registry retention amendment

Implementation identified that consumed outcome custody must survive source
sessions without indefinite payload retention. Proposed bound: 64 identities
per App instance, one full prepared/in-flight payload, compact retained outcomes
and tombstones thereafter. Cancel/supersede consumes a slot; capacity refuses
without eviction/restart/retry. Started-write outcomes survive session changes;
uncertainty retains original Attempt even after explicit reconciliation.

TASK route_persistence confirmed feasibility in the active task exchange,
including refusal of prepare while publishing and atomic replacement only after
final bytes validate. Internal discarded preflight IDs are not exposed registry
identities. No code is changed by this amendment. Exact independent review and
parent technical confirmation remain required before adoption; account/schema
meaning, 1 MiB cap and cold-reader limits are unchanged.
