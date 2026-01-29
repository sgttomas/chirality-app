# Specification: DEL-09.05 Marine Outfitting Installation & Test Records

## Scope

This specification defines the requirements for producing **Marine Outfitting Installation & Test Records** within **PKG-09 Marine Outfitting**.

**Decomposition definition (authoritative):** Provides evidence of completion, inspection, and testing for marine outfitting. (**Source:** Decomposition, DEL-09.05 row)

**Package scope (PKG-09):** Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs. (**Source:** Decomposition, PKG-09)

**Anticipated deliverable artifacts:**
- Installation records
- Proof load test records

**Purpose:** Records are evidence artifacts for acceptance — they demonstrate what was installed, inspected, and tested, and who witnessed/accepted it. Records close the loop from design (DEL-09.01, DEL-09.02, DEL-09.03, DEL-09.04) to as-installed verification.

## Requirements

### 1) Records Package Structure Requirements

The records package shall include the following (per `Datasheet.md` Content Checklist and `Guidance.md § Examples`). Cross-reference to procedural steps in `Procedure.md`.

#### 1.1 Records Index/Matrix

**Requirements:**
- Master index listing all required records by equipment tag and location.
- Record status tracking (complete, pending, NCR open, closed).
- Cross-reference to drawings (DEL-09.01 drawing numbers) and data sheets (DEL-09.04 data sheet references).
- **Table structure:**
  - Equipment tag
  - Equipment description (type, model)
  - Location (coordinate or descriptive location)
  - Drawing reference (DEL-09.01)
  - Data sheet reference (DEL-09.04)
  - Installation record reference
  - Proof load test record reference (if applicable)
  - Status (complete, pending, NCR open)
  - Notes (NCR number, special conditions, deviations)
- **TBD:** Format per project document control procedures.

**Rationale:** See `Guidance.md § Principles (Records Intent)`.
**Verification:** See `Procedure.md § Step 1` (define records matrix); `Procedure.md § Step 5` (verify completeness).

#### 1.2 Record Forms

**Requirements:**
- Completed installation/inspection forms with:
  - **Equipment identification:** Tag, serial number (if applicable), manufacturer, model, drawing reference, location
  - **Inspection/verification checks:** Checklist items per equipment type (per DEL-09.02 requirements and vendor installation instructions)
  - **Measured values where applicable:** Dimensions, alignments, torques, coating thickness, grouting strength
  - **Pass/fail determination:** Clear indication of acceptance vs rejection
  - **Signatures:** Installer, inspector, witness (as required by ITP hold/witness points) with names, titles, dates
  - **Date and time:** When inspection/test occurred
  - **Attachments:** Photos, certificates, test data (cross-referenced)
- **Form templates:** **TBD** — per project QA/QC standard forms (see `Guidance.md § Examples` for typical record form structure).
- **Legibility requirement:** All records shall be clear, complete, unambiguous; handwritten entries legible; signatures identifiable.

**Rationale:** See `Guidance.md § Principles (Evidence Rules)`.
**Verification:** See `Procedure.md § Step 2` (prepare record forms); `Procedure.md § Step 5` (verify completeness and signatures).

#### 1.3 Attachments

**Requirements:**
- **Material certificates:** Mill certificates (MTRs) for steel components, coating inspection reports (DFT measurements), rubber compound certificates (for fenders), material compliance statements.
- **Test equipment calibration certificates:** Calibration records for test equipment used (proof load equipment, torque wrenches, measurement equipment); current calibration status verified.
- **Photographic records:** Photos documenting installation stages (before, during critical steps, after completion); organized by equipment tag; dated and annotated; show relevant details (fixings, alignments, interfaces, etc.).
- **NCR dispositions and closure evidence:** Nonconformance reports (NCRs) with disposition (use-as-is, repair, replace, scrap) and closure verification (re-inspection, corrective action verification, sign-off); NCR status summary included in package.
- **Attachment organization:** Attachments shall be organized logically (by equipment tag or record type); cross-referenced in record forms; legible and complete.

**Rationale:** See `Guidance.md § Principles (Evidence Rules)` and `Guidance.md § Considerations (Evidence quality)`.
**Verification:** See `Procedure.md § Step 6` (compile records package with attachments).

### 2) Content Coverage Requirements

The records package shall contain records for each PKG-09 scope item (per `Datasheet.md` Content Checklist). Records shall verify compliance with DEL-09.02 specification requirements.

#### 2.1 Installation Records

**Requirements (per equipment category):**

**Fender Installation Records:**
- **Equipment identification:** Tag (from DEL-09.01), manufacturer/model (from DEL-09.04), location, drawing reference.
- **Pre-installation checks:** Receiving inspection (visual inspection, dimensional verification), material certificate verification (rubber grade, steel backing), surface preparation verification (cleaning, coating touch-up if required).
- **Installation verification checks:**
  - Position relative to structure (coordinate verification, elevation verification)
  - Chain installation and tensioning (if chain-suspended fender)
  - Frontal frame alignment (if applicable)
  - Anchor bolt installation and torque (torque values per specification or vendor requirements)
  - Interface to marine structure (connection details, load transfer verification)
- **Post-installation inspection:** Visual inspection (no damage, proper orientation), dimensional check (verify position within tolerances), coating integrity check (touch-up applied if needed).
- **Photographic records:** Before installation, during critical steps (anchor installation, chain tensioning), after completion.
- **Sign-off:** Installer, inspector, witness (if ITP hold/witness point).
- **TBD:** Specific installation checklist items per DEL-09.02 § 2.1 requirements and vendor installation instructions.

**Bollard Installation Records:**
- **Equipment identification:** Tag, manufacturer/model, location, drawing reference.
- **Pre-installation checks:** Receiving inspection, material certificate verification (steel grade, casting quality), foundation preparation verification (excavation, formwork, reinforcement if applicable).
- **Installation verification checks:**
  - Setting-out accuracy (position survey, alignment verification within tolerances)
  - Foundation preparation (substrate condition, cleanliness, moisture)
  - Base plate placement and alignment (level, plumb, orientation)
  - Anchor bolt installation (embedment depth, spacing, alignment) or through-bolt installation
  - Grouting (if applicable): batch identification, grout placement, curing records, compressive strength test results
  - Final alignment after grouting (verify alignment maintained during cure)
  - Torque verification (anchor bolts, hold-down bolts per specification)
- **Post-installation inspection:** Visual inspection (no deformation, proper orientation), dimensional check, coating/galvanizing integrity.
- **Photographic records:** Foundation preparation, anchor installation, grouting, final installation.
- **Sign-off:** Installer, inspector, witness (if ITP hold/witness point).
- **TBD:** Specific installation checklist items per DEL-09.02 § 2.2 requirements and vendor installation instructions.

**Ladder Installation Records:**
- **Equipment identification:** Tag, manufacturer/model (if applicable), location, drawing reference.
- **Pre-installation checks:** Material certificate verification (stainless steel grade or galvanizing), surface preparation.
- **Installation verification checks:**
  - Fixing security (bolt torques, weld inspection if welded attachments)
  - Safety cage installation (if applicable): cage clearances per code, landing platform at top
  - Rest platforms (if applicable): spacing per code, platform dimensions, attachment security
  - Rung spacing and toe clearance (verify per code requirements)
  - Anti-slip tread or surface treatment (if specified)
  - Interface to supporting structure (attachment adequacy, load transfer)
- **Post-installation inspection:** Visual inspection, dimensional check, safety feature verification.
- **Photographic records:** Fixing details, safety features, completed installation.
- **Sign-off:** Installer, inspector, witness (if ITP hold/witness point).
- **TBD:** Specific checklist items per DEL-09.02 § 2.3 ladder requirements and applicable safety codes.

**Life-Saving Equipment Installation Records:**
- **Equipment identification:** Tag, equipment type (life ring, rescue ladder, etc.), location, drawing reference.
- **Pre-installation checks:** Receiving inspection (equipment condition, compliance certification verification).
- **Installation verification checks:**
  - Mounting security (fixing method, attachment adequacy)
  - Equipment functionality (deployment test if applicable, e.g., quick-release mechanism)
  - Accessibility verification (verify accessible for emergency use, no obstructions)
  - Visibility verification (equipment visible per regulations)
  - Signage and marking (if required)
- **Post-installation inspection:** Visual inspection, equipment condition.
- **Photographic records:** Mounting details, installed location, accessibility.
- **Sign-off:** Installer, inspector.
- **TBD:** Specific checklist items per DEL-09.02 § 2.3 life-saving equipment requirements and applicable regulations.

**Existing Berth 10 Upgrade/Repair Records:**
- **Scope identification:** Repair/upgrade scope per ER and condition survey.
- **Pre-repair documentation:** Before photos, condition assessment notes.
- **Repair/upgrade verification:** Work completion per scope, materials used (if new materials), workmanship quality.
- **Post-repair documentation:** After photos, completion verification, interface to existing elements.
- **Sign-off:** Installer, inspector.
- **TBD:** Specific repair scope and verification requirements per ER and condition survey findings.

**Rationale:** See `Guidance.md § Principles (Installation Records)`.
**Verification:** See `Procedure.md § Step 3` (collect installation records).

#### 2.2 Proof Load Test Records

**Requirements (if testing required per DEL-09.02 § 2.2 and applicable codes):**

**Bollard Proof Load Test Records:**
- **Equipment identification:** Bollard tag, manufacturer/model, location, SWL rating (from DEL-09.04).
- **Test setup documentation:**
  - Load application method (hydraulic jack with load cell, calibrated weights, pulling equipment, etc.)
  - Test equipment identification (jack model/serial, load cell serial, gauge serial)
  - Test equipment calibration certificates (current calibration status verified)
  - Test rig arrangement (sketch or photo showing load application point, reaction point, geometry)
- **Test execution:**
  - Applied load value (kN or tonnes) — per DEL-09.02 or code requirements (typically 1.25× to 1.5× SWL)
  - Load application rate and duration (gradual loading, hold time per procedure)
  - Load vs time curve or load steps (if recorded)
  - Measured deflection or movement (if required by procedure) — measurement method, values
- **Observations during test:**
  - Visual inspection for deformation, cracking, bolt slippage, foundation movement
  - Any anomalies noted (unusual sounds, visible distress, excessive deflection)
- **Pass/fail determination:**
  - Comparison to acceptance criteria (no visible deformation, cracking, or movement exceeding limits)
  - **Acceptance criteria:** **TBD** — per DEL-09.02 § 2.2 and applicable codes
  - Pass/fail statement with justification
- **Witness signatures:**
  - Tester (person performing test)
  - Inspector (QA/QC inspector)
  - Witness (if ITP requires witness for proof load testing) — may be Employer's representative, third-party inspector, or authority representative
  - Names, titles, signatures, dates
- **Photographic records:** Test setup, load application, bollard under load, post-test condition.
- **Test certificate:** Formal test certificate signed by tester and witness documenting test results and acceptance.
- **TBD:** Proof load test requirements and acceptance criteria to be confirmed from DEL-09.02 § 2.2 and applicable codes.

**Other Proof Test Records (if applicable):**
- As specified by DEL-09.02 or Employer's Requirements (e.g., ladder load testing if required by codes or project).
- **TBD:** Specific test requirements to be confirmed.

**Rationale:** See `Guidance.md § Principles (Proof Load Testing)`.
**Verification:** See `Procedure.md § Step 4` (perform and record proof load tests); `Procedure.md § Step 5` (verify test pass).

### 3) Interface / Coordination Requirements

**Tag consistency is critical across all project deliverables:**
- Equipment tags in records shall align with:
  - **DEL-09.01 drawings:** Tags shown on drawings
  - **DEL-09.04 data sheets:** Tags used in data sheets
  - **Project asset tagging convention:** Tags used in facility asset management system (**TBD** — asset tagging system to be confirmed)
- **As-installed verification:** Records shall confirm that installed equipment matches DEL-09.04 data sheet specifications (manufacturer, model, capacity, materials, dimensions).
- **Coordination mode:** Dependencies are managed externally (NOT_TRACKED). See `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.

**Verification:** See `Procedure.md § Step 5` (verify tag alignment and as-installed vs as-designed).

### 4) Quality / Traceability Requirements

**Record attributes (per `Guidance.md § Principles (Evidence Rules)`):**
- Each record shall be:
  - **Attributable:** Who performed, inspected, witnessed (names, titles, signatures)
  - **Dated:** When inspection/test occurred (date and time)
  - **Located:** Which equipment/tag/location (unique identification)
  - **Legible:** Clear, complete, unambiguous (handwritten entries legible; signatures identifiable)
  - **Revision-controlled:** Per project document control procedures (records typically non-revisable once issued; supplemental records or NCRs used for changes)

**Hold and witness point requirements:**
- Hold and witness point records shall show required signatures per ITP (**TBD** — project ITP to define hold/witness points).
- **Hold point:** Work shall not proceed without required signature (typically QA/QC inspector or Employer's representative).
- **Witness point:** Witness shall be notified; work may proceed if witness not available, but notification and outcome documented.

**NCR management:**
- NCRs shall be logged in NCR register with:
  - NCR number, equipment tag, date issued
  - Nonconformance description
  - Disposition (use-as-is, repair, replace, scrap) with justification
  - Corrective action (if repair or replace)
  - Closure verification (re-inspection, acceptance)
  - Sign-off (QA/QC manager or authorized representative)
- NCR status summary shall be included in records package (open NCRs listed with status and planned closure date).

**Verification:** See `Procedure.md § Step 5` (verify signatures and NCR status).

## Standards

**Applicable standards and codes (to be confirmed from Employer's Requirements and regulatory approvals):**

- Employer's Requirements (Vol 2 Part 1–3) — applicable clauses **TBD** (see `_REFERENCES.md`); QA/QC requirements, record content, hold/witness points.
- **ASSUMPTION:** Testing/inspection standards, which may include:
  - Proof load testing per applicable marine/port design codes (BS 6349, PIANC, local port authority requirements)
  - Visual inspection per industry standards
  - Torque verification per fastener specifications or AWS standards
  - Coating inspection per SSPC/NACE standards (if coating touch-up performed)
  - Grouting per ACI standards or manufacturer instructions

**Code compliance verification:** Per `Procedure.md § Step 5` (verify completeness and acceptance).

## Verification

**Verification methods for Record deliverables (per `Procedure.md`):**

| Method | Applicability | Criteria | Procedure § |
|--------|---------------|----------|-------------|
| Completeness check | All records | All required records per matrix are present; all record fields complete | Proc § Step 5 |
| Data accuracy verification | All records | Recorded values are reasonable and complete; measurements within expected ranges | Proc § Step 5 |
| Signature verification | Witness/hold points | Required signatures are present (installer, inspector, witness per ITP) | Proc § Step 5 |
| Tag alignment check | All records | Equipment tags match DEL-09.01 drawings and DEL-09.04 data sheets; no discrepancies | Proc § Step 5 |
| As-installed vs as-designed verification | All records | Installed equipment matches DEL-09.04 data sheet specs (manufacturer, model, capacity, materials); deviations documented in NCRs | Proc § Step 5 |
| Test pass verification | Proof load tests | All proof load tests demonstrate pass vs acceptance criteria (no failures or unresolved NCRs) | Proc § Step 5 |
| NCR status verification | All records | NCRs closed with disposition evidence or listed as open with status and corrective action plan | Proc § Step 5 |
| Archival format compliance | All records | Per project document control and retention requirements | Proc § Step 7 |

**Acceptance criteria (per `Datasheet.md § Acceptance`):**
- Records package is complete per the records matrix (all required records present).
- All required signatures are present (installer, inspector, witness per ITP).
- All proof load tests (where required) demonstrate pass.
- Equipment tags align with DEL-09.01 drawings and DEL-09.04 data sheets.
- As-installed equipment verified to match DEL-09.04 data sheet specifications.
- Outstanding NCRs are listed with status and corrective actions (or all NCRs closed).

## Documentation

**Required documentation outputs (per decomposition and `Datasheet.md`):**
- Installation records (fenders, bollards, ladders, life-saving equipment, Berth 10 upgrades/repairs)
- Proof load test records (bollards if required; other tests as applicable)

**Documentation requirements:**
- All documents shall comply with project document control procedures.
- Revision control per project numbering system — **TBD** (**Note:** Records typically non-revisable once issued; supplemental records or NCRs used for changes).
- Format: **TBD** — **ASSUMPTION:** Per project document management requirements; PDF for archival; scanned originals if paper forms used; electronic forms preferred.
- Retention: **TBD** — **ASSUMPTION:** Permanent retention for as-built project record and regulatory compliance evidence.
- Records management per `Procedure.md § Records`.
