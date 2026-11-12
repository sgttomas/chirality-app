# reconciliation — representation-migration profile

Load this profile only when a concordance run performs or verifies an
authorized deliverable-format or representation migration. It governs
reconciliation verification; production batching for the same migration is
governed by `scope-of-work`'s own representation-migration resource. It adds to
the [contract](contract.md) and [method](method.md); it does not apply to an
ordinary concordance run. The migration-specific validity clauses remain in
the contract.

## Invariants

- **Format-aware preservation.** During authorized conversion, legacy
  path/section claims remain the bound source and candidate stable IDs are
  derivative mappings. Every source claim receives exactly one disposition;
  deterministic finalization must externalize migration metadata and bind the
  clean production hash before atomic replacement selects `SOW_V1`.
  Unauthorized dual, evidence-candidate integration, silent loss, or semantic
  change fails closed.
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

## Ledger additions

For a deliverable-format migration, the accepted ledger additionally records
the four source hashes, evidence-candidate hash, clean production hash,
finalization-report hash, legacy source reference, candidate
compound ID, and `PRESERVED | MERGED | SPLIT | SUPERSEDED | DEFERRED |
CONFLICT` disposition. `MERGED` and `SPLIT` must preserve a complete
many-to-many mapping; format conversion does not authorize a content change.

## Narrowed third-layer fan-in

For a representation-migration wave that satisfies the prerequisite above,
the narrowed third-layer fan-in is:

1. Rehash 100% of package and child manifests and validate 100% of paths for
   containment, portability, existence, uniqueness, and self-exclusion.
2. Reproduce the full member census, terminal-result population, aggregate
   mapping/source totals, evidence and production hashes, replacement rows, inverse rollback
   rows, status/control preservation assertions, and project-write audit.
3. Execute or independently verify apply/target/rollback simulation for every
   member through the registered deterministic harness.
4. Freshly reproduce every member with a verifier finding, retry,
   remediation, failed check, hash/path discrepancy, unknown, or waiver.
5. Freshly reproduce a deterministic clean sample of at least one member per
   package, selecting the numerically final clean member to retain sensitivity
   to late-batch context/task drift. Increase the sample when risk, package
   heterogeneity, or prior escape evidence warrants it.
6. Treat every author/verifier disagreement as an exception requiring fresh
   reproduction. Escalate any exception or aggregate/sample failure to full
   affected-package reproduction, including all numeric sub-batches. Preserve
   the initial finding and remediation chain.

This profile narrows only redundant third-layer member reproduction. It keeps
100% independent package verification, 100% aggregate/manifest/simulation
coverage, and rare-escape detection.
