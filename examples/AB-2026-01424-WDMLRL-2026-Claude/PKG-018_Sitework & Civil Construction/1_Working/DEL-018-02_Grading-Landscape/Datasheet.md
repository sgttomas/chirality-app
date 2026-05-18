# Datasheet — DEL-018-02: Site Grading & Landscaping

---

## Identification

| Field | Value |
|-------|-------|
| **Deliverable ID** | DEL-018-02 |
| **Title** | Site Grading & Landscaping |
| **Package** | PKG-018 — Sitework & Civil Construction |
| **Type** | Construction |
| **Responsible Party** | General Contractor |
| **SOW Reference** | SOW-0076 |
| **Objective** | OBJ-001 |
| **Contract Form** | CCDC 14–2013 Design-Build Stipulated Price |
| **Owner** | Camrose County |
| **Project** | 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition |
| **Location** | SW 14–44–21–W4, near Ferintosh, Alberta |
| **Completion Deadline** | December 31, 2026 |

Source: `_CONTEXT.md`; Decomposition `WDMLRL_Decomposition_Claude.md` §PKG-018; RFP `AB-2026-01424-WDMLRL_RFP.pdf` §1.0, §3.1

---

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| **Work Type** | Site grading and landscaping | `_CONTEXT.md` |
| **Scope Statement** | Grade and landscape the proposed lot | RFP §3.3.2; Decomposition SOW-0076 |
| **Grading Requirement — Drainage** | Grading design shall account for positive site drainage and future storm events | RFP §3.4; Decomposition SOW-0020 |
| **Grading Requirement — Offsite Drainage** | Grading design shall not alter drainage conditions of neighboring properties | RFP §3.4; Decomposition SOW-0021 |
| **Grading Area** | Proposed lot expansion area (construction zone shown in site maps) | Appendix C — Site Maps |
| **Design Basis** | Issued for Construction (IFC) civil grading plan with drainage features and components | RFP §3.3.2; Decomposition SOW-0015 |
| **Aggregate Supply** | Supplied by County (OUT of Proponent scope) | Decomposition PKG-018 exclusions; Appendix B note: "Landfill to supply gravel" |
| **Bulk Cut/Fill** | Performed by County forces (OUT of Proponent scope) | RFP §3.3.1; Decomposition PKG-018 exclusions |
| **Brushing/Clearing** | Performed by County forces (OUT of Proponent scope) | RFP §3.3.1; Decomposition PKG-018 exclusions |
| **Grading Design Authority** | Civil Engineer (PKG-005); grading plan must be P.Eng.-stamped | RFP §3.3.2; Decomposition PKG-005 |
| **Landscape Design Authority** | Landscape Architect (PKG-007) | Decomposition PKG-007 |
| **Compaction** | Required (ASSUMPTION: standard construction compaction testing applies for graded surfaces; specific standard TBD pending civil design) | `_CONTEXT.md`; `MEMORY.md` |
| **Specific Grading Elevations** | TBD (to be established by civil grading plan DEL-005-02). **Note:** These are essential execution data — grading cannot proceed without design elevations, slope percentages, and drainage invert elevations from the civil engineer (PKG-005). Populate when DEL-005-02 is issued. [Lensing: B-001] | Decomposition DEL-005-02 |
| **Grading Slopes** | TBD (to be established by civil grading plan DEL-005-02). See Grading Elevations note above. [Lensing: B-001] | Decomposition DEL-005-02 |
| **Landscape Scope** | TBD (to be established by landscape plans DEL-007-02, DEL-007-03). **Note:** Species, areas, quantities, and materials are required for landscape execution planning. Populate when DEL-007-02 and DEL-007-03 are issued by landscape architect (PKG-007). [Lensing: B-002] | Decomposition DEL-007-02, DEL-007-03 |

---

## Conditions

| Condition | Value | Source |
|-----------|-------|--------|
| **Prerequisite — Upstream** | DEL-018-01 (Topsoil Stripping) must be complete before grading commences | `_DEPENDENCIES.md` |
| **Prerequisite — Design** | Civil grading plan (DEL-005-02) must be finalized and issued for construction | `_DEPENDENCIES.md`; Decomposition SOW-0015 |
| **Prerequisite — Survey** | Site survey with benchmark established (SURVEY-001) | `_DEPENDENCIES.md` |
| **On Critical Path** | YES — second-order critical path; upstream to DEL-018-03, 04, 05, 06 | `_DEPENDENCIES.md` |
| **Climate/Site** | Rural landfill site, Central Alberta; exposed prairie/landfill environment | Appendix C — Site Maps; RFP §1.0 |
| **Site Context** | Active landfill facility; existing Old North Shop adjacent to expansion area | Appendix C — Site Maps |
| **Guarantee Period** | 2 years post Construction Completion Certificate (CCC) | RFP §2.10 |

---

## Construction

| Element | Description | Source |
|---------|-------------|--------|
| **Work Sequence** | (1) Confirm graded surface is clear of topsoil per DEL-018-01; (2) Grade to IFC civil plan elevations; (3) Establish positive drainage per design; (4) Compact graded surfaces; (5) Execute landscaping per landscape plan | ASSUMPTION — inferred from construction sequence logic and `_CONTEXT.md` |
| **Downstream Work Enabled** | Gravel Driving Surface (DEL-018-03); Cement & Gravel Pads (DEL-018-04); Wash Bay Drainage (DEL-018-05); Utility Tie-Ins (DEL-018-06) | `_DEPENDENCIES.md` |
| **Cross-Package Dependency** | Provides site foundation for crane equipment installation (PKG-016) and building operations (PKG-017) | `_DEPENDENCIES.md` |
| **IFC Drawing Compliance** | All construction must conform to IFC civil and landscape drawings | RFP §3.3.2 |
| **Inspection** | County project representative must be present at all inspections; copies of all inspection reports to be provided to County | RFP §3.3.2; Decomposition SOW-0084, SOW-0085 |
| **Compaction Testing** | Required for quality assurance (specific standard TBD) | `MEMORY.md`; ASSUMPTION |
| **As-Built Survey Responsibility** | DEL-008-04 provides the formal as-built survey record. DEL-018-02 is responsible for field-level grade checks during execution (e.g., grade rod measurements, level checks against IFC plan) to confirm work is proceeding to design. The formal survey (DEL-008-04) serves as the definitive verification instrument at completion. [Lensing: E-001] | Decomposition DEL-008-04; Specification §Verification REQ-01, REQ-04 |

---

## References

| Ref | Title | Role |
|-----|-------|------|
| R-01 | AB-2026-01424-WDMLRL_RFP.pdf §3.3.2, §3.4 | Primary scope and design requirements source |
| R-07 | AB-2026-01424-Appendix_C_-_Site_Maps.pdf | Site location and expansion area context |
| Decomposition | WDMLRL_Decomposition_Claude.md — §PKG-018, SOW-0076, SOW-0020, SOW-0021, DEL-005-02, DEL-007-02/03 | Scope decomposition and dependency mapping |
| App B | AB-2026-01424-Appendix_B__Shop_.pdf | Site layout context; aggregate supply note |
| `_CONTEXT.md` | DEL-018-02 Context File | Deliverable identity and scope |
| `_DEPENDENCIES.md` | DEL-018-02 Dependencies File | Upstream/downstream constraint list |
| `MEMORY.md` | DEL-018-02 Memory File | Agent operational notes |
