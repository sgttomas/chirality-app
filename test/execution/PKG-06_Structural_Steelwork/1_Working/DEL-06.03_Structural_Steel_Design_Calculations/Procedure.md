# Procedure: DEL-06.03 Structural Steel Design Calculations

## Purpose

This procedure defines the process for producing and managing the **Structural Steel Design Calculations** within **PKG-06 Structural Steelwork**.

The deliverable provides the engineering basis and sizing/verification calculations for structural steel (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250).

**Deliverable type:** Calculation  
**Responsible party:** D&B Contractor

## Prerequisites

**Dependencies:**
- See `_DEPENDENCIES.md` — **NOT_TRACKED**: dependencies coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`).
- Confirm availability of design basis inputs needed for calculation (loads, criteria, exposure category) (Dependencies: NOT_TRACKED).

**Reference materials:**
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-06 / DEL-06.03 definition) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:238-252).
- Employer's Requirements — relevant clauses **TBD** (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).
- Document control / QA expectations (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

**Personnel requirements:**
- Qualified structural engineer and checker per project QA/QC expectations (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

## Steps

1. **Define scope and artifacts** — Identify required calculation deliverables and create calculation index (Platform structural calculations, Pipe rack calculations, Connection design calculations) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250; Datasheet.md: Attributes; Specification.md: Scope, Calculation Package Structure; Guidance.md: Considerations).
2. **Assemble inputs** — Collect geometry, material properties, support conditions, equipment/piping loads, and criteria; create Input Register and Interface Assumptions Register (Dependencies: NOT_TRACKED; Specification.md: Calculation Package Structure; Guidance.md: Principles, Examples).
3. **Select methodology** — Choose analysis approach and tools; record software/tool versions and key settings (**TBD**) (ASSUMPTION; Datasheet.md: Attributes; Specification.md: Cross-Reference Matrix; Guidance.md: Trade-offs).
4. **Execute analysis** — Perform calculations for governing load cases and combinations; create Load Case and Combination List (**TBD** list until ER criteria extracted; Datasheet.md: Attributes; Specification.md: Calculation Package Structure; Guidance.md: Examples).
5. **Document results** — Record governing members/connections, deflections/limits checks, and any required design notes for drawings (DEL-06.01) or specification clauses (DEL-06.02); create Results Summary with drawing notes implications.
   - Populate the "Calculation Package Structure (Minimum)" items in `Specification.md` or explicitly mark TBD (Specification.md: Calculation Package Structure, Cross-Reference Matrix; Guidance.md: Examples).
6. **Independent check** — Checker verifies critical results and reviews assumptions; create Independent Check Record (checker name/date, scope of check) (Procedure requires explicit check record; **TBD** format; Specification.md: Calculation Package Structure, Quality Requirements, Cross-Reference Matrix).
7. **Issue preparation** — Apply numbering/revisioning and compile package (native + PDF, model files as required) for CHECKING as required; ensure `Datasheet.md` attributes match calculation number and revision (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Specification.md: Documentation).

## Verification

- Scope completeness: calculation index covers all three anticipated artifacts (Platform structural calculations, Pipe rack calculations, Connection design calculations) (Specification.md: Cross-Reference Matrix; Datasheet.md: Attributes; Step 1).
- Inputs and assumptions recorded: Input Register and Interface Assumptions Register complete (**TBD** format; Specification.md: Calculation Package Structure, Cross-Reference Matrix; Guidance.md: Principles, Examples; Steps 2).
- Analysis methodology: software/tool versions and key settings recorded (**TBD**; Specification.md: Cross-Reference Matrix; Datasheet.md: Attributes; Step 3).
- Load cases and combinations: Load Case and Combination List created (**TBD**; Specification.md: Calculation Package Structure, Cross-Reference Matrix; Datasheet.md: Attributes; Step 4).
- Results documented: Results Summary with governing members, deflections, and drawing notes implications created (Specification.md: Calculation Package Structure, Cross-Reference Matrix; Guidance.md: Examples; Step 5).
- Independent check completed and recorded: Independent Check Record present (**TBD** format; Specification.md: Calculation Package Structure, Cross-Reference Matrix; Step 6).
- Key assumptions/inputs reconciled with drawings (DEL-06.01), specification (DEL-06.02), data sheets (DEL-06.04) (Dependencies: NOT_TRACKED; Specification.md: Cross-Document Notes; Guidance.md: Cross-Document Notes; Steps 2, 5).
- Cross-check: confirm `Specification.md` Cross-Reference Matrix evidence is available for the issue package (**TBD**; Specification.md: Cross-Reference Matrix).

## Records

**Documentation outputs:**
- Platform structural calculations
- Pipe rack calculations
- Connection design calculations

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250; Datasheet.md: Attributes; Specification.md: Scope, Documentation)

**Record management:**
- Calculation package files (native + PDF), independent check record, and any model files required by project QA (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: Documentation; Step 7).
- Filing convention: working files remain in `1_Working/`; review/issue copies can be packaged to `2_Checking/` / `3_Issued/` as adopted by the team (Source: README.md; Datasheet.md: References).
- Revision tracking: per project numbering system and `Datasheet.md` attributes (Datasheet.md: Attributes; Step 7).
- Retention requirements: **TBD**.

## Cross-Document Traceability

| Document | Section | Linked Content |
|----------|---------|----------------|
| Datasheet.md | Identification | Deliverable identity verified in Step 1 |
| Datasheet.md | Attributes | Calculation metadata (number, software, design basis) verified in Steps 3, 7 |
| Datasheet.md | Construction | Linked deliverables referenced in Steps 2, 5 |
| Specification.md | Scope | Anticipated artifacts checklist used in Step 1 |
| Specification.md | Calculation Package Structure | Minimum content requirements checked in Steps 2–6 |
| Specification.md | Cross-Reference Matrix | Verification traceability confirmed in Step 6 |
| Guidance.md | Principles | Intent guiding Steps 2, 4, 5 (traceability, ER authority, interface register) |
| Guidance.md | Considerations | Trade-offs considered in Steps 1, 3, 5 |
| Guidance.md | Examples | Formats for load case summary, governing member summary, interface register |

**Cross-Deliverable Consistency (PKG-06):**
- DEL-06.01: Calculation assumptions/results reconciled with drawing notes (Step 5)
- DEL-06.02: Material/coating assumptions aligned with specification clauses (Steps 2, 5)
- DEL-06.04: Gangway/grating design justification traceable to calculation package (Step 5)
- DEL-06.05: Critical items (welds, bolting, coating systems) identified for downstream inspection/records (Step 5)
