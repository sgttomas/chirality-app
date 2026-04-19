# SCA-004 Agent Prompt — Deepcut (04-25)

You are the orchestrating agent for SCA-004 on the Deepcut root. You adopt the SCOPE_CHANGE persona and execute the full 5-gate amendment protocol, then dispatch downstream Phase 6 work using Sonnet subagents.

---

## Bootstrap (read in this order before doing anything else)

1. `INIT.md`
2. `AGENTS.md`
3. `agents/AGENT_SCOPE_CHANGE.md` — adopt SCOPE_CHANGE persona
4. `plans/WEST_DOE_SCA004_PARALLEL_MECHANICAL_PACKAGE_STRUCTURE_PLAN.md` — the governing plan for this amendment
5. `plans/WEST_DOE_EXECUTION_MODEL.md` — agent topology and ownership boundaries
6. `plans/WEST_DOE_TWO_ROOT_DBM_REMEDIATION_AND_PUBLICATION_PLAN.md` — campaign context (skim for Phase 7/8 context only)
7. `agents/AGENT_AUDIT_DECOMP.md` — you will invoke this after Phase 6

After reading these, confirm to the human that you have loaded all governance documents and are ready to proceed.

---

## Your Root

- **Root:** `domain-test/domains/West_Doe_Deepcut_DBM`
- **Active _LATEST.md:** currently points to `SCA-003_2026-04-19_0900/`
- **Primary decomposition:** `_Decomposition/DeepCut_DOMAIN_DECOMP_FINAL_v4.md`
- **Decomposition naming:** `DeepCut_*_v4.*` files (main doc + named register CSVs + JSON telemetry)

## Source Authority for SCA-004

Read these two CSVs — they are the only source authority for this amendment:

- `_Sources/Packages_4-25_1.csv` (33 data rows)
- `_Sources/Line-Items_4-25_1.csv` (72 data rows)

Do not read or use any other source file as authority for SCA-004.

## What You Are Adding

One new Knowledge Type under CAT-007 Plant Design Requirements:

- **KTY ID:** `KTY-07-07_Mechanical-Package-Structure`
- **Name:** Mechanical Package Structure
- **Subjects:** exactly two:
  - `SUB-07-07-01_Package-Summary` (authority: Packages CSV)
  - `SUB-07-07-02_Package-Line-Items` (authority: Line-Items CSV)
- **Evidence model:** derived singleton — exactly two new HBK units:
  - `HBK-5978` → SUB-07-07-01
  - `HBK-5979` → SUB-07-07-02
- **Objective mapping:** `OBJ-004` (this is where all existing CAT-007 KTYs map in this root — "Maintain safe and controllable plant operation through isolation, pressure containment, flare and drain systems, shutdown logic, detection systems, and acid gas handling")
- **Schema:** `Design Data Reference`

## Expected Deltas

- UnitCount: 5690 → 5692
- KnowledgeTypeCount: 97 → 98 (active; 1 retired KTY-04-18 remains)
- SubjectCount: 432 → 434
- OpenIssueCount: unchanged (571)
- CAT-007: 6 → 7 KTYs, 15 → 17 subjects, 178 → 180 IN units
- StandaloneSubjectCount: unchanged (the new KTY has 2 explicit subjects)

## Write Scope (Gates 1-5)

Update at minimum these decomposition-local and _ScopeChange surfaces:

- `_Decomposition/DeepCut_DOMAIN_DECOMP_FINAL_v4.md`
- `_Decomposition/DeepCut_Category_Register_v4.csv`
- `_Decomposition/DeepCut_Coverage_Telemetry_v4.json`
- `_Decomposition/DeepCut_Domain_Ledger_v4.csv`
- `_Decomposition/DeepCut_Knowledge_Subject_Register_v4.csv`
- `_Decomposition/DeepCut_Knowledge_Type_Register_v4.csv`
- `_Decomposition/DeepCut_Node_Summary_v4.csv`
- `_Decomposition/DeepCut_Objective_Register_v4.csv`
- `_ScopeChange/_LATEST.md`
- New snapshot: `_ScopeChange/SCA-004_2026-04-19_<HHMM>/`

Do NOT edit these unless Gate 2 identifies a concrete duplicate-truth requirement:
- `DeepCut_Open_Issues_v4.csv`
- `DeepCut_Scope_Boundary_Register_v4.csv`
- `DeepCut_Standalone_Subject_Coverage_v4.csv`
- `DeepCut_Vocabulary_Map_v4.csv`
- `DeepCut_Publication_Manifest_v4.md`

## Do NOT Do During Gates 1-5

- Do not generate KTY-local `Scoping.md` or `KA-*.md`
- Do not create the `KTY-07-07_Mechanical-Package-Structure/` folder
- Do not edit existing KTY folders
- Do not edit `_Aggregation/`, hypergraph, or publication outputs
- Do not modify the source CSVs

## Important: Deepcut Decomposition File Format

The Deepcut root uses a different file naming convention from Comp & Liquids. The main document is `DeepCut_DOMAIN_DECOMP_FINAL_v4.md` (not `WEST_DOE_DOMAIN_DECOMPOSITION.md`). Register files are named `DeepCut_*_Register_v4.csv`. Telemetry is JSON (`DeepCut_Coverage_Telemetry_v4.json`), not CSV. Read the existing files before writing to understand the local format conventions.

The Deepcut main document embeds some data (like the Coverage & Telemetry table and the Open Issues table) as markdown within the document. When you update the main document, you must update both the embedded markdown tables AND the corresponding standalone CSV/JSON files.

## Gate Execution

Follow the AGENT_SCOPE_CHANGE 5-gate protocol exactly. At each gate, present your work to the human and wait for explicit approval before proceeding.

### Gate 1 — Change Intake
- Confirm the two source CSVs exist and match expected counts
- Confirm KTY-07-07 does not already exist
- Confirm _LATEST.md points to SCA-003
- Parse the amendment into atomic actions (ADD KTY, ADD 2 SUBs, ADD 2 HBKs, MODIFY OBJ-004, MODIFY CAT-007 counts)
- Capture Pre_Change_Coverage.json

### Gate 2 — Impact Assessment
- Enumerate every decomposition-local surface that needs updating
- Classify each as DIRECT_EDIT / RECOMPUTE / NO_CHANGE
- Identify downstream rerun obligations (domain-documents for the new KTY)

### Gate 3 — Amendment Text
- Draft exact changes to the main decomposition document
- Present as diff-style preview

### Gate 4 — Propagation Plan
- Produce Propagation_Plan.md and Amendment_Actions.csv
- **PAUSE HERE** — tell the human you are ready for the cross-root checkpoint. The human will compare your Gate 4 output with the Comp & Liquids agent's Gate 4 output to confirm naming, subject IDs, wording, and schema alignment before authorizing Gate 5.

### Gate 5 — Execute and Validate
- Apply all approved writes
- Capture Post_Change_Coverage.json
- Run post-change validation (all DOMAIN invariants)
- Write the 9-artifact snapshot
- Update _LATEST.md to SCA-004
- Produce RUN_SUMMARY.md with explicit handoff-state fields
- Update the telemetry JSON revision tag

## Phase 6 Downstream (After Gate 5 Acceptance)

After the human accepts Gate 5, execute this sequence:

1. **TASK + domain-documents for KTY-07-07** — dispatch as a Sonnet subagent. Brief it with:
   - KTY ID: KTY-07-07_Mechanical-Package-Structure
   - Folder path: `CAT-007_Plant Design Requirements/1_Working/KTY-07-07_Mechanical-Package-Structure/`
   - The two source CSVs as input
   - Schema: Design Data Reference
   - Two subjects only
   - Read `skills/domain-documents/SKILL.md` for skill contract

2. **TASK + kty-metadata-align for KTY-07-07** — you do this yourself or dispatch Sonnet. Verify _CONTEXT.md, _STATUS.md, _REFERENCES.md are consistent with decomposition.

3. **AUDIT_DECOMP** — you do this yourself (full-root scope). Follow `agents/AGENT_AUDIT_DECOMP.md`.

4. **DOMAIN_HYPERGRAPH** — you do this yourself (full-root scope). Note: the prior hypergraph run had 36 pre-existing KA-naming blockers. Expect these to persist; they are not caused by SCA-004.

5. **Terminology check** — verify no naming conflicts introduced.

6. Report final status to the human.

## Subagent Rules

- Sonnet subagents handle KTY-local tasks only (domain-documents, metadata-align)
- You (Opus) handle all decomposition-truth writes, AUDIT_DECOMP, DOMAIN_HYPERGRAPH, and full-root tasks
- One KTY per Sonnet subagent (in this case there is only one new KTY)
- Sonnet subagents must not write to `_Decomposition/` or `_ScopeChange/`

## Source Interpretation Rules (from the plan — follow exactly)

- Do not infer package hierarchy beyond what the CSVs explicitly state
- Do not normalize or rename package names
- Do not deduplicate repeated equipment tags
- Treat Building/Skid/Train/Unit as source row content, not a separate modeling layer
- If the package summary CSV and line-item CSV disagree on totals, record that as an explicit finding

## Acceptance Condition

This root's SCA-004 is complete when:
- Gate 5 snapshot exists with all 9 artifacts
- _LATEST.md points to SCA-004
- KTY-07-07 folder exists with generated Scoping.md and KA files
- AUDIT_DECOMP passes
- DOMAIN_HYPERGRAPH regenerated (pre-existing blockers accepted)
- No blocking findings remain
