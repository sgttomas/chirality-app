# Datasheet
## DEL-009-02 | Building Permit Application & Approval

---

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-009-02 |
| Deliverable Name | Building Permit Application & Approval |
| Package | PKG-009 — Permitting & Regulatory Compliance |
| Package Description | Development permit, building permit, Safety Code permits, code compliance tracking, inspection coordination |
| Discipline | Project Manager |
| Type | Permit |
| Responsible Party | Project Manager |
| Accountable | Project Manager |
| Consulted | Building Authority, Design Team, Legal |
| Informed | Project Sponsor, Client (Camrose County) |
| Current Status | SEMANTIC_READY |
| Date Initialized | 2026-02-25 |
| SOW Reference | SOW-0006 (R-01, §3.3.2) |
| Objectives Supported | OBJ-001 (Regulatory-Compliant Delivery), OBJ-002 (Schedule) — ASSUMPTION: package-grouping heuristic applied; PKG-009 maps to OBJ-001 and OBJ-002 per decomposition §7 and Scope Ledger |

---

## Attributes

| Attribute | Value | Source |
|-----------|-------|--------|
| Permit type | Building Permit | R-01, §3.3.2; SSOW SOW-0006 |
| Issuing authority | Camrose County (building authority) | R-01, §3.3.2; _CONTEXT.md |
| Permit fee responsibility | Camrose County (Owner pays fees) | R-01, §3.3.1; SOW-0202 (OUT-of-scope for Proponent) |
| Application preparation responsibility | Proponent (Design-Builder / Project Manager) | R-01, §3.3.2; SOW-0006 |
| Predecessor deliverable | DEL-009-01 Development Permit Application & Approval | _DEPENDENCIES.md; _CONTEXT.md |
| Primary design input required | IFC drawings (all disciplines), stamped by P.Eng. licensed in Alberta | R-01, §3.3.2; SOW-0018 |
| Building code jurisdiction | Alberta (Province of Alberta) | R-01, §3.3.2; SOW-0008 |
| Building code applicability | All applicable Alberta building codes and regulations | R-01, §3.3.2; SOW-0008 |
| Safety code applicability | All applicable Alberta Safety Codes | R-01, §3.3.2; SOW-0009 |
| Specific Alberta code(s) | TBD — Requires identification of: (a) Alberta Safety Codes Act citation (RSA 2000, c S-1), (b) Alberta Building Code specific edition, and (c) Camrose County Land Use Bylaw number. Not cited with specific identifiers in accessible sources. **Proposed authority: Camrose County building authority; Alberta Municipal Affairs** (Lensing ref: A-001) |
| Application form(s) | TBD — Obtain Camrose County building permit application form(s) and submission checklist; record form identifiers here upon receipt. **Proposed authority: Camrose County building authority** (Lensing ref: B-001) |
| Inspection coordination requirement | County project representative must be present at all inspections; copies of all completed inspection reports provided to County | R-01, §3.3.2; SOW-0084, SOW-0085 |
| Construction commencement gate | Building permit approval is a hard gate before construction may begin | _DEPENDENCIES.md; decomposition §7, PKG-009 |
| Completion deadline (project) | December 31, 2026 | R-01, §3.1 |
| Processing timeline | TBD — Camrose County Building Authority processing SLAs not specified in accessible sources. Define a target or acceptable range (in weeks) so that schedule impact can be evaluated against the December 2026 deadline. **Proposed authority: Camrose County building authority; Project Manager** (Lensing ref: D-002) |
| Submission tracking reference | TBD — Define the tracking reference format or system for the building permit application submission (e.g., authority receipt number, internal tracking ID). Required at time of submission per Procedure Step 8. **Proposed authority: Project Manager** (Lensing ref: E-001) |

---

## Conditions

| Condition | Description | Source |
|-----------|-------------|--------|
| Predecessor gate | DEL-009-01 (Development Permit) must be approved before building permit application is submitted | _DEPENDENCIES.md; _CONTEXT.md |
| Design completeness | Complete, P.Eng.-stamped IFC drawings across all disciplines required before application can be assembled | R-01, §3.3.2; SOW-0018 |
| Code compliance | Building design must adhere to all applicable Alberta building codes, regulations, and Safety Codes | R-01, §3.3.2; SOW-0008, SOW-0009 |
| County fee payment | County is responsible for paying permit fees; Proponent excludes fee costs from proposal | R-01, §3.3.1; SOW-0202 |
| Inspection presence | County project representative must attend all inspections; reports copied to County | R-01, §3.3.2; SOW-0084, SOW-0085 |
| Permit conditions tracking | All conditions attached to the building permit must be tracked and incorporated into construction procedures | _CONTEXT.md (Success Criteria) |
| Development permit conditions | Conditions flowing from DEL-009-01 may constrain building permit application content | _DEPENDENCIES.md |
| Environmental / heritage overlays | TBD — Confirm whether environmental assessment, heritage overlay, or other municipal/provincial regulatory overlays apply to this site. For a new 13,000 sq ft structure on County land, additional regulatory checks (wetland, environmental, heritage) may apply. Not addressed in accessible sources. **Proposed authority: Camrose County planning department; Alberta Environment** (Lensing ref: F-002) |

---

## Construction (Artifact Description)

The deliverable is a **permit artifact set** comprising:

1. **Building Permit Application Package** — assembled documents submitted to the Camrose County building authority, including:
   - Completed application form(s) (sourced from building authority — TBD)
   - IFC drawings across all disciplines (architectural, structural, mechanical, electrical, civil, plumbing), stamped by P.Eng. licensed in Alberta (R-01, §3.3.2; SOW-0018)
   - Site plan / grading plan (R-01, §3.3.2; SOW-0015)
   - Supporting calculations and specifications as required by building authority (TBD — specific submission requirements defined by Camrose County building authority)
   - Development permit conditions documentation (from DEL-009-01)

2. **Issued Building Permit** — the approved permit document(s) issued by Camrose County, authorizing construction to commence.

3. **Permit Conditions Register** — record of all conditions, restrictions, and requirements attached to the issued building permit, incorporated into DEL-009-04 (Code Compliance Register & Inspection Log).

4. **Inspection Coordination Records** — documentation of inspection submissions and copies of completed inspection reports provided to the County (SOW-0084, SOW-0085). Note: detailed inspection tracking resides in DEL-009-04 (primary record location); copies retained in DEL-009-02 folder as reference.

---

## References

| Ref ID | Document | Relevance |
|--------|----------|-----------|
| R-01 | AB-2026-01424-WDMLRL RFP.pdf | §3.3.1 (County responsibilities / fee payment), §3.3.2 (Proponent scope — permitting, code compliance, inspections), §3.1 (completion deadline) |
| R-02 | AB-2026-01424-Addendum 1.pdf | Addendum No. 1 — bid security additions; no additional permitting content |
| DECOMP | WDMLRL_Decomposition_Claude.md | §3.B SOW-0006, §7 PKG-009 deliverable table, §8 Scope Ledger, §5 Objectives OBJ-001/OBJ-002 |
| _CONTEXT.md | DEL-009-02 _CONTEXT.md | Deliverable identity, scope, success criteria, stakeholders |
| _DEPENDENCIES.md | DEL-009-02 _DEPENDENCIES.md | Upstream/downstream dependency declarations |
