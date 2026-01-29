# INIT — Session Orientation

This document orients the agent to the **Estimate Aggregation Pipeline** for the Canola Oil Transload Facility project.

---

## Your Role: AGGREGATION Agent (Estimate Collation)

You are running an **incremental package-by-package estimate collation pipeline** that combines estimate artifacts from individual packages into cumulative project-level totals.

---

## Quick Start (First-Time Setup)

### Step 0: Orient to the Project (5 minutes)

Read these files in order:
1. `/Users/ryan/ai-env/projects/chirality-app/README.md` — Project overview and filesystem paths
2. `/Users/ryan/ai-env/projects/chirality-app/AGENTS.md` — Agent framework and conventions
3. `/Users/ryan/ai-env/projects/chirality-app/agents/AGENT_AGGREGATION.md` — Your specific instructions and protocol

**Key Takeaway:** You are collating estimate snapshots (Detail.csv, BOE.md, Assumptions, Risks) from package-level estimates into cumulative project files. The deliverable-level UID rule must avoid collisions for `WBS_DeliverableID = N/A`; prefer package-namespaced UIDs.

### Step 1: Check Pipeline Status

Check which packages have been completed:
- Read: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/_LATEST.md`
- Read: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/_Pipelines/EstimateCollation_PhaseByPackage/_LATEST.md`

This tells you:
- Which packages are already collated
- What the cumulative total is so far
- Which package to process next

---

## Running the Pipeline (Per-Package Workflow)

The user will tell you which package to process (e.g., "PKG-03"). Follow this workflow:

### Phase 1: Update the Brief (1 minute)

Update `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/INIT.md` with the current package details:

```markdown
# Aggregation Brief — PKG-XX [Package Name]

## Purpose
`Estimate_Collation`

## Pipeline ID
`EstimateCollation_PhaseByPackage`

## Scope
This run collates estimate artifacts for **PKG-XX [Package Name]** only.

## Where to Look
- Estimate snapshot: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/EST_PKGXX_DRAFT_2026-01-28_HHMM/`

## Output Labeling Preferences
- Package tag: `PKG-XX`
- Estimate label: `EST_PKGXX_DRAFT_2026-01-28_HHMM`

## Notes
- This is the [Nth] package in the incremental collation pipeline
- Prior packages completed: [list prior snapshot IDs]
- Incremental pipeline will incorporate all prior package data into cumulative totals
- Report back when PKG-XX aggregation is complete
```

### Phase 2: Read Source Estimate Artifacts (2-3 minutes)

For the target package (e.g., PKG-03), read these files from the estimate snapshot:

**Location Pattern:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/EST_PKGXX_DRAFT_YYYY-MM-DD_HHMM/`

**Required Reads:**
1. `Detail.csv` — Line items with Qty, Unit, UnitRate (this is the canonical cost data)
2. `Summary.md` — Package total, CBS breakdown, key drivers
3. `BOE.md` (first 100 lines) — Basis of estimate overview
4. `Assumptions_Log.md` — All assumptions
5. `Risk_Register.md` — All risks
6. `Decision_Log.md` — All decisions

**Optional (if present):** QA or source index artifacts (e.g., `QA_Report.md`, `Source_Index.md`) are informational and do not affect aggregation.

**Common gap:** `Risk_Register.md` may be missing in some packages; log as WARNINGS in QA_Report and Coverage.csv.

**What to capture:**
- Number of line items
- Base estimate and contingency amounts
- Total estimate
- Number of assumptions, risks, decisions
- Deliverables covered
- Major cost drivers

### Phase 3: Create Aggregation Snapshot (5-10 minutes)

**3.1 Create Snapshot Folder**

```bash
# Get timestamp
date +"%Y-%m-%d_%H%M"  # e.g., 2026-01-29_0128

# Create folder structure
mkdir -p "/path/to/_Aggregation/AGG_Estimate_Collation_YYYY-MM-DD_HHMM/{Extracts,Aggregated/Estimate}"
```

**3.2 Copy Raw Extracts (Audit Trail)**

```bash
# Copy current package extracts
cp /path/to/_Estimates/EST_PKGXX_*/\{Detail.csv,BOE.md,Assumptions_Log.md,Risk_Register.md,Decision_Log.md\} Extracts/

# Rename with package prefix
cd Extracts/
for f in Detail.csv BOE.md Assumptions_Log.md Risk_Register.md Decision_Log.md; do
  mv "$f" "PKG-XX_$f"
done

# Copy prior package extracts (for incremental pipeline)
cp /path/to/prior_snapshot/Extracts/PKG-* ./
```

**3.3 Create Aggregated Data Files**

Create these files in `Aggregated/Estimate/`:

1. **Project_Detail.csv** — Combine all packages' line items with UID namespacing
   - Format: `LineUID,FromPackageID,FromDeliverableID,LineID,CBS,WBS_PackageID,WBS_DeliverableID,Description,Qty,Unit,UnitRate,Amount,Currency,Method,SourceRef,Confidence,Notes`
   - UID pattern: `PKG-XX::L001` (LineUID must be package-namespaced; do not use DeliverableID-based UIDs)

2. **Project_Assumptions.csv** — Combine all assumptions
   - UID pattern: `PKG-XX::A-001`

3. **Project_Risks.csv** — Combine all risks
   - UID pattern: `PKG-XX::R-001`

4. **Project_Summary_CBS.csv** — Cumulative totals by CBS category
   - Sum across all packages: E, PM, P, MAT, CD, CI, COM

5. **BOE_Index.csv** — One row per package with snapshot ID and totals

6. **Coverage.csv** — Package status (COMPLETE/etc.) and line counts

7. **Conflicts.csv** — Empty (header only) unless conflicts found

8. **Duplicates.csv** — Empty (header only) unless duplicates found

**3.4 Create Summary Documents**

Create these markdown files in the snapshot root:

1. **Brief.md** — Verbatim brief + normalized brief from INIT.md

2. **Plan.md** — What was done, statistics table showing cumulative totals across all packages

3. **RUN_SUMMARY.md** — Run status (OK/WARNINGS/FAILED), cumulative statistics, financial summary

4. **QA_Report.md** — Validation results, schema checks, data quality metrics

5. **Aggregated/Estimate/BOE_Collection.md** — Consolidated basis of estimate from all packages

6. **Decision_Log.md** — Copy from prior snapshot + append current package decisions

7. **Assumptions_Log.md** — Copy from prior snapshot + append current package assumptions

8. **Source_Index.csv** — List all source artifact paths processed

### Phase 4: Update Pointers (1 minute)

Update these pointer files to reference the new snapshot:

1. `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/_LATEST.md`
   - Update snapshot ID, path, date
   - Update cumulative totals
   - Update pipeline progress

2. `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/_Pipelines/EstimateCollation_PhaseByPackage/_LATEST.md`
   - Update snapshot ID
   - List completed packages and their totals
   - Update cumulative total

### Phase 5: Report Completion (1 minute)

Report to the user with:
- Snapshot ID and location
- This package summary (deliverables, line items, estimate total)
- Cumulative project totals (packages, deliverables, line items, total estimate)
- Key findings for this package (major cost drivers, confidence, risks)
- Cumulative CBS breakdown table
- Pipeline progress (X of ~36 packages complete)
- Ready message asking for next assignment

---

## Key Patterns and Conventions

### File Naming
- Snapshot folders: `AGG_Estimate_Collation_YYYY-MM-DD_HHMM`
- Extract files: `PKG-XX_[ArtifactName]`
- UID namespacing: `PKG-XX::[ID]` (prevents conflicts in cumulative files)

### Incremental Pipeline Behavior
- Each snapshot incorporates ALL prior packages (not just the current one)
- Copy prior extracts to new snapshot for complete audit trail
- Cumulative CSV files combine data from all packages processed so far
- No need to re-read prior estimates; use prior snapshot's aggregated files as base

### Efficiency Tips
1. **Parallel reads**: Read Detail.csv, Summary.md, BOE.md, Assumptions, Risks, Decisions in parallel when possible
2. **Bash for file ops**: Use bash for copying extracts, creating CSVs from heredocs
3. **Template reuse**: Copy/adapt files from prior snapshot rather than recreating from scratch
4. **Focus on essentials**: Brief, Plan, RUN_SUMMARY, BOE_Collection, and CSV files are critical; others can be streamlined

### Data Validation Checklist
- [ ] All line items have Qty, Unit, UnitRate populated
- [ ] Financial totals match (package base + contingency = total)
- [ ] Cumulative totals = sum of all packages
- [ ] All UIDs are unique (no duplicates across packages; ensure package prefix is applied)
- [ ] Schema validation passed (Detail.csv has required columns)
- [ ] No conflicts or duplicates detected

---

## Common Issues and Solutions

**Issue:** Estimate snapshot not found
- **Solution:** Check `_CONFIG.md` and `_LATEST.md` in _Estimates/ for correct snapshot ID

**Issue:** Line items missing Qty/Unit/UnitRate
- **Solution:** Mark as SCHEMA_INVALID in Coverage.csv, exclude from totals, flag in QA_Report

**Issue:** Prior snapshot not accessible
- **Solution:** Each snapshot should be self-contained; if prior unavailable, start fresh with current package only

**Issue:** UID collision
- **Solution:** Use package prefix (PKG-XX::) for all UIDs to ensure uniqueness (do not rely on WBS_DeliverableID where it may be `N/A`)

---

## Implementation Notes (Recent Updates)

- Use `python3` for aggregation scripts; `python` may not be available in the environment.
- Risk registers may be missing in some estimate snapshots; log as WARNINGS in QA_Report and Coverage.csv.

---

## Workflow Orientation Rules

- **No re-reading past deliverables:** Prior packages are already collated. Only read the CURRENT package estimate.
- **Incremental accumulation:** Copy prior snapshot's aggregated data and ADD current package to it.
- **Focus on aggregation, not estimation:** You are NOT creating estimates. You are collecting and organizing existing estimate data.
- **One package at a time:** Complete each package fully before moving to the next.
- **Report and await:** After each package, report completion and wait for user to assign the next package.

---

## Success Criteria

A successful aggregation run produces:
1. ✓ New timestamped snapshot with all required files
2. ✓ Cumulative data combining all packages processed to date
3. ✓ RUN_STATUS: OK (no errors or missing artifacts)
4. ✓ Updated pointer files
5. ✓ Complete audit trail (raw extracts preserved)
6. ✓ Clear completion report to user

---

## Next Package Assignment

When the user says "PKG-XX", immediately:
1. Update INIT.md brief (Phase 1)
2. Read estimate artifacts (Phase 2)
3. Create aggregation snapshot (Phase 3)
4. Update pointers (Phase 4)
5. Report completion (Phase 5)

**Current Pipeline Status:**
- Check `_LATEST.md` to see which packages are complete
- Next package will be assigned by the user
- Progress through packages sequentially (PKG-00 → PKG-01 → PKG-02 → ...)

---

**Pipeline Type:** EstimateCollation_PhaseByPackage (Incremental)
**Output Root:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/`
**Estimate Source Root:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`

---

*This INIT.md was updated based on efficient workflow patterns learned during PKG-00, PKG-01, and PKG-02 aggregation runs.*
