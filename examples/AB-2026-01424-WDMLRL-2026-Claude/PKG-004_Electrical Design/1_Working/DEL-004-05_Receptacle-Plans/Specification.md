# Specification — DEL-004-05 Receptacle Layout Plans

---

## Scope

### What This Deliverable Covers

DEL-004-05 consists of the Receptacle Layout Plans drawing set for the New North Shop addition at the West Dried Meat Lake Regional Landfill (SW 14-44-21-W4, near Ferintosh, Alberta). The drawing set graphically locates and annotates all electrical receptacle outlets to be installed in the new building, showing outlet type, ampere rating, voltage, and zone assignment.

This deliverable covers:
- Layout and annotation of all general-purpose and specialized receptacle outlets (15 A/120 V through 50 A/240 V) within the new addition, as indicated on the conceptual electrical drawing (R-05) and as developed by the Electrical Engineer to final IFC standard.
- Electrical legend specific to receptacle types used.
- Dimensional/positional coordination with architectural floor plan (DEL-001-02).
- Notes identifying special installation requirements (e.g., GFCI, wet-location ratings).
- Receptacle mounting heights shown on the drawing or noted as general standards per code (see REQ-009).

### What This Deliverable Excludes

- Lighting fixture layout (DEL-004-04).
- Single-line diagram and main service design (DEL-004-02).
- Power distribution for equipment circuits (cranes, compressor, pumps, overhead doors) — those are covered by DEL-004-03 (Power Distribution Plans). **Note (X-001):** The boundary between "receptacle" and "equipment power circuit" is defined by circuit function: a receptacle is a general-purpose or designated outlet into which portable equipment is plugged; a dedicated hardwired equipment circuit (e.g., compressor at 40 A) is not a receptacle. Where a high-amperage receptacle (e.g., 50 A/240 V) serves as the connection point for portable welding equipment, it is within DEL-004-05 scope. Where a circuit is hardwired to fixed equipment, it is within DEL-004-03 scope. **ASSUMPTION** — this boundary follows standard electrical practice; confirm with Electrical Engineer.
- Panel schedules and circuit breaker sizing (DEL-004-06).
- Low-voltage and communications wiring (DEL-004-07).
- Electrical work within the existing Old North Shop renovation beyond what is explicitly scoped (renovation receptacle scope is TBD pending architectural renovation plans DEL-001-10).

---

## Requirements

### REQ-001 — Receptacle Types and Ratings
**Source:** R-05 (App B-Elec legend); R-01 S3.4; Decomposition SOW-0058

The drawing set shall show receptacles of the following types, consistent with the conceptual electrical drawing:

| Requirement | Rating | Notes |
|---|---|---|
| REQ-001a | 15 A / 120 V | General purpose — office, parts room, utility room, wash bay, and as required per code |
| REQ-001b | 20 A / 120 V | General purpose higher demand — work bench, main shop bays |
| REQ-001c | 20 A / 240 V | As shown on conceptual drawing at selected main shop locations |
| REQ-001d | 30 A / 240 V | As shown on conceptual drawing at welding station area |
| REQ-001e | 50 A / 240 V | Welding-grade; shop area (welding station and distributed bays) — assumed 50 A/240 V per D-009; treated as scope change if County-supplied welder specifications differ |

### REQ-002 — Welding Receptacle Coverage
**Source:** R-01 S3.4 ("Multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment"); R-05 (App B-Elec); Decomposition SOW-0057

Multiple high-voltage welding-grade receptacles (assumed 50 A/240 V) shall be shown throughout the main shop area. Exact count and spacing shall be developed by the Electrical Engineer to meet operational coverage requirements. The conceptual drawing shows a cluster at the welding station and additional 50 A symbols distributed through the main shop bays.

> **Enrichment (X-004):** For verification purposes, the Electrical Engineer shall define what "distributed through main shop bays" means quantitatively. TBD — proposed minimum threshold (e.g., minimum one 50 A receptacle per bay, maximum spacing between welding receptacles, or a minimum per-bay count) to be confirmed by the Electrical Engineer in coordination with the County's operational requirements. Source: R-01 S3.4 ("multiple electrical plugs throughout the shop area"); R-05 (App B-Elec shows 50 A symbols in multiple bay locations).

### REQ-003 — Receptacle Coverage by Zone
**Source:** R-05 (App B-Elec); R-01 S3.1 (room program)

Receptacles shall be provided in all occupiable zones of the new addition. Per the conceptual drawing:

| Zone | Minimum Coverage Indicated |
|---|---|
| Main Shop bays | 20 A/120 V and 50 A/240 V distributed; exact layout per Electrical Engineer |
| Work Bench area | 20 A/120 V along bench — quantity per final design |
| Welding Station | 50 A/240 V (welding), 30 A/240 V, 20 A/240 V, 20 A/120 V cluster |
| Parts Room | 15 A/120 V — quantity per final design |
| Office | 15 A/120 V — quantity per final design |
| Utility Room | 15 A/120 V — quantity per final design |
| Wash Bay | 15 A/120 V — wet-location/GFCI rated; quantity per final design |
| Mezzanine | TBD — not shown on conceptual drawing |

### REQ-004 — GFCI Protection (Wet and Damp Locations)
**Source:** ASSUMPTION — Alberta Electrical Utility Code / CEC Part I (location TBD); R-01 S3.3.2 (code compliance required)

Receptacles in the wash bay and any other wet or damp locations shall be shown as GFCI-protected. The Electrical Engineer shall enumerate all locations within the building that qualify as wet or damp per CEC Part I classification and shall show GFCI protection for all receptacles in those locations. At a minimum, the wash bay qualifies; the utility room and any area with a wash sink or floor drain shall be evaluated. Final determination of GFCI requirements is the responsibility of the Electrical Engineer per applicable code. **ASSUMPTION:** CEC Part I rules for wet and damp locations apply.

> **Enrichment (A-002):** The requirement has been strengthened to require the Electrical Engineer to enumerate all qualifying wet/damp locations (not just the wash bay). This addresses the ambiguity in the original formulation "wash bay and any other wet or damp locations" by making the enumeration an explicit deliverable checkpoint. Source: R-01 S3.3.2 (code compliance); R-01 S3.1 (room program includes wash bay, utility room with potential wet areas); R-05 (App B-Elec layout).

### REQ-005 — Code Compliance
**Source:** R-01 S3.3.2 ("The proposed building must adhere to all Alberta Safety Codes")

All receptacle locations, ratings, and circuit assignments shown on the drawing set shall comply with:
- Alberta Safety Codes Act and applicable Safety Codes (electrical) — **ASSUMPTION:** Canadian Electrical Code Part I (CEC Part I), CSA C22.1, as adopted in Alberta, is the applicable standard (location TBD in code text). The Electrical Engineer shall confirm the applicable CEC Part I edition with the Authority Having Jurisdiction (AHJ) and record the confirmed edition number in the Standards table below and in the drawing set notes prior to IFC issue.
- National Building Code of Canada (as adopted in Alberta) for occupancy classification — **ASSUMPTION.** The NBC reference is included because occupancy classification may affect receptacle spacing, type, or protection requirements (e.g., industrial vs. commercial vs. assembly occupancies may have different CEC Part I receptacle rules). If the Electrical Engineer determines that NBC occupancy classification does not directly affect receptacle design requirements beyond what CEC Part I mandates, this reference may be removed with a documented rationale.

> **Enrichment (A-001, C-001):** The requirement now explicitly directs the Electrical Engineer to confirm the applicable CEC Part I edition with the AHJ and record it. This addresses the gap where the code edition was unspecified.
>
> **Enrichment (C-002):** The NBC reference has been clarified to explain how occupancy classification may affect receptacle requirements, with an instruction to remove it with documented rationale if it proves inapplicable.

### REQ-006 — IFC Drawing Standard
**Source:** R-01 S3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta"); OBJ-003

The drawing set shall be:
- Issued For Construction (IFC) quality.
- Signed and stamped by a P.Eng. licensed to practice in Alberta.
- Coordinated with architectural floor plans (DEL-001-02) for dimensional accuracy.

> **Enrichment (D-001):** County preliminary design review acceptance criteria: The County shall review the preliminary receptacle layout (as part of DEL-004-01 preliminary electrical design) and provide written approval or comments. Acceptance format and criteria are TBD — the Project Manager shall confirm with the County what constitutes formal approval (e.g., signed approval letter, stamped drawing markup, email confirmation) and what the resubmission protocol is if the preliminary design is rejected. Source: R-01 S3.3.2 (County to approve preliminary design); OBJ-003.

### REQ-007 — Electrical Legend
**Source:** R-05 (App B-Elec legend)

The drawing set shall include an electrical legend defining all receptacle symbols used. As a minimum, the legend shall include the five receptacle types listed in REQ-001.

### REQ-008 — Three-Phase Supply Context
**Source:** R-01 S3.4 ("The Proposed building shall run on three-phase power")

The receptacle layout shall be designed within the context of a three-phase service. 240 V receptacles shall be served from appropriate phases of the three-phase panel. Specific panel/circuit origination is covered by DEL-004-06. The receptacle layout drawing shall reference DEL-004-06 for circuit assignments; whether circuit numbers appear directly on the DEL-004-05 drawing or only on the panel schedule (DEL-004-06) is TBD — the Electrical Engineer shall determine the convention and apply it consistently.

> **Enrichment (F-004):** The circuit numbering cross-reference convention has been clarified. Specification REQ-008 previously said "panel/circuit origination is covered by DEL-004-06" while Procedure Step 5 said "assign each receptacle circuit to a specific panel circuit number." This enrichment makes explicit that the convention (whether DEL-004-05 carries circuit numbers or only references DEL-004-06) is a decision for the Electrical Engineer, to be applied consistently. Source: standard electrical drawing practice; ASSUMPTION.

### REQ-009 — Receptacle Mounting Heights
**Source:** ASSUMPTION — CEC Part I governs mounting heights (location TBD); standard industrial shop design practice

The drawing set shall show receptacle mounting heights or include a general note specifying mounting height standards per CEC Part I and applicable industrial shop design practice. In an industrial shop environment, mounting heights may differ from standard residential/commercial practice (e.g., higher mounting at work bench areas to reduce damage from equipment movement). The Electrical Engineer shall determine appropriate mounting heights per code and zone function.

> **Enrichment (C-003):** This requirement has been added because mounting heights were previously discussed in Guidance (Considerations) and Procedure (Step 4.4) but had no normative requirement in the Specification. Adding this requirement ensures that the drawing set explicitly addresses mounting heights as a design element. Source: CEC Part I (location TBD); R-05 (App B-Elec does not specify mounting heights); standard industrial practice — ASSUMPTION.

### REQ-010 — AFCI and Tamper-Resistant Receptacles (Applicability TBD)
**Source:** ASSUMPTION — CEC Part I may require AFCI or tamper-resistant receptacles in certain occupancies (location TBD)

TBD — The Electrical Engineer shall determine whether CEC Part I requires arc-fault circuit interrupter (AFCI) protection or tamper-resistant receptacles for any zones in this building type (industrial maintenance shop, Group F Division 2 or 3 occupancy — **ASSUMPTION**). If AFCI or tamper-resistant receptacles are required by code for any zone, they shall be shown on the drawing set. If not required, the Electrical Engineer shall document the determination.

> **Enrichment (F-002):** This requirement has been added as a TBD to ensure the Electrical Engineer explicitly addresses AFCI and tamper-resistant receptacle applicability. CEC Part I requirements for these devices vary by occupancy type and may apply to certain spaces within the building (e.g., office areas). Source: CEC Part I (location TBD); R-01 S3.3.2 (code compliance required).

---

## Standards

| Standard | Applicability | Access Status |
|---|---|---|
| Alberta Safety Codes Act (Electrical) | Governing electrical design standard for Alberta | Not directly accessible — location TBD |
| Canadian Electrical Code Part I (CEC Part I), CSA C22.1 — **Edition: TBD (to be confirmed with AHJ)** | **ASSUMPTION:** applicable as adopted in Alberta for electrical installation design | Not directly accessible — location TBD |
| CCDC 14-2013 | Contract form governing design-build delivery | Referenced in R-01 S2.7; full text not accessible |
| National Building Code of Canada (as adopted in Alberta) | **ASSUMPTION:** applicable for occupancy classification affecting receptacle requirements — see REQ-005 for clarification on applicability | Not directly accessible — location TBD |

> **Note (A-001):** The CEC Part I entry now includes a placeholder for the edition number, to be confirmed by the Electrical Engineer with the AHJ. This is tracked as an open item.

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-001 — Receptacle types and ratings | Drawing review: confirm legend defines all five types; confirm each symbol on plan matches legend |
| REQ-002 — Welding receptacle coverage | Drawing review: confirm 50 A/240 V receptacles are distributed through main shop bays, not only at welding station. Quantitative threshold TBD per Electrical Engineer (see REQ-002 enrichment note). |
| REQ-003 — Zone coverage | Drawing review: confirm all named zones have receptacles of the correct type shown |
| REQ-004 — GFCI (wet locations) | Drawing review: confirm GFCI notation/symbol is shown for wash bay and all other wet/damp locations as enumerated by the Electrical Engineer |
| REQ-005 — Code compliance | (a) Pre-IFC: Electrical Engineer confirms applicable CEC Part I edition with AHJ; edition number recorded in Standards table and drawing notes. (b) Construction phase: Engineer stamp + AHJ permit approval. |
| REQ-006 — IFC standard | Verify P.Eng. stamp present; verify coordination with DEL-001-02 floor plan dimensions; verify County preliminary design review acceptance documented |
| REQ-007 — Legend | Drawing review: legend present and complete |
| REQ-008 — Three-phase context | Coordination check with DEL-004-02 (Single-Line) and DEL-004-06 (Panel Schedules); confirm circuit numbering convention applied consistently |
| REQ-009 — Mounting heights | Drawing review: confirm mounting heights shown or general note provided per CEC Part I and industrial practice |
| REQ-010 — AFCI / tamper-resistant | Electrical Engineer provides documented determination of applicability; if required, drawing review confirms correct notation |
| Architectural coordination (X-005) | Coordination check: confirm receptacle locations do not conflict with structural elements, door swings, or equipment clearances shown on DEL-001-02. Review overlay of receptacle layout on architectural base drawing. |

> **Enrichment (A-003):** REQ-005 verification now includes a pre-IFC code-edition confirmation step (verification approach (a)), not just post-construction permit approval.
>
> **Enrichment (X-004):** REQ-002 verification now references the quantitative threshold to be defined by the Electrical Engineer.
>
> **Enrichment (X-005):** An architectural coordination verification check has been added to confirm that receptacle placements do not conflict with structural elements, door swings, or equipment clearances shown on DEL-001-02. This supplements the existing "dimensional accuracy" check for REQ-006. Source: standard drawing coordination practice; ASSUMPTION.
>
> **Enrichment (F-001):** An intermediate quality gate is specified in the Procedure (Step 6) — the Electrical Engineer shall perform a self-check of the drawing against CEC Part I receptacle coverage rules using a documented checklist before P.Eng. stamp application. See Procedure Step 6.

---

## Documentation

### Required Artifacts (Anticipated)

| Artifact | Description |
|---|---|
| Receptacle Layout Plan sheet(s) | IFC-quality drawing(s) showing receptacle locations, types, and notations for all zones of the new addition |
| Electrical Legend | Defined on drawing set |
| Engineer stamp | P.Eng. Alberta stamp on IFC issue |
| CEC Part I edition confirmation | Written record of confirmed code edition from AHJ (see REQ-005) |
| GFCI location enumeration | Documented list of wet/damp locations per CEC Part I (see REQ-004) |
| AFCI / tamper-resistant determination | Documented determination of applicability (see REQ-010) |

### Coordinating Deliverables (upstream context)

| Deliverable | Dependency |
|---|---|
| DEL-004-01 (Preliminary Electrical Design) | Preliminary design to be County-approved before IFC development |
| DEL-001-02 (Architectural Floor Plans) | Dimensional base for receptacle layout |
| DEL-004-02 (Single-Line Diagram) | Service entry and panel configuration context |
| DEL-004-03 (Power Distribution Plans) | Equipment circuit coordination |
| DEL-004-06 (Panel Schedules) | Circuit assignment origination |
