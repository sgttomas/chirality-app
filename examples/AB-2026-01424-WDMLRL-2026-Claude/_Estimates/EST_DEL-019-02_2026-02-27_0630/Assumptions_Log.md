# Assumptions Log — EST_DEL-019-02_2026-02-27_0630

## Assumptions Applied During This Run

### ASM-001: LOE hours represent total project duration effort
- **Statement:** The hours in Level_of_Effort.csv for DEL-019-02 represent the total estimated effort for the full project duration, not per-meeting or per-cycle values.
- **Basis:** CSV schema has no frequency column; all other deliverables in the file appear to use the same total-hours convention.
- **Risk:** If hours are per-occurrence, the estimate understates effort by ~39x.
- **Resolution path:** Confirm with LOE source author whether hours are total or per-occurrence.

### ASM-002: Project duration for weekly meetings is approximately 9 months (~39 weeks)
- **Statement:** Weekly meetings run from contract execution (assumed ~April 2026, after mandatory site meeting March 3, 2026 and award) through CCC issuance (deadline December 31, 2026).
- **Basis:** Assumed_Project_Parameters.csv (PP-07: completion deadline 2026-12-31; PP-08: mandatory site meeting 2026-03-03); Datasheet Conditions (operative period: contract execution through CCC issuance).
- **Risk:** If project starts earlier or extends beyond December 2026, the meeting count changes.
- **Resolution path:** Confirm construction start date and expected CCC date.

### ASM-003: QA/QC Lead and HSE Manager attend weekly meetings
- **Statement:** The QA/QC Lead (R-06) and HSE Manager (R-05) are included as meeting attendees based on Specification ASSUMPTION REQ-019-02-A02 (QC/subcontractor status as agenda items) and OBJ-007 (OH&S program implementation).
- **Basis:** Level_of_Effort.csv includes R-05 and R-06 for DEL-019-02; Specification and _CONTEXT.md link this deliverable to OBJ-007.
- **Risk:** Low — these roles are standard attendees for construction coordination meetings with OH&S scope.
- **Resolution path:** Confirm attendee list with County PM at project kickoff.

### ASM-004: No non-labour costs are required for this deliverable
- **Statement:** The estimate covers labour costs only. No meeting room, travel, technology, or printing costs are included because no pricing source provides these for DEL-019-02.
- **Basis:** No non-labour pricing source available in PRICE_SOURCES for this deliverable.
- **Risk:** If in-person meetings are required at the rural site (~30km from Camrose), travel costs could be material. Guidance C-2 and C-10 note that meeting format is TBD.
- **Resolution path:** Determine meeting format at kickoff; provide non-labour cost source if applicable.

### ASM-005: Currency is CAD
- **Statement:** All amounts are in Canadian Dollars.
- **Basis:** Brief specifies CURRENCY=CAD; Assumed_Project_Parameters.csv (PP-17: Currency=CAD); Alberta, Canada project location.
- **Risk:** None — Alberta project, CAD is the appropriate currency.
- **Resolution path:** N/A.

### ASM-006: CBS codes are agent-assigned
- **Statement:** CBS codes (LABOUR-MGMT, LABOUR-CONST) are assigned by the estimating agent based on role categories in Professional_Staff_Rates.csv, not from a project-level CBS dictionary.
- **Basis:** No CBS dictionary was provided in the brief or pricing sources.
- **Risk:** CBS codes may not align with the project's actual cost breakdown structure if one exists.
- **Resolution path:** Provide project CBS dictionary if one exists; remap if needed.
