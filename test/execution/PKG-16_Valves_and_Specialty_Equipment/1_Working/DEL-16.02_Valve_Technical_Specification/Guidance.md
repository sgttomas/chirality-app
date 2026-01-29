# Guidance: DEL-16.02 Valve Technical Specification

## Purpose

This guidance document supports the development of **Valve Technical Specification** for **PKG-16 Valves & Specialty Equipment**.

**Deliverable Purpose:** Defines performance, materials, and workmanship requirements for valves per ER requirements for the Canola Oil Transload Facility.

**Source:** `_CONTEXT.md`

**Deliverable Classification:**
- **Type:** Specification (Technical/Procurement)
- **Discipline:** Mechanical
- **Responsible Party:** D&B Contractor

**Project Context:**
This deliverable supports **OBJ-1: Safe & Reliable Operation** by establishing valve procurement requirements that ensure suitable valve performance, materials, and quality for safe and reliable facility operation.

**Source:** Decomposition document Section 6 (Objective-to-Deliverable Mapping), OBJ-1 includes PKG-16 (DEL-16.01–DEL-16.05)

## Principles

**Engineering Rationale:**

**1. Purpose of Technical Specifications**

Technical specifications serve multiple functions in EPC projects:

- **Procurement Basis:** Provides vendors with complete technical requirements for bidding and fabrication
- **Quality Standard:** Defines acceptance criteria for inspection and testing
- **Contract Document:** Forms part of purchase order; legally binding requirements
- **Communication Tool:** Ensures common understanding between contractor, employer, and vendors

**Source:** General principles of technical specification development

**2. Specification Philosophy for Valve Procurement**

**Performance-Based vs. Prescriptive Specifications:**

- **Performance-Based:** Specifies required performance (flow capacity, pressure drop, leakage class) but allows vendor flexibility in design details
  - **Advantages:** Encourages innovation, leverages vendor expertise, potentially lower cost
  - **Disadvantages:** Requires careful verification, may result in non-standard designs

- **Prescriptive:** Specifies exact valve type, materials, dimensions, and design features
  - **Advantages:** Ensures consistency, simplifies spare parts management, reduces vendor variability
  - **Disadvantages:** May be more expensive, limits vendor options, may miss better alternatives

**Guidance:** Use hybrid approach — specify performance requirements (pressure, temperature, flow, leakage) and prescribe critical features (materials, flange ratings, actuation type) while allowing vendor flexibility in non-critical details.

**Source:** Typical specification philosophy for valve procurement; specific approach TBD per project procurement strategy

**3. Materials Selection Principles**

**Material Selection for CSD Canola Oil Service:**

Canola oil is a vegetable oil with specific material compatibility considerations:

- **Compatibility:** Canola oil is generally non-corrosive to most metals, but food-grade service requires cleanable, non-contaminating materials
- **Stainless Steel (316SS or 304SS):** Preferred for product-contact valves
  - **Advantages:** Corrosion-resistant, smooth surface finish, food-grade acceptable, suitable for coastal environment
  - **Disadvantages:** Higher cost than carbon steel
- **Carbon Steel:** Acceptable for non-product services (nitrogen, utilities) or product service with internal coating
  - **Advantages:** Lower cost
  - **Disadvantages:** Requires coating for product contact; susceptible to corrosion in coastal environment
- **Gasket Materials:** PTFE, RTFE, or EPDM (food-grade elastomers); avoid materials that may leach into product

**Temperature Considerations:**
- Canola oil solidifies at low temperatures (pour point approximately -10°C)
- Product lines may require heating (steam tracing, electric heat tracing) to maintain pumpability
- Valve body design should accommodate heating provisions where required

**Source:** Material selection principles for food-grade vegetable oil service; pour point **ASSUMPTION** based on typical canola oil properties

**4. Control Valve Selection Principles**

**Control Valve Sizing and Selection:**

Control valve selection involves balancing multiple factors:

- **Valve Type:**
  - **Globe valves:** Best for throttling control, high pressure drop capability, characterized trim
  - **Ball valves:** Good for on-off or wide-open service, lower pressure drop, V-ball for control
  - **Butterfly valves:** Large sizes, low pressure drop, limited rangeability

- **Flow Characteristic:**
  - **Equal Percentage:** Most common; provides good control across wide flow range
  - **Linear:** Constant gain across flow range; suitable for level control
  - **Quick-Opening:** Primarily for on-off service

- **Rangeability:** Ratio of maximum to minimum controllable flow; typically 50:1 for good control valves

- **Cavitation and Flashing:** Less concern for viscous canola oil, but verify for high-pressure drop applications

**Actuator Sizing:**
- Size actuator for maximum expected differential pressure (not normal operating ΔP)
- Include safety factor (typically 1.5× calculated torque/thrust)
- Consider failure mode (spring-return requires larger actuator for fail-closed mode)

**Source:** Control valve selection principles per ISA-75 series standards; specific selections TBD pending control philosophy and sizing calculations (DEL-16.03)

**5. Relief Valve Principles**

**Pressure Relief Valve Sizing and Selection:**

Relief valves are safety-critical devices subject to strict code requirements:

- **Sizing Basis (per API 520/521 and ASME Section VIII):**
  - Fire case (external fire scenario)
  - Blocked outlet (thermal expansion)
  - Cooling failure (loss of cooling)
  - Runaway reaction (not applicable to canola oil storage)
  - Control valve failure (overpressure from upstream)

- **Set Pressure:**
  - Typically set at MAWP (Maximum Allowable Working Pressure) or slightly below
  - Must not exceed vessel MAWP when accounting for overpressure allowance (10% for single relief, 16% for multiple reliefs per ASME Section VIII)

- **Capacity Certification:**
  - ASME stamped (UV or "V" stamp) required for code compliance
  - National Board Registration required in some jurisdictions

- **Discharge Arrangement:**
  - Must discharge to safe location away from personnel, platforms, and ignition sources
  - Consideration of reaction forces on discharge piping
  - Back pressure effects on relief valve capacity

**Source:** Relief valve sizing and selection principles per API 520/521 and ASME Section VIII; specific sizing TBD pending DEL-16.03 (Valve Design Calculations)

**Applicable Standards Context:**

**Key Valve Standards:**
- **API 600/6D:** Minimum design requirements for gate and ball valves (pressure-temperature ratings, materials, end connections, testing)
- **API 526/527:** Relief valve design, set pressure tolerance (±3 psi or ±2%), seat tightness requirements
- **API 598:** Valve pressure testing and seat leakage testing (shell test, seat test, visual examination)
- **IEC 60534 (ISA-75):** Control valve sizing equations, flow characteristics, performance testing
- **ASME B16.34:** Pressure-temperature ratings for valves by material group

**Canadian Regulatory Context:**
- **CSA B51:** Governs pressure-retaining equipment in BC; relief valves on registered vessels must comply with ASME BPVC
- **Transport Canada:** Requirements for pressure equipment on rail cars (relevant to railcar unloading valves)

**Source:** Standards inferred from valve scope; applicability to be confirmed during specification development

## Considerations

**Factors to consider during specification development:**

**1. Project-Specific Factors**

- **Package Scope:** PKG-16 covers control valves, isolation valves, relief valves, strainers, specialty items
- **Facility Type:** Transload facility (railcar to storage to ship) — diverse valve applications
- **Throughput:** 1,000,000 MT/annum — valve sizing must support design flow rates
- **Location:** Fraser Surrey Terminal — coastal environment requires corrosion protection
- **Product:** CSD canola oil — food-grade cleanliness, viscosity considerations, temperature control

**Source:** Decomposition document Sections 1.1 and 5 (PKG-16 scope)

**2. Procurement Strategy**

- **Single Source vs. Multi-Source:** Balance standardization (single vendor) vs. competition (multiple vendors)
- **Bid Package Structure:** Separate packages per valve category vs. combined package for all valves
- **Pre-Qualification:** Vendor pre-qualification criteria (experience, quality system, delivery capability)
- **"Or Equal" Provisions:** Allow vendor alternates to specified brands/models subject to approval

**Source:** Typical procurement considerations for valve specifications; specific strategy TBD per project procurement plan

**3. Standardization vs. Optimization**

- **Standardization Benefits:** Reduces spare parts inventory, simplifies maintenance training, leverages volume pricing
- **Optimization Benefits:** Right-sizes each valve, may reduce cost per valve, better performance for specific applications

**Guidance:** Standardize where practical (common valve sizes, actuator types, positioners) but optimize critical valves (large control valves, relief valves).

**4. Lifecycle Cost Considerations**

Valve specifications should consider total cost of ownership, not just initial capital cost:

- **Operating Cost:** Energy consumption (pressure drop through valves affects pumping power)
- **Maintenance Cost:** Frequency of maintenance, spare parts availability, repair complexity
- **Reliability:** High-reliability valves reduce unplanned downtime
- **Design Life:** Specify design life consistent with facility design life (25 years typical) to avoid premature replacement

**Source:** Lifecycle cost principles; aligns with **OBJ-9: Lifecycle Cost Optimization** from decomposition Section 6

**5. Quality and Testing Requirements**

Balance quality assurance rigor with cost and schedule:

- **Factory Acceptance Testing (FAT):** Mandatory for critical valves (relief valves, large control valves, ESDs); optional for standard isolation valves
- **Witness Hold Points:** Identify which tests require Employer or contractor witness (relief valve set pressure test, control valve stroking test)
- **Third-Party Inspection:** Consider third-party inspection for critical valves to provide independent verification

**6. Documentation Requirements**

Specify documentation needed for operation, maintenance, and regulatory compliance:

- **O&M Manuals:** Detailed operation and maintenance instructions for each valve type
- **Spare Parts Lists:** Identify recommended spare parts for commissioning and ongoing maintenance
- **Test Certificates:** Pressure test certificates, seat test certificates, relief valve set pressure certificates
- **Material Certificates:** Material test reports (MTRs) for pressure-retaining components

**7. Schedule Considerations**

Valve procurement lead times vary significantly:

- **Standard Valves:** 8–12 weeks typical for gate/ball/butterfly valves
- **Control Valves:** 12–16 weeks typical (longer for large or special trim)
- **Relief Valves:** 10–14 weeks typical (longer if ASME stamping required)
- **Specialty Valves:** 16–24+ weeks (custom designs, exotic materials)

**Guidance:** Issue specifications early to enable long-lead procurement. Consider specifying readily available valve models to reduce lead times.

**Source:** Typical valve procurement lead times; specific durations TBD per project schedule

## Trade-offs

**Competing concerns to evaluate:**

**1. Material Selection: Stainless Steel vs. Carbon Steel**

| Factor | Stainless Steel (316SS) | Carbon Steel (with coating) |
|--------|-------------------------|------------------------------|
| **Cost** | Higher capital cost (~2–3× carbon steel) | Lower capital cost |
| **Corrosion Resistance** | Excellent (coastal environment) | Requires coating; coating may degrade |
| **Food-Grade Suitability** | Ideal (smooth, non-contaminating) | Acceptable if coating approved for food contact |
| **Maintenance** | Lower (no coating maintenance) | Higher (coating inspection, touch-up) |
| **Lifecycle Cost** | Lower over 25-year design life | Higher (coating maintenance, earlier replacement) |

**Guidance:** Specify stainless steel for product-contact valves (aligns with food-grade requirements and lifecycle cost optimization). Carbon steel acceptable for utilities and non-product services.

**Source:** Material trade-off analysis; aligns with **OBJ-9: Lifecycle Cost Optimization**

**2. Actuator Type: Pneumatic vs. Electric**

| Factor | Pneumatic Actuators | Electric Actuators |
|--------|---------------------|---------------------|
| **Response Speed** | Fast (1–5 seconds typical) | Slower (10–60 seconds typical) |
| **Fail-Safe Capability** | Easy (spring-return for fail-safe) | Difficult (requires battery backup) |
| **Precision** | Good (with smart positioner) | Excellent (precise positioning) |
| **Utility Requirements** | Requires compressed air or nitrogen | Requires electrical power |
| **Maintenance** | Moderate (air supply maintenance) | Lower (fewer moving parts) |
| **Cost** | Lower capital cost | Higher capital cost (especially with fail-safe battery backup) |
| **Hazardous Area** | Intrinsically safe options available | Requires explosion-proof enclosure |

**Guidance:** Use pneumatic actuators for control valves and ESDs (fast response, fail-safe capability). Use electric actuators for infrequent-operation isolation valves (no air supply required, precise positioning for large valves).

**Source:** Actuator selection trade-offs; specific selections TBD pending control philosophy

**3. Specification Detail Level: Generic vs. Prescriptive**

- **Generic Specification:** Specifies performance requirements and allows vendors to propose suitable valve models
  - **Advantages:** Competitive bidding, may identify better/cheaper alternatives
  - **Disadvantages:** Requires detailed technical evaluation of vendor proposals; may result in non-standard equipment

- **Prescriptive Specification:** Specifies exact valve manufacturer and model number ("or approved equal")
  - **Advantages:** Ensures known, proven equipment; simplifies evaluation
  - **Disadvantages:** May limit competition; vendor may discontinue specified model

**Guidance:** Use prescriptive approach for critical valves where proven performance is essential (large control valves, relief valves). Use generic approach for standard isolation valves.

**4. Testing Requirements: Full FAT vs. Reduced Testing**

- **Full Factory Acceptance Test (FAT):** Complete functional testing of valve at vendor facility before shipment
  - **Advantages:** Verifies performance before delivery; reduces field commissioning issues
  - **Disadvantages:** Higher cost; requires witness travel; extends schedule

- **Reduced Testing:** Pressure test and basic functional check only
  - **Advantages:** Lower cost; faster delivery
  - **Disadvantages:** May discover issues during field commissioning (costly to resolve)

**Guidance:** Require full FAT for critical valves (large control valves, relief valves, ESDs). Accept reduced testing for standard isolation valves.

**Source:** Testing trade-offs typical for valve procurement

**5. Single Vendor vs. Multi-Vendor Procurement**

- **Single Vendor:** Procure all valves (or all valves of one category) from single vendor
  - **Advantages:** Volume pricing discount; standardized parts; simplified warranty management
  - **Disadvantages:** Less competitive pricing; schedule risk if vendor has delivery issues

- **Multi-Vendor:** Procure valves from multiple vendors (competitive bid per valve group)
  - **Advantages:** Competitive pricing; schedule flexibility
  - **Disadvantages:** Multiple spare parts inventories; more complex vendor management

**Guidance:** Consider single vendor for control valves (standardize positioners, actuators, parts). Multi-vendor acceptable for isolation valves (less critical to standardize).

**Source:** Procurement strategy trade-offs; specific strategy TBD per project procurement plan

## Examples

**Reference examples and precedents:**

**1. Employer's Requirements**

Refer to Employer's Requirements (Volume 2 Parts 1–3) for project-specific valve requirements:
- Valve standards and codes
- Materials of construction
- Testing and inspection requirements
- Documentation and submittals

**Location:** `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf` — **TBD** (not yet available in `_REFERENCES.md`)

**2. Industry Precedents**

**Typical valve specifications for similar facilities:**
- **API Standards:** Many oil/gas facilities use API 600 (gate valves), API 609 (butterfly valves), API 526 (relief valves) as baseline specifications
- **ISA Standards:** Control valve specifications commonly reference ISA-75 series for sizing and performance
- **Food-Grade Facilities:** Edible oil facilities typically specify 316SS valves for product contact, sanitary design features (drainable, cleanable)

**Source:** Industry precedents inferred from facility type; specific examples TBD

**3. Anticipated Artifacts for Reference**

Per `_CONTEXT.md`, this deliverable includes:
- **Control Valve Specification:** Requirements for flow, pressure, and level control valves
- **Isolation Valve Specification:** Requirements for gate, ball, butterfly valves (manual and automated)
- **Relief Valve Specification:** Requirements for pressure relief valves

**4. Related Deliverables (PKG-16)**

- **DEL-16.01 (Valve Design Drawing Set):** Valve arrangement drawings inform specification (valve sizes, types, services)
- **DEL-16.03 (Valve Design Calculations):** Valve sizing calculations inform specification (Cv/Kv, pressure drops, relief capacities)
- **DEL-16.04 (Valve Data Sheet Package):** Individual valve datasheets implement specification requirements
- **DEL-16.05 (Valve Installation & Test Records):** Installation and testing records verify compliance with specification

**Source:** PKG-16 deliverable structure from decomposition Section 5

**5. Sample Specification Section (Control Valve Actuator Requirements)**

**Example specification language (typical format):**

> **3.5 Actuators**
>
> **3.5.1 General**
> Control valve actuators shall be pneumatically operated with spring-return fail-safe action unless otherwise specified. Actuator shall be sized to provide 1.5 times the calculated stem force or torque at maximum differential pressure.
>
> **3.5.2 Pneumatic Actuators**
> Pneumatic actuators shall be piston type or diaphragm type. Air supply pressure shall be 80 psig nominal. Actuator shall include the following accessories:
> - Air filter regulator
> - Solenoid valve (three-way for spring-return, four-way for double-acting)
> - Manual override (handwheel or lever)
> - Position indicator (local visual indication)
>
> **3.5.3 Positioners**
> Control valves shall be equipped with smart digital positioners with 4–20 mA input signal and HART communication protocol. Positioner shall provide valve position feedback, diagnostic information, and auto-tuning capability.
>
> **3.5.4 Fail-Safe Action**
> Fail-safe action (fail-open or fail-closed) shall be as indicated on the valve datasheet and P&ID. Failure mode shall be achieved by spring-return action; stored energy from compressed air is not acceptable.

**Source:** **ASSUMPTION** — Typical specification language for control valve actuators; actual specification language TBD during specification development

**6. Lessons Learned (Typical Issues)**

**Common valve specification issues to avoid:**
- **Under-Specification:** Insufficient detail leads to vendor clarifications, non-compliant bids, or unsuitable equipment
- **Over-Specification:** Excessive requirements (e.g., requiring exotic materials for non-critical service) increase cost without benefit
- **Conflicting Requirements:** Internal contradictions confuse vendors and delay procurement
- **Obsolete Models:** Specifying discontinued valve models by part number; vendor unable to supply
- **Inadequate Lead Time:** Late specification issue delays procurement and affects critical path schedule

**Source:** **ASSUMPTION** — Typical valve specification issues from industry experience; project-specific lessons TBD
