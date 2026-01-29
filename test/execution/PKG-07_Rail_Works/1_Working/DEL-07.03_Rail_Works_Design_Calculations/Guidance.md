# Guidance: DEL-07.03 Rail Works Design Calculations

**Enrichment Status:** Pass 3 Complete (3-pass enrichment: Initial draft, Cross-reference enrichment, Final reconciliation)

## Purpose
- Guide development of the rail works calculation package for PKG-07, ensuring that track geometry and ballast depth calculations substantiate the rail works scope (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259, :267).
- Provide context so calculation outputs can be used consistently by the drawing set (DEL-07.01), technical specification (DEL-07.02), and installation/test records (DEL-07.04) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:265-268).

## Principles
- Anchor every calculation assumption to a documented input or an Employer’s Requirements clause; otherwise label as **ASSUMPTION** and flag for resolution (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, clauses TBD).
- Clearly distinguish calculation inputs/criteria for new works (Tracks 6 & 7) versus restoration/modifications (Track 5) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259).
- Maintain consistent units, notation, and terminology with DEL-07.01 drawings and DEL-07.02 specification so coordination does not introduce conversion errors.

## Considerations
- Dependencies are coordinated externally (NOT_TRACKED; see `_DEPENDENCIES.md`). Record any missing inputs (survey/as-built track info) as **TBD** rather than assuming values (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:47).
- Ensure that calculation results can be verified and evidenced via DEL-07.04 records once acceptance criteria are known (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:268).
- Align calculation format with the project quality and calculation control expectations (clauses TBD) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf).
- Maintain an explicit assumptions register and keep it aligned to any **TBD** ER clause placeholders so the calculation package can later be “filled in” without rework (Source: Procedure.md: Steps; and test/Volume_2_Part_2_Employers_Requirements.pdf, clauses TBD).

## Trade-offs
- Calculation detail vs schedule: use conservative assumptions where data is lacking, but label them and plan for revision once inputs/ER clauses are confirmed.
- Sensitivity vs simplicity: where criteria are unclear, sensitivity checks may be needed; extent is **TBD** until ER expectations are identified (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, clauses TBD).

## Examples (from anticipated artifacts)
- Track geometry calculation package addressing relevant geometry parameters (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:267).
- Ballast depth calculation package addressing sizing/verification for ballast sections (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:267).

## Cross-Document Notes
- Datasheet: Use Datasheet.md to keep the calculation scope and metadata aligned with document control and the decomposition artifacts.
- Specification: Use Specification.md to ensure calculations address the “what must be calculated” requirements and verification expectations.
- Procedure: Procedure.md defines how checks and approvals are recorded prior to issue.
