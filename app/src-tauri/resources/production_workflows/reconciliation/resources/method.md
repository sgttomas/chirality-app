# reconciliation — method

## Method

### R0 — Activate and calibrate

1. Verify the activation ruling is committed on the shared baseline before any
   discovery dispatch. An independent review of the activation diff may run
   before its merge; record that launch in the run evidence. It performs no
   discovery work.
2. Freeze `RUN_BASIS.md`: source state, accepted authorities, corpus census,
   concurrent-work check, method/profile revisions, and fences.
3. Ask the human about off-code events (signing, notarization, native checks,
   manual reviews, releases) and their result artifacts; an event without a
   located result is unknown evidence, not proof that it did not occur.
4. Select a diverse calibration sample spanning claim types, evidence classes,
   lifecycle states, and project-specific risks.
5. Dispatch one bounded TASK or ephemeral generalist per sampled deliverable.
6. Validate row schema, citation quality, disposition consistency, false
   positives, and project-specific evidence rules.
7. Present conventions, addenda, named repairs, and scale-out choice to the
   human. Do not edit deliverables.

### R1 — Read-only corpus inventory

Build source-state-bound inventories for deliverables, objectives/scope,
implementation surfaces, verification, validation/provenance where applicable,
decisions/authority, lifecycle state, and unfulfilled obligations (legacy
Remaining only where pinned). Resolve live pointers
rather than trusting historical snapshot names. Record unmapped surfaces,
identity collisions, stale evidence, and reliability exclusions. Route the
reverse ownership pass for each unmapped surface to every proposed owner; an
owner never asked has not declined.

### R2 — Package concordance waves

1. Derive wave order from accepted package/dependency state and the objective.
2. Freeze a wave brief with disjoint deliverable/run-artifact writes.
3. Dispatch one claim-ledger worker per deliverable, using the accepted
   conventions and project divergence layer.
4. Structurally validate each sub-batch before launching more.
5. Dispatch an independent verifier per package/wave over all self-flagged and
   non-aligned rows plus the adopted representative aligned sample.
6. Rerun defective ledgers through a fresh worker. Preserve verifier findings.
7. Derive package summaries from the accepted ledgers and record calibration
   lessons for later waves.

Keep a run-wide register of shared readings for recurring forks, inherited by
later waves, and preserve the original disagreements it normalizes. Hash each
newly created subclaim body when it is minted; a stable key alone does not
bind text.

For a deliverable-format or representation-migration wave, load
[the representation-migration profile](representation-migration.md) for its
ledger additions and narrowed third-layer fan-in.

Terminal fan-out/fan-in is the default when deliverables are independent.
Supervised many-to-many coordination is used when a discovery changes active
or planned siblings; the notice flows through the parent and preserves claim
status and evidence.

### R3 — Cross-package synthesis

Reconcile duplicate/incompatible ownership, shared implementation surfaces,
cross-package dependencies, inconsistent decisions or terminology, reused
evidence with incompatible meanings, unmapped implementation, stale
verification/validation, lifecycle mismatches, and unfulfilled-obligation
defects (legacy Remaining only where pinned).
Do not change dependencies or deliverables during synthesis.

Cluster rows whose disposition rests on mechanism-level wording (the claim
describes how the implementation works rather than what it must satisfy) as
a granularity cause, so that R4 can put the repair posture to the human once
rather than packet by packet. The test is the shared method's claim
granularity rule (`sgttomas/chirality:docs/COMPATIBILITY_FORMATS.md#historical-concordance-method` (private archive) §3.1).

### R4 — Human and engineering decision gate

First sort the rows into ruled-but-not-yet-applied rows and genuinely open
decisions. A row an existing ruling already settles becomes R5 work under that
ruling, citing it; do not ask the owner to decide it again. Where the owner has
given an explicit written delegation that names the decision class or rows it
covers, record its words verbatim; each application stays within those words
and this run and is recorded as an agent disposition, not a human ruling;
issuance, professional acceptance, and holds are never delegated this way.

For the open decisions, produce decision packets containing options, evidence,
provenance/reliability, affected claim IDs and packages, risks, recommended
routing, and the exact on-ruling mechanism. Distinguish owner, engineering,
WORKING_ITEMS (workflow: scope-change), HELPS_HUMANS, and external-authority
decisions. Route to WORKING_ITEMS
(workflow: review) only a single deliverable's lifecycle transition; route any
other review act to a bounded independent TASK review with a named output, or
to the owner or engineering holder whose judgment it needs. Stop affected
repair paths until the responsible human acts.

Wherever an option changes deliverable text, state both executions and
which one the packet recommends:

- **(a) rewrite** the mechanism detail so it matches the current
  implementation;
- **(b) lift** the claim to the level the claim granularity rule identifies
  (decision-bound, depended on, or checkable by named evidence) and move the
  mechanism into the evidence columns.

(b) is the default; recommend (a) only with a stated reason, such as the
mechanism itself being decision-bound. Put the run-level posture to the human
as its own item, ruled before the packets, and sort the packets by whether
the default posture dissolves the question, narrows it, or leaves it
untouched. Rows where it is a judgment whether the statement is
decision-bound stay visible as rows; the posture does not absorb them.

### R5 — Authorized repair tranches

Execute only adopted repairs. Partition writes by owning package/deliverable or
one declared integration owner. Update normative/declared surfaces only under
their ruling; update implementation/tests only under accepted production
briefs; update lifecycle only through its owning contract. For graph-led work,
return unfinished execution to its graph; supply central result pointers for the
subsequent terse MEMORY run entry.
Do not generate a mandatory future-work list in deliverables.
Do not edit agent instructions, workflows, root governance, or a project's
governing corpus (DIRECTIVE/CONTRACT/SPEC/TYPES/PRD) from a product repair
tranche. Protect ISSUED or otherwise formally accepted baselines through
their governing change path. Account for completed, held, and deferred repair
rows and affected claims exactly; mechanical selectability is never execution
authority.

Write repairs at claim level. For each repaired claim the worker applies the
claim granularity rule (`sgttomas/chirality:docs/COMPATIBILITY_FORMATS.md#historical-concordance-method` §3.1) in
this order:

1. **Decision.** Would changing the implementation so the statement no longer
   holds need a ruling, a scope change, or another registered act? If so, it
   is a claim.
2. **Interface.** Does another deliverable, a user, another project, or a
   governing document depend on it? If so, it is a claim.
3. **Verification.** Can it be checked by named evidence (a test, proof
   record, script, or run record) rather than only by reading the code? If
   so, it is a claim, and the repaired text names that evidence.

A statement that fails all three is removed from the claim surface under the
lift execution (b), and, where it helps a reader, kept as an evidence
reference. The rewrite execution (a) is used only where the ruling says so,
with its reason quoted in the repair manifest. A repaired claim describes what
the implementation must satisfy and cites its verification; it does not
describe the implementation. Unmapped implementation named in the ruling
either gains a claim at requirement level or is recorded as evidence of the
existing claim the ruling names. Record every (a)/(b) choice per claim in the
repair manifest so the R6 backcheck can reproduce it.

### R6 — Backcheck and close

Create a new immutable backcheck derivative; do not rewrite the accepted
discovery snapshot. Re-extract every changed claim reference against the final
repaired source basis and prove multiset equality with the authorized repair
manifest. Record authorized no-change or no-repair rows explicitly rather than
dropping them from accounting. Rerun required checks, verify decision and
graph/result accounting, and audit project-specific riders, stale assessments, and
other preserved conditions.

Perform this final post-repair backcheck even if discovery already produced an
R6 or equivalent coverage backcheck. Preserve the earlier discovery closeout
as upstream evidence; a project-local phase label does not substitute for
verification of the repaired state.

Produce a source-bound closing account with every compared deliverable represented,
including explicit `NONE` rows where no residual remains. Reproduce
package/corpus summaries, record stale or deferred derivatives, and issue a
handoff that names the accepted upstream snapshot, current derivative, exact
repaired source basis, closure verdict, blockers, lifecycle posture, and
material-change rerun triggers. Closure is evidence coherence, not issuance,
release readiness, certification, or professional approval.

### Recovery and continuation

Keep phase state append-only in `RUN_STATE.jsonl` (phase openings, frozen
briefs and bound-input hashes, launches, returns, capacity) with a `RESUME.md`
that says how to replay it. Freeze briefs so that relaunching one is
idempotent: it rewrites only its declared outputs. A launch without a matching
return is unresolved; confirm it is no longer executing, or interrupt it, before
relaunching it from its stored brief with a fresh agent. An
interrupted or partial return is recorded as an execution failure and never
promoted to PASS; hand its partial findings to a fresh agent for independent
checking.

An authorized continuation after R6 writes a successor derivative under
`BACKCHECK/<SuccessorID>/`, never into the discovery snapshot or an earlier
backcheck. It names its predecessor, authorizing instruction, and source
basis, and carries its own changed-claim multiset proof against its own repair
manifest together with full-key continuity with the original census.

## Local-graph adoption and historical accounting

Newly adopted graph-led programs account for unfinished obligations through the
actual graph or owning decision, not a new Remaining list. Existing Remaining
units and legacy result fields are historical inputs when present in a frozen
comparison; preserve their identities and exact authorized disposition. A program
pinned to an earlier census or activation convention changes only through its
specific adoption. A filename or legacy field does not authorize a duplicate
current execution queue. Memory indexes the actual run and its central evidence and decisions.
