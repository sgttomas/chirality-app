# Deliverable Concordance Method

Chirality AI Ltd. Date: 2026-07-11. Revision 1.

**Status: RATIFIED — owner ratification 2026-07-11 (K-AUTH-1).** Owner
direction of record (2026-07-11, in-session, Ryan Tufts): "You can now take
all the `docs/` out of the DRAFT state, making them authoritative." This
document is the authoritative shared concordance method. The Revision-0
self-declared ratification gate (completion of both adopting projects' R0
method calibrations) is superseded by that owner act — ratification is an
owner act and was exercised ahead of the calibrations; R0 calibration
findings now flow in as ordinary owner-ruled amendments (§7). Earlier owner
direction of record (2026-07-11): the method is intended as part of
Chirality itself.

**Provenance.** Distilled from the two project method plans —
`projects/chirality-app-dev/plans/PLAN_2026-07-10_deliverable_implementation_reconciliation.md`
and
`projects/chirality-piping/plans/PLAN_2026-07-10_deliverable_implementation_reconciliation.md`
— and the 2026-07-10/11 owner design session recorded in those plans and in
`projects/chirality-app-dev/loop/LOOP_RECEIPTS.md`. Precedence now that this
document is ratified: it governs the shared method; each project's plan
remains that project's operative adoption record and governs its
project-specific parameters and divergence layers; a genuine conflict
between the two is surfaced (`AUTHORITY_CONFLICT`), never resolved by agent
precedence-invention.

## 1. Purpose

Restore and keep a deliverable corpus as a reliable statement of accepted
scope, implemented behavior, verification evidence, unresolved work, and
lifecycle state — without requiring anyone to reconstruct project truth from
plans, chat history, or memory.

## 2. The problem this method exists for

Project truth decays when it is distributed across too many representations —
plans, assessments, specifications, status files, coordination records,
implementation, tests, decisions, run records — each maintained independently.
Together they behave like an unsynchronized database: every copy made sense
when written, and their disagreements compound silently. Drift is therefore a
**normalization problem**: each kind of truth must have exactly one designated
home, and everything else must be derivative and dated.

The normalized homes:

| Kind of truth | Sole home |
|---|---|
| Normative scope | Current authority documents and decomposition |
| Accepted decisions | The project decision register and its ruling records |
| Executable open work | Deliverable-local `_STATUS.md` `## Remaining` |
| Lifecycle state | Deliverable-local `_STATUS.md`, human-gated |
| Implementation truth | Source, tests, and build/validation artifacts |
| Evidence | Immutable, dated, source-state-bound run artifacts |
| Shared method | This document (ratified 2026-07-11) |
| Project adoption parameters and provenance | The project's own plan — historical record, never a work-selection surface |

Executable work is never selected from the method or from plans — only from
the owning deliverable's `## Remaining` (see §6).

## 3. Reconciliation is an epistemic operation

Concordance is not "update documents from code" — implementation is evidence,
not scope authority. Every claim is audited by distinguishing kinds of
knowledge: normative scope, accepted decisions, declared current state,
observed implementation, verification evidence, validation evidence (where the
claim class demands it), lifecycle state, and recorded remaining work. The
audit unit is the **claim** (a requirement or stable scope statement), never
the whole deliverable: one deliverable can simultaneously contain aligned
requirements, stale wording, unvalidated mechanics, and legitimate deferrals,
and a single verdict would destroy that information. Deliverable summaries are
derived from claim rows, never substituted for them.

Core controlled dispositions (projects extend, never weaken): `ALIGNED`,
`IMPLEMENTED_UNDOCUMENTED`, `DOCUMENTED_UNIMPLEMENTED`, `PARTIALLY_IMPLEMENTED`,
`IMPLEMENTED_DIFFERENTLY`, `ACCEPTED_DIVERGENCE`,
`LIFECYCLE_REASSESSMENT_REQUIRED`, `DEFERRED_AGENT_WORKFLOW`,
`AUTHORITY_CONFLICT`, `UNKNOWN`, `STALE_INPUT`.

Fixed epistemic guardrails: discovery is read-only and separated from repair
(never edit the audit target while determining what it means); every evidence
citation binds to the source state it actually evaluated; named snapshots and
prior evidence artifacts are provenance baselines, not current truth — a run
resolves the live discovery pointer and re-verifies current state before
relying on them; conflicts between live normative sources are recorded
(`AUTHORITY_CONFLICT`), never resolved by agent precedence-invention; no agent
disposition is ever represented as a human ruling; completion is an
evidence-coherence state, never issuance, release readiness, or professional
approval.

## 4. Lifecycle model

Lifecycle states are **governed production and change-control regimes with
maturity/readiness entry conditions; they are not percentage-complete
scores**. Advancing `IN_PROGRESS` → `CHECKING` → `ISSUED` carries maturity
meaning — each transition asserts readiness against declared entry
conditions — while the states themselves define which changes are lawful and
under what control:

- `IN_PROGRESS` — ordinary edits permitted. The honest holding state whenever
  warranted open scope exists, however advanced the implementation.
- `CHECKING` — a frozen candidate under review against a declared basis.
  Reversal to `IN_PROGRESS` is the only edit path; review evidence appends to
  run/review records, never to the frozen claim surfaces. The review is
  internal to the claims the deliverable makes about itself.
- `ISSUED` — accepted baseline; changes only through the governed
  scope-change process.

**Entry to `CHECKING` is layered**, not a single trigger:

1. **Universal minimums (candidacy).** The deliverable's `## Remaining` is
   **warranted-empty** — empty, and a current evidence basis (a concordance
   pass or equivalent review bound to the candidate source state) certifies
   that the emptiness is warranted. This is a necessary prerequisite — the
   owner formulation of record names it the *primary* trigger — never the
   complete entry criteria.
2. **Candidate-specific checking basis.** Satisfaction of the declared review
   basis appropriate to the deliverable's claims and risk. These criteria are
   emergent: maturity feedback from real checks hardens into reusable ruled
   profiles (ruled documentation surfaces, not predetermined checklists).
   This method does not predetermine them.
3. **Human declaration.** The owner declares the checking basis and freezes
   the candidate; entry is a human act.

There are no disclosed-deferral carve-outs: any warranted Remaining item —
owner-gated included — keeps the deliverable `IN_PROGRESS`; boundary
adjustments happen through the decision register while `IN_PROGRESS` (rescope
before freeze, never carve out during review). A failed check exits by
reversal, its findings becoming Remaining items. Concordance is thus the
process that makes `## Remaining` sections warranted — the path back to
`CHECKING`.

**Rebaseline asymmetry:** demotion to `IN_PROGRESS` requires no criteria —
only the absence of a current, accepted basis for the asserted state.
Promotion requires a contemporary declared basis. Lifecycle corrections are
human-authorized administrative acts recorded through the register; they do
not invalidate prior work or evidence, which is preserved as history.

**Canonical authority precedence.** This method does not amend any project's
canonical lifecycle authority (e.g. its `SPEC`/`TYPES` surfaces or
decomposition codifications). An adopting project runs under this lifecycle
model only after its own separately ruled semantics amendments have merged to
the shared mainline; until then, the project's current canonical semantics
govern.

## 5. Program state model

A concordance program creates no standing surface. Its state divides three
ways, each with an existing home:

1. **One run's phase state** — the immutable, append-only run folder
   (`execution/_Reconciliation/DeliverableConcordance/<RunID>/`), bound to its
   source state and expected to age out.
2. **Cross-session visibility** (program open/closed) — the activation
   decision's register row, whose ruling-record cell points at the run folder
   and receives a closure note; registers are re-read every loop iteration.
3. **The recurring process asset** (checking-entry profiles, maturity
   feedback) — a ruled docs profile surface, amended only by ruling.

## 6. Activation pattern

- Activation is a **register decision**: a PROPOSAL packet, an owner ruling
  naming the activated scope, and a ruling record. The ruling record and
  register flip **land on the shared mainline before any dispatch** —
  concurrent sessions are mutually blind, and an owner act that exists only
  in one session's context is a governance fork waiting to happen.
- The project plan has **no authority to activate or select work**; the
  activation ruling may incorporate a **pinned revision** of the plan (a
  commit SHA on the shared mainline) as the run's execution method. Bootstrap
  items and the ruling record cite that pinned revision; later plan edits do
  not change the method of an in-flight run absent a new ruling.
- Executable per-deliverable work is seeded as gated `## Remaining` items in
  the owning deliverables and unlocked by the ruling's suffix flips; run-level
  phases execute directly under the ruling as ruled-program work.
- Single-surface compliance: the plan, the run artifacts, and this document
  never select work. Owner decisions live in the register; executable
  residuals live only in the owning deliverable's `## Remaining`.

## 7. Adoption

Each adopting project keeps a self-contained project plan as its operative
method and adoption record. Project-local layers are expected to diverge —
e.g. engineering validation/provenance disciplines in one project,
inspection-assessment recency disciplines in another — and are never
flattened into this kernel. Sibling plans are not resynchronized without
owner direction. This kernel is amended only by owner act; now that it is
ratified, the project plans may thin to project-specific parameters citing
this document as the shared method (an owner-directed act, not required).

## Document History

| Revision | Date | Change |
|---|---|---|
| 0 (DRAFT) | 2026-07-11 | Initial distillation from the two project concordance plans and the 2026-07-10/11 owner design session. Non-binding pending ratification after both R0 calibrations. |
| 1 (DRAFT) | 2026-07-11 | Original-author review feedback incorporated on owner direction ("Consider this feedback. Incorporate what has merit."): lifecycle reformulated as governed regimes with maturity/readiness entry conditions; CHECKING entry restructured as layered (warranted-empty universal minimum, candidate-specific basis, human declaration); canonical-authority precedence note; normalization table splits shared method / project adoption record; pinned-revision activation formulation; snapshots-as-provenance-baselines guardrail. |
| 1 (RATIFIED) | 2026-07-11 | Owner ratification (direction of record: "You can now take all the `docs/` out of the DRAFT state, making them authoritative."), superseding the Revision-0 self-declared R0-calibration gate by owner act. Post-ratification precedence recorded in the status/provenance block. |
