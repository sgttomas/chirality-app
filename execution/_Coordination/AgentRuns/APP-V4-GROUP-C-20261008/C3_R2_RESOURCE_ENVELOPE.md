# R2 resource envelope and evidence retention

PROPOSED technical measurement and decision package; independent review pending.
Basis: current main 52f5f3494b97f0bd7547fd437b656483450a9ae5, received in
bb61c5a2c857c21678fb11fa8c2f1a87c2ee4b1f. No production storage, numeric product
policy, schema, retention or contract adoption. OD-02 already selects recoverable
current status and exact recovery-critical evidence, with replaceable older full
snapshots. This package prepares the remaining choice; it does not ask the owner
to choose unexplained integers.

## 1. Current evidence and resource accounting

The merged dormant proof (#1193, b59e08b9a5fa89e065db65d2c4cc2ebabedf9d91)
passed 32 constructed tests in each feature configuration independently. Its
32,768-byte test snapshot and 418,090-byte maximum conservative Rust allocation
account are test observations, not product sizing. The allocation measure sums
requested allocations plus retained capacities; it is not RSS, C/OS memory,
physical disk or a general peak guarantee at a different snapshot size. Original
admission-inode failures and repair remain in the implementation review.

| Resource | What must be counted | What current evidence does not establish |
|---|---|---|
| Simultaneous resident memory | Host input retained during handoff; exact UTF-8 bytes, parsed strings/objects, escaped serialization, descriptor/control buffers, evidence resolver buffers and outstanding attempts | One serialized payload does not mean one allocation; proof measurement does not include a real Host handoff or all App memory |
| Logical project Q | Both snapshot slots, descriptor and temporary, admissions/control/reservations, immutable critical artifacts, terminal markers and ambiguous/orphan leftovers | A per-journal cap or App mutex is not shared project quota |
| Physical disk | Allocated blocks, filesystem metadata, copy-on-write old extents/snapshots, temporary writes and free-space margin | Logical byte limits cannot promise exact device usage or available capacity |
| Cross-project cost | Sum of independently admitted project stores and process-resident working sets | A project Q does not bound aggregate App or device use |
| CAM identities | Every successful final freeze, including later cancelled/superseded/failed/uncertain publication; preflight failure consumes none | R2 cannot reset 64 App-instance lifetime identities, revive tokens or make restart a recovery policy |

The current one-payload/1 MiB CAM development bound remains unchanged. A question
may require multiple freezes. The current generic cold discovery acquisition gap
also remains: format-specific post-acquisition limits do not bound unknown-format
allocation. Exact known references can use bounded acquisition; this does not
retroactively qualify generic discovery.

Measured rows from [the JSON matrix](C3_R2_BYTE_MEASUREMENTS.json), replayable with
`python3 measure_c3_r2_bytes.py <repository>` using existing offline validators:

| Constructed subject | Raw UTF-8 bytes | As one JSON string | Standing |
|---|---:|---:|---|
| Exact 0.4 base fixture | 8,504 | 9,393 | Definition-valid base |
| Exact answer artifact | 629 | 681 | Constructed answer, no observed authorship |
| Positive content-only review0.2 | 736 | 785 | Definition-valid message; no adopted outer carrier |
| Base padded with spaces | 1,048,576 | 1,049,465 | Base semantics preserved; exact hash changes and answer/review rebound synthetically |
| Base padded with linefeeds | 1,048,576 | 2,089,537 | Legal JSON whitespace, escaping stress |
| 65,536 ASCII review characters plus message | 66,093 | 66,141 | Message validator accepts |
| 65,536 quote review characters plus message | 131,629 | 262,749 | Message validator accepts; outer escaping costs more |
| 65,536 four-byte review characters plus message | 262,701 | 262,749 | Schema-valid, refused by 262,144-byte artifact cap |

The three-string illustrative base/answer/review envelope is 10,888 bytes for
ordinary fixtures and 1,050,958 with the space-padded base (2,382 above1MiB).
It excludes actual Host custody, intent/outcome, target observations, attempts,
status metadata and descriptor costs: it is not the complete recovery-critical
set, a selected codec or a product maximum. Those artifacts have no adopted
combined carrier yet; their numeric costs remain missing, not zero. The retained
script checks 11 exact committed source files and existing owner definitions.

The accompanying reproducible byte matrix measures constructed source-valid
artifacts and illustrative envelopes. It must distinguish schema validity,
semantic validity and artifact admissibility. Character limits are not UTF-8 byte
limits. JSON escaping and outer metadata consume additional bytes. A valid raw
0.4 base at 1 MiB cannot coexist with a nonempty answer/review in a 1 MiB inline
exact-byte JSON snapshot. That is a boundary of this inline carrier family, not
proof that every possible reviewed codec/reference design fails. It is not a
measurement of typical user work or fleet throughput.

## 2. Critical-set carrier and reference lifetime

| Recovery subject | Required survival and standing | Source owner / receiving work |
|---|---|---|
| Exact selected 0.4 base | Original bytes/hash/question/claims; a current mutable file or hash alone is insufficient | C3 semantic resolver and CRP account reader |
| Answer and manager review | Exact original artifacts plus supplied/request/emission custody facts actually available; content-only review remains distinct from integration readiness | CCE/Host/role/RS; message0.2 needs its separate outer carrier adoption |
| Ordinary request intent | Actual supplied request and target/basis where known, persisted before tracked dispatch; absent intent stays absent for unrelated supplier work | Host and W2-M; no App confinement from later fileChange |
| Outcome and unresolved attempt | Original observed events/attempt identity, errors and missing acknowledgment; no replay from matching bytes | Host, C3 and storage; RS reference standing |
| Target observations | Exact pre/post independent bytes or retained bounded evidence selected by source; no exclusive causality inference | C3/W2-M ordinary-operation observation |
| Final account | Definite CRP binding stays definite if later journal update fails; unknown original acknowledgment remains unknown | CAM/CRP and C3 |

**Inline exact critical set:** simplest survival closure, no external garbage
collector; rewriting/escaping and one-payload pressure grow with cumulative
critical evidence. It must refuse rather than summarize away required evidence.

**Bounded immutable artifact references:** separates small current status from
large stable evidence. It needs a named source-owned carrier containing kind,
claimed identity, method, byte length/hash and original/current resolution,
plus retention coupling. References into reusable A/B slots are forbidden.
Artifact admission and every referring record must participate in shared logical
quota; reachability, orphan handling and terminal retention must be proven before
reclamation. Sharing identical bytes saves storage only if identity/custody
claims remain separate. No unbounded blob store is authorized.

**Hybrid:** embed small critical artifacts and retain exact immutable references
for larger ones. This is a hypothesis for measurement, not selected thresholds
or a new schema. Compare the same workload and failure cases across all three.
No carrier may recreate a live RoleSourceLease, SourceRequest, permission or human
act on cold reopen. Descriptor-selected bytes establish recorded state only.

## 3. Deriving finite budgets before product selection

Measure ordinary small/large questions, boundary-valid UTF-8, revisions, separate
manager review, cancellation before/after dispatch, missing outcome, multiple
simultaneously paused undertakings and retained terminal outcomes. Constructed
fixtures establish limits, not real fleet frequencies. Genuine producer workload
traces remain unavailable while TASK admission/source joining is held.

For each carrier, report logical maxima and measured resident/physical costs.
A conservative logical reservation must include N times both S slots plus all
per-journal descriptor/staging/admission costs, shared control, independently
retained critical artifacts and T terminal history, including leftovers after
failure. Do not credit deduplication or reclamation before its proof. Reserve
before writes, and preserve refusal/uncertain evidence when capacity is exhausted.

N (admitted undertakings), S (snapshot bytes), D (descriptor/parser envelope),
T (terminal retention) and Q (aggregate logical quota) remain unselected. Closed
codec depth/member/reference bounds and checked arithmetic can be engineering
choices derived from the selected carrier. N/Q require a workload and acceptable
refusal/storage bargain; S requires admitted evidence size and memory proof.
T requires an explicit terminal-history/retention bargain. The owner need not
choose parser constants individually. Technical qualification cannot decide how
much useful work the product should retain or when refusal is acceptable.

## 4. Terminal retention alternatives and CAM separation

| Alternative | Benefit | Cost / refusal behavior |
|---|---|---|
| Retain all admitted journals until explicit project archive | Simplest identity/evidence preservation; no automatic deletion | Finite N/Q eventually refuses new work, including after successful completion; not established suitable for long-running fleet use |
| Retire confirmed terminal bulk state while retaining bounded immutable critical evidence and terminal identity | Reuses bulk capacity without losing required current/final evidence | Needs crash-safe marker/accounting order, finite identity history, reference closure and archive policy; unknown attempts cannot be expired to make room |
| Defer production R2 | Avoids claiming unqualified recovery or selecting arbitrary limits | Pre-freeze restart loss remains; PM05 and whole-product90 sufficiency are not met, although independent answer/review development can continue |

Cancellation alone is not terminal while effects are unknown. Restart is not
retirement. A failed/ambiguous cleanup keeps reservations counted. Even a sound
R2 retirement design leaves CAM64 final freezes finite. A separate durable-outcome
and hot-entry-retirement assessment must address tombstones, one-use proof,
uncertain attempts, process exit and cross-session identity before changing CAM.
This package neither changes that policy nor treats it as sufficient at scale.

## 5. Smallest platform qualification plan

The accepted first platform is macOS Apple Silicon (PRD V4-CST-02). First qualify
one explicitly identified local filesystem/configuration with cooperating App
processes. Network/synced storage, hostile same-user replacement/rollback and
power-loss durability are not implied. Whether those exclusions fit intended
use is a product suitability question after technical results.

A later bounded proof brief should exercise actual two-process writer/reader
exclusion and quota races; bounded acquisition and bootstrap; crash/kill at each
snapshot/descriptor/directory-sync and admission boundary; ENOSPC and retained
leftovers; no-follow/single-link/inode substitution and concurrent rename;
reference survival through replacement and proposed retirement; and a repeated
cold reopen without retry or capability restoration. Measure peak resident
allocations, actual allocated disk and latency on the same corpus. Physical
power-loss/device durability needs separate evidence if claimed; process-kill
and injected sync errors do not prove it. Consistent rollback cannot establish
freshness without an independently warranted monotonic anchor. No such tests,
new helper processes or production opener are authorized by this package.

## 6. Decision interface after measurements

- PROPOSAL: Measure carrier and workload costs before selecting product caps.
  - Evidence: R2-S §§4–8, merged dormant proof and accompanying byte matrix.
  - Change: Compare inline, immutable-reference and hybrid exact critical sets on the same bounded corpus; derive finite engineering caps and report resource/refusal consequences.
  - Why: Avoid treating test constants or serialized size as product capacity.
  - Risk: A new carrier affects CCE/RS/CRP readers and retained-reference lifetime.
  - Status: PROPOSED
- PROPOSAL: Present one concrete retention/resource bargain and deferral to the owner.
  - Evidence: PRD §1.2 at-scale reliability, §4.6 fleet coordination and V4-PM-05; OD-02; measured costs required above.
  - Change: Ask only which supported workload/refusal/storage envelope and terminal-history/archive behavior is acceptable, and whether qualified platform exclusions fit use. Keep CAM capacity as a separate decision with its own proof route.
  - Why: These are product suitability choices, unlike parser arithmetic.
  - Risk: Too-small limits can be correct yet unusable; deleting uncertainty or unsupported scope narrowing is prohibited.
  - Status: PROPOSED

MISSING: measured real producer workloads; adopted critical-set carrier; qualified
cross-process/platform/retirement implementation; product envelope and separate
CAM capacity treatment. Constructed byte measurements do not fill these gaps.
NEEDS_HUMAN_RULING: none requested now. Product workload/refusal, terminal-history
and support tradeoffs will require a concrete evidence-backed owner choice.
DEPENDENCY_NOTES: #1194 is dormant original-call/unavailable-response custody,
not TASK admission or an authored account producer. C2 PEC, C4 Domains and C5
activation remain at their external holds; this package does not adopt their
sources or make them R2 prerequisites. No full reconstruction, PM05 completion,
product acceptance or90% claim follows.
