# Decision log — post-acceptance audit (node AK2)

These are the TASK's defaults, overrides and judgments. None of them changes
the decomposition.

- **D-1 · Output location.** As in BASELINE and POSTCHANGE, the brief confines
  the audit snapshot to `POSTACCEPT/` in the run folder instead of
  `_Evaluation/DecompCoverage/`. No scaffolding script was run. No
  `_Evaluation` pointer was created or moved.
- **D-2 · What was audited.** The working package at `3d006a909` after the
  owner's group-3 acceptance (DECISION-8), with:
  - H-1…H-4 applied;
  - the accepted snapshot finalized;
  - `_ScopeChange/_LATEST.md` naming it.
- **D-3 · Scope.** It is identical to BASELINE and POSTCHANGE D-3: PKG-01,
  02, 03, 04, 05, 08 and 09 (30 deliverables).
- **D-4 · Script.** It is POSTCHANGE's script with the two additions recorded
  in `QA_Report.md`:
  - (a) the Check-9b Change Register clause follows the actual binding;
  - (b) Check 10 runs because `_LATEST.md` now exists.

  A control run shows both additions are inert on the POSTCHANGE subject.
  BASELINE decisions D-4 to D-10 apply unchanged.
- **D-5 · COV-131.** The brief expects COV-131, the Change Register binding,
  to close. The Change Register part closes: "Decision Log" binds at rank
  exact. The finding ID COV-131 remains, as a WARNING, for the four
  pre-existing heading bindings (Ledger, Objectives, Partitions, Production
  Units), which BASELINE (COV-127) and IMPACT_ASSESSMENT §9 record as
  pre-existing and outside this amendment. Its severity is not reduced.
- **D-6 · `EXPECTED_CONSEQUENCE`.** The issue log keeps the baseline
  severities. No finding is now an expected consequence (`COMPARISON.md` §4).
- **D-7 · DAG currency.** The check is recorded in the post-acceptance
  validation record (`_PostAcceptanceValidation/SCA-V4-001_20260929T132946Z/DAG_CURRENCY.txt`),
  not here.
