# Decision log — pre-change baseline (node P3)

Defaults, overrides and judgments made by the TASK. None changes the decomposition.

- **D-1 · Output location (override of the contract write zone).** The audit-decomp contract writes a snapshot under
  `{EXECUTION_ROOT}/_Evaluation/DecompCoverage/COV_{RUN_LABEL}_{date}/`. The brief confines writes to `BASELINE/` in the
  run folder, so the snapshot contents are written there. The scaffolding scripts (`scaffold_tool_root.sh`,
  `create_snapshot_folder.sh`) were not run, and no `_LATEST.md` was created or moved. The integrator may copy this folder
  into `_Evaluation/DecompCoverage/` or into the scope-change snapshot as `Pre_Change_Coverage.json` (the contract's
  copy slot).
- **D-2 · What was audited.** The pre-change state is the **working** decomposition package at `306291bdd`. The accepted
  basis resolves via `checkpoint_snapshots/_LATEST_ACCEPTED.md` to `GROUP3-20260928T001055Z`. `_Decomposition/_LATEST.md`
  reads `Latest: (none)`. The GROUP3 snapshot is cited as `expected_source_snapshot`. 13 of 16 package files equal the
  GROUP3 canonical bytes. `SOFTWARE_DECOMP.md`, `Open_Issues.csv` and `External_Dependencies.csv` differ because they carry
  later standing and receiving updates (commit `ddd721a90`). No decomposition file changed between `874508f16` (P1's
  basis) and `306291bdd`. That is why P1 found reuse of the GROUP3 audit inadmissible (method step 5).
- **D-3 · Scope.** Method step 5 scopes the baseline to the affected packages and deliverables. O-20 recommends
  PKG-02, 03, 04, 05, 08, 09. IMPACT_ASSESSMENT §3 action **A41 modifies DEL-01-01 (PKG-01)**, so PKG-01 is added. The
  scope is therefore every package that holds an entity named by A18–A47:
  - ledger rows SOW-015, 016, 017, 137 and 138 are in PKG-05; SOW-052 is in PKG-02; SOW-201 and 202 are in PKG-09;
  - the deliverables of A32–A47 fall in PKG-01, 02, 03, 04, 05, 08 and 09.

  That makes 7 packages and 30 deliverables. `repository_topology` carries the whole-decomposition totals. The structure
  tool was run over all 41 declared units, so a whole-decomposition census is also available (`structure.json`).
- **D-4 · Section binding.** The Variant Section Binding algorithm was applied exactly to the `##` headings of
  `SOFTWARE_DECOMP.md`: strip the number, case-fold, then match exact, then prefix, then substring.
  - "Scope Ledger", "Objectives", "Packages" and "Deliverables" all get **no hit**.
  - The scope-change Change Register targets for SOFTWARE ("Decision Log", "Revision History") also get **no hit**.
  - The PROJECT-form target "Change Log" hits "Artifact coverage and decision/change log" by substring. This is recorded
    for reference only.

  Parsing continued rather than stopping at FAILED_INPUTS. Method step 0.2 makes the companion registers named in the
  package inventory the authoritative machine-truth for the matching semantic sections, and `Companion_Inventory.csv`
  names them explicitly: `ScopeLedger.csv`, `Objectives.csv`, `Packages.csv` and `Deliverables.csv`. The main document
  carries no Packages or Deliverables table to compare against, apart from the package summary table under "Accepted flat
  work domains", which was compared. The Change Register is **not bound**: no companion register exists for it and no
  heading rank matches. It is reported, not resolved by judgment (Check 9b, COV-127).
- **D-5 · Objectives (SOFTWARE).** For Check 7, the `ObjectiveIDs` column of `ScopeLedger.csv` is authoritative.
  `Objectives.csv` `MappedDeliverables` and `ScopeItemIDs`, and the counts in `Coverage_Telemetry.json`, were compared
  with it as support-count surfaces. All 10 objectives were evaluated because objective support is whole-decomposition;
  the scoped figures are identical.
- **D-6 · Checks 7 and 8.** Both were evaluated over the whole registers. Scoped counts are reported: 178 IN / 14 OUT /
  7 TBD ledger rows are homed in the scoped packages.
- **D-7 · Check 5 fields.** The `_CONTEXT.md` bullet fields were compared by exact value after whitespace normalization:
  - against Deliverables.csv: Name, PackageID, Type, ResponsibleParty, Description, ContextEnvelope,
    ContextEnvelopeNotes, AnticipatedArtifacts, CoversScopeItems, SupportsObjectives and PhaseHint;
  - against Packages.csv: Package Name, ScopeDescription, InclusionCriteria and Exclusions.

  The `ScopeOfWork.md` frontmatter identity, `project_scope_refs` and `package_objective_refs` were also compared, at
  INFO severity.
- **D-8 · Check 6 rule.** AnticipatedArtifacts are descriptive (for example `DOC: portable workflow/role/checkpoint
  contract`). A deterministic fuzzy rule is used: two or more shared significant tokens (length at least 4, with a
  stop-list) between the artifact text and a non-control file stem, or stem tokens that are a subset of the artifact
  tokens. `_run_records/` and `_Archive/` are excluded. All units are INITIALIZED, so absences are INFO. The resulting
  11.22 % is a heuristic indicator of Design drafts, not evidence that an artifact was produced. Production format was
  taken from `audit_structure.py`: SOW_V1, valid, for all units.
- **D-9 · Checks 9 and 10.** Check 9 is SKIPPED because the variant is not DOMAIN. Derivative-currency observations are
  logged under `CheckNumber=9` as the method directs. Check 10 is SKIPPED because `execution/_ScopeChange/_LATEST.md`
  does not exist (FIRST_AMENDMENT posture). `handoff_state_status` is SKIPPED with it.
- **D-10 · Severity of the stale main-document sentence (COV-121).** This is a WARNING rather than INFO, because A30 edits
  this document and the sentence contradicts its own status line and the 41 existing SoW folders. Per method Step 9, it
  "could mislead amendment work".
- **D-11 · `EXPECTED_CONSEQUENCE`.** None is used. No accepted decision was supplied, and the amendment is not yet
  accepted.
