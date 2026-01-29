# Guidance: DEL-26.02 Coating Procedures

## Purpose

This guidance document supports the development and use of **Coating Procedures** for **PKG-26 Protective Coatings & Painting**.

**Deliverable purpose:** Define execution methods and controls for surface preparation and coating application to meet safety, quality, and operational requirements specified in DEL-26.01 (Coating Technical Specification).

**Source:** Decomposition DEL-26.02 description; `_CONTEXT.md`

**Deliverable classification:**
- **Type:** Procedure
- **Discipline:** Coatings
- **Responsible:** D&B Contractor
- **Source:** `_CONTEXT.md`

**Relationship to other PKG-26 deliverables:**
- **DEL-26.01** (Coating Technical Specification) defines WHAT (coating systems, standards, requirements, acceptance criteria)
- **DEL-26.02** (Coating Procedures — this deliverable) defines HOW (execution methods and controls to meet DEL-26.01 requirements)
- **DEL-26.03** (Coating Data Sheet Package) provides manufacturer data sheets referenced by procedures
- **DEL-26.04** (Coating Installation & Test Records) provides record templates used by procedures
- **Source:** Decomposition Section 5; Datasheet.md

**Project objectives supported:**
- **OBJ-1:** Safe & Reliable Operation — Procedures ensure safe coating application with appropriate safety controls (confined space, respiratory protection, fall protection)
- **OBJ-3:** Storage Capacity (45,000 MT) — Tank internal coating procedures maintain food-grade integrity without compromising storage capacity
- **OBJ-9:** Lifecycle Cost Optimization — Proper application procedures ensure coating durability and lifecycle performance (avoiding premature failures and rework)
- **Source:** Decomposition Section 6; Datasheet.md

## Principles

### Engineering Rationale

**Why Rigorous Procedures Are Essential:**

Protective coating performance is highly sensitive to application quality. Unlike many engineered systems where performance is primarily determined by design and materials, coating systems depend critically on surface preparation and application execution. Poor application practices can reduce coating service life by 50% or more, even with the best coating materials.

**Source:** **ASSUMPTION** — Industry experience; coating performance literature

**Three Pillars of Coating Quality:**

1. **Surface Preparation Quality:**
   - The coating-to-substrate bond is the foundation of all coating performance
   - Surface preparation creates mechanical anchor (profile) and chemical bond (cleanliness)
   - SSPC standards define cleanliness (removal of contaminants, rust, mill scale) and profile (surface roughness for mechanical anchor)
   - Inadequate surface preparation is the most common cause of coating failure (adhesion loss, under-film corrosion)
   - **Source:** SSPC standards; **ASSUMPTION** — Coating failure analysis data

2. **Application Environment Control:**
   - Coatings cure through chemical reactions sensitive to temperature and humidity
   - Dew point control prevents moisture contamination during application and cure
   - Temperature affects viscosity, atomization (spray), and cure rate
   - Out-of-specification application conditions cause defects (poor adhesion, pinholing, slow cure, solvent entrapment)
   - **Source:** DEL-26.01 (PR-6 Application Conditions); manufacturer data sheets; **ASSUMPTION** — Coating chemistry principles

3. **Application Quality Control:**
   - Dry film thickness (DFT) directly affects corrosion protection and service life
   - Insufficient DFT reduces protection; excessive DFT can cause cracking or sagging
   - In-process quality control (WFT measurement, visual inspection) prevents defects from progressing
   - Hold points ensure non-conforming work is caught before additional coating or acceptance
   - **Source:** DEL-26.01 (QR-1 Inspection and Testing); SSPC-PA 2; **ASSUMPTION** — Quality management principles

**Procedures as Quality Control Tools:**

Well-written procedures:
- Standardize work methods and reduce variability
- Define critical control points and hold points
- Ensure personnel know what to do, how to do it, and when to stop for inspection
- Provide traceability (record what was done, when, and under what conditions)
- Support training and competency verification

**Source:** **ASSUMPTION** — Quality management principles

### Surface Preparation Quality

**SSPC Surface Preparation Standards:**

SSPC standards define both cleanliness (removal of contaminants) and profile (surface roughness):
- **SSPC-SP 5 (White Metal Blast):** Highest cleanliness, for critical immersion service
- **SSPC-SP 10 (Near-White Blast):** High cleanliness, for demanding atmospheric service and food-contact coatings
- **SSPC-SP 6 (Commercial Blast):** Moderate cleanliness, for general atmospheric service
- **SSPC-SP 1 (Solvent Cleaning):** Removes oil and grease, required before blasting
- **SSPC-SP 3, SP-11 (Power Tool Cleaning):** For touch-up and repair where blasting is impractical

**Source:** SSPC standards; DEL-26.01 (PR-5 Surface Preparation)

**Surface Profile:**

Surface profile (roughness) provides mechanical anchor for coating adhesion:
- Profile depth should match coating system (typically 1.5–2.5 mils for epoxy systems, higher for high-build coatings)
- Profile created by abrasive selection (abrasive type and size)
- Excessive profile wastes coating (fills deep valleys); insufficient profile reduces adhesion
- Measured per ASTM D4417 or SSPC-PA 17

**Source:** ASTM D4417; **ASSUMPTION** — Coating application best practices

**Confined Space Considerations (Tank Internals):**

Tank internal coating presents unique surface preparation challenges:
- **Access:** Limited access through manholes requires specialized equipment (vacuum blast systems, portable compressors)
- **Containment:** Blast abrasive and dust containment within confined space
- **Ventilation:** Adequate ventilation for dust control and respiratory protection
- **Safety:** Confined space entry protocols, rescue procedures, air monitoring
- Procedures must address these constraints while achieving required SSPC standards

**Source:** Datasheet.md (Hazardous Area and Safety Context); **ASSUMPTION** — Confined space coating practice

### Application Quality Control

**Dry Film Thickness (DFT) Control:**

DFT is the single most important application quality parameter:
- **Target DFT:** Specified in DEL-26.01 per coating system (e.g., 10-16 mils for tank internals, 9-14 mils total for multi-coat atmospheric systems)
- **DFT measurement:** Per SSPC-PA 2 using magnetic gages (non-destructive)
- **WFT measurement:** Wet film thickness measured during application to control dry film thickness (WFT × % solids = DFT)
- **Acceptance:** Typically specified as minimum DFT with allowable distribution (e.g., no individual reading below minimum, average above target)

**Source:** DEL-26.01 (PR-4 DFT); SSPC-PA 2; **ASSUMPTION** — DFT specification practice

**Inter-Coat Timing:**

Multi-coat systems require careful timing between coats:
- **Minimum recoat time:** Allow previous coat to cure sufficiently to support next coat (per manufacturer data sheet)
- **Maximum recoat window:** Apply next coat before previous coat fully cures to achieve chemical bond (per manufacturer data sheet)
- Exceeding maximum recoat window requires surface preparation (sanding/abrading) before next coat
- Environmental conditions affect cure rate and recoat windows

**Source:** Manufacturer data sheets; **ASSUMPTION** — Multi-coat application practice

**Holiday Detection (Immersion Service):**

Holiday (pinhole) detection required for coatings in immersion service (tank internals, marine immersion zones):
- **Purpose:** Detect pinholes, holidays, and defects that allow moisture/corrosive fluid to reach substrate
- **Methods:**
  - Low-voltage wet sponge (for thin coatings, typically < 20 mils DFT)
  - High-voltage holiday detector (for thicker coatings, typically > 20 mils DFT)
- **Frequency:** Typically 100% coverage for immersion service
- Detected holidays must be repaired and re-inspected

**Source:** DEL-26.01 (QR-1 Inspection and Testing); **ASSUMPTION** — Holiday detection practice

### Environmental Sensitivity

**Dew Point Control:**

Dew point is the temperature at which moisture condenses from air onto the surface:
- **Minimum surface temperature:** Typically minimum 3°C (5°F) above dew point to prevent condensation
- **Moisture contamination effects:** Reduced adhesion, pinholing, blistering, under-film corrosion
- **Monitoring:** Measure ambient temperature, relative humidity, and surface temperature; calculate dew point
- **Control:** Delay coating if surface temperature approaches dew point; use heating or dehumidification if needed

**Source:** DEL-26.01 (PR-6 Application Conditions); **ASSUMPTION** — Dew point control practice

**Temperature Effects:**

Ambient temperature affects coating application and cure:
- **Low temperature:** Increases viscosity (poor atomization, difficulty achieving specified DFT), slows cure, risk of condensation
- **High temperature:** Decreases pot life, rapid solvent evaporation (dry spray, poor flow), rapid cure (reduced recoat window)
- **Manufacturer limits:** Typically 50°F (10°C) minimum, 90°F (32°C) maximum, but varies by coating type

**Source:** DEL-26.01 (PR-6 Application Conditions); manufacturer data sheets; **ASSUMPTION** — Temperature effects on coatings

**BC Coastal Climate Considerations:**

Fraser Surrey Terminal location presents seasonal application challenges:
- **Winter (Nov–Mar):** Wet, cool conditions; high humidity and low temperatures challenge dew point control; shop coating preferred for critical work
- **Summer (Jun–Sep):** Dry, warm conditions; favorable for field coating
- **Spring/Fall (Apr–May, Oct):** Transitional; variable conditions require careful environmental monitoring
- **Planning implications:** Schedule critical coating work (especially tank internals) during favorable weather or provide environmental controls (tenting, heating, dehumidification)

**Source:** **ASSUMPTION** — BC coastal climate; Datasheet.md (Environmental Conditions — Seasonal constraints)

### Worker Safety

**Confined Space Entry (Tank Internals):**

Tank internal coating is high-risk work requiring confined space entry protocols:
- **Hazards:** Oxygen deficiency, toxic atmospheres (coating solvents), fire/explosion (flammable coatings), falls, engulfment
- **Controls:**
  - Confined space entry permit per WorkSafeBC and PKG-33 procedures
  - Air monitoring (oxygen, LEL, toxics) before entry and continuous during work
  - Ventilation (forced air supply or exhaust)
  - Attendant stationed outside confined space
  - Rescue equipment and procedures
  - **Source:** Datasheet.md (Hazardous Area and Safety Context); WorkSafeBC; PKG-33 (HSE Management)

**Respiratory Protection:**

Coating application generates airborne contaminants requiring respiratory protection:
- **Abrasive blasting:** Dust and silica (if silica abrasive used) — full facepiece supplied air or powered air-purifying respirator (PAPR)
- **Coating application (spray):** Coating mist and solvent vapors — half-mask or full-facepiece organic vapor respirator (minimum); supplied air for confined spaces or high-exposure work
- **Confined space:** Supplied air mandatory
- **Source:** Datasheet.md (Safety and Environmental Controls); WorkSafeBC; **ASSUMPTION**

**Other Safety Controls:**

- **Fall protection:** Required for elevated work (platforms, scaffolds, tanks)
- **Fire prevention:** Flammable coating storage, hot work control, ventilation, fire extinguishers
- **Hearing protection:** Required for abrasive blasting (high noise levels)
- **Eye protection:** Required for all coating work
- **Source:** Datasheet.md (Safety and Environmental Controls); WorkSafeBC; PKG-33 (HSE Management)

## Considerations

### Procedure Development Factors

**1. Application-Specific Procedures:**

Procedures should be tailored to specific applications rather than generic:
- **Tank internal coatings:** Confined space entry, food-grade requirements, specialized equipment, holiday detection
- **Tank external coatings:** Access (scaffolding or lifts), weather protection, multi-coat systems
- **Structural steel coatings:** Shop vs. field coordination, large areas, weather exposure
- **Marine coatings:** Tidal access, immersion/splash zone demarcation, specialized systems

Application-specific procedures provide relevant detail and avoid clutter from inapplicable information.

**ASSUMPTION:** Best practice for procedure usability

**2. Shop vs. Field Considerations:**

Shop coating and field coating have different constraints:
- **Shop coating:**
  - Controlled environment (temperature, humidity, cleanliness)
  - Better access to equipment (blast rooms, spray booths, material handling)
  - Higher quality potential
  - Requires protection during shipping and handling
- **Field coating:**
  - Weather-dependent (temperature, humidity, precipitation, wind)
  - Limited equipment access
  - Quality challenges (environmental control, dust/contamination)
  - In-place application (no handling damage)

Procedures must address the specific constraints and controls for each application environment.

**Source:** DEL-26.01 (Guidance — Trade-offs — Shop vs. Field); **ASSUMPTION**

**3. Hold Points and Inspection Frequency:**

Critical decision: How much inspection is required?
- **100% inspection:** For critical applications (tank internals, marine immersion) — all surfaces inspected and tested
- **Spot inspection:** For less critical applications (structural steel atmospheric) — random sampling at specified frequency
- **Hold points:** Define where work must stop for inspection and acceptance before proceeding

**Trade-off:** More inspection improves quality and traceability but increases cost and schedule. Less inspection reduces cost but increases risk of undetected defects.

**Guidance:** Use 100% inspection for:
- Tank internals (food-contact, immersion service)
- Marine immersion zones
- High-consequence coatings (difficult to repair or replace)

Use spot inspection (with sufficient frequency) for:
- Structural steel atmospheric coatings
- Accessible areas where repair is practical

**ASSUMPTION:** Risk-based inspection approach

**4. Environmental Monitoring and Control:**

Decisions required for environmental control strategy:
- **Passive monitoring:** Measure conditions and delay work if out of spec (lowest cost, weather-dependent schedule)
- **Active control:** Provide environmental controls (tenting, heating, dehumidification) to enable work in adverse conditions (higher cost, schedule certainty)

**Guidance:** Use active controls for:
- Critical work that cannot be delayed (schedule-critical path)
- Confined space work (tank internals) where natural ventilation is insufficient
- Out-of-season work (winter coating in BC climate)

Use passive monitoring for:
- Non-critical work with schedule flexibility
- Favorable seasonal conditions (summer coating)

**ASSUMPTION:** Cost-schedule-risk trade-off

**5. Training and Competency:**

Procedures are only effective if personnel are competent to execute them:
- **Training:** Review procedures with personnel before use; hands-on training for complex procedures (confined space entry, specialized equipment)
- **Competency verification:** Verify understanding of critical steps, hold points, safety requirements
- **Qualifications:** Verify industry certifications or equivalent (NACE/AMPP coating inspector, SSPC coating applicator)

Procedures should be written for the expected competency level of users (avoid assuming expert knowledge; provide sufficient detail for trained technicians).

**Source:** Specification.md (QR-2 Competency and Training); **ASSUMPTION**

### Coordination Points

**DEL-26.01 (Coating Technical Specification):**
- Procedures must implement all requirements from DEL-26.01 (coating systems, surface prep standards, DFT, acceptance criteria)
- Any deviation from DEL-26.01 requirements requires specification revision or approved variance
- **Source:** Specification.md (IR-1)

**DEL-26.03 (Coating Data Sheet Package):**
- Procedures reference manufacturer data sheets for coating-specific parameters (pot life, mixing, environmental limits, cure times, recoat windows)
- Manufacturer data sheets are authoritative source for product-specific application requirements
- **Source:** Specification.md (IR-2)

**DEL-26.04 (Coating Installation & Test Records):**
- Procedures use record templates from DEL-26.04 for consistent documentation
- Procedures define what records are completed and when (during surface prep, during application, at hold points, at final acceptance)
- **Source:** Specification.md (IR-3)

**PKG-33 (HSE Management):**
- Coating procedures must comply with project HSE procedures:
  - Confined space entry procedures
  - Hot work permit procedures
  - Respiratory protection program
  - Fall protection procedures
  - Environmental controls (VOC management, waste disposal)
- Coordinate procedure development with HSE personnel
- **Source:** Specification.md (IR-4); Datasheet.md (Cross-references)

**PKG-13 (Storage Tanks):**
- Tank internal coating procedures coordinate with tank design for access (manhole size, spacing, internal appurtenances)
- Tank internal coating procedures coordinate with tank fabrication and construction schedule
- **Source:** Datasheet.md (Cross-references)

**PKG-30 (Commissioning):**
- Tank internal coating acceptance procedures coordinate with commissioning (food-grade cleanliness verification before product loading)
- **Source:** Datasheet.md (Cross-references)

## Trade-offs

### 1. Procedure Detail vs. Flexibility

**Trade-off:** Detailed step-by-step procedures provide clarity and reduce variability, but can be rigid and difficult to adapt to field conditions. Flexible performance-based procedures allow adaptation but require more user judgment.

**Considerations:**
- **Prescriptive procedures (detailed steps):** Appropriate for:
  - Critical work with low tolerance for variation (tank internal coatings)
  - Complex procedures with many steps (confined space entry + blasting + coating)
  - Less experienced personnel
- **Performance-based procedures (define outcomes, allow methods flexibility):** Appropriate for:
  - Experienced personnel
  - Variable field conditions requiring adaptation
  - Non-critical work

**Guidance:** Use prescriptive procedures for tank internal coatings (critical, confined space, food-grade). Use moderate detail for other applications (define critical controls and hold points, allow some methods flexibility).

**ASSUMPTION:** Procedure design trade-off

### 2. Generic vs. Application-Specific Procedures

**Trade-off:** Generic procedures cover multiple applications in a single document (fewer documents to manage), but may be cluttered with inapplicable information. Application-specific procedures are targeted and easier to use, but create more documents to manage.

**Recommendation:** Use application-specific procedures for PKG-26:
- Surface Preparation Procedure for Tank Internals
- Surface Preparation Procedure for Tank Externals and Structural Steel
- Surface Preparation Procedure for Marine Structures
- Coating Application Procedure for Tank Internals (Food-Grade Coatings)
- Coating Application Procedure for Tank Externals and Structural Steel
- Coating Application Procedure for Marine Structures and Loading Equipment

Rationale: Application-specific procedures improve usability and reduce risk of error (user applies wrong procedure for the application). Number of procedures is manageable (6–8 procedures total).

**ASSUMPTION:** Procedure organization trade-off

### 3. Procedure Verification vs. Schedule

**Trade-off:** Rigorous procedure verification (walkthrough, safety review, trial run) improves procedure quality and reduces execution risk, but requires time and resources. Minimal verification (document review only) is faster but risks procedural errors or safety hazards during execution.

**Recommendation:**
- **Full verification (walkthrough + safety review + trial run if practical):** For tank internal coating procedures (high safety risk, food-grade critical application)
- **Standard verification (walkthrough + safety review):** For other coating procedures (moderate risk)
- **Minimal verification (document review):** Not recommended for any coating procedure (high consequence of procedural error)

**ASSUMPTION:** Verification rigor trade-off

### 4. Shop Coating vs. Field Coating

**Trade-off:** (Already discussed in DEL-26.01 Guidance; reiterated here for procedure context)

Shop-applied coatings offer better quality control but require field touch-up and protection during handling. Field-applied coatings avoid handling damage but have environmental and quality challenges.

**Procedure implications:**
- **Shop coating procedures:** Emphasize quality (high DFT uniformity, 100% inspection) and protection for shipping (packaging, touch-up procedures)
- **Field coating procedures:** Emphasize environmental monitoring, surface cleanliness (dust control), and adaptive controls for weather conditions

**Source:** DEL-26.01 (Guidance — Trade-offs — Shop vs. Field); **ASSUMPTION**

## Examples

### Procedure Structure Example (Illustrative)

**Example: Surface Preparation Procedure for Tank Internals (SSPC-SP 10)**

1. **Purpose:** Prepare tank internal surfaces to SSPC-SP 10 (near-white blast cleaning) per DEL-26.01 requirements for application of food-grade coating system.

2. **Scope:** Applies to interior surfaces of canola oil storage tanks (3 × 15,000 MT tanks per PKG-13).

3. **Prerequisites:**
   - Tank fabrication complete and ready for coating
   - Confined space entry permit obtained
   - Equipment and materials available (blast equipment, abrasive, air supply, ventilation, lighting, PPE)
   - Personnel trained and competent (blasters, attendant, inspector)

4. **Equipment and Materials:**
   - Blast equipment (vacuum blast system or blast pot with dust collector)
   - Abrasive (coal slag or equivalent, size per profile requirement)
   - Air supply (compressor, hoses)
   - Ventilation equipment (forced air supply or exhaust)
   - Lighting (portable explosion-proof lighting for confined space)
   - PPE (supplied air respirator, hearing protection, protective clothing)

5. **Safety and PPE:**
   - Confined space entry permit active
   - Air monitoring (oxygen ≥ 19.5%, LEL < 10%, no toxic gases)
   - Continuous ventilation during work
   - Supplied air respiratory protection for blasters
   - Attendant stationed outside tank (continuous communication with blasters)
   - Rescue equipment ready (tripod, winch, harness)
   - Hearing protection
   - Eye protection
   - Protective clothing (blast suit)

6. **Steps:**
   1. Inspect tank interior for oil, grease, and contaminants; perform solvent cleaning per SSPC-SP 1 if needed
   2. Set up ventilation and verify airflow adequate for dust control and respiratory protection
   3. Set up blast equipment and verify functionality (air pressure, abrasive flow)
   4. Verify air monitoring and confined space entry controls active
   5. Perform abrasive blast cleaning to SSPC-SP 10 standard (near-white blast — minimum 95% removal of visible rust, mill scale, and coatings)
   6. Remove blast abrasive and dust from tank (vacuum or sweep)
   7. **HOLD POINT:** Notify inspector for surface preparation inspection

7. **Quality Control and Hold Points:**
   - **Hold point:** Surface preparation inspection before coating application
   - **Inspection:** Visual inspection per SSPC-VIS 1 (compare to SSPC-SP 10 visual standard)
   - **Profile measurement:** Measure surface profile per ASTM D4417 (target 1.5–2.5 mils for epoxy coating)
   - **Acceptance criteria:**
     - Surface cleanliness: SSPC-SP 10 (near-white blast, ≥ 95% clean)
     - Surface profile: 1.5–2.5 mils (per DEL-26.01)
   - **Non-conformance:** Re-blast areas not meeting acceptance criteria; re-inspect

8. **Documentation:**
   - Complete Surface Preparation Record (form per DEL-26.04):
     - Date and time of surface preparation
     - Environmental conditions (temperature, humidity)
     - Abrasive type and size
     - Surface cleanliness verification (SSPC-SP 10 achieved)
     - Surface profile measurement
     - Inspector name and signature
     - Acceptance for coating application (yes/no)

9. **References:**
   - DEL-26.01 Coating Technical Specification (surface prep requirements, acceptance criteria)
   - SSPC-SP 10: Near-White Blast Cleaning
   - SSPC-VIS 1: Visual Standard for Abrasive Blast Cleaned Steel
   - ASTM D4417: Surface Profile Measurement
   - PKG-33 Confined Space Entry Procedure

**Source:** **ASSUMPTION** — Illustrative procedure structure; not actual project procedure

### Anticipated Artifacts (Final Procedure Documents)

Per Decomposition DEL-26.02, this deliverable shall produce:

1. **Surface Preparation Procedures** (multiple procedures by application):
   - Tank internals (SSPC-SP 10 or SP-5)
   - Tank externals and structural steel (SSPC-SP 6 or SP-10)
   - Marine structures (SSPC-SP 10)
   - Touch-up and repair (power tool cleaning, SSPC-SP 3 or SP-11)
   - Solvent cleaning (SSPC-SP 1 as prerequisite)

2. **Coating Application Procedures** (multiple procedures by application):
   - Tank internal coating application (food-grade epoxy phenolic or equivalent)
   - Tank external coating application (multi-coat epoxy/polyurethane system)
   - Structural steel coating application (zinc-rich epoxy primer + intermediate + topcoat)
   - Marine coating application (high-build epoxy or marine system)
   - Field touch-up and repair

**Source:** Decomposition DEL-26.02 anticipated artifacts; Specification.md (Documentation section)

These procedures shall be formatted per project procedure template and reviewed/approved per project quality procedures (Procedure.md).
