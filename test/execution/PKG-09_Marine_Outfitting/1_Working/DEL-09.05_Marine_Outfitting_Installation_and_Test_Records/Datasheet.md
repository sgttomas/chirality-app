# Datasheet: DEL-09.05 Marine Outfitting Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-09.05 |
| Name | Marine Outfitting Installation & Test Records |
| Package | PKG-09 Marine Outfitting |
| Discipline | Marine |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

## Scope (Decomposition)

**Package scope (PKG-09):** Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs. (**Source:** Decomposition, PKG-09)

**Deliverable intent (DEL-09.05):** Provides evidence of completion, inspection, and testing for marine outfitting. (**Source:** Decomposition, DEL-09.05 row)

**Anticipated artifacts (from decomposition):**
- Installation records
- Proof load test records

## Deliverable Attributes (Records Package)

| Attribute | Value |
|-----------|-------|
| Record package numbering | **TBD** — per project document control procedure |
| Record categories | Installation / Inspection / Testing / Certificates / NCRs (**TBD** — final list per project QA/QC procedures) |
| Record form templates | **TBD** — per project QA/QC standard forms |
| Retention period | **TBD** — **ASSUMPTION:** Permanent retention for as-built project record and regulatory compliance |
| Revision | **TBD** — per project revision scheme (records typically non-revisable once issued) |
| Classification | **TBD** — **ASSUMPTION:** QA/QC records (construction completion evidence) |

## Content Checklist (Minimum)

Each record category corresponds to requirements in `Specification.md § 2` and has corresponding rationale in `Guidance.md` and procedural steps in `Procedure.md`.

### Installation Records (SPEC § 2.1)

| Record Type | Content | Specification § | Guidance § | Procedure Step | Status |
|-------------|---------|-----------------|------------|----------------|--------|
| Fender installation records | Tag, location, as-installed position/alignment verification, anchor bolt torque records, chain installation verification, photographic records | SPEC § 2.1 | Guidance § Principles (Installation Records) | Proc Step 3 | **TBD** — records generated during construction |
| Bollard installation records | Tag, location, foundation preparation records, setting-out verification, grouting records (batch tickets, strength tests), base plate alignment verification, photographic records | SPEC § 2.1 | Guidance § Principles (Installation Records) | Proc Step 3 | **TBD** — records generated during construction |
| Ladder installation records | Tag, location, fixing verification (bolt torques, weld inspection), safety feature check (cage installation, rest platforms, rung spacing), material certificates, photographic records | SPEC § 2.1 | Guidance § Principles (Installation Records) | Proc Step 3 | **TBD** — records generated during construction |
| Life-saving equipment records | Tag, location, mounting verification, equipment functionality check, accessibility verification, photographic records | SPEC § 2.1 | Guidance § Principles (Installation Records) | Proc Step 3 | **TBD** — records generated during construction |
| Existing Berth 10 upgrade/repair records | Repair/upgrade completion records per specific scope, before/after photographic records, material certificates (if new materials used) | SPEC § 2.1 | Guidance § Principles (Installation Records) | Proc Step 3 | **TBD** — records generated during construction; scope per ER and condition survey |

### Proof Load Test Records (SPEC § 2.2)

| Record Type | Content | Specification § | Guidance § | Procedure Step | Status |
|-------------|---------|-----------------|------------|----------------|--------|
| Bollard proof load test records | Tag, test setup (method, equipment, calibration), applied load (value, duration, load curve), measured deflection (if required), pass/fail determination vs acceptance criteria, witness signatures (per ITP), photographic records | SPEC § 2.2 | Guidance § Principles (Proof Load Testing) | Proc Step 4 | **TBD** — if required per DEL-09.02 § 2.2 and applicable codes |
| Other proof test records | As specified by DEL-09.02 or Employer's Requirements (e.g., ladder load testing if required) | SPEC § 2.2 | — | Proc Step 4 | **TBD** — if required |

### Supporting Evidence (SPEC § 1.3)

| Evidence Type | Content | Specification § | Guidance § | Procedure Step | Status |
|---------------|---------|-----------------|------------|----------------|--------|
| Photographic records | Before/during/after installation photos, proof load test photos, repair completion photos; organized by equipment tag; dated and annotated | SPEC § 1.3 | Guidance § Considerations (Evidence quality) | Proc Step 3, 4 | **TBD** — generated during construction |
| Material certificates | Mill certificates (MTRs) for steel components, coating inspection reports (DFT measurements), rubber compound certificates (fenders), compliance statements | SPEC § 1.3 | — | Proc Step 3 | **TBD** — from vendor submittals and field inspection |
| Calibration certificates | Test equipment calibration records (for proof load testing, torque wrenches, measurement equipment) | SPEC § 1.3 | Guidance § Principles (Proof Load Testing) | Proc Step 4 | **TBD** — if testing performed |
| NCR dispositions | Nonconformance reports with disposition (use-as-is, repair, replace) and closure evidence (re-inspection, corrective action verification) | SPEC § 4 | Guidance § Principles (NCR Management) | Proc Step 3, 5 | **TBD** — if NCRs generated during construction |

## Related Deliverables (PKG-09)

This records package provides evidence that construction meets design intent and specification requirements:

| Deliverable | Relationship | Interface Point |
|-------------|--------------|-----------------|
| DEL-09.01 Marine Outfitting Design Drawing Set | **Baseline** — record tags align with drawing equipment tags | Equipment tags and locations from drawings used in records identification; verify as-installed matches drawings |
| DEL-09.02 Marine Outfitting Technical Specification | **Requirements** — specification defines inspection/test requirements | Inspection checklists and test procedures implement DEL-09.02 § 1.6 quality/inspection requirements and § 2 equipment-specific testing requirements |
| DEL-09.03 Marine Outfitting Design Calculations | **Acceptance criteria** — calculations provide test acceptance criteria | Proof load test acceptance criteria (bollard test load, acceptance limits) from DEL-09.03 bollard load calculations |
| DEL-09.04 Marine Outfitting Data Sheet Package | **Baseline** — data sheets provide as-designed baseline | Verify as-installed equipment matches DEL-09.04 data sheet specifications (manufacturer, model, capacity, materials, etc.) |

## Inputs / Dependencies (NOT_TRACKED)

Dependencies are coordinated externally (see `execution/_Coordination/_COORDINATION.md`). Required inputs:

| Input | Source | Specification § | Guidance § | Required For | Status |
|-------|--------|-----------------|------------|--------------|--------|
| Inspection/test requirements | DEL-09.02 | SPEC § 2 | — | Records matrix, acceptance criteria, hold/witness points | **TBD** — DEL-09.02 § 1.6, 2.1, 2.2 |
| Equipment tags and locations | DEL-09.01 | SPEC § 3 | Guidance § Considerations (Tag consistency) | Record identification, equipment inventory | **TBD** — DEL-09.01 drawings |
| As-designed equipment data | DEL-09.04 | SPEC § 3 | Guidance § Considerations (As-installed vs. as-designed) | Baseline for as-installed verification | **TBD** — DEL-09.04 data sheets |
| Proof load acceptance values | DEL-09.03 / DEL-09.02 | SPEC § 2.2 | Guidance § Principles (Proof Load Testing) | Test acceptance criteria (test load value, deflection limits) | **TBD** — DEL-09.03 bollard calculations; DEL-09.02 § 2.2 |
| Employer's Requirements | Employer | SPEC § Standards | — | QA/QC requirements, record content, hold/witness points | **TBD** — ER clauses for QA/QC and records |
| Vendor installation instructions | Vendor | SPEC § 2.1 | — | Installation checklist basis, installation procedures | **TBD** — vendor submittals |
| ITP with hold/witness points | Project QA/QC | SPEC § 4 | Guidance § Considerations (ITP alignment) | Witness requirements, inspection hold points | **TBD** — project ITP to be established |
| Record form templates | Project QA/QC | SPEC § 1.2 | — | Standardized forms for consistency | **TBD** — project QA/QC standard forms |

## Acceptance (Definition of Done)

- Records package includes all decomposition-listed artifacts (installation records + proof load test records).
- All Content Checklist items (above) are completed with required data, signatures, and dates.
- Record set completeness verified against records matrix — all required records present (verified per `Procedure.md § Step 5`).
- Equipment tags in records align with DEL-09.01 drawings and DEL-09.04 data sheets (verified per `Procedure.md § Step 5`).
- As-installed equipment verified to match DEL-09.04 data sheet specifications (manufacturer, model, capacity, materials).
- Proof load tests (where required per DEL-09.02) demonstrate pass vs acceptance criteria (verified per `Procedure.md § Step 5`).
- All required signatures present (installer, inspector, witness per ITP hold/witness points).
- Any outstanding NCRs are either closed (with disposition evidence) or listed with current status and corrective actions.
- Cross-document consistency verified with `Specification.md`, `Guidance.md`, and `Procedure.md`.

## References

- `Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (PKG-09 scope; DEL-09.05 definition)
- `_REFERENCES.md` (this deliverable) — lists applicable reference documents
- `Specification.md` (DEL-09.05) — requirements governing this datasheet
- `Guidance.md` (DEL-09.05) — rationale and record-keeping considerations
- `Procedure.md` (DEL-09.05) — production/verification process
