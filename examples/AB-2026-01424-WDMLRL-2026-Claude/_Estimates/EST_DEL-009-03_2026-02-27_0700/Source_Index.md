# Source_Index.md

## Pricing Sources Indexed

### Source 1: Professional_Staff_Rates.csv
- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv
- **Source Type:** PARAMETRIC (rate table with parametric basis)
- **Parsing Notes:** CSV with columns RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. 25 roles defined.
- **Supports:** Hourly rate pricing for all professional staff roles. Used for unit rates in Detail.csv.
- **Key Rates Used:**
  - R-01 Project Manager: $165/hr CAD (MEDIUM confidence)
  - R-05 HSE Manager: $140/hr CAD (MEDIUM confidence)
  - R-08 Cost Estimator: $135/hr CAD (MEDIUM confidence)
  - R-22 Permitting Specialist: $125/hr CAD (MEDIUM confidence)
- **Limitations:** Rates are PARAMETRIC basis with MEDIUM confidence. No firm quotes.

### Source 2: Level_of_Effort.csv
- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv
- **Source Type:** PARAMETRIC (estimated hours per deliverable per role)
- **Parsing Notes:** CSV with columns Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes.
- **Supports:** Hour quantities for DEL-009-03. Only two rows found:
  - R-01 Project Manager: 6 hours
  - R-08 Cost Estimator: 4 hours
- **Limitations:** LOE data for DEL-009-03 is sparse — only 2 of the anticipated 3-4 roles are represented. The 5-phase permitting process described in the Procedure document implies significantly more effort than 10 total hours. The LOE appears to capture only management-level oversight, not the specialist permitting effort.

### Source 3: Assumed_Project_Parameters.csv
- **Path:** _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv
- **Source Type:** PARAMETRIC (project parameters informing scope)
- **Parsing Notes:** CSV with columns ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes. 19 parameters defined.
- **Supports:** Contextual parameters used to justify scope assumptions (e.g., building type, area, equipment, systems informing the number of Safety Code permit categories).
- **Key Parameters Used:**
  - PP-09: Maintenance shop addition (building type)
  - PP-10: ~13,000 sqft floor area
  - PP-12/PP-13: 2 x 5-tonne overhead cranes (triggers elevator/crane safety code)
  - PP-14: 50,000 L cistern (triggers plumbing safety code)
  - PP-15: 2,000 US gal septic holding tank (triggers plumbing safety code)
  - PP-16: Forced-air makeup air system (triggers mechanical/gas safety code)
  - PP-17: Currency = CAD
- **Limitations:** Does not directly contain pricing data. Provides scope context only.

### Source 4: Deliverable Documents (DEL-009-03)
- **Path:** PKG-009_Permitting & Regulatory Compliance/1_Working/DEL-009-03_Safety-Code-Permits/
- **Source Type:** Engineering content (read-only; not a pricing source but the basis for quantity takeoff)
- **Documents Read:**
  - _CONTEXT.md — deliverable identity and scope
  - Datasheet.md — attributes, conditions, references
  - Specification.md — requirements (12 REQs), standards, verification
  - Guidance.md — principles, considerations, trade-offs, conflict table
  - Procedure.md — 5 phases, 15 steps, prerequisites, verification, records
- **Supports:** Identification of priceable items (quantity takeoff). All items in Items.csv trace to these documents.
- **Limitations:** Multiple TBDs in Datasheet (permit types, number of permits, accredited agency identity) affect quantity certainty.
