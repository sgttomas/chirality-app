# Guidance — DEL-015-01 Three-Phase Power Service

---

## Purpose

DEL-015-01 establishes the primary electrical infrastructure for the entire new maintenance shop addition. Three-phase power is explicitly mandated by the Owner (RFP §3.4) and is the upstream dependency for every other electrical and low-voltage deliverable in PKG-015. Without a commissioned main distribution panel (MDP), no downstream electrical work (lighting, receptacles, equipment power circuits, low-voltage systems) can be energized or tested.

This deliverable directly supports:
- OBJ-001: Code-compliant, fully functional facility that passes all applicable inspections.
- OBJ-005: Install and commission all electrical and low-voltage systems to operational readiness.

*Sources: RFP §3.4; Decomposition OBJ-001, OBJ-005; _REFERENCES.md.*

---

## Principles

### Design precedes installation
The electrical service configuration (voltage, ampacity, MDP size, grounding system) cannot be finalized by the installation contractor in isolation. This work depends on IFC electrical drawings produced by PKG-004 (Electrical Design), stamped by an Alberta P.Eng. The installation contractor should not size the service independently — the design package governs.
*Source: RFP §3.3.2; Decomposition PKG-004 / PKG-015 boundary.*

### Three-phase is non-negotiable
The Owner has explicitly specified three-phase power (RFP §3.4). This is not a design option. The electrical contractor and design engineer must confirm with the utility that three-phase service is available at the site (SW 14–44–21–W4) and coordinate the tie-in early, as utility lead times can affect the project schedule.
*Source: RFP §3.4; Decomposition SOW-0051, SOW-0081.*

### Utility coordination is a critical-path activity
SOW-0081 (coordinate and execute electrical service tie-in) is explicitly in scope for the Proponent (Decomposition §3-K). Utility companies in rural Alberta may have extended lead times for service extensions or upgrades. This coordination should begin during the design phase, not after construction starts.
*Source: Decomposition SOW-0081; RFP §3.3.2.*

### Service must accommodate all conceivable loads at completion
The conceptual electrical drawing (App B-Elec) shows high-demand loads: two 70A loads (fire hose pump and pressure washer), one 40A compressor, two 5-tonne crane circuits (ampacity TBD), welding station 50A 240V circuits, and numerous general circuits. The MDP and service must be sized to handle all simultaneous loads with appropriate demand factor applied. Under-sizing at this stage is a structural project risk.
*Source: App B-Elec (conceptual load schedule); RFP §3.4.*

### Inspection compliance governs schedule
Alberta Safety Code electrical inspections must pass before the service can be legally energized. Scheduling inspections in advance and ensuring the County representative is present (RFP §3.3.2) are contractor obligations that affect downstream work sequencing.
*Source: RFP §3.3.2.*

---

## Considerations

### Site location and utility access
The project is located at SW 14–44–21–W4, approximately 30 km south of Camrose in a rural area (RFP §1.0). Three-phase availability and utility provider identity should be confirmed during the design phase. ASSUMPTION: three-phase service is available from the local distribution utility, but this has not been confirmed in the available source documents.

### Service voltage selection
App B-Elec shows branch circuits at 120V (15A, 20A) and 240V (20A, 30A, 50A). This is consistent with a 208Y/120V 3-phase system or a 240V delta/wye system, but also potentially 480Y/277V with step-down transformers. The design engineer must select the appropriate system voltage in consultation with the utility and the Owner's operational requirements (crane voltage, welding equipment, etc.). This selection significantly affects MDP equipment specifications and procurement lead times.
*Source: App B-Elec circuit legend; RFP §3.4.*

### Welding equipment specifications
RFP §3.4 notes that the County will supply welding equipment specifications. These specifications are needed to properly size the 50A 240V welding circuits and confirm voltage requirements. If these specifications are not provided to the design team (PKG-004) before IFC design is completed, the electrical service sizing could be under-specified.
*Source: RFP §3.4 ("County to supply welding equipment specifications").*

### Crane power circuits
Two 5-tonne overhead crane circuits are required (RFP §3.4; App B-Elec). Crane power circuit sizing depends on the specific crane units selected (PKG-016). Crane procurement should be coordinated with PKG-004 (electrical design) before IFC drawings are finalized. DEL-015-04 (Equipment Power Circuits) covers the crane circuits, but they originate from this service.
*Source: App B-Elec; Decomposition PKG-016, DEL-015-04.*

### Guarantee and deficiency obligations
The two-year guarantee period (RFP §2.10) begins at CCC. Electrical service defects — particularly grounding, bonding, or panel workmanship issues — may not manifest immediately. Thorough as-installed documentation supports deficiency resolution.
*Source: RFP §2.10.*

### [C-003] Lifecycle cost implications of voltage and capacity decisions
The maintenance shop addition is expected to have a long operational life. Voltage selection and spare capacity decisions have material lifecycle cost implications that should be considered during the PKG-004 design phase:
- **Higher voltage (480Y/277V):** Reduces conductor sizing and associated material costs for large motor loads but requires step-down transformers for 120V branch circuits, adding equipment and maintenance cost.
- **Lower voltage (208Y/120V):** Simpler branch circuit distribution (no step-down transformers for general circuits) but larger conductor sizes for high-amperage loads, increasing installation cost.
- **Spare capacity:** Including 20-25% spare capacity increases initial MDP and service entrance cost but avoids costly service upgrades if future loads are added (see Trade-offs table).

The total cost of ownership for each configuration option should be evaluated by the PKG-004 design engineer in consultation with the Owner. TBD — lifecycle cost analysis not available in current sources.
*Source: ASSUMPTION — standard engineering practice for commercial/industrial facilities; no lifecycle cost data available in RFP or reference documents.*

### [E-002] Scoping rationale: welding circuits under DEL-015-01
The RFP §3.4 groups the welding circuit requirement with the three-phase power statement ("Multiple electrical plugs throughout the shop area suitable for connecting high voltage welding equipment"), which places it in the same scope area as the primary power service. The App B-Elec drawing shows 50A 240V circuits at the welding station. Although welding circuits are technically branch-level circuits that might logically belong to DEL-015-03 (Receptacle Installation) or DEL-015-04 (Equipment Power Circuits), they have been scoped under DEL-015-01 because:
1. The RFP §3.4 text associates them directly with the power service narrative.
2. The 50A 240V rating places them in the high-demand category alongside motor loads.
3. The Decomposition SOW-0051 scope description encompasses the power supply to the building, which includes provisions for these high-demand circuits.

ASSUMPTION: This scoping decision is based on the RFP's textual grouping. The boundary between service-level and branch-level scope may need to be confirmed with the PKG-004 design engineer.
*Source: RFP §3.4; App B-Elec; Decomposition SOW-0051.*

### [D-003] Recording Owner value decisions
Several decisions in this deliverable require Owner input (voltage preference, spare capacity preference, welding equipment specifications). There is currently no defined mechanism for recording the Owner's value-based decisions once they are made. It is recommended that:
1. A decision log be maintained (by the Proponent project manager or PKG-004 design engineer) that captures each Owner decision with date, rationale, and impact on the design.
2. Owner decisions that affect this deliverable be communicated formally (e.g., meeting minutes, written direction) and referenced in the IFC drawing package.
3. The Conflict Table entries (CON-015-01-001 through CON-015-01-005) be resolved through this mechanism, with the "Human Ruling" column updated when each decision is made.

TBD — no formal decision-recording process is defined in the available source documents.
*Source: ASSUMPTION — standard project management practice for design-build projects.*

---

## Trade-offs

| Trade-off | Option A | Option B | Recommended approach |
|---|---|---|---|
| Service voltage | 208Y/120V 3-phase (lower voltage, simpler branch circuits) | 480Y/277V 3-phase (more efficient for large motor loads, requires step-down for 120V circuits) | Decision deferred to PKG-004 design engineer in consultation with utility. **[F-004] Selection criteria: if total motor load (cranes, compressor, pressure washer, fire hose pump) exceeds approximately 50% of total service capacity, 480V may be more cost-effective for conductor sizing. If motor loads are a smaller proportion, 208Y/120V avoids transformer cost. Owner to confirm voltage compatibility with intended welding equipment.** Note crane and motor loads favor 480V (ASSUMPTION). **[C-003] Lifecycle cost implications should be evaluated — see Considerations.** |
| Service capacity margin | Size to exact calculated load (lower initial cost) | Include 20–25% spare capacity for future expansion (higher initial cost) | **[A-005] Rationale for spare capacity:** Industry practice (ASSUMPTION — IEEE Std 141 "Red Book" recommends spare capacity for industrial facilities; specific clause location TBD) and the long operational life of a municipal maintenance facility support including spare capacity. The cost of a service upgrade after construction is significantly higher than the incremental cost of oversizing during initial installation. **[F-004] Criteria: if the Owner has identified potential future loads (e.g., additional equipment, electric vehicle charging, building expansion), spare capacity is strongly recommended. If no future loads are anticipated, sizing to calculated load with standard code-required margins may be sufficient.** Owner (Camrose County) and design engineer to confirm. |
| MDP location | Electrical room as shown in App B-Elec (fixed position) | TBD by final architectural/structural layout (PKG-011/PKG-012) | Follow IFC drawings; electrical room position to be confirmed in coordinated design |

---

## Examples

No worked examples are available from current sources. TBD — to be populated when IFC drawings and design specifications from PKG-004 are available.

---

## Conflict Table (for human ruling)

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-015-01-001 | **Service voltage authority:** Service voltage is not specified in any source document. App B-Elec shows 120V and 240V branch circuits, which are consistent with multiple 3-phase system types (208Y/120V, 240 delta, 480Y/277V with transformers). The design engineer must select, but no instruction is given in the RFP. **[D-001] Additionally:** Specification REQ-015-01-002 says voltage "shall be as specified in the IFC electrical design drawings" while this table (CON-015-01-001) proposes the design engineer determines it "in consultation with utility and Owner." These are compatible but the directive authority is not identical — one makes the IFC drawing the sole authority, the other makes a consultation process the authority. Clarify whether the IFC drawing alone is authoritative or whether Owner consultation is a prerequisite to the design engineer's decision. | RFP §3.4 (three-phase required, voltage not stated) | App B-Elec (branch voltages 120V and 240V shown, no service voltage stated); Specification REQ-015-01-002 | Datasheet Attributes; Specification REQ-015-01-002, REQ-015-01-003; Guidance Considerations | PKG-004 electrical design engineer to determine and specify; Owner to confirm acceptability. **Human ruling needed: clarify whether IFC drawing is sole authority or whether Owner consultation is a prerequisite.** | TBD |
| CON-015-01-002 | **Utility availability:** Three-phase service availability at this rural Alberta location is assumed but not confirmed in any source document. | Decomposition SOW-0051 (three-phase supply in scope) | _DEPENDENCIES.md (utility service connection listed as external upstream dependency, no confirmation of phase availability) | Specification REQ-015-01-001; Guidance Principles | Proponent to confirm with utility during design phase (PKG-004); escalate to Owner if three-phase is unavailable or requires major infrastructure investment | TBD |
| CON-015-01-003 | **Welding equipment specifications:** RFP §3.4 states "County to supply welding equipment specifications" for circuit sizing, but no specifications have been provided in the available source documents. This leaves welding circuit sizing (50A 240V per App B-Elec) potentially unconfirmed. | RFP §3.4 | App B-Elec (shows 50A 240V at welding station as conceptual) | Specification REQ-015-01-010; Datasheet (load table) | Owner (Camrose County) to supply welding equipment specifications before IFC design is finalized | TBD |
| CON-015-01-004 | **[F-002] SOW-0081 scope boundary:** SOW-0081 ("Coordinate and execute electrical service tie-in") is assigned to DEL-018-06 (Utility Tie-Ins) in the Decomposition, but DEL-015-01 also addresses utility coordination for the electrical service under SOW-0051 scope. _CONTEXT.md describes scope as "Grounding and safety systems" without mentioning SOW-0081. Datasheet Identification lists "SOW-0081 (utility tie-in coordination)." Specification REQ-015-01-007 says "coordinate and execute the electrical service tie-in." The scope descriptions differ across documents. | _CONTEXT.md: Scope of Work (no mention of SOW-0081) | Datasheet Identification ("SOW-0081 utility tie-in coordination") vs. Decomposition (SOW-0081 assigned to DEL-018-06) | Datasheet Identification; Specification REQ-015-01-007; Procedure Steps 1.1-1.2 | Decomposition document (SOW-0081 definition) — clarify whether DEL-015-01 or DEL-018-06 owns the electrical tie-in coordination, or whether scope is shared | TBD |
| CON-015-01-005 | **[E-003] Verification boundary at MDP:** Procedure Verification table includes "Downstream circuits energizable" as a verification check, but Specification Out of Scope explicitly excludes "Branch circuit wiring and fixtures downstream of MDP." The verification scope for this deliverable should end at the MDP output terminals; verifying that downstream circuits are energizable may require downstream deliverable completion and is not within this deliverable's control. | Procedure Verification table ("Downstream circuits energizable") | Specification Out of Scope ("Branch circuit wiring and fixtures downstream of MDP") | Specification Out of Scope; Procedure Verification table; Specification Verification REQ-015-01-009 | Human ruling needed: define verification boundary at MDP output terminals vs. downstream load points | TBD |

---

## Enrichment Provenance (Pass 3)

*The following warranted items from `_SEMANTIC_LENSING.md` were incorporated into this document during Pass 3 enrichment:*

| ItemID | Type | Section Modified | Action Taken |
|---|---|---|---|
| A-005 | RationaleGap | Trade-offs table (spare capacity row) | Added rationale basis for 20-25% spare capacity recommendation |
| C-003 | MissingSlot | New Considerations subsection "Lifecycle cost implications" | Added lifecycle cost discussion for voltage and capacity decisions |
| D-001 | Conflict | Conflict Table CON-015-01-001 (expanded) | Merged directive authority conflict into existing voltage conflict entry |
| D-003 | MissingSlot | New Considerations subsection "Recording Owner value decisions" | Added mechanism recommendation for recording Owner decisions |
| E-002 | RationaleGap | New Considerations subsection "Scoping rationale: welding circuits" | Added rationale for welding circuit scoping under DEL-015-01 |
| E-003 | Conflict | New Conflict Table entry CON-015-01-005 | Added verification boundary conflict between Procedure and Specification |
| F-002 | Normalization | New Conflict Table entry CON-015-01-004 | Added SOW-0081 scope boundary conflict for human ruling |
| F-004 | WeakStatement | Trade-offs table (all rows) | Strengthened recommended approach columns with explicit selection criteria |
