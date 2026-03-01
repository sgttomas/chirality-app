# Guidance — DEL-004-05 Receptacle Layout Plans

---

## Purpose

The Receptacle Layout Plans drawing set exists to communicate, in a spatially precise and code-compliant form, where every electrical receptacle outlet shall be installed in the New North Shop addition. It provides the primary reference used by the electrical contractor during installation (PKG-015 / DEL-015-03) and serves as the document against which the Authority Having Jurisdiction (AHJ) verifies electrical permit compliance.

From the project decomposition perspective, this deliverable directly advances:
- **OBJ-001** — Deliver a code-compliant, fully functional maintenance shop. Receptacle coverage is a functional completeness requirement.
- **OBJ-003** — Produce complete, P.Eng.-stamped IFC design documentation across all disciplines before construction begins.
- **OBJ-005** — Install and commission all electrical systems to operational readiness, specifically "receptacles per the electrical drawing" (Decomposition OBJ-005 statement).

The conceptual electrical drawing (R-05, App B-Elec) is the Owner's expression of intent. This deliverable translates that intent into an engineered, dimensioned, code-compliant drawing set.

### Scope Boundary Rationale (DEL-004-05 vs. DEL-004-03)

The boundary between DEL-004-05 (Receptacle Layout Plans) and DEL-004-03 (Power Distribution Plans) is defined by how equipment connects to the electrical system. Receptacles are general-purpose or designated outlets into which portable or plug-in equipment is connected. Hardwired equipment circuits (e.g., 40 A compressor circuit, 70 A fire hose pump circuit) are dedicated power circuits covered by DEL-004-03.

Where a high-amperage receptacle (e.g., 50 A/240 V) serves as the connection point for portable welding equipment, it falls within DEL-004-05 scope because it is a receptacle outlet. Where a circuit is hardwired to fixed equipment, it falls within DEL-004-03 scope regardless of amperage. **ASSUMPTION** — this boundary follows standard electrical practice. The Electrical Engineer should confirm this convention and flag any ambiguous cases (e.g., a 50 A receptacle that feeds a semi-permanently installed compressor) for project team resolution.

> Source: Standard electrical practice; R-05 (App B-Elec shows both receptacle symbols and equipment circuit callouts separately); Specification Scope section.

> **Enrichment (X-001):** This scope boundary rationale section has been added to explain the logic behind the DEL-004-05/DEL-004-03 boundary, which was previously listed only as an exclusion in the Specification without explanation.

---

## Principles

### 1. The Conceptual Drawing Is a Starting Point, Not a Final Design
The conceptual electrical drawing (R-05) provides the types of receptacles and a schematic sense of distribution, but is not dimensioned and does not claim code compliance. The Electrical Engineer must treat it as a programmatic expression of the Owner's needs and must develop the final layout to comply with CEC Part I (as applicable in Alberta) and Alberta Safety Codes. Counts, spacing, heights, and GFCI designations are all engineering judgments to be confirmed in the final IFC drawing.
> Source: R-01 S3.4 ("The County only has a concept in mind; therefore, it will be a design/build project."); R-01 S3.3.2 (code compliance requirement).

### 2. Welding Receptacle Distribution Is a Primary Operational Requirement
The single most operationally distinctive requirement for this shop is the distribution of high-voltage welding-grade receptacles (assumed 50 A/240 V) throughout the main shop bays — not merely at a dedicated welding station. The RFP explicitly calls for "multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment" (R-01 S3.4). The conceptual drawing reinforces this with 50 A symbols appearing in multiple bays. The Electrical Engineer should treat widespread welding capability as a first-order layout principle, not an afterthought.
> Source: R-01 S3.4; R-05 (App B-Elec); Decomposition SOW-0057, SOW-0302, D-009.

### 3. Welding Receptacle Voltage Is Assumed — Confirm with County
Decision D-009 in the project decomposition records that welding receptacles are assumed to be 50 A/240 V based on the conceptual electrical drawing. The RFP states "County to supply welding equipment specifications" (R-01 S3.4). If the County-supplied welder specifications indicate a different rating (e.g., a welder requiring 60 A or a different plug configuration), the receptacle design will require revision. This is tracked as a potential scope change. The Electrical Engineer should seek County confirmation of welder specifications before IFC issue. **This is the single most critical external input; the Electrical Engineer should establish a target receipt date and an escalation path if specifications are not received in time for IFC.**
> Source: R-01 S3.4; Decomposition D-009, SOW-0302.

### 4. Zone-by-Zone Coverage Must Be Adequate for All Occupancies
The building contains a range of occupancy types — heavy industrial shop floor, parts storage, office, utility, and wet wash bay — each with different receptacle density and protection requirements. The layout plan should address each zone with coverage appropriate to its use. In particular:
- The wash bay is a wet location: GFCI protection is required per code (**ASSUMPTION**: CEC Part I — location TBD).
- The office and parts room require general-purpose coverage at practical working heights.
- The mezzanine, while not shown on the conceptual drawing, will require receptacle coverage if it is a useable storage area; the Electrical Engineer must determine this in coordination with the architectural design.
> Source: R-05 (App B-Elec); R-01 S3.1 (room program).

### 5. Coordination with Panel Schedules and Power Plans Is Essential
The Receptacle Layout Plans do not stand alone. Each receptacle circuit must originate from a panel (DEL-004-06) and must be accounted for in the power distribution design (DEL-004-03). The Electrical Engineer should produce these deliverables in a coordinated set so that circuit numbers shown on the layout plan match circuit designations in the panel schedule without ambiguity.
> Source: Standard electrical drawing practice; ASSUMPTION.

---

## Considerations

### Receptacle Heights and Mounting
Standard receptacle mounting heights are governed by CEC Part I and Alberta Safety Codes (location TBD). In an industrial shop environment, receptacles at work bench level and higher mounting to reduce damage risk from equipment movement are common practice. **ASSUMPTION:** The Electrical Engineer will apply appropriate mounting heights per code and standard shop design practice. This is now also captured as a normative requirement in Specification REQ-009.

### GFCI Scope May Be Broader Than Wash Bay Only
While the wash bay is the most obvious wet location, the utility room (which may contain wash sink facilities per R-01 S3.1 and R-05) may also require GFCI protection at certain outlets. The Electrical Engineer should review all locations for damp or wet classification. See Specification REQ-004 for the requirement to enumerate all qualifying locations.
> Source: R-01 S3.1; R-05; ASSUMPTION per CEC Part I.

### 20 A/120 V vs. 15 A/120 V Distribution
The conceptual drawing shows a mix of 15 A/120 V and 20 A/120 V general-purpose receptacles. In an industrial shop, upsizing to 20 A circuits is common for operational flexibility. The Electrical Engineer should consider whether any 15 A locations on the conceptual drawing should be 20 A in the final design, particularly in areas with higher tool usage.
> Source: R-05 (App B-Elec); ASSUMPTION based on industrial shop design convention.

### Old North Shop Renovation Receptacle Scope
The conceptual electrical drawing (R-05) focuses on the new addition. The Old North Shop renovation (washroom, locker room, kitchenette — per R-01 S3.4 and S3.1) is not shown on the conceptual electrical drawing. Whether receptacle design for the renovation is included within this deliverable or a separate drawing is TBD. The Electrical Engineer should clarify this scope boundary with the project team.
> Source: R-01 S3.1, S3.4; R-05 (not showing renovation electrical in detail).

### Mezzanine Receptacle Scope
The mezzanine over the parts room, utility room, and wash bay (R-01 S3.4) is referenced as a storage area for heavy items. No receptacle symbols are shown on the mezzanine in the conceptual electrical drawing. Whether receptacle outlets are required on the mezzanine (for lighting maintenance, equipment charging, etc.) is TBD. The Electrical Engineer should address this in the IFC drawing.
> Source: R-01 S3.4; R-05 (mezzanine not detailed electrically).

### Future Expansion and Spare Capacity

The New North Shop is an industrial maintenance facility with evolving equipment needs. The Electrical Engineer should consider whether the receptacle infrastructure should include provisions for future expansion, such as:
- Spare conduit runs or empty conduit to potential future receptacle locations.
- Spare breaker positions in panels (coordinate with DEL-004-06) to accommodate future receptacle circuits.
- Oversizing conduit where marginal cost is low, to allow future circuit additions without new conduit runs.

This consideration is directional only and does not create a requirement. The cost-benefit of future-proofing should be weighed against the project budget. **ASSUMPTION** — future-proofing considerations are standard practice for industrial shop electrical design. TBD — the Electrical Engineer should discuss spare capacity provisions with the County during preliminary design review.

> **Enrichment (E-001):** This consideration has been added because the existing documents addressed only current design trade-offs without considering future-proofing. An industrial shop with evolving equipment needs benefits from spare capacity provisions. Source: R-01 S3.4 (design/build concept with evolving needs); standard industrial electrical practice — ASSUMPTION.

### Phasing of Drawing Production (Preliminary vs. IFC)

The Procedure (Step 7) references a preliminary design submittal that may include the receptacle layout. The level of detail required at the preliminary stage versus IFC stage is TBD. The Electrical Engineer and Project Manager should consider:
- Whether a preliminary receptacle layout showing zone coverage and receptacle types (without final circuit numbers or exact dimensions) is sufficient for County preliminary review.
- Whether the County's preliminary review focuses on functional coverage (types and zones) rather than exact placement.
- Whether circuit assignments and final coordination with DEL-004-06 can be deferred to the IFC stage.

**ASSUMPTION** — standard design-build practice allows preliminary submittals at a lower level of detail than IFC. TBD — confirm with County what level of detail is expected at preliminary review.

> **Enrichment (E-002):** This consideration has been added to address the absence of phasing guidance for drawing production. Source: R-01 S3.3.2 (preliminary design approval required); Procedure Step 7; ASSUMPTION based on standard design-build practice.

---

## Trade-offs

| Trade-off | Options | Consideration | Cost-Benefit Context | Source |
|---|---|---|---|---|
| Welding receptacle density | More receptacles = more flexibility but higher cost and panel load | County expressed need for "multiple" outlets throughout shop; operational flexibility is the priority per RFP | Higher density increases material/labor cost (each 50 A/240 V circuit requires dedicated wiring and breaker) but reduces operational downtime from equipment repositioning. For a heavy equipment maintenance shop, operational flexibility typically outweighs incremental wiring cost. **ASSUMPTION** — cost-benefit ranking is directional; specific cost data TBD per Electrical Engineer. | R-01 S3.4; R-05 |
| 15 A vs. 20 A general purpose | 20 A costs marginally more but adds flexibility | For an industrial shop, 20 A is generally preferred; 15 A shown on conceptual may reflect minimum intent | Upsizing from 15 A to 20 A circuits involves marginally larger wire gauge and breakers. The per-circuit cost increment is small relative to the total electrical scope. In an industrial environment, 20 A circuits avoid nuisance tripping from power tools. **ASSUMPTION** — cost increment is minor for industrial projects; specific cost data TBD. | R-05; ASSUMPTION |
| GFCI scope | Minimum code compliance vs. broader GFCI coverage | Broader coverage improves safety in industrial wet environments; cost difference is modest | GFCI devices add ~$15-30 per outlet (ASSUMPTION — general market range). Broader coverage provides safety margin in an environment where water, oil, and other fluids may be present beyond designated wet areas. | ASSUMPTION; CEC Part I location TBD |
| Receptacle circuit grouping | Group by zone vs. intersperse phases | Grouping by zone simplifies maintenance; phase balancing may drive some cross-zone circuits | Zone grouping makes troubleshooting easier for maintenance staff; phase balancing across zones may be required for panel load management. The Electrical Engineer should balance both considerations. | ASSUMPTION; coordinate with DEL-004-06 |

> **Enrichment (A-006):** A "Cost-Benefit Context" column has been added to the Trade-offs table. The original table listed options and considerations but did not quantify or rank the value/cost implications. The added context provides directional cost-benefit framing to help the Electrical Engineer make informed choices. Specific cost data remains TBD per project pricing. Source: R-01 S3.4; R-05; general market data — ASSUMPTION.

---

## Examples

No project-specific examples of similar industrial shop receptacle layouts are available from the project sources (R-01, R-05, Decomposition). The conceptual electrical drawing (R-05, App B-Elec) serves as the closest available precedent, showing the Owner's intent for receptacle types and general distribution.

For reference, the Electrical Engineer may consult:
- Standard practice references for industrial maintenance shop electrical design (e.g., IEEE Std 141 "Red Book" for industrial power distribution, or NFPA 70 commentary for industrial occupancies — **ASSUMPTION: these are standard industry references**).
- Comparable county or municipal maintenance shop projects in the Electrical Engineer's portfolio, if available.

> **Enrichment (D-003):** The Examples section has been updated from a bare "TBD" to acknowledge that no project-specific examples exist and to suggest standard practice references the Electrical Engineer may consult. Source: standard electrical engineering practice references — ASSUMPTION.

---

## Conflict Table (for human ruling)

No direct conflicts have been identified between accessible sources. The following items represent ambiguities or normalization issues that may require human ruling:

| Conflict ID | Conflict (short statement) | Source A (file + section) | Source B (file + section) | Impacted sections | Proposed authority (PROPOSAL) | Human ruling |
|---|---|---|---|---|---|---|
| CF-001 | Circuit numbering convention: Does DEL-004-05 drawing carry circuit numbers, or only reference DEL-004-06? | Specification REQ-008 ("panel/circuit origination is covered by DEL-004-06") | Procedure Step 5 ("assign each receptacle circuit to a specific panel circuit number") | Specification REQ-008; Procedure Steps 4.5, 5 | Electrical Engineer (PROPOSAL) | TBD |
| CF-002 | Old North Shop renovation: Is receptacle design for the renovation included in DEL-004-05 or a separate drawing? | Specification Scope (excludes "beyond what is explicitly scoped") | Datasheet Receptacle Distribution by Zone (new renovation row marked TBD) | Specification Scope; Datasheet Attributes; Procedure Step 1 | Project Team / County (PROPOSAL) | TBD |

> **Note:** The primary open item (welding receptacle voltage confirmation) is tracked as an assumption (D-009) and a conditions entry in the Datasheet, not as a source conflict. The items above represent cases where the documents themselves contain ambiguous or potentially inconsistent statements that the human should resolve.
