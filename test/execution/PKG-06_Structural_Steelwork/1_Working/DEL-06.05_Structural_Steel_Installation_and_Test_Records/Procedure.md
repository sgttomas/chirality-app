# Procedure: DEL-06.05 Structural Steel Installation & Test Records

## Purpose

This procedure defines the process for producing and managing the **Structural Steel Installation & Test Records** within **PKG-06 Structural Steelwork**.

The deliverable provides evidence of completion, inspection, and testing for structural steelwork (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252).

**Deliverable type:** Record  
**Responsible party:** D&B Contractor (QA/QC)

## Prerequisites

**Dependencies:**
- See `_DEPENDENCIES.md` — **NOT_TRACKED**: dependencies coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`).
- Confirm the latest drawings/specification/data sheets are available to define required record types and traceability identifiers (Dependencies: NOT_TRACKED).

**Reference materials:**
- test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-06 / DEL-06.05 definition) (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:238-252).
- Employer's Requirements — QA record expectations **TBD** (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).
- Any structural steel inspection/testing requirements **TBD** (Source: test/Volume_2_Part_3_Employers_Requirements.pdf, location TBD).

**Personnel requirements:**
- QA/QC personnel per project quality requirements (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD).

## Steps

1. **Define required record list** — Confirm required record categories and sub-types: Mill certificates, Weld inspection records, Galvanizing certificates; create Record Category Register (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Datasheet.md: Attributes; Specification.md: Scope, Cross-Reference Matrix; Guidance.md: Principles).
2. **Define traceability scheme** — Agree item IDs (from DEL-06.01), heat numbers, drawing references (DEL-06.01), specification clause references (DEL-06.02), data sheet references (DEL-06.04 where applicable) that each record must carry; document mapping rules (**TBD**) (ASSUMPTION; Specification.md: Record Index Structure, Cross-Reference Matrix; Datasheet.md: Attributes; Guidance.md: Considerations).
3. **Collect source records** — Obtain vendor certificates and inspection reports as work progresses; ensure completeness of identifiers (heat numbers, coating batch, inspection date, inspector ID) (Specification.md: Cross-Reference Matrix; Guidance.md: Considerations).
4. **Verify records** — Check that each record meets required fields, signatures, and acceptance criteria aligned to DEL-06.02 specification clauses (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: Performance Requirements, Cross-Reference Matrix; Guidance.md: Considerations).
5. **Compile package** — Create an indexed record package (by item ID and record type) suitable for review/closeout; organize by folder structure (Mill certificates / Weld inspection records / Galvanizing certificates); create compiled PDF set if required (ASSUMPTION; format TBD).
   - Use the `Specification.md` "Record Index Structure" as the minimum required index fields (item ID, drawing ref, spec clause ref, data sheet ref, record category, record identifier/filename, date/inspector, status) (Specification.md: Record Index Structure, Cross-Reference Matrix; Datasheet.md: Construction; Guidance.md: Considerations, Examples).
6. **Issue preparation** — Apply document control metadata, revisioning, and approvals per project requirements; ensure `Datasheet.md` attributes match record package number and revision (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Specification.md: Documentation).

## Verification

- Required record categories defined: Mill certificates, Weld inspection records, Galvanizing certificates (Specification.md: Cross-Reference Matrix; Datasheet.md: Attributes; Step 1).
- Traceability scheme defined: mapping rules for item IDs (DEL-06.01), heat numbers, drawing references, spec clauses (DEL-06.02), data sheet references (DEL-06.04) (**TBD**; Specification.md: Record Index Structure, Cross-Reference Matrix; Datasheet.md: Attributes; Step 2).
- Records collected: vendor certificates and inspection reports with required identifiers (heat numbers, coating batch, inspection date, inspector ID) (Specification.md: Cross-Reference Matrix; Guidance.md: Considerations; Step 3).
- Records verified: required fields, signatures, acceptance criteria checked against DEL-06.02 specification clauses (**TBD**; Specification.md: Cross-Reference Matrix; Guidance.md: Considerations; Step 4).
- Indexed package compiled: records index (per Record Index Structure), folder structure (Mill certificates / Weld inspection records / Galvanizing certificates), compiled PDF set created (**TBD** format; Specification.md: Record Index Structure, Cross-Reference Matrix; Datasheet.md: Construction; Guidance.md: Examples; Step 5).
- Completeness check: records provided for all three required categories (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Specification.md: Verification; Guidance.md: Principles).
- Traceability check: each record maps to item ID(s), drawing references (DEL-06.01), spec clauses (DEL-06.02), data sheets (DEL-06.04 where applicable) (**TBD** mapping method; Specification.md: Verification; Datasheet.md: Cross-Document Points).
- Archival/format check: files meet document control requirements (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: Verification).
- Cross-check: confirm `Specification.md` Cross-Reference Matrix evidence is available for the issue package (**TBD**; Specification.md: Cross-Reference Matrix; Step 6).

## Records

**Documentation outputs:**
- Mill certificates
- Weld inspection records
- Galvanizing certificates

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:252; Datasheet.md: Attributes; Specification.md: Scope, Documentation)

**Record management:**
- Record package files (records index per `Specification.md` Record Index Structure + supporting PDFs organized by category), QA checklists, and approval/sign-off evidence (**TBD**) (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Specification.md: Documentation; Datasheet.md: Construction; Step 5).
- Filing convention: working files remain in `1_Working/`; review/issue copies can be packaged to `2_Checking/` / `3_Issued/` as adopted by the team (Source: README.md; Datasheet.md: References).
- Revision tracking: per project numbering system and `Datasheet.md` attributes (Datasheet.md: Attributes; Step 6).
- Retention requirements: **TBD**.

## Cross-Document Traceability

| Document | Section | Linked Content |
|----------|---------|----------------|
| Datasheet.md | Identification | Deliverable identity verified in Step 1 |
| Datasheet.md | Attributes | Package metadata (number, categories) verified in Step 6 |
| Datasheet.md | Construction | Index structure used in Step 5 |
| Specification.md | Scope | Required record categories used in Step 1 |
| Specification.md | Record Index Structure | Index fields used in Steps 2, 5 |
| Specification.md | Cross-Reference Matrix | Verification traceability confirmed in Step 6 |
| Guidance.md | Principles | Intent guiding Steps 1, 2, 4 (traceability, completeness, ER authority) |
| Guidance.md | Considerations | Trade-offs considered in Steps 3, 4, 5 |
| Guidance.md | Examples | Index format used in Step 5 |

**Cross-Deliverable Consistency (PKG-06):**
- DEL-06.01: Drawing item IDs and references used in traceability scheme (Step 2)
- DEL-06.02: Specification clause references drive record acceptance criteria (Steps 2, 4)
- DEL-06.03: Critical design assumptions inform inspection/record requirements (Step 2)
- DEL-06.04: Data sheet "Required Records" fields used for record completeness (Steps 2, 5)
