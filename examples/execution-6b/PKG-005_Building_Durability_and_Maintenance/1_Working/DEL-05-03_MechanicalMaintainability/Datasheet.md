# Datasheet — DEL-05-03: Mechanical Maintainability

---

## Identification

| Property | Value |
|---|---|
| **Deliverable ID** | DEL-05-03 |
| **Deliverable Name** | Mechanical Maintainability |
| **Package** | PKG-005 — Building Durability & Maintenance |
| **Type** | Durability / Narrative |
| **Discipline** | Mechanical Engineering |
| **Responsible Party** | Mechanical Engineer |
| **Scope Coverage** | SOW-0013: Durability/maintenance narrative |
| **Primary Objective** | OBJ-005: Demonstrate durability and ease of maintenance (15 pts) |
| **RFP Reference** | §7.1.4; §10.3.4; §11.1.1; §11.1.2; §11.2; §11.3 |
| **Project** | Town of Penhold — Public Services Building (RFP 2024_004) |
| **RFP Issued** | July 10, 2024 |
| **Addendum 03 Issued** | July 31, 2024 (governs mechanical special requirements) |
| **Status** | INITIALIZED |

---

## Attributes

| Attribute | Value | Source |
|---|---|---|
| **Design life — Main Building** | 50 years | RFP §2.2 ("lifespan of 50 years"); Decomposition v2 §5 |
| **Design life — Cold Storage (ancillary)** | 20 years | Decomposition v2 §5; ASSUMPTION: inferred from "ancillary" classification |
| **Building program** | Combined Fire Hall + Public Works Operations + shared administrative/support spaces | RFP §2.2; OSR §10.2.2 |
| **Evaluation weight (OBJ-005)** | 15 evaluation points (second-highest technical criterion) | RFP §8.3 (Scoring Matrix); Decomposition v2 §6 |
| **Design intent — all systems** | "Practical, energy efficient, cost effective, and easy to maintain" | RFP OSR §10.3.4 (Project Design — verbatim) |
| **Mechanical systems in scope** | HVAC (all zones); apparatus bay direct exhaust; PW bay general ventilation; Cold Storage anti-condensation ventilation; bunker gear room ventilation; plumbing (domestic hot water, water distribution, sanitary/storm drainage); bay sumps; water fill stations; fire protection (sprinkler); backup generator/emergency power | RFP §11.1–§11.3; Addendum 03 §§1.8, 1.11–1.16 |
| **Apparatus bay exhaust** | Direct exhaust ventilation required; 2 apparatus per bay; annual apparatus call frequency TBD (required to validate filter duty cycle and quarterly replacement assumption — see _SEMANTIC_LENSING.md B-001) | RFP §11.1.1 (verbatim: "direct exhaust ventilation for each fire apparatus bay based on two apparatus per bay"); Addendum 03 §1.12; call frequency data: TBD pending Town of Penhold Fire Chief confirmation |
| **PW bay ventilation** | General ventilation adequate for occasional short-term vehicle idling and very occasional welding; no dedicated welding ventilation required | Addendum 03 §1.11 (verbatim) |
| **Cold Storage ventilation** | "Adequate ventilation or alternate air circulation to prevent condensation and icing" | RFP §11.1.2 (verbatim) |
| **Bay sumps** | Required in all bays — snow melting and minor washing | Addendum 03 §1.8 (verbatim) |
| **Water fill stations** | 2" minimum; 1 at ground level in fire apparatus bay; 1 at ground level in PW bay | Addendum 03 §1.16 (verbatim) |
| **Backup generator** | Required; minimum loads: kitchen, meeting room (ICP), 2 bathrooms; bay doors require secondary opening mechanisms (generator-powered OR manual — Design-Builder's choice) | Addendum 03 §1.15 (verbatim) |
| **Bunker gear room ventilation** | Room-level ventilation required; direct ventilation to each locker not required; 40 lockers | Addendum 03 §1.13 (40 lockers); §1.14 (verbatim: "the room itself should have ventilation") |
| **Overhead door hardware — main building** | "Car wash" grade hardware (corrosion-resistant); 16 ft minimum door height | RFP OSR §10.3.9 (verbatim: "car wash grade hardware for the main building"); Addendum 03 §1.10 |
| **Materials basis** | "Durable, flexible materials for longevity and easy maintenance"; stainless steel base plates for corrosive environments | RFP §11.3 (verbatim) |
| **Plumbing/storm sewer** | Design-Builder responsible for all code requirements and locations; positive drainage of condensation at wall joints and penetrations | RFP §11.2 |
| **Mechanical room total area** | TBD — total mechanical room area not yet established; constrains the 150–300 sq ft spare parts storage allocation referenced in Construction table, Specification R-MEL-10, Guidance P-006, and Procedure A1/A2 (see _SEMANTIC_LENSING.md B-002) | Mechanical room sizing basis: TBD pending Architect/Mechanical Engineer coordination at Design Brief phase |
| **Cold Storage fire protection** | TBD — confirm whether Cold Storage building requires fire protection (sprinkler) system; Specification scope includes "Cold Storage ancillary building mechanical maintainability provisions" but no fire protection requirement is explicitly stated or excluded for Cold Storage (see _SEMANTIC_LENSING.md E-001) | TBD pending Fire Protection Engineer / AHJ confirmation |
| **Pickled Sand Storage building** | Removed from project scope; not applicable to this deliverable | Addendum 03 §1.2 |

---

## Conditions

| Condition | Description | Source |
|---|---|---|
| **Apparatus bay environment** | Mud, salt/brine residue from apparatus, diesel combustion exhaust, high humidity from snow/ice melt in bay sumps, frequent wet-dry cycling; primary driver of filter maintenance frequency and corrosion protection requirements | RFP §11.1.1; Addendum 03 §1.8, §1.12 |
| **PW bay environment** | Vehicle exhaust, occasional welding fumes, general grime and grease from maintenance activities; less stringent than fire apparatus bays; general ventilation sufficient | Addendum 03 §1.11 |
| **Cold Storage environment** | Unheated ancillary building (ASSUMPTION: unheated designation inferred from "cold storage" classification and 20-year design life context); freeze-thaw exposure is the primary durability driver; condensation and icing risk on interior surfaces and any installed mechanical equipment | RFP §11.1.2 |
| **Fill station corrosion risk** | 2" fill stations subject to frequent use and potential de-icing chemical contamination; corrosion-resistant fittings and accessible backflow prevention/check valves required | Addendum 03 §1.16; RFP §11.3 ("stainless steel base plates for corrosive environments") |
| **Municipal operations context** | Small municipal team with combined Fire Department and Public Works functions; limited in-house mechanical trade expertise; standardized parts and common models reduce procurement complexity and cross-training burden | ASSUMPTION (operations-aware inference consistent with OBJ-005 "credible, operations-aware" framing; RFP §10.3.4: "easy to maintain") |
| **Geotechnical basis** | Design relies on existing 2021 geotechnical report only (no additional investigation); relevant for sump pit design, below-grade mechanical equipment placement, and foundation drainage | RFP Appendix D; Decomposition v2 §DEC-013 (OI-004 resolution) |
| **Fire apparatus population** | Four large fire apparatus + four small fire apparatus in main building; future maximum of 5 in main building | RFP OSR §10.3.5 |

---

## Construction

**Mechanical System Categories and Maintainability Features:**

| System Category | Maintainability Features | Status / Notes |
|---|---|---|
| **Apparatus bay direct exhaust** | Dedicated exhaust fans with accessible filter cartridges; isolation dampers with labeled hand-lever for service mode; drain/condensate provisions; quarterly filter inspection; annual filter replacement without full system shutdown | System type (drop-hose vs. overhead rail) TBD at Mechanical Design Brief; RFP §11.1.1; Addendum 03 §1.12 confirms direct exhaust required |
| **PW bay general ventilation** | Fan access panels; belt and motor replacement clearance at floor or low-ladder level; gravity damper or powered louver accessible; filter bank front-accessible | System sizing TBD at detailed design; Addendum 03 §1.11 |
| **Cold Storage ventilation** | Low-maintenance passive or thermostatically-controlled circulation fans; corrosion-resistant housing suited for freeze-thaw cycling; minimal maintenance intervals targeted; condensate drain provisions (freeze-thaw rated) | System type TBD; RFP §11.1.2 (anti-condensation and anti-icing requirement explicit) |
| **Bunker gear room ventilation** | Dedicated supply/exhaust fan with outside-air makeup; accessible filter and damper for service; designed to provide sufficient air changes to prevent moisture and mold accumulation across 40 lockers; cartridge-type filter for non-specialist replacement | Addendum 03 §1.13, §1.14 |
| **HVAC — office/residential/shared zones** | Modular air-handling units with front-accessible filter racks and visible pressure-drop indicators; standardized refrigerant and controls; BAS-integrated (ASSUMPTION); filter replacement cycle TBD (quarterly assumed for high-load zones) | RFP §11.1.1; ASSUMPTION: BAS integration |
| **Backup generator** | Outdoor-mounted unit (fuel type TBD: natural gas available per Addendum 03 §1.6, or diesel); accessible fuel fill, oil/coolant service points, and battery terminals; provisions for annual load testing at exterior pad; automatic transfer switch (ATS) accessible for test/troubleshooting | Generator kW sizing TBD at detailed design; Addendum 03 §1.15; runtime target: TBD pending Town confirmation (see Guidance.md CONF-01; 72-hour figure is ASSUMPTION from prior project context, not confirmed in Addendum 03 §1.15) |
| **Bay sumps** | Accessible sump pump for inspection and replacement on 3–5 year cycle (ASSUMPTION — design basis to be validated during detailed design; see _SEMANTIC_LENSING.md F-003); sump basin sized for snow melt volumes per bay; manual backup pump provision; check valve and discharge strainer accessible; sump pit design based on existing 2021 geotechnical report | Basin dimensions and pump sizing TBD at detailed design; Addendum 03 §1.8 |
| **Water fill stations (2")** | Ground-level installation in each bay (fire apparatus bay and PW bay); double-check valve or backflow preventer with accessible test ports; corrosion-resistant fittings; strainer basket accessible for annual flushing and cleaning without system shutdown | 2" minimum confirmed; ground-level installation confirmed; Addendum 03 §1.16 |
| **Plumbing (domestic, sanitary)** | Isolation valves at each zone; cleanout access per code; equipment shut-off valves accessible from mechanical room or adjacent service corridor; positive drainage of condensation at wall joints (RFP §11.2) | System layout TBD at detailed design; RFP §11.2 |
| **Fire protection (sprinkler)** | Inspector's test and drain valve accessible; gauges at riser; drain provisions for system maintenance; wet or dry pipe per detailed design (TBD — **note:** Cold Storage building, if unheated, would require dry pipe to prevent freeze damage; main building may use wet pipe; system type selection must distinguish between main building and Cold Storage; see Guidance.md CONF-02); main control valve accessible for annual inspection | System type (wet/dry) TBD; NFPA 13/25 governs inspection and maintenance access; Cold Storage fire protection requirement itself is TBD (see Attributes table) |
| **Spare parts storage** | Dedicated shelf/bin space in mechanical room; 1-year consumable supply + 5-year major item inventory; estimated 150–300 sq ft storage allocation (ASSUMPTION); confirmed at occupancy | Dimensions TBD at mechanical room layout; ASSUMPTION consistent with fire/PW facility standard practice |

---

## References

| Document | Section / Reference | Relevance |
|---|---|---|
| RFP 2024_004 (AB-2024-07156) | §7.1.4 | "Describe the approach to building durability … including design approach, selection of various systems, components, materials, and construction methods used. Also describe the ease of repair and maintenance of the building and all systems and components." |
| RFP 2024_004 (AB-2024-07156) | OSR §10.3.4 | "Project design of all systems and assemblies must be practical, energy efficient, cost effective, and easy to maintain." |
| RFP 2024_004 (AB-2024-07156) | §11.1.1 | "Main Building is to have adequate ventilation per the building code and further to include direct exhaust ventilation for each fire apparatus bay based on two apparatus per bay." |
| RFP 2024_004 (AB-2024-07156) | §11.1.2 | "Cold Storage building is to have adequate ventilation or alternate air circulation to prevent condensation and icing." |
| RFP 2024_004 (AB-2024-07156) | §11.2 | Plumbing and storm sewer — Design-Builder responsible for all code requirements; positive drainage of condensation |
| RFP 2024_004 (AB-2024-07156) | §11.3 | "Use durable, flexible materials for longevity and easy maintenance … stainless steel base plates for corrosion resistance." |
| RFP 2024_004 (AB-2024-07156) | OSR §10.3.5 | Fire apparatus population (4 large + 4 small; future max 5) and Public Works equipment list |
| RFP 2024_004 (AB-2024-07156) | OSR §10.3.9 | Overhead door hardware grade — "car wash grade hardware for the main building"; 16' x 16' doors |
| Addendum 03 (Jul 31, 2024) | §1.6 | Gas services "within a few feet of the site" — natural gas generator option viable |
| Addendum 03 (Jul 31, 2024) | §1.8 | "All bays require sumps to allow for snow melting and minor washing." |
| Addendum 03 (Jul 31, 2024) | §1.10 | "16 feet height for the main building doors." |
| Addendum 03 (Jul 31, 2024) | §1.11 | PW bay ventilation — "adequate ventilation … for occasional short-term vehicle idling and very occasional welding" |
| Addendum 03 (Jul 31, 2024) | §1.12 | "Yes, direct exhaust ventilation for fire apparatus is required to accommodate two apparatus per bay." |
| Addendum 03 (Jul 31, 2024) | §1.13 | "40" bunker gear lockers required |
| Addendum 03 (Jul 31, 2024) | §1.14 | "Direct ventilation to each locker is not required, however, the room itself should have ventilation." |
| Addendum 03 (Jul 31, 2024) | §1.15 | "Yes, a backup generator is required to operate at a minimum the kitchen, meeting room (which doubles as an Incident Command Post) and two bathrooms. Bay doors require secondary opening mechanisms (either by backup generation power or manually opening)." |
| Addendum 03 (Jul 31, 2024) | §1.16 | "Yes, one fill station at ground level in the fire apparatus bay and one fill station at ground level in the public works bay. Both fill stations should be 2" minimum." |
| Decomposition v2 (Penhold_PSB_Project_Decomposition_v2.md) | DEL-05-03 entry; PKG-005 context; §3 Hard Constraints; §4 Addenda Integration | Deliverable description, scope, objectives, design life constraints |
| DEL-02-04 (Mechanical Concept Narrative) | TBD (not yet produced) | Upstream system selections — alignment required |
| DEL-04-02 (Mechanical Energy and Solar Readiness) | TBD (not yet produced) | Lifecycle coordination for major mechanical equipment |
