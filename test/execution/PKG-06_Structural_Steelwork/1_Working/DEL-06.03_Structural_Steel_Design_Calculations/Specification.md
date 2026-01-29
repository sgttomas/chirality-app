# Specification: DEL-06.03 Structural Steel Design Calculations

## Scope

This deliverable provides the engineering basis and sizing/verification calculations for structural steel within **PKG-06 Structural Steelwork** (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250).

Package scope includes steel platforms, stairs, gangways, access structures, handrails, and pipe supports (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:242). The calculations should support those items unless explicitly excluded by the Employer’s Requirements or scope focus boundaries (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).

**Anticipated calculation artifacts:**
- Platform structural calculations
- Pipe rack calculations
- Connection design calculations

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250; Datasheet.md: Attributes; Procedure.md: Step 1; Guidance.md: Considerations)

## Requirements

### Functional Requirements

- Provide a calculation package that states assumptions, inputs, analysis method, governing load cases, and results for the anticipated artifacts list (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250).
- Identify governing design criteria (codes/standards, load/environmental criteria, design life) as required by the Employer’s Requirements (clauses **TBD**) (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).
- Present outputs in a form suitable for independent checking and review (ASSUMPTION; to be confirmed in ER clauses).

### Calculation Package Structure (Minimum) — **ASSUMPTION / TBD**

Until Employer's Requirements clauses and project calculation standards are extracted, the following structure is treated as **ASSUMPTION** (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

- Calculation index (Platform structural calculations, Pipe rack calculations, Connection design calculations) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250; Datasheet.md: Attributes; Procedure.md: Step 1).
- Input register (geometry, material properties, support conditions, loads) (**TBD** format; Procedure.md: Step 2).
- Load case and combination list (**TBD** list until ER criteria extracted; Datasheet.md: Attributes; Procedure.md: Step 4; Guidance.md: Examples).
- Interface assumptions register (equipment/piping loads, foundation assumptions) (Dependencies: NOT_TRACKED; Procedure.md: Step 2; Guidance.md: Principles, Examples).
- Results summary highlighting governing members/connections, deflection/limit checks, and any required drawing notes for DEL-06.01 or specification clauses for DEL-06.02 (ASSUMPTION; Procedure.md: Step 5; Guidance.md: Examples).
- Independent check record (checker name/date, scope of check) (**TBD** format; Procedure.md: Step 6).

### Performance Requirements

- Demonstrate that structural steel members and connections satisfy the governing criteria for strength/serviceability/stability (**TBD** explicit criteria) (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).
- Where multiple load cases control, clearly identify governing members and controlling combinations (**TBD** approach) (ASSUMPTION; standard structural calculation practice).

### Interface Requirements

- Coordinate interface assumptions (support conditions, anchor/bearing assumptions, equipment loads, piping loads) through project coordination workflows; dependency edges are not tracked in-file (see `_DEPENDENCIES.md`) (Dependencies: NOT_TRACKED).
- Where Employer-responsible items exist, calculations should address only the interface connection requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49).

### Quality Requirements

- Calculations shall follow the project’s QA/QC and document control expectations (numbering, revisioning, checking) (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).
- Each calculation shall be independently checked and signed off per the Procedure workflow (Procedure.md: Steps).

## Standards

- Governing structural design codes/standards are **TBD** until extracted from Employer’s Requirements (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).

## Verification

- Independent check: reproduce critical results or verify via alternate method/tool (Procedure.md: Steps; **TBD** acceptance criteria).
- Model/software verification: record model inputs and sanity checks (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).
- Cross-check: ensure key assumptions match those referenced in drawings and specification (Dependencies: NOT_TRACKED).

## Cross-Reference Matrix (Specification → Procedure → Outputs)

| Requirement area | Primary procedure step(s) | Evidence / output |
|------------------|---------------------------|------------------|
| Scope completeness (Platform structural calculations, Pipe rack calculations, Connection design calculations) | Procedure.md: Steps 1, 5 | Calculation index + governing results summary (**TBD** format; Datasheet.md: Attributes) |
| Inputs and assumptions recorded | Procedure.md: Steps 2, 3 | Input register (geometry, material properties, support conditions, loads) + interface assumptions register (**TBD** format; Guidance.md: Principles, Examples) |
| Analysis methodology and software recorded | Procedure.md: Step 3 | Software/tool versions and key settings (**TBD**; Datasheet.md: Attributes) |
| Governing load cases and combinations stated | Procedure.md: Step 4 | Load case list and combinations (**TBD**; Datasheet.md: Attributes; Guidance.md: Examples) |
| Results documented (governing members, deflections, drawing notes) | Procedure.md: Step 5 | Results summary with drawing notes implications (**TBD**; Guidance.md: Examples) |
| Independent check performed | Procedure.md: Step 6 | Independent check record (**TBD**) |
| Document control applied | Procedure.md: Step 7 | Revision history / approvals (**TBD**; Datasheet.md: Attributes) |

## Documentation

**Deliverable artifacts:**
- Platform structural calculations
- Pipe rack calculations
- Connection design calculations

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:250; Datasheet.md: Attributes; Procedure.md: Step 1)

**Documentation requirements:**
- Include calculation index, revision history, and approvals per document control requirements (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Procedure.md: Step 7).
- Calculation package files (native + PDF), independent check record, model files as required (**TBD**) (Procedure.md: Records).

## Cross-Document Notes

- Datasheet: calculation number, software used, design basis/code, load cases, and calculation coverage should remain consistent with document control and the Procedure's release workflow (Datasheet.md: Attributes; Procedure.md: Steps).
- Drawings (DEL-06.01): drawings should reference calculation assumptions/results (governing load cases, member sizing, design notes) where required (DEL-06.01 Specification.md: Interface Requirements; Datasheet.md: Construction; Guidance.md: Cross-Document Notes).
- Technical Specification (DEL-06.02): calculation inputs (material properties, coating assumptions, workmanship criteria) should align to DEL-06.02 clauses (DEL-06.02 Specification.md; Datasheet.md: Construction; Guidance.md: Cross-Document Notes).
- Data Sheets (DEL-06.04): gangway/grating standard details requiring design justification should be traceable to this calculation package (Datasheet.md: Construction).
- Installation/Test Records (DEL-06.05): critical design assumptions affecting inspection/hold points (critical welds, bolting categories, coating systems) should be traceable to record requirements (Datasheet.md: Construction; Guidance.md: Considerations, Cross-Document Notes).
