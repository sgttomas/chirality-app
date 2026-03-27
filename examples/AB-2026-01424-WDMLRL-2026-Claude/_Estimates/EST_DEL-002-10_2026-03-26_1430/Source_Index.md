# Source Index -- EST_DEL-002-10_2026-03-26_1430

## Price Sources Used

| PS-ID | File | Source Type | Rows Used | Supports |
|---|---|---|---|---|
| PS-STAFF | Professional_Staff_Rates.csv | Rate Table | R-01 ($165/hr), R-08 ($135/hr), R-13 ($95/hr), R-14 ($170/hr) | Unit rates for all labour line items |
| PS-LOE | Level_of_Effort.csv | Parametric | DEL-002-10 rows: R-01 (6h), R-08 (4h), R-13 (24h), R-14 (56h) | Baseline hours for RATE_TABLE lines |
| PS-CBS | CBS_Taxonomy.csv | Reference | CBS-01 (Design & Engineering), CBS-02 (Project Management) | CBS code assignment |

## Price Sources Available but Not Used

| PS-ID | File | Reason |
|---|---|---|
| PS-DF | Professional_Design_Fees.csv | Fee-percentage method not selected; RATE_TABLE (hours x rate) used instead |
| PS-PARAMS | Assumed_Project_Parameters.csv | No project-parameter-based pricing needed for this deliverable |
| PS-SC | Structural_Concrete_Rates.csv | Construction rates; DEL-002-10 is a design labour deliverable |
| PS-BE | Building_Envelope_Rates.csv | Construction rates; not applicable |
| PS-LAB | Construction_Labour_Rates.csv | Construction rates; not applicable |

## Addenda Sources (Scope Change Evidence)

| Ref | Document | Used For |
|---|---|---|
| R-08 | AB-2026-01424-Addendum_2.pdf | Structural system change to full concrete (later relaxed by Add. 4) |
| R-10 | AB-2026-01424-Addendum_4.pdf | Precast concrete walls + steel roof acceptable; corbel-supported crane; interior walls precast concrete |
| R-09 | AB-2026-01424-Addendum_3.pdf | Crane hook height 26 ft confirmation |

## Deliverable Sources Read

| Document | Path (relative to DEL-002-10 folder) | Used For |
|---|---|---|
| Datasheet.md | PKG-002_Structural Design/1_Working/DEL-002-10_Calculation-Package/Datasheet.md | Structural subsystem scope, key design parameters |
| Specification.md | PKG-002_Structural Design/1_Working/DEL-002-10_Calculation-Package/Specification.md | Requirements, standards, verification criteria |
| Guidance.md | PKG-002_Structural Design/1_Working/DEL-002-10_Calculation-Package/Guidance.md | Trade-offs, considerations, long-term factors |
| Procedure.md | PKG-002_Structural Design/1_Working/DEL-002-10_Calculation-Package/Procedure.md | Steps, decision gates, QA requirements |
| Dependencies.csv | PKG-002_Structural Design/1_Working/DEL-002-10_Calculation-Package/Dependencies.csv | Upstream/downstream dependency evidence |

## Parsing Notes

- Professional_Staff_Rates.csv: standard CSV; all rates in CAD; Confidence=MEDIUM for all roles used.
- Level_of_Effort.csv: standard CSV; pre-SCA-001 vintage; hours for DEL-002-10 confirmed at lines 93-96.
- CBS_Taxonomy.csv: standard CSV; CBS-01 and CBS-02 confirmed as applicable to PKG-002 per ApplicablePackages column.
