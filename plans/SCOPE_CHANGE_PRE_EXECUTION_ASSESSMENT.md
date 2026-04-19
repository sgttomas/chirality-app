# SCOPE_CHANGE Pre-Execution Assessment: West Doe Two-Root DBM Remediation Plan

## Context

The plan at `plans/WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md` proposes an eight-phase campaign to remediate two DOMAIN roots against the cleaned West Doe source authority package and publish two independent DBMs. This assessment evaluates the plan's assumptions against the actual state of the target domain folders as of 2026-04-18, after creation of the cleaned replacement package under `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/`.

## Agent Persona

Operating as **SCOPE_CHANGE** — the controlled decomposition amendment agent. This assessment is a pre-execution review, not a gate action. No decomposition truth is being modified.

---

## Finding 1: Authority Allocation Matrix Is Template-Only

**File:** `plans/Authority_Allocation_Matrix.csv`
**Status:** Contains 4 template placeholder rows with notes like "Template example only. Replace or delete."
**Plan reference:** Phase 2 requires this matrix built, approved, and frozen before any remediation run.

**Assessment:** Phase 2 is the immediate blocking work item. The plan correctly sequences it before remediation, but the matrix does not yet exist in any substantive form. The extraction task has changed shape: instead of authoring from the archived raw `Process_DBM.md` alone, the matrix should now be built from the cleaned authority package consisting of an 820-line narrative Markdown, 16 canonical CSV tables, `metadata/tables.yaml`, and the package validation record.

---

## Finding 2: Both Roots Already Have SCA-001 and SCA-002 Applied

### Deepcut (Root A)
- `_ScopeChange/_LATEST.md` points to SCA-002 (2026-04-14, 3-25 interface coordination)
- Prior: SCA-001 (2026-04-14, VE workshop closure — 34 actions)
- Telemetry: v4.2-SCA-002-final
- Ledger: 5,961 rows (4,965 IN / 701 OUT / 14 TBD / 281 RETIRED)
- All structural invariants PASS

### Comp & Liquids (Root B)
- `_ScopeChange/_LATEST.md` points to SCA-002 (2026-04-14)
- Prior: SCA-001 (2026-04-14, VE + condensate dehy removal)
- Ledger: 319 rows (267 IN / 47 OUT / 5 TBD)
- 3 KTYs retired by SCA-002 (KTY-04-03, KTY-04-04, KTY-05-03)
- All structural invariants PASS except 5 flare-system TBD units

**Assessment:** Phase 1 freeze must capture these as the starting baselines. The next SCOPE_CHANGE runs in each root will be SCA-003. The plan does not explicitly state the starting SCA pointer — it should.

---

## Finding 3: KTY-Local Content Maturity

### Deepcut
- 18 categories, 97 KTYs, 432 subjects
- CAT-level folders exist (CAT-000 through CAT-017)
- KTY-local Scoping.md/KA files confirmed present (different folder structure than Comp & Liquids)
- Rich aggregation content: 90+ equipment extracts, process flow narrative, equipment list with validation suite
- Publication planning started: test_Section_Map.csv exists in `_Publication/DBM/_Planning/`

### Comp & Liquids
- 18 categories, 84 KTYs (3 retired), 272 subjects
- Full KTY-local content: each KTY folder contains Scoping.md, KA-*.md files, _CONTEXT.md, _STATUS.md, _MEMORY.md, _SEMANTIC.md, _DEPENDENCIES.md, _REFERENCES.md
- Equipment extracts in _Aggregation (85 subdirectories)
- Publication planning folder exists but is empty

**Assessment:** Both roots have KTY-local production artifacts. Phases 4 and 6 are regeneration tasks as the plan states.

---

## Finding 4: Flare System Boundary Is an Unresolved Shared-Interface Issue

**Root:** Comp & Liquids
**Issues:** ISS-006-003 through ISS-006-007 (5 issues, all HBK-0201 through HBK-0205)
**Type:** Boundary contradiction — shared flare system scope
**Status:** TBD (pending user ruling via DEC-006-005)

**Resolution:** Record a preliminary classification in the allocation matrix (Phase 2) as SHARED_INTERFACE/TBD, then finalize the ruling during Comp & Liquids SCOPE_CHANGE (Phase 5) with the full protocol. This keeps the matrix honest without forcing a premature ruling.

---

## Finding 5: Cleaned Source Authority Package Aligns With Plan Assumptions

- Active authority package root: `domain-test/domains/West_Doe_Combined/_Sources/west_doe_process_design_basis_clean/`
- Narrative working authority: `Process_DBM_fixed.md` (820 lines), organized by facility (03-25 / 04-25)
- Canonical tabular authority: 16 CSV tables under `data/`
- Traceability map: `metadata/tables.yaml`
- Validation record: `validation/validation_report.md` with PASS status
- Source anchor: the original PDF remains in `_Sources/`
- Remaining limitation: the page 18 and 19 product-specification tables are manual transcriptions from rendered PDF pages and still require human second-person review for production engineering use

**Assessment:** The plan should treat the cleaned package as the governing source bundle, not the archived raw `Process_DBM.md`. The facility-based organization still maps naturally to the two-root split, and the CSV-backed tables materially reduce prior data-extraction risk.

---

## Finding 6: Scale Difference Between Roots

| Metric | Deepcut | Comp & Liquids |
|--------|---------|----------------|
| Ledger rows | 5,961 | 319 |
| IN units | 4,965 | 267 |
| KTYs | 97 | 84 |
| Subjects | 432 | 272 |
| Open issues | 553 | 5 |

**Assessment:** Deepcut is roughly 18x larger by ledger unit count but has a comparable KTY/subject count. Deepcut's open-issue burden (553 items across TBD, deferred confirmation, future scope, assumptions) is substantial. Some of these open issues may intersect with cleaned-package content — particularly TBD items that the cleaned narrative and canonical CSV tables may now resolve.

---

## Finding 7: Existing Publication Artifacts Will Need Rebuild

Deepcut has `test_Section_Map.csv` and `test_Section_Map_Coverage.md` in `_Publication/DBM/_Planning/`. These were created before the remediation campaign and will be stale after SCOPE_CHANGE + downstream regeneration.

**Assessment:** The plan correctly sequences publication (Phase 8) after all remediation. Existing publication planning artifacts should be treated as superseded.

---

## Finding 8: Plan Structural Soundness

The plan's architecture is sound:
- Eight-phase sequence prevents premature publication
- Deepcut-first ordering leverages its mature scope-change history
- Shared-system policy (the cleaned source authority package governs, Deepcut normalizes first, escalation rule for conflicts) is well-defined
- Authority hierarchy is clear and non-contradictory
- Failure handling rules correctly escalate upstream
- Explicit acceptance criteria are testable

No structural defects found in the plan logic.

---

## Recommendations

1. **Record starting SCA pointers and source-bundle freeze details in Phase 1.** Both roots are at SCA-002. The next amendments will be SCA-003. Phase 1 deliverable should state this explicitly and identify the frozen cleaned package plus source PDF.

2. **Scope the open-issue intersection.** Deepcut's 553 open issues may overlap with cleaned-package content. Phase 3 `SCOPE_CHANGE` should be briefed on which open issues the cleaned narrative or canonical CSV tables potentially resolve.

3. **Phase 2 is the immediate blocking work.** The allocation matrix must be built from a full read of `Process_DBM_fixed.md`, supported by the canonical CSV tables and `metadata/tables.yaml`.

4. **Record manual-review status for pages 18 and 19.** If the manually transcribed specification tables have not yet had human second-person review, any matrix rows derived from them should be flagged for confirmation before publication.

## Execution Readiness

The plan is ready for execution after the source-authority amendments incorporated in this document set. Phase 1 (freeze authority inputs) and Phase 2 (build allocation matrix) are the immediate next steps. No workflow resequencing amendments are required; the required changes were source-model and execution-note updates.
