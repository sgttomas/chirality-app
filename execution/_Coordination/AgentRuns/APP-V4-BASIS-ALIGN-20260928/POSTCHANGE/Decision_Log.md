# Decision log — post-change audit (node AK1)

Defaults, overrides and judgments of the TASK. None changes the decomposition.

- **D-1 · Output location.** As in BASELINE D-1, the brief confines the audit snapshot to `POSTCHANGE/` in the run
  folder instead of `_Evaluation/DecompCoverage/`. No scaffolding script was run and no `_LATEST.md` was created or
  moved.
- **D-2 · What was audited.** The working decomposition package and deliverable folders at `f4ba34c2c` plus the
  uncommitted SCA-V4-001 candidate edits (checkpoint groups 1–2 accepted, DECISION-7). The acceptance-conditional
  edits A07, A17a–c and D-15 are not in the subject.
- **D-3 · Scope.** Identical to BASELINE D-3: PKG-01, 02, 03, 04, 05, 08, 09 (30 deliverables).
- **D-4 · Like-for-like script.** BASELINE's `audit_checks.py`, with only the two label fields parameterized. BASELINE
  decisions D-4 to D-10 (binding, objectives, Checks 7/8 whole-register evaluation, Check 5 fields, Check 6 heuristic,
  Checks 9/10, COV-121 severity) apply unchanged.
- **D-5 · Control run.** To attribute each difference, the same script ran on the pre-application tree at
  `f4ba34c2c` (scratch only). Its result is quoted in `COMPARISON.md`; it is not a deliverable of this run.
- **D-6 · `EXPECTED_CONSEQUENCE`.** The issue log keeps the baseline script's severities, so that the counts compare
  like for like; `issues_expected_consequence` is 0. The group-3 classification (the Change Register part of COV-131 as
  an expected consequence of holding D-15) is recorded in `COMPARISON.md` §3, where the scope-change method asks for
  it. COV-131 also carries pre-existing heading findings, so its severity is not reduced.
- **D-7 · Projections.** `projections.py` simulates the acceptance-conditional edits in memory with a placeholder
  date and recomputes the register-derivable `Coverage_Telemetry.json` fields. It writes only `projections.json`
  and changes no repository file.
- **D-8 · DAG currency.** `shasum -a 256 -c _DAG/DAG-001/SOURCE_MANIFEST.sha256`, run from the execution root, is
  recorded in `DAG_CURRENCY.txt` (130/130 OK, exit 0).
