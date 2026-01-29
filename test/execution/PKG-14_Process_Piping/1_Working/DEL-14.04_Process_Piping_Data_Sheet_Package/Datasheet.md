# Datasheet: DEL-14.04 Process Piping Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-14.04 |
| Name | Process Piping Data Sheet Package |
| Package | PKG-14 Process Piping |
| Discipline | Mechanical |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Data Sheet Type | Piping line list and piping material data sheets (scope: Specification.md Scope; rationale: Guidance.md Purpose; procedure: Procedure.md Purpose) |
| Number of Lines | **TBD** — estimate: 50-150 piping lines (construction: Construction item 1; procedure: Procedure.md Step 1, Step 2; to be confirmed during P&ID development per DEL-14.01) |
| Material Classes | **TBD** — estimate: 3-6 material classes (carbon steel liquid, SS liquid, nitrogen, etc.) (construction: Construction item 2; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 3) |
| Line List Format | **TBD** — Excel spreadsheet or database format typical (requirements: Specification.md Documentation - Line list format; procedure: Procedure.md Prerequisites; examples: Guidance.md Examples item 1) |
| Revision Control | **TBD** — per project data sheet numbering system (requirements: Specification.md QR-4; procedure: Procedure.md Step 6) |

## Conditions

**Applicability:** All process piping in PKG-14 (headers, export lines, recycle lines, nitrogen distribution) (scope: Specification.md Scope; construction: Construction section; cross-reference DEL-14.01)

**Product/Service:** CSD canola oil (source: Decomposition Section 1.1; scope: Specification.md Scope; requirements: Specification.md PR-2; cross-reference DEL-14.01, DEL-14.02)

**Design Conditions:**
- **Operating temperature:** **TBD** — **ASSUMPTION**: -10°C to +60°C for canola oil; ambient for nitrogen (requirements: Specification.md FR-2; construction: Construction item 1; interface: Specification.md IR-3; procedure: Procedure.md Step 2; cross-reference DEL-14.02, DEL-14.03)
- **Operating pressure:** **TBD** — varies by system (railcar unloading, marine loading, recycle, nitrogen) (requirements: Specification.md FR-2; construction: Construction item 1; interface: Specification.md IR-3; procedure: Procedure.md Step 2; cross-reference DEL-14.02, DEL-14.03)
- **Design pressure/temperature:** Per ASME B31.3 and DEL-14.03 calculations (requirements: Specification.md PR-1; interface: Specification.md IR-3; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 2; cross-reference DEL-14.03)
- **Flow rates:** **TBD** — based on 1,000,000 MT/annum throughput (source: Decomposition Section 1.1; construction: Construction item 1; procedure: Procedure.md Step 2; cross-reference DEL-14.03)

## Construction

**Anticipated artifacts** (source: Decomposition DEL-14.04; scope: Specification.md Scope; procedure: Procedure.md Steps 1-4):

**1. Line List:**
- Tabular register of all piping lines in PKG-14 (scope: Specification.md Scope; requirements: Specification.md FR-1, FR-2; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 1, Step 2; examples: Guidance.md Examples items 1, 2)
- Typical columns: Line Number, Service Description, From/To Equipment, Pipe Size (NPS/DN), Material Class, Design Pressure, Design Temperature, Insulation Required (Y/N), Spec Reference (requirements: Specification.md FR-2; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Line List Development; procedure: Procedure.md Step 2; documentation: Specification.md Documentation - Line list columns; examples: Guidance.md Examples item 1)
- **TBD** — Number of lines (estimated 50-150 based on facility size and complexity) (attributes: Number of Lines; procedure: Procedure.md Step 1, Step 2; cross-reference DEL-14.01)
- Provides traceability from P&IDs to specifications and drawings (requirements: Specification.md FR-3; rationale: Guidance.md Principles item 3; interface: Specification.md IR-1, IR-2; considerations: Guidance.md Considerations - Coordination; procedure: Procedure.md Step 2; cross-reference DEL-14.01, DEL-14.02)

**2. Piping Material Data Sheets:**
- Material specifications organized by material class (scope: Specification.md Scope; requirements: Specification.md FR-4, FR-5; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 3, Step 4; examples: Guidance.md Examples item 3)
- Each class specifies: Pipe material and schedule, Fitting material and type, Flange material and rating, Gasket material, Bolting material (requirements: Specification.md FR-5; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; procedure: Procedure.md Step 4; documentation: Specification.md Documentation - Material data sheets; examples: Guidance.md Examples item 3)
- Typical classes: CS-150 (carbon steel Class 150), CS-300 (carbon steel Class 300), SS-150 (stainless steel Class 150 for nitrogen/CIP) (attributes: Material Classes; construction: Material Class Examples below; requirements: Specification.md FR-4; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 3; examples: Guidance.md Examples item 3)
- Cross-reference to DEL-14.02 (detailed piping technical specification) (requirements: Specification.md FR-6, IR-2; interface: Specification.md IR-2; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 4; verification: Specification.md Verification; examples: Guidance.md Examples item 3)

**Material Class Examples:**
- **CS-150:** Carbon steel (ASTM A106 Gr. B), ASME B16.5 Class 150 flanges — for canola oil liquid service at moderate pressure (requirements: Specification.md FR-4, PR-2; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; procedure: Procedure.md Step 3; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)
- **CS-300:** Carbon steel, Class 300 flanges — for high-pressure services (requirements: Specification.md FR-4; rationale: Guidance.md Principles item 2; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 3; examples: Guidance.md Examples item 3; cross-reference DEL-14.02, DEL-14.03)
- **SS-150:** Stainless steel (ASTM A312 Gr. 304/316), Class 150 — for nitrogen distribution or clean-in-place systems (requirements: Specification.md FR-4; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 3; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)

## References

**Project References:**
- Decomposition file: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md
- ER Volume 2 Part 1 (General Requirements), Part 2 (Civil & Process Mechanical Works) (procedure: Procedure.md Prerequisites; cross-reference DEL-14.01, DEL-14.02)

**Applicable Standards:**
- ASME B31.3 — Process Piping (material selection guidance) (requirements: Specification.md PR-1, Standards section; rationale: Guidance.md Principles item 2; procedure: Procedure.md Prerequisites, Step 3; cross-reference DEL-14.02, DEL-14.03)

**Cross-references:**
- DEL-14.01 (Process Piping Design Drawing Set) — P&IDs provide line numbers and services for line list (interface: Specification.md IR-1; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Line List Development, Coordination; procedure: Procedure.md Prerequisites, Step 1; verification: Specification.md Verification; examples: Guidance.md Examples items 1, 2)
- DEL-14.02 (Process Piping Technical Specification) — detailed material specifications; data sheets summarize/reference this spec (interface: Specification.md IR-2; requirements: Specification.md FR-6; rationale: Guidance.md Principles items 2, 3; considerations: Guidance.md Considerations - Coordination; procedure: Procedure.md Prerequisites, Step 4; verification: Specification.md Verification; examples: Guidance.md Examples item 3)
- DEL-14.03 (Process Piping Design Calculations) — pipe sizing and design pressure/temperature for line list (interface: Specification.md IR-3; requirements: Specification.md PR-1, FR-2; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Line List Development; procedure: Procedure.md Prerequisites, Step 2; verification: Specification.md Verification)
- PKG-13 (Storage Tanks), PKG-15 (Pumps), PKG-16 (Valves) — equipment interfaces and material compatibility (interface: Specification.md IR-4; considerations: Guidance.md Considerations - Coordination; procedure: Procedure.md Step 2)

**Related Project Objectives:**
- OBJ-2: Throughput Capacity (1,000,000 MT/annum) — line sizes support throughput (requirements: Specification.md FR-1; conditions: Flow rates; procedure: Procedure.md Step 2)
- OBJ-9: Lifecycle Cost Optimization — material standardization reduces inventory and maintenance costs (attributes: Material Classes; rationale: Guidance.md Principles item 2; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 3)
