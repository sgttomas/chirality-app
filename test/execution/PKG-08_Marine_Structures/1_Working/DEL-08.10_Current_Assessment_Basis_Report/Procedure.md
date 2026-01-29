# Procedure: DEL-08.10 Current Assessment Basis Report

## Purpose

Define repeatable workflow for producing **Current Assessment Basis Report** for design verification and approvals.

**Deliverable intent:** Documents analysis and results for current assessment basis report required for design verification and approvals. *(Source: Decomposition line 290)*

---

## Prerequisites

**Dependency mode:** NOT_TRACKED

**Required Inputs (TBD):**

| Input | Source | Status |
|---|---|---|
| Site location | Project basis | Known (Fraser Surrey Terminal) |
| Current data sources | CHS, Port, studies | **TBD** |
| ER current requirements | ER | **TBD** |
| Design return period | ER/standards | **TBD** |

---

## Procedure Steps

### Step 1: Establish Requirements
1. Extract ER clauses for current assessment
2. Determine design return period
3. Identify downstream uses (mooring, structural, debris)
4. Define current parameters needed

**Outputs:** ER register, return period, use case list, parameter checklist

---

### Step 2: Gather Data
1. Search for site measurements (ADCP, current meter)
2. Obtain CHS tide/current predictions
3. Search for historical studies/reports
4. Identify numerical model data
5. Assess data quality and coverage

**Outputs:** Data source list, data quality assessment

---

### Step 3: Analyze Data
1. Characterize tidal current (flood/ebb)
2. Characterize river flow (normal/freshet)
3. Combine tidal and river components
4. Perform extreme value analysis if data supports
5. Determine design current values

**Outputs:** Tidal summary, river flow summary, combined analysis, design current table

---

### Step 4: Document Methodology
1. Document assessment approach
2. Document data processing methods
3. Document statistical methods (if used)
4. List assumptions with rationale
5. Document limitations and applicability

**Outputs:** Methodology section, assumptions register, limitations statement

---

### Step 5: Prepare Report
1. Draft executive summary
2. Compile data sources section
3. Compile methodology section
4. Compile results summary with design current table
5. Include data source register

**Outputs:** Draft report

---

### Step 6: QA/QC Review
1. Submit for independent check
2. Address comments
3. Obtain sign-off

**Outputs:** Review record, updated report

---

### Step 7: Issue and Control
1. Finalize per document control
2. Issue with transmittal
3. Update `_STATUS.md`
4. Archive

**Outputs:** Final report, transmittal

---

## Requirement Coverage Matrix

| Req ID | Step(s) | Evidence |
|---|---|---|
| R-001 | 3, 4, 5 | Complete report |
| R-002 | 1, 3, 5 | Current parameters |
| R-003 | 2, 5 | Data sources with quality assessment |
| R-004 | 4, 5 | Methodology with assumptions/limitations |
| R-005 | 1 | ER compliance |
| R-006 | 6, 7 | QA/QC and control |

---

## Verification Checkpoints

| Checkpoint | Hold Point |
|---|---|
| After Step 2: Data sources identified | No |
| After Step 3: Design currents derived | No |
| After Step 5: Report complete | No |
| After Step 6: QA review complete | **Yes** |
| After Step 7: Controlled issue | No |

---

## Sources

- Decomposition line 290
- `Specification.md` R-001 through R-006
