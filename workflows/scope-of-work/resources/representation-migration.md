# Package representation migration

WORKING_ITEMS selects this profile only for an explicitly authorized LEGACY_FOUR_DOC to SOW_V1 conversion. The method retains the accepted operating limits and member-level evidence requirements from the frozen pre-overhaul WORKING_ITEMS package.

- **Bounded representation-migration batches.** For related four-document to
  `SOW_V1` conversion work, use one package-wide author Agent 2 followed by one
  fresh package-wide verifier Agent 2 for a batch of no more than five members
  and no more than 2,053 frozen legacy source lines. If either bound would be
  exceeded, partition the package deterministically by ascending numeric
  `DeliverableID` into the minimum number of consecutive sub-batches that each
  satisfy both bounds. One WORKING_ITEMS instance retains package ownership
  across all sub-batches. The observed bound is a qualified operating limit,
  not a claim about unbounded context capacity or other production methods.
- **Batch evidence is member-complete.** Package-wide execution does not
  collapse deliverable identity or evidence. Author and verifier returns must
  retain complete per-member mappings, source-line coverage, hashes,
  finalization reports, replacement/inverse rows, simulations, checks,
  telemetry, findings, and rerun triggers. The fresh verifier is evidence-only
  and must not repair author outputs; a defect returns to a fresh author run or
  an explicitly authorized bounded remediation node.

- **Target versus residual.** `ScopeOfWork.md` is the stable `SOW_V1` target
  contract while `_STATUS.md ## Remaining`
  remains the executable residual surface. Tests are evidence against `AC-*`;
  they do not create scope or acceptance criteria.
- **Single-file integration ownership.** Agent 2 children may prepare disjoint
  proposals and evidence concurrently, but only one declared integration owner
  writes a conversion-candidate `ScopeOfWork.md` for a deliverable. That
  evidence-rich candidate is not integration input: deterministic finalization
  must produce a separate clean production contract, and all terminal checks
  and integration manifests bind that final hash.

Use one author and a fresh evidence-only verifier, serially. The verifier covers every selected member. Bind clean production hashes after deterministic finalization; integrate only those clean artifacts.
