# Decision Log

**Snapshot ID:** EST_PKG31_DRAFT_2026-01-29_1030

**Package:** PKG-31 Documentation & Deliverables

**Date:** 2026-01-29

---

## Purpose

This log records all decisions made during the estimating process where ambiguity, missing information, or multiple valid approaches required a choice. Each decision is traceable and can be overridden in future estimate runs.

---

## Decision Entries

### D-001: Workspace Paths

**Decision:** Using default project paths per agent instruction defaults.

**Trigger:** Agent initialization; no explicit paths provided by human.

**Evidence:** Agent instructions default paths table.

**Impacted WBS/CBS:** All (entire estimate).

**Estimate Impact:** None (procedural).

**How to Override:** Provide explicit paths in conversation or update agent defaults.

---

### D-002: Estimate Label

**Decision:** Updated estimate_label from PKG25_DRAFT to PKG31_DRAFT for this estimate.

**Trigger:** Config file contained previous package label (PKG25_DRAFT).

**Evidence:** `_CONFIG.md` parameter.

**Impacted WBS/CBS:** All (estimate identity).

**Estimate Impact:** None (labeling only).

**How to Override:** Update estimate_label in `_CONFIG.md` before next run.

---

### D-003: Deliverable Folder Status

**Decision:** Deliverable folders not yet created. Proceeding with decomposition-based estimating using parametric methods.

**Trigger:** Checked for PKG-31 deliverable folders under `execution/PKG-31_Documentation_Deliverables/1_Working/` but none exist yet.

**Evidence:** File system check returned no folders.

**Impacted WBS/CBS:** All (entire estimate methodology).

**Estimate Impact:** HIGH - Entire estimate is parametric/allowance because no deliverable content (Datasheet, Specification, Guidance, Procedure) exists to extract quantities from.

**How to Override:** Run ORCHESTRATOR → Scaffold → Initialize Drafts to create deliverable folders and content, then re-run estimating pipeline.

---

### D-004: Pricing Sources

**Decision:** No project-specific rate tables or quotes found for documentation services. Using parametric methods based on typical drawing production rates and document management effort.

**Trigger:** Searched `_RateTables/` and deliverable `_REFERENCES.md` files; no documentation-specific rates or quotes found.

**Evidence:** File system search in `_Estimates/_RateTables/` returned no applicable rate tables for documentation services.

**Impacted WBS/CBS:** All CBS buckets (E, PM, MAT).

**Estimate Impact:** HIGH - 100% parametric/allowance pricing reduces confidence to MEDIUM-LOW.

**How to Override:** Provide rate table in `_Estimates/_RateTables/` with columns: Service, Unit, Rate_CAD, Source. Or provide vendor quotes for printing/binding services.

---

### D-005: CBS Mapping

**Decision:** Documentation deliverables split between Engineering (drafting/technical writing) and Project Management (coordination/compilation/registers).

**Trigger:** PKG-31 contains both technical documentation (drawings, manuals) and administrative documentation (registers, certificates).

**Evidence:** Decomposition deliverable descriptions (DEL-31.01 through DEL-31.11).

**Impacted WBS/CBS:**
- E: DEL-31.01, DEL-31.02, DEL-31.03, DEL-31.04
- PM: DEL-31.05, DEL-31.06, DEL-31.07, DEL-31.08, DEL-31.09, DEL-31.10, DEL-31.11
- MAT: Printing, binding, software (not deliverable-specific)

**Estimate Impact:** MEDIUM - CBS split affects contingency application (E and PM at 10%, MAT at 25%).

**How to Override:** If project prefers different CBS allocation (e.g., all under PM or separate "Documentation" CBS code), update WBS→CBS mapping rules and re-run.

---

### D-006: Drawing Production Rates

**Decision:** Drawing production rates estimated at:
- Record drawings: 12 hours/sheet average (multi-discipline coordination)
- As-built incorporation: +8 hours/sheet additional (field markup review, updates, QA)

**Trigger:** No project-specific production rates available; needed to price DEL-31.01 and DEL-31.02.

**Evidence:** Parametric typical rates for EPC projects with multi-discipline coordination and VFPA standards compliance.

**Impacted WBS/CBS:** E (Engineering), specifically line items L001 and L002.

**Estimate Impact:** MEDIUM-HIGH - Drawing production is largest cost component (~$75k base). Rate variance of ±25% would impact estimate by ±$19k.

**How to Override:** If project has historical data or agreed production rates, provide rate table with: DrawingType, Discipline, Hours_per_Sheet, Complexity_Factor. Re-run estimate.

---

### D-007: Manual Development Rates

**Decision:** Manual development rates estimated at:
- Operation manuals: 80 hours/system average
- Maintenance manuals: 16 hours/equipment average (compilation from vendor docs + project-specific additions)

**Trigger:** No project-specific rates available; needed to price DEL-31.03 and DEL-31.04.

**Evidence:** Parametric typical rates for technical writing on EPC projects.

**Impacted WBS/CBS:** E (Engineering), specifically line items L003 and L004.

**Estimate Impact:** HIGH - Manual development is largest cost component (~$396k base). Rate variance of ±30% would impact estimate by ±$119k.

**How to Override:** Provide rate table with: DocumentType (OpManual/MaintManual), Hours_per_Unit, Complexity. Or provide historical data from similar projects.

---

### D-008: PM Coordination Effort

**Decision:** PM coordination effort estimated at:
- Asset hierarchy: 120 hours (database structure + population)
- Registers: 40 hours each (warranties register, H&S file)
- Certificate compilation: 60 hours (collection, organization, verification)

**Trigger:** No project-specific effort estimates available; needed to price DEL-31.05 through DEL-31.11.

**Evidence:** Parametric typical effort for document control and compilation on EPC projects of this scale.

**Impacted WBS/CBS:** PM (Project Management), line items L005 through L011.

**Estimate Impact:** MEDIUM - PM coordination is ~$161k base (21% of total). Effort variance of ±30% would impact estimate by ±$48k.

**How to Override:** If Employer provides detailed asset hierarchy requirements or specifies register formats, refine effort estimates based on actual complexity.

---

### D-009: Document Control & Submittal

**Decision:** Document control and submittal effort estimated at:
- Ongoing document control: 400 hours (throughout project)
- Final submittal preparation: 80 hours

**Trigger:** No project-specific effort estimates available; needed to price ongoing PM effort (line items L017 and L018).

**Evidence:** Parametric typical effort for document control on 24-30 month EPC project with ~275 drawings and 11 deliverables.

**Impacted WBS/CBS:** PM (Project Management), line items L017 and L018.

**Estimate Impact:** MEDIUM - $63k base. Effort variance of ±25% would impact estimate by ±$16k.

**How to Override:** If project schedule is confirmed (different from 24-30 month assumption), adjust document control hours proportionally. Provide schedule in config as: project_duration_months.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Decisions | 9 |
| Procedural Decisions | 2 (D-001, D-002) |
| Methodology Decisions | 2 (D-003, D-004) |
| Technical Decisions | 5 (D-005 through D-009) |
| High Impact Decisions | 4 (D-003, D-004, D-007, D-008) |

---

**High-Impact Decisions Requiring Validation:**

1. **D-003:** Proceeding without deliverable folders (affects entire estimate basis)
2. **D-004:** Using parametric pricing for all items (no quotes/rates available)
3. **D-007:** Manual development rates (largest cost component)
4. **D-008:** PM coordination effort (second-largest cost component)

**Recommended Actions:**
- Initialize deliverable folders and re-run estimate once engineering content is available
- Obtain vendor quotes for printing/binding services
- Validate drawing count estimate at 30% design milestone
- Validate equipment and system counts from engineering deliverables (PKG-27)

---

**Document Control:**
- **Snapshot ID:** EST_PKG31_DRAFT_2026-01-29_1030
- **Author:** ESTIMATING Agent
- **Date:** 2026-01-29 10:30
- **Entries:** D-001 through D-009
