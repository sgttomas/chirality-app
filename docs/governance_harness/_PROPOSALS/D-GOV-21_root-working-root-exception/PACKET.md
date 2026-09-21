# D-GOV-21 — Root Working-Root Exception and Replacement Containment Contract

> **Status: CANDIDATE — NOT RULED.** This packet binds nothing (K-AUTH-1). It
> becomes authority only through an explicit owner ruling recorded in
> `docs/governance_harness/_DECISIONS/` and bound to git SHAs per §14. Silence,
> file creation, validation, commit, or Git transport is not approval.
>
> **Revision: 3 (candidate).** Rev 1 agent-drafted 2026-07-25; Rev 2
> incorporated the adversarial review of the same date; Rev 3 incorporates the
> reviewer's verification pass against Rev 2 (dispositions in §16).
>
> **Provisional ID:** D-GOV-21 (next free after D-GOV-20; reconcile to the
> actual next-free ID at staging, per the D-GOV-20 collision-repair precedent).
>
> **AcceptedBasis:** `main` @ `1049e011c` (all file/line citations are against
> this state; re-verify if staged against a later basis).
>
> **AcceptedCandidateSHA:** TBD — assigned when this exact packet is committed;
> the owner ruling approves that exact candidate SHA (§14).
>
> **FramedBy:** Agent-drafted under owner direction, root-PRD inquiry session,
> 2026-07-25, with independent adversarial review by a second agent. The owner
> direction quoted in §1 is transcribed from that session; the owner confirms
> or corrects the verbatim text at ruling.
>
> **RecordConvention:** Options + Recommendation + Owner ruling; verbatim
> ruling fence and exact-candidate-SHA approval per the D-GOV-18/19 pattern;
> supersede-never-edit.

---

## 0. Purpose

Establish the Chirality monorepo root as the working root for development of
the root product, with root `execution/` as its lawful execution root,
eligible to hold `PKG-*` packages and `DEL-*` deliverables after the gates in
§6 close; enumerate the exact doctrine this supersedes or amends; and
establish the replacement containment contract that supplies the finer
discrimination root development requires. This is a root-governance change,
not a decomposition change: no accepted root decomposition exists for
`SCOPE_CHANGE` to amend, so the vehicle is this decision.

## 1. Owner direction of record

Received in-session, 2026-07-25 (transcription; owner confirms at ruling):

<!-- BEGIN OWNER DIRECTION TRANSCRIPTION -->
> "we will now develop Packages PKG and Deliverables DEL in the Execution
> folder."
>
> "On my authority you can supersede previous rulings that are inconsistent
> with the direction I've given you here about using the Execution folder for
> packages and deliverables. This is NOT a blanket waiver of all
> requirements."
<!-- END OWNER DIRECTION TRANSCRIPTION -->

## 2. Decision to make

Rule the following five effects as one decision:

1. **Root as working root (narrow exception).** The repository root is both
   the shared instruction root and the working root for development of the
   root product. No other working root gains this property; `projects/*` and
   `domains/*` remain separate working roots and do not inherit the exception.
2. **Root execution root.** Root `execution/` is the root product's lawful
   execution root and becomes **eligible** to hold `PKG-*`/`DEL-*` structure
   after the §6 gates close — materialized only from an accepted root
   decomposition derived from an adopted root PRD. Existing root coordination
   and evidence records (`execution/_Coordination/**`) remain valid historical
   state.
3. **Enumerated supersessions.** The normative clauses in §3 are amended
   exactly per Annex A, and no further (§4). Non-binding surfaces propagate
   per §3b.
4. **Replacement containment contract.** The mechanisms and deterministic
   guards in §5 are required, with the §5.3 gate ordering.
5. **PRD-development basis.** Development of the candidate root PRD is
   authorized on this basis. The PRD's own adoption is a separate future act
   (§11).

## 3. Enumerated supersessions and amendments (normative clauses)

Per the owner's "NOT a blanket waiver," the amended set is exactly this table.
Exact before/after prose is in Annex A; the ruling approves the dispositions
here and the Annex A candidate prose, applied under the §14 exact-prose gate.
Anything not listed remains in force unchanged. This inventory was completed
through adversarial review; any further conflicting clause discovered during
implementation returns as an amendment to this record, not absorbed silently.

| # | Clause (at AcceptedBasis) | Current effect | Disposition |
|---|---|---|---|
| S1 | `docs/DIRECTIVE.md:199-206` (§2.6), operative MUST at `:204` — "A working root MUST NOT be located inside the instruction root." | Prohibits root-as-working-root outright | **Superseded in part**: append the narrow root exception; the prohibition remains for every other working root |
| S2 | `docs/DIRECTIVE.md:13` (§1) — working-roots "nested under `projects/*` and `domains/*`" | Defines where working roots live | **Amended** to admit the root itself as the working root for the root product |
| S3 | `docs/DIRECTIVE.md:76` (§2, praxiology) — "The instruction root … is physically separated from the working root …" | Restates the separation | **Amended** with an exception pointer |
| S4 | `docs/DIRECTIVE.md:300` (§5) — "Instruction root separate from working root" | Structural constraint | **Amended** with the root exception |
| S5 | `docs/DIRECTIVE.md:301` (§5) — "One shared instruction root serves many working roots" | Structural constraint | **Amended**: the instruction root additionally serves as the root product's own working root |
| S6 | `docs/SPEC.md:48-52` (§0.2.2), first clause of the compound rule at `:52` — "A working root MUST NOT be the shared instruction surface itself" | Prohibits the identity outright | **Superseded in part**: append the narrow root exception. The second clause of `:52` is preserved and load-bearing (see below) |
| S7 | `docs/SPEC.md:79` (path-anchor table) — `{WORKING_ROOT}` = "the active `projects/<name>/` or `domains/<name>/` (or user-selected folder)" | Restricts `{WORKING_ROOT}` resolution | **Amended** to admit `REPO_ROOT` for the root product |
| S8 | `docs/SPEC.md:97` (§1) — execution instance "self-contained project workspace" | Execution-instance model | **Amended** to admit the root execution instance |
| S9 | `docs/TYPES.md:51-52` — Working Root / Execution Root definitions | Working Root = `projects/<name>/` or `domains/<name>/` | **Amended** definitions admitting `REPO_ROOT` (root product only) |
| S10 | `execution/_Coordination/LOOP_INIT.md:18-20` (fence) and `:103-105` ("Root control-plane records never authorize project-content writes…") | Orientation-surface fence and write rule | **Updated, not superseded** — the file self-describes as "orientation, not authority"; rewritten after ruling to describe the new arrangement, including clarifying that `:103-105` continues to bar authorization of *other* working roots' content while root-product work now runs through root `execution/` |

**Ruled-record relation.** D-GOV-09 remains the historical ratification act,
in force as ruled. This decision **prospectively amends** the enumerated
normative clauses of the corpus D-GOV-09 ratified (S1–S9), and nothing else.
No other D-GOV record is identified as inconsistent with the owner direction.

**Surviving clauses made load-bearing.** Two ratified clauses are *not*
superseded and become the ratified basis for mechanism M2:

- `docs/SPEC.md:52`, second clause: "agents operating in a working root MUST
  NOT write to `agents/`, `skills/`, `tools/`, or root `docs/` except through
  an explicit, separately-authorized repo-wide instruction change."
- `docs/SPEC.md:44`: "The instruction surface is read-mostly: changing it is a
  repo-wide governance action, not ordinary working-root execution."

## 3b. Propagation table (non-binding and derivative surfaces)

These are not supersessions; they are required propagation, classified per the
derivative-package rule. Each is executed in the implementation tranche or
explicitly deferred in that tranche's handoff state naming the authoritative
source SHA:

| Surface | Class | Action |
|---|---|---|
| `README.md:84-86` (instruction/working root separation description) | Direct propagation | Reword to reflect the exception in the implementation tranche |
| `exports/chirality-app` export derivative (`docs/` is in the export allowlist; DIRECTIVE/SPEC/TYPES edits stale exported copies and manifest hashes) | Derivative regeneration | Regenerate the export staging in the implementation tranche, or defer explicitly in the handoff state with source SHA named |
| `domains/chirality` governance-corpus snapshot | Routed notice (no active detection) | The domain's source map marks the root governance docs `RETIRED_ARCHIVED_AFTER_BATCH1` (disposition OUT) and its active source manifest does not list DIRECTIVE/SPEC/TYPES — corpus drift will **not** detect these changes. Ship the routed M6 notice; any carry-forward or rebaseline is that domain's own gated act |
| App Dev authority-reference corpus and SHA-pinned contract mirrors (demonstrably active) | Routed notice | Per-tranche notice per M6; adoption is that loop's own act |

## 4. Scope not granted

- No change to K-AUTH-1, K-AUTH-2, K-BIND-1, K-GATE-1, K-SEAL-1, or any
  invariant or clause not named in §3. Ratification mechanics, human gates,
  lifecycle states, and the decision-record system are untouched.
- No waiver of the decomposition pipeline: `PKG-*`/`DEL-*` at root may come
  only from an accepted root decomposition (§6). Nothing in this record
  authorizes inventing packages from discussion.
- No change to the public-export boundary. Root `execution/` is not in the
  export allowlist and this record does not add it.
- No extension of the exception to any `projects/*` or `domains/*` working
  root, nor to the desktop harness's user-selected working folders.
- No adoption of the root PRD, its genus wording, its accountability model,
  or its placement — expressly reserved (§11).
- No blanket authority for future root-structure changes; this record's
  supersessions are closed-form (§3).

## 5. Replacement containment contract

### 5.1 Why the contract is mandatory

K-WRITE-2 (`docs/CONTRACT.md:124`) supplies **checkout containment**: writes
must path-contain within `REPO_ROOT`. Within a monorepo checkout,
working-root containment has always depended on narrower accepted scopes —
briefs, declared write targets, agent permissions, and the SPEC §0.2.2
instruction-surface prohibition — not on K-WRITE-2 alone. When the root
itself becomes the working root, the outer checkout boundary and the
working-root boundary coincide, and the SPEC §0.2.2 prohibition (which did
the fine-grained work for the instruction surface) acquires its S6 exception.
The replacement contract therefore supplies the finer discrimination root
development requires, and mechanizes protections that were previously
prose-enforced: preflight verification found no production harness or
validator code guarding root `execution/` structure.

Routed debt (not amended here): the explanatory gloss inside K-WRITE-2's
CONTRACT entry ("confines a task's effects to its working root") overstates
the invariant's mechanical reach in a monorepo; recorded for separate
reconciliation.

### 5.2 Mechanisms

Provenance labels: **TRANSCRIBED** (existing accepted doctrine, cited),
**PROPOSED** (new commitment, effective only if this record is ruled).

- **M1 — Fine-grained write ownership** [PROPOSED at root; pattern
  TRANSCRIBED from `AGENTS.md` mixed-work-graph rules]. Every root package and
  deliverable declares write targets finer than the checkout, recorded in the
  static ownership register (G2). Concurrent sibling write targets must be
  disjoint; overlap requires serialization against an accepted predecessor or
  one declared integration owner.
- **M2 — Instruction-surface touches are governance actions** [basis
  TRANSCRIBED: `docs/SPEC.md:52` (second clause) and `:44`, plus the
  `AGENTS.md` Bash-bearing-child rule; root application PROPOSED].
  Root-product instruction changes require independent owner authorization
  through a human-gated repo-wide change tranche satisfying M2. M2 supplies
  the containment and evidence conditions — any root child whose declared
  write targets intersect the instruction surface (`AGENTS.md`, `agents/`,
  `skills/`, `tools/`, root `docs/`, `init/`) is serialized as the sole
  integration owner for that tranche, which merges only through a human-gated
  PR carrying a tranche manifest (G4). M2 does not itself grant authority; a
  deterministic marker or gate cannot confer authorization (K-AUTH-1).
- **M3 — Frozen instruction basis** [PROPOSED; mechanism TRANSCRIBED from the
  snapshot rule]. Every root run binds to the accepted instruction-surface
  state (commit SHA) under which it was dispatched. A sibling's candidate
  change to an instruction surface is never consumed by an in-flight run;
  adoption of a changed instruction basis happens only between runs, at a
  recorded point.
- **M4 — Worktree isolation** [mechanism TRANSCRIBED; mandatory root
  application PROPOSED]. Concurrent root children execute in isolated git
  worktrees.
- **M5 — Accepted snapshots at fan-in** [TRANSCRIBED]. Fan-in consumes
  accepted snapshots; partial or invalid returns are not accepted.
- **M6 — Routed change notices** [agents/ scope TRANSCRIBED from the
  `AGENTS.md` agent-index change-notice rule; extension PROPOSED]. Notices
  fire once per accepted tranche, identifying all affected project loops.
  PROPOSED extension: the same per-tranche routing applies to accepted root
  tranches changing `docs/`, `skills/`, or `tools/` surfaces that project
  loops pin or mirror.
- **M7 — Rollback posture** [PROPOSED]. Defined in §8.

### 5.3 Deterministic guards and gate ordering

All guards are **PROPOSED** new tooling. G0 resolves the bootstrap problem:
the ordering below is enforced by a guard that exists *before* anything it
gates.

- **G0 — Materialization fence** [shipped in this decision's implementation
  tranche, wired into governance-harness CI]. Fails BLOCK if direct children
  matching `execution/PKG-*` or `execution/DEL-*` exist while G1–G4 are not
  registered and passing; once they are, verifies their registration and
  passing state. G0 makes the §6 ordering mechanically real from the moment
  this decision takes effect.
- **G1 — Root harness adapter.** Root `_harness/adapter.yaml` (or equivalent
  registration) with pinned baselines, giving root `execution/` the same
  deterministic status/drift surface the project working roots have.
- **G2 — Static surface-ownership register + validator.** A root
  surface-ownership register created during root Project Setup, mapping
  packages/deliverables to declared write targets; a validator that fails
  BLOCK on undeclared targets, unregistered materialized packages, or
  register/decomposition mismatch. Static facts only; no concurrency claims.
- **G3 — Pre-dispatch work-graph check.** Validates, at dispatch time against
  the accepted work graph and run briefs, that each active node's write
  targets are declared, that concurrently active nodes' targets are disjoint
  or serialized per M1, and that instruction-surface intersection carries the
  M2 marker.
- **G4 — Instruction-surface tranche manifest check.** Each accepted root
  tranche that changes protected instruction-surface paths must carry a
  tranche manifest declaring those changes; the check verifies manifest
  presence, path coverage of the actual diff, and the M2 gate and M6 notice
  for the tranche. It checks recorded provenance; it does not infer origin
  from diffs.

**Gate:** no `PKG-*`/`DEL-*` materialization under root `execution/` until
G0–G4 exist, run in CI, and pass. Guard **capability** (validator code and CI
wiring, G1–G4) exists before root Project Setup; root Project Setup then
**instantiates** guard state — the G2 ownership register and the first
accepted work graph that G3 checks against. G0 gates materialization on both:
registered, passing guard capability and instantiated guard state. This gate
exists because the enforcement map's "future tooling" bucket has a
demonstrated languishing failure mode; these guards are preconditions, not
future tooling.

## 6. Sequence

1. Inventory affected doctrine, assumptions, pins, and coordination surfaces
   — initial inventory completed and hardened through adversarial review;
   findings are §3, §3b, §5.1. Further finds return as amendments (§3).
2. Rule this record per the §14 mechanics.
3. Implementation tranche: apply Annex A doctrine edits, §3b propagation,
   LOOP_INIT rewrite (S10), G0, and the register row — at the EffectiveSHA.
4. Reorient the root coordination loop (obligation of this ruling; §7 class a)
   — before root-PRD development work begins.
5. Develop the candidate root PRD.
6. Implement and validate guard capability G1–G4 (validator code and CI
   wiring); G0 enforces the ordering.
7. Adopt the root PRD (exact bytes, separate instrument; §11).
8. Perform the first root decomposition from the adopted PRD; root Project
   Setup instantiates the G2 ownership register and the first accepted work
   graph (G3's input).
9. Materialize `PKG-*`/`DEL-*` under root `execution/` from that accepted
   decomposition only, with G0–G4 passing.

After step 4 completes, steps 5 and 6 may proceed in parallel; nothing else
reorders. Step 9 is gated per §5.3.

## 7. Adjacent obligations, by class

- **(a) Obligations of this ruling, executed in separate tranches.**
  Root-loop reorientation (`execution/_Coordination/CURRENT_WORKPLAN.md`
  currently targets a closed workplan): required before root-PRD development
  begins (§6 step 4). G0 and the Annex A edits: the implementation tranche
  (§6 step 3).
- **(b) Independent historical reconciliation (not required by this ruling;
  may run in parallel).** Reconcile the missing root receipts for D-GOV-19
  and D-GOV-20 as a historical-reconciliation act. Reconcile the K-WRITE-2
  explanatory gloss (§5.1 routed debt).
- **(c) Conditional runtime work (required only before runtime-backed root
  execution).** Author a root `chirality.project.json` and test
  project-registry containment with `instructionRoot` = `workingRoot` = `.`
  (never exercised at AcceptedBasis).
- **Preflight verification (before G1–G4 design).** Run the full
  practitioner-harness and validation suites against a scratch materialization
  of a root `PKG-*` skeleton to confirm the §5.1 preflight finding.

## 8. Rollback

Rollback is a governed superseding act, not erasure of history. A future
ruling may, without invalidating any prior accepted decision or evidence:

1. stop further root-package activation;
2. freeze the accepted root-development state;
3. restore the instruction-root/working-root separation prospectively;
4. relocate or retire unfinished derivative work under a recorded disposition;
5. preserve all accepted decisions, receipts, and evidence in place.

## 9. Falsifiers

The exception design is considered falsified — triggering §8 consideration —
if any of the following is observed and recorded:

- **F1 — Containment failure.** Root self-development corrupts a shared
  instruction surface out from under a situated loop (detected by that loop's
  corpus-drift or pin checks) in a way the superseded separation would have
  prevented, and M1–M6/G0–G4 did not detect or gate it first.
- **F2 — Loop bypass.** Root product development proceeds outside the root
  governed loop — work materialized at root `execution/` without a current
  workplan pointer, receipts, and the M2/G4/M6 machinery engaged.
- **F3 — Self-authorization.** A root node consumes a capability produced by
  root development before that capability was accepted through the basis or an
  explicitly accepted predecessor (the SCA-001 C16 discipline, applied to
  root).

## 10. Consequences upon ruling

- Root `execution/` becomes **eligible** to hold `PKG-*`/`DEL-*` after the
  stated gates close (§5.3, §6); nothing materializes at ruling time.
- The Annex A doctrine edits, §3b propagation, S10 LOOP_INIT rewrite, G0, and
  the D-GOV register row are applied in the implementation tranche at the
  EffectiveSHA, each edit carrying a pointer to this record.
- The candidate root PRD may cite root-as-working-root as **TRANSCRIBED**
  rather than carrying it as PROPOSED.
- Harness live-baseline pins that consciously change (root adapter
  registration, new dispositions) are updated as conscious pin updates in the
  established pattern.
- Everything in §4 remains exactly as it was.

## 11. Decisions expressly not made here

Routed to the PRD development/adoption track; recorded so their absence from
this ruling is deliberate:

1. Genus wording of the root product statement.
2. Accountability model (one accountable human per consequential act vs. one
   owner per root), including who may amend
   `docs/governance_harness/human_actors.md`.
3. The root PRD's adoption instrument and its concordance map against
   `docs/DIRECTIVE.md` §1.
4. The adopted PRD's placement relative to the public-export boundary
   (`docs/` is exported; `execution/` is not — placement is a publication
   decision).

## 12. Options

- **O-A — Adopt as specified.** All five effects of §2, supersessions closed
  to §3/Annex A, containment contract §5 with the §5.3 gate.
- **O-B — Dedicated project working root instead.** Develop the root product
  in a new `projects/chirality-root/`, preserving the instruction/working-root
  separation. (Retained for the record; contradicts the §1 owner direction
  unless the owner revises it.)
- **O-C — Decline.** Root `execution/` remains control-plane-only; the root
  PRD track proceeds without a materialization target until re-framed.

## 13. Recommendation

**O-A.** The owner direction of §1 selects the substance; this packet's
contribution is the closed supersession set with exact candidate prose, the
corrected containment argument (§5.1), the mechanically real gate ordering
(G0), and the falsifiers that make the exception self-testing.

## 14. Ruling mechanics and owner ruling

Per the D-GOV-18/19 exact-candidate pattern, because this packet contains
substantial PROPOSED requirements:

1. Commit this exact packet; record its commit as **AcceptedCandidateSHA**.
2. The owner confirms both §1 transcribed quotations and rules on O-A/O-B/O-C
   against that exact candidate SHA; the ruling is recorded verbatim below
   and published as the decision record in `_DECISIONS/`.
3. The implementation tranche applies Annex A per its stated application
   semantics (exact wording constraints at identified insertion anchors;
   complete resulting text where the amended unit is a sentence or table
   row). Any necessary deviation from Annex A prose returns for exact-prose
   re-acceptance before merge (the D-GOV-19 two-gate pattern). The merged
   implementation commit is recorded as **EffectiveSHA**.

<!-- BEGIN OWNER RULING VERBATIM -->
PENDING — not ruled. This packet binds nothing until an owner ruling is
recorded here verbatim and the record is published.
<!-- END OWNER RULING VERBATIM -->

**AcceptedCandidateSHA:** TBD · **Ruling/publication SHA:** TBD ·
**EffectiveSHA:** TBD

## 15. Supersession relations

- **Prospectively amends:** the S1–S9 normative clauses of the corpus
  ratified by D-GOV-09. D-GOV-09 itself remains the historical ratification
  act, in force as ruled.
- **Leaves in force:** every other clause of the ratified corpus; all D-GOV
  records 01–20; the D-T0, D-APP, D-PEC, and project decision families.
- **Consumed by:** the future root-PRD adoption act (§11.3), which will cite
  this record as accepted basis.

## 16. Review dispositions

**Rev 2** (first adversarial review): (1) supersession inventory completed —
S3, S6, S7, S8 added, S1 broadened, S10 extended to LOOP_INIT:103-105;
non-binding surfaces moved to §3b. (2) K-WRITE-2 argument corrected to
checkout-containment; gloss routed as debt. (3) Ruling mechanics unified on
the D-GOV-18/19 exact-candidate pattern with AcceptedCandidateSHA /
EffectiveSHA and an exact-prose gate over Annex A. (4) G0 added; bootstrap
resolved. (5) G2 split into static register (G2) and pre-dispatch work-graph
check (G3); provenance-inference removed from the manifest check (G4).
(6) Preflight contradiction resolved by §7 classes. (7) §3b propagation table
added, including the export derivative. Smaller: M4 relabeled; D-GOV-09
phrasing corrected (§15); `human_actors.md` "apex" characterization removed
(§11.2); §10 reworded to eligibility.

**Rev 3** (reviewer verification of Rev 2): (1) S7 restored to `SPEC.md:79`
— Rev 2's line-number "correction" to `:81` was itself erroneous; the
reviewer's original citation was right (verified: `:79` is `{WORKING_ROOT}`,
`:81` is `{COORDINATION_ROOT}`). (2) Annex A completed for the universal
statements the table claimed but the annex missed: DIRECTIVE:199, :202 (S1
now three anchors), SPEC:48 (S6 now two anchors), and the DIRECTIVE:300
constraint label itself (S4/S5 now complete resulting rows). (3) M2 and Annex
S6 reworded so the gate supplies containment and evidence conditions and does
not grant authorization (K-AUTH-1); independent owner authorization required.
(4) Sequence contradiction resolved: step 4 completes before steps 5–6
parallelize; guard capability (pre–Project Setup) distinguished from guard
state (instantiated at Project Setup) in §5.3 and §6. (5) §3b corrected on
evidence: `domains/chirality` source map marks the root governance docs
`RETIRED_ARCHIVED_AFTER_BATCH1` (OUT) with no active manifest entries, so no
active corpus-drift detection is claimed; the App Dev authority corpus is
named as the demonstrably active pinned surface. (6) Annex A given explicit
application semantics (wording constraints at anchors; full resulting text
for sentence/row units).

---

## Annex A — Exact candidate prose for S1–S9

**Application semantics.** Annex entries are exact wording constraints at
identified insertion anchors; complete resulting text is given where the
amended unit is a single sentence or table row. Current text is verbatim at
AcceptedBasis. The implementation tranche applies these constraints; any
deviation returns for exact-prose re-acceptance (§14).

**S1 — `docs/DIRECTIVE.md` §2.6, three anchors.**

*Anchor `:199`.* Current: "The system separates the **instruction root** (the
release-managed agent operating system) from the **working root** (the
project state agents read and write):"
Amended: "The system separates the **instruction root** (the release-managed
agent operating system) from the **working root** (the project state agents
read and write) — with the single D-GOV-21 exception that the root product's
working root is the repository root:"

*Anchor `:202`.* Current (fragment): "One instruction root serves **many**
working roots — each `projects/<name>/` and `domains/<name>/` in this
monorepo, or a user-selected folder under the desktop harness."
Amended (append to bullet): "Under D-GOV-21, the repository root is
additionally the working root for the root product itself."

*Anchor `:204`.* Current: "This preserves a single stable agent operating
system across many projects and domains while keeping execution fully
filesystem-native in user-controlled state. A working root MUST NOT be
located inside the instruction root."
Amended (append): "Exception (D-GOV-21): the repository root is itself the
working root for development of the root product, with root `execution/` as
its execution root, under the replacement containment contract of D-GOV-21.
No other working root may be located inside the instruction root."

**S2 — `docs/DIRECTIVE.md:13`.**
Current (fragment): "…that serves multiple project and domain
**working-roots** nested under `projects/*` and `domains/*`."
Amended: "…that serves multiple project and domain **working-roots** nested
under `projects/*` and `domains/*`, and — under the D-GOV-21 exception — the
root product's own working root at the repository root."

**S3 — `docs/DIRECTIVE.md:76`.**
Current (fragment): "The instruction root (release-managed agent operating
system) is physically separated from the working root (user-controlled
project state)."
Amended (append to paragraph): "The root product itself is the one governed
exception: its working root is the repository root (D-GOV-21)."

**S4 — `docs/DIRECTIVE.md:300`** (constraints table row; complete resulting
row).
Current row: "| Instruction root separate from working root | Agent
instructions are release-managed; project data is user-controlled |"
Amended row: "| Instruction root separate from working root (root product
excepted per D-GOV-21) | Agent instructions are release-managed; project data
is user-controlled; root-product development excepted per D-GOV-21 |"

**S5 — `docs/DIRECTIVE.md:301`** (constraints table row; complete resulting
row).
Current row: "| One shared instruction root serves many working roots | A
single release-managed agent OS governs many projects and domains without
per-workspace instruction drift |"
Amended row: "| One shared instruction root serves many working roots | A
single release-managed agent OS governs many projects and domains without
per-workspace instruction drift; the instruction root additionally serves as
the root product's own working root (D-GOV-21) |"

**S6 — `docs/SPEC.md` §0.2.2, two anchors.**

*Anchor `:48`.* Current: "`WORKING_ROOT` is the project or domain workspace
an agent is scoped to — `projects/<name>/` or `domains/<name>/` in this
monorepo, or the user-selected folder under the desktop harness. It is where
governed project truth lives (`{EXECUTION_ROOT}`, tool roots, deliverables,
decomposition state)."
Amended (append): "For the root product only, `WORKING_ROOT` is `REPO_ROOT`
(D-GOV-21)."

*Anchor `:52`.* Current: "A working root MUST NOT be the shared instruction
surface itself; agents operating in a working root MUST NOT write to
`agents/`, `skills/`, `tools/`, or root `docs/` except through an explicit,
separately-authorized repo-wide instruction change."
Amended: "A working root MUST NOT be the shared instruction surface itself,
except that the root product's working root is the repository root under
D-GOV-21; agents operating in any working root MUST NOT write to `agents/`,
`skills/`, `tools/`, or root `docs/` except through an explicit,
separately-authorized repo-wide instruction change (root-product instruction
changes obtain that authorization through an independently owner-authorized,
human-gated repo-wide change tranche satisfying the D-GOV-21 M2 containment
and evidence conditions; the M2 gate does not itself grant authorization)."

**S7 — `docs/SPEC.md:79`** (path-anchor table row).
Current definition: "the active `projects/<name>/` or `domains/<name>/` (or
user-selected folder)"
Amended definition: "the active `projects/<name>/` or `domains/<name>/` (or
user-selected folder); for the root product only, `REPO_ROOT` (D-GOV-21)"

**S8 — `docs/SPEC.md:97`.**
Current: "An execution instance is a self-contained project workspace rooted
at `{EXECUTION_ROOT}/` (which resolves `WORKING_ROOT`-relative; see
§0.2–0.3). The execution root contains packages (work partitions) and tool
roots (derived/operational outputs)."
Amended (append): "The root product's execution instance is
`REPO_ROOT/execution` (D-GOV-21)."

**S9 — `docs/TYPES.md:51-52`.**
Current (Working Root): "The active project or domain workspace —
`projects/<name>/` or `domains/<name>/`, or a user-selected folder under the
desktop harness. Where governed project truth lives. One instruction root
serves many working roots."
Amended (append): "For the root product only, the repository root is its own
working root (D-GOV-21)."
Current (Execution Root): "The execution-instance root within a working root;
contains packages and tool roots."
Amended (append): "For the root product, `REPO_ROOT/execution` (D-GOV-21)."
