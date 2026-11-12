# reconciliation — contract

## Invariants

- **Activation before discovery dispatch.** A project decision register must
  contain the human ruling, activated scope, pinned method revision, and run
  pointer on the shared baseline before any discovery dispatch. Independent
  review of the activation diff, where required before its merge, is permitted
  before activation and recorded in the run evidence; it performs no discovery.
- **Frozen accepted basis.** Record accepted decomposition, decisions,
  lifecycle semantics, source/reliability rules, implementation state, current
  dependency pointer, evidence boundary, and overlapping work.
- **Claim-level audit.** Requirements and stable scope claims are atomic audit
  units. Deliverable/package summaries are derived from claim rows and never
  replace them. A claim is a statement whose invalidation by implementation
  change would need a recorded decision, or that another surface depends on,
  or that named evidence can check (shared method §3.1). Mechanism-level
  descriptions are evidence, not claims, and a claim written at that level is
  a granularity defect in the deliverable, repaired by default by lifting
  it, and by rewriting it to the code only where the ruling gives a reason.
- **Representation migration.** A run that performs or verifies an authorized
  deliverable-format or representation migration also follows
  [the representation-migration profile](representation-migration.md).
- **Discovery is read-only.** Calibration, inventory, claim concordance, and
  synthesis do not repair the target corpus.
- **Evidence is not authority.** Implementation and tests are evidence, not
  permission to invent or change scope. Agent dispositions are not human
  rulings. A ruling not yet applied to its carriers is R5 work under that
  ruling, not a new owner question. An application under an explicit written
  owner delegation that names the decision class or rows it covers, recorded
  verbatim and kept within its words and this run, is an agent disposition;
  issuance, professional acceptance, and holds stay with their holders.
- **Source-state binding.** Every evidence citation names the source state it
  evaluated. Material source change marks affected work `STALE_INPUT` and
  requires rerun.
- **Project divergence is preserved.** Engineering validation/provenance,
  inspection recency, professional-boundary, security, or other adopted
  project layers remain explicit rather than being flattened into the kernel.
- **Human-calibrated conventions.** Scale-out occurs only after the human
  accepts the project convention set and named repairs/addenda.
- **Bounded waves.** Partition the corpus into package/tranche waves with
  disjoint run-artifact writes and declared dependencies. When runtime slot
  capacity is lower than the preferred package fan-out, use capacity-bounded
  batches while preserving one owning worker per deliverable and independent
  package fan-in; do not treat a temporary capacity variance as a standing
  orchestration-policy rewrite.
- **Validated fan-in.** Every wave receives structural checks and a bounded
  adversarial/semantic verifier. Defective ledgers are rerun; they are not
  silently patched by the manager.
- **Containment includes ignored state.** Check tracked changes, untracked
  non-ignored paths, and ignored-path allowlists. Keep frozen evidence trees
  unchanged; use copy-out or external cache/target roots when validation would
  otherwise contaminate them.
- **Independent progress.** Blocked claims or packages do not halt independent
  work. Declared dependants remain held.
- **No invented repair authority.** R4 human/engineering decisions authorize
  R5 tranches. Scope changes route to WORKING_ITEMS (workflow: scope-change).
  Only a single deliverable's lifecycle transition routes to WORKING_ITEMS
  (workflow: review); other review acts route to a bounded independent TASK
  review with a named output, or to the owner or engineering holder. Git
  closeout remains with the responsible implementation owner under the
  project's authorization and Git conventions (AGENTS.md for the Chirality Library).
  Workflow-component findings route to HELPS_HUMANS.
- **One execution record.** In an adopting local-graph loop, the authorized
  graph carries executable work; no new Remaining seeding or duplicate residual
  list is required. Scope and decisions retain their authority; MEMORY is
  a terse index of actual runs and central evidence. Earlier pinned programs
  retain their own Remaining-based conventions and audited source populations
  until a specific migration.
- **No false closure.** Closure requires backchecked changed claims, evidence
  accounting for unfulfilled obligations and their owning work/decision,
  derivative disposition, source-state binding, blockers and handoff state.
  A legacy Remaining state is required only by a still-pinned convention.

## Inputs

- `PROJECT_ROOT`, `EXECUTION_ROOT`, `RunID`;
- activation ruling and accepted scope;
- pinned shared method and project adoption/profile revision;
- accepted decomposition, decision register, current dependency pointer, and
  lifecycle authority;
- source/implementation/test/evidence roots and reliability rules;
- project-specific claim classes, dispositions, gates, and validation layers;
- allowed tools, write boundaries, wave policy, and return contracts.

## Validity

A concordance run is valid only when:

1. Activation, accepted scope, pinned method/profile, and source state are
   explicit and committed before any discovery dispatch; any independent review
   of the activation diff that preceded it is recorded.
2. Discovery phases do not modify the target corpus.
3. Every claim has an authority source or an explicit unmapped/unknown status.
4. Behavioral aligned claims cite implementation and current verification;
   project-required validation/provenance is separately satisfied or flagged.
5. Evidence and dispositions are bound to the actual source state.
6. Project-specific reliability and professional-boundary rules are applied.
7. Every wave passes structural validation and independent fan-in review. A
   narrowed [representation-migration](representation-migration.md) fan-in
   additionally proves its 100% aggregate coverage, exception population,
   deterministic sample, and escalation disposition.
8. Package and corpus summaries reproduce from accepted claim rows.
9. Conflicts, unknowns, stale inputs, unmapped implementation, lifecycle
   issues, and unfulfilled-obligation mismatches (legacy Remaining only where
   pinned) remain visible.
10. Repairs cite the authorizing human decision and respect owning workflows.
    Held and deferred rows retain their exact claim populations, gates, and
    non-activation evidence; issued baselines use their formal change path.
11. Backcheck covers every changed claim reference and proves exact multiset
    equality to the authorized repair manifest; authorized no-change rows are
    separately and explicitly accounted for. Auxiliary assessment tables
    (dependency-record, capability, and reverse-pass populations) are
    accounted separately with their own exact keys, never folded into the
    claim population. Each coverage checker demonstrates, by negative controls,
    that it rejects a missing key and a duplicate key.
    A conversion candidate proves 100% source-claim disposition and source-hash
    equality; deterministic finalization proves the clean production binding
    without treating isolated dual-format output as accepted truth.
12. Every compared deliverable is accounted for in the closing result, including
    unmet obligations and their actual owning work or decision, or evidence that
    none remains in the stated scope. This snapshot does not create a second
    maintained queue. A still-pinned legacy Remaining census retains its exact
    population and convention until the owning program explicitly migrates it.
13. The accepted discovery snapshot remains immutable and R6 is a new
    source-state-bound derivative snapshot. An authorized post-R6 continuation
    is a further successor derivative under `BACKCHECK/` with its own
    multiset proof.
14. Closure records unresolved blockers, waivers, reruns, derivative status,
    validation limitations, and next owner without making reliance claims.
    Routed authority residuals may remain open when their non-activation is
    proven and the run's closure meaning is explicitly bounded.

## Artifacts and schemas

```text
{EXECUTION_ROOT}/_Reconciliation/DeliverableConcordance/<RunID>/
  RUN_BASIS.md
  RUN_STATE.jsonl                            # append-only phase state
  RESUME.md
  R0_CALIBRATION/
  CONVENTIONS.md
  DELIVERABLE_INVENTORY.csv
  IMPLEMENTATION_SURFACES.csv
  VERIFICATION_INDEX.csv
  VALIDATION_AND_PROVENANCE_INDEX.csv        # when applicable
  AUTHORITY_AND_SOURCE_RELIABILITY_MAP.md
  WAVES/<WaveID>/
    <DeliverableID>_claims.csv
    <DeliverableID>_notes.md
    <PackageOrWave>_VERIFICATION.md
  PACKAGE_SUMMARIES/
  CROSS_PACKAGE_FINDINGS.csv
  DECISION_PACKETS/
  REPAIR_TRANCHES/
  BACKCHECK/<BackcheckSnapshotID>/           # R6 or an authorized successor
    CHANGED_CLAIM_REEXTRACTION.csv
    DETAILED_EVIDENCE.csv
    RIDER_AND_ASSESSMENT_AUDIT.md
    HELD_AND_DEFERRED_AUDIT.md
    CONTAINMENT_AUDIT.md
    OBLIGATION_ACCOUNT.csv             # legacy pinned programs retain REMAINING_WORK_CENSUS.csv
    BACKCHECK.md
    HANDOFF.md
  HANDOFF_STATE.md
```

Claim ledgers minimally identify claim, claim class, normative source,
declared/current state, implementation evidence, verification evidence,
validation/provenance where required, lifecycle, unfulfilled obligations and
their actual owning work or decision,
disposition, authority needed, selectability, source-state binding, notes, and
evidence references. Projects may extend the schema but may not remove the
kernel evidence distinctions.

The canonical run root is
`_Reconciliation/DeliverableConcordance/<RunID>/`. Historical generic audit
subtrees are not migrated into this contract.

The app-dev proto-run `RUN_D55_CONCORDANCE_2026-07-11_1904Z` is closed and
integrated. Its R6 derivative at
`projects/chirality-app-dev/execution/_Reconciliation/DeliverableConcordance/R6_D55_BACKCHECK_2026-07-12_1903Z/`
provides the changed-claim multiset, rider/assessment audit, obligation account,
source-basis binding, and handoff requirements incorporated above.

The piping proto-run `DELIVERABLE_CONCORDANCE_2026-07-11_1305` is closed and
integrated. Its distributed terminal package—`RUN_SUMMARY.md`, DEC-074,
`R5_RUN_SUMMARY.md`, T1–T9 closeouts, `RUN_BASIS.md`, and Receipt 42—provides
the exact repair/hold/deferral accounting, frozen/active containment evidence,
ISSUED-baseline protection, capacity-bounded fan-out evidence, limitations,
and routed-residual posture incorporated above. Historical files are not
renamed or retrofitted merely to resemble this template.

The obligation account is a closing evidence snapshot of the declared comparison,
not a maintained task list. It references graph/decision sources for current
execution. Legacy Remaining columns and filenames are retained only for an
explicitly pinned input/output contract; preserve their identities in that run.
