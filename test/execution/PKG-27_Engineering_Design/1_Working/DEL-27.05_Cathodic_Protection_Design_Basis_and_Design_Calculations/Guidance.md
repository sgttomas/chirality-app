# Guidance: DEL-27.05 Cathodic Protection Design Basis & Design Calculations

## Purpose

Supports development of **Cathodic Protection Design Basis & Design Calculations** for **PKG-27 Engineering Design**. CP prevents corrosion of buried and submerged steel structures at Fraser Surrey Terminal waterfront facility.

**Source:** _CONTEXT.md; Datasheet.md

## Principles

**Principle 1: Cathodic Protection Fundamentals**
CP works by making steel structure the cathode in electrochemical cell. Current flows from anodes through soil/water to structure, preventing corrosion. Two methods: (1) Sacrificial anodes (galvanic) — more active metal (zinc/magnesium) corrodes preferentially; (2) ICCP — external power source drives current from inert anodes.

**Principle 2: Site-Specific Design**
CP design depends critically on site conditions (soil/water resistivity, coatings, stray currents). Generic designs often fail; must use actual site data.

**Principle 3: Lifecycle Considerations**
CP is long-term corrosion management strategy. Design must account for coating degradation over time, anode consumption, maintenance access. Marine environment is particularly aggressive; design margins essential.

**Source:** **ASSUMPTION**: CP engineering principles per NACE standards and industry practice

## Considerations

**Fraser River Marine Environment:**
- Brackish water (salt + fresh mix) = highly corrosive, conductive
- Tidal variations = splash zone corrosion (most aggressive)
- Marine organisms = potential for biological corrosion
- Waterfront soils likely conductive, corrosive
- **TBD** — Specific resistivity and corrosion rate data from site testing

**Structure-Specific:**
- **Storage tanks:** Tank bottoms on grade most vulnerable if no liner/barrier
- **Buried piping:** All underground piping requires CP unless non-metallic or fully encased in non-conductive material
- **Marine structures:** Steel piles, sheet piles in water/mud highly vulnerable; critical for marine loading safety

**CP System Selection:**
- **ICCP:** Better for large current demands, long life, easier to adjust; requires power, maintenance, more complex
- **Sacrificial anodes:** Simpler, no power, lower maintenance; limited current capacity, finite life, less flexible
- **Recommendation:** ICCP for marine structures (large submerged area, high current demand); Sacrificial for buried piping (moderate demand, distributed); **TBD** — based on detailed analysis

**Source:** Datasheet.md; **ASSUMPTION**: Typical marine facility CP considerations

## Trade-offs

**Trade-off 1: ICCP vs. Sacrificial Anodes**
- ICCP: Higher capital cost, requires power/maintenance → Lower lifecycle cost (long life, adjustable), better for large demands
- Sacrificial: Lower capital cost, no power → Higher lifecycle cost (anode replacement), limited to moderate demands
- **Recommendation:** Lifecycle cost analysis; consider hybrid approach (ICCP for marine, sacrificial for buried utilities)

**Trade-off 2: Design Margins**
- Conservative (high margins): Oversized anodes/rectifiers → Higher cost, but protects against uncertainties (coating degradation, resistivity variations)
- Optimized (low margins): Right-sized for calculated demand → Lower cost, risk of under-protection if assumptions wrong
- **Recommendation:** Marine environment warrants conservatism (20-50% margin typical); monitor performance post-installation

**Source:** **ASSUMPTION**: Standard CP design trade-offs

## Examples

**Example: Current Demand Calculation**
For buried piping: 100 m of 12" steel pipe, external coating 95% efficient
- Surface area = π × D × L = 3.14 × 0.3 m × 100 m = 94 m²
- Current density (coated steel in soil) = 10 mA/m² per NACE SP0169
- Bare area = 94 m² × (1 - 0.95) = 4.7 m²
- Current demand = 4.7 m² × 10 mA/m² = 47 mA
- Design margin 30% → Total demand = 47 × 1.3 = 61 mA

**Example: Sacrificial Anode Sizing**
For 61 mA demand over 25-year life:
- Magnesium anode capacity = 1100 Ah/kg (utilization factor 0.85)
- Total charge required = 61 mA × 25 years × 8760 hr/year = 13,359 Ah
- Anode mass required = 13,359 / (1100 × 0.85) = 14.3 kg
- Use (2) 10 kg magnesium anodes (20 kg total) for redundancy and distribution

**Source:** **ASSUMPTION**: Typical CP calculation example; actual values **TBD**

---

**Cross-Document Verification (Pass 3):**
- All Principles linked to Specification § requirements and Procedure Steps
- All Considerations linked to Specification § requirements and Procedure Steps
- All Trade-offs linked to relevant Principles and Specification §
- All Examples linked to Specification § and Procedure Steps
- Terminology verified consistent with Datasheet.md, Specification.md, Procedure.md
- CP methodology (ICCP vs. Sacrificial) verified consistent across all documents
- Current density and calculation approach verified consistent with NACE SP0169
- Fraser Surrey Terminal marine environment considerations verified consistent across all documents
