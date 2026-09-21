# reconciliation — contract

## Invariants

- **Activation before dispatch.** A project decision register must contain the
  human ruling, activated scope, pinned method revision, and run pointer on the
  shared baseline before discovery begins.
- **Frozen accepted basis.** Record accepted decomposition, decisions,
  lifecycle semantics, source/reliability rules, implementation state, current
  dependency pointer, evidence boundary, and overlapping work.
- **Claim-level audit.** Requirements and stable scope claims are atomic audit
  units. Deliverable/package summaries are derived from claim rows and never
  replace them.
- **Format-aware preservation.** During authorized conversion, legacy
  path/section claims remain the bound source and candidate stable IDs are
  derivative mappings. Every source claim receives exactly one disposition;
  deterministic finalization must externalize migration metadata and bind the
  clean production hash before atomic replacement selects `SOW_V1`.
  Unauthorized dual, evidence-candidate integration, silent loss, or semantic
  change fails closed.
- **Discovery is read-only.** Calibration, inventory, claim concordance, and
  synthesis do not repair the target corpus.
- **Evidence is not authority.** Implementation and tests are evidence, not
  permission to invent or change scope. Agent dispositions are not human
  rulings.
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
- **No blanket third-pass duplication.** When a representation-migration wave
  already has 100% deterministic member validation plus a fresh evidence-only
  verifier over every member, WORKING_ITEMS independently validates the full
  aggregate evidence surface but does not automatically repeat every member's
  complete semantic/deterministic suite. Fresh member reproduction is
  exception-driven plus the deterministic sample below. This optimization
  never removes the package verifier or weakens fail-closed escalation.
- **Accepted batch-production prerequisite.** A representation-migration
  package may arrive from one package-wide author plus one fresh package-wide
  verifier when each deterministic numeric batch contains no more than five
  members and 2,053 frozen legacy source lines. Larger packages are consecutive
  numeric sub-batches under one WORKING_ITEMS manager. This changes production
  session topology only: every member still requires complete author and
  verifier evidence, and the verifier remains evidence-only with no repair
  authority.
- **Containment includes ignored state.** Check tracked changes, untracked
  non-ignored paths, and ignored-path allowlists. Keep frozen evidence trees
  unchanged; use copy-out or external cache/target roots when validation would
  otherwise contaminate them.
- **Independent progress.** Blocked claims or packages do not halt independent
  work. Declared dependants remain held.
- **No invented repair authority.** R4 human/engineering decisions authorize
  R5 tranches. Scope changes route to WORKING_ITEMS (workflow: scope-change); lifecycle acceptance to
  WORKING_ITEMS (workflow: review); Git closeout to WORKING_ITEMS (workflow: change); workflow-component findings to HELPS_HUMANS.
- **Remaining is executable truth.** Deliverable-local `_STATUS.md ## Remaining`
  is the executable residual surface where the adopting project uses it.
  Plans and run artifacts do not select work.
- **No false closure.** Closure requires backchecked changed claims, warranted
  Remaining state, derivative disposition, source-state binding, unresolved
  blockers, rerun requirements, and handoff state.

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
   explicit and committed before dispatch.
2. Discovery phases do not modify the target corpus.
3. Every claim has an authority source or an explicit unmapped/unknown status.
4. Behavioral aligned claims cite implementation and current verification;
   project-required validation/provenance is separately satisfied or flagged.
5. Evidence and dispositions are bound to the actual source state.
6. Project-specific reliability and professional-boundary rules are applied.
7. Every wave passes structural validation and independent fan-in review. A
   narrowed representation-migration fan-in additionally proves its 100%
   aggregate coverage, exception population, deterministic sample, and
   escalation disposition.
8. Package and corpus summaries reproduce from accepted claim rows.
9. Conflicts, unknowns, stale inputs, unmapped implementation, lifecycle
   issues, and Remaining mismatches remain visible.
10. Repairs cite the authorizing human decision and respect owning workflows.
    Held and deferred rows retain their exact claim populations, gates, and
    non-activation evidence; issued baselines use their formal change path.
11. Backcheck covers every changed claim reference and proves exact multiset
    equality to the authorized repair manifest; authorized no-change rows are
    separately and explicitly accounted for.
    A conversion candidate proves 100% source-claim disposition and source-hash
    equality; deterministic finalization proves the clean production binding
    without treating isolated dual-format output as accepted truth.
12. Every deliverable appears in the final Remaining census, including an
    explicit `NONE` row where applicable; project-specific riders and stale
    assessments are dispositioned without historical recoding.
13. The accepted discovery snapshot remains immutable and R6 is a new
    source-state-bound derivative snapshot.
14. Closure records unresolved blockers, waivers, reruns, derivative status,
    validation limitations, and next owner without making reliance claims.
    Routed authority residuals may remain open when their non-activation is
    proven and the run's closure meaning is explicitly bounded.

## Artifacts and schemas

```text
{EXECUTION_ROOT}/_Reconciliation/DeliverableConcordance/<RunID>/
  RUN_BASIS.md
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
  BACKCHECK/<BackcheckSnapshotID>/
    CHANGED_CLAIM_REEXTRACTION.csv
    DETAILED_EVIDENCE.csv
    RIDER_AND_ASSESSMENT_AUDIT.md
    HELD_AND_DEFERRED_AUDIT.md
    CONTAINMENT_AUDIT.md
    REMAINING_WORK_CENSUS.csv
    BACKCHECK.md
    HANDOFF.md
  HANDOFF_STATE.md
```

Claim ledgers minimally identify claim, claim class, normative source,
declared/current state, implementation evidence, verification evidence,
validation/provenance where required, lifecycle and Remaining state,
disposition, authority needed, selectability, source-state binding, notes, and
evidence references. Projects may extend the schema but may not remove the
kernel evidence distinctions.

The canonical run root is
`_Reconciliation/DeliverableConcordance/<RunID>/`. Historical generic audit
subtrees are not migrated into this contract.

The app-dev proto-run `RUN_D55_CONCORDANCE_2026-07-11_1904Z` is closed and
integrated. Its R6 derivative at
`projects/chirality-app-dev/execution/_Reconciliation/DeliverableConcordance/R6_D55_BACKCHECK_2026-07-12_1903Z/`
provides the changed-claim multiset, rider/assessment audit, Remaining census,
source-basis binding, and handoff requirements incorporated above.

The piping proto-run `DELIVERABLE_CONCORDANCE_2026-07-11_1305` is closed and
integrated. Its distributed terminal package—`RUN_SUMMARY.md`, DEC-074,
`R5_RUN_SUMMARY.md`, T1–T9 closeouts, `RUN_BASIS.md`, and Receipt 42—provides
the exact repair/hold/deferral accounting, frozen/active containment evidence,
ISSUED-baseline protection, capacity-bounded fan-out evidence, limitations,
and routed-residual posture incorporated above. Historical files are not
renamed or retrofitted merely to resemble this template.
