# Guidance: DEL-27.03 Phase 2 Expansion Documentation

## Purpose

This guidance document supports the development of **Phase 2 Expansion Documentation** for **PKG-27 Engineering Design**.

**Context:** Documents analysis and results for Phase 2 expansion documentation; ensures Phase 1 design facilitates Phase 2 expansion with minimal disruption per OBJ-8.

**Role in Project:** Phase 2 Expansion Documentation serves strategic and technical planning functions:
- **Strategic:** Supports Employer's long-term business planning and investment decisions for Phase 2
- **Technical:** Ensures Phase 1 design accommodates future Phase 2 expansion through interface provisions, upsizing, and footprint reservations
- **Operational:** Minimizes operational disruption during future Phase 2 construction and tie-ins
- **Value:** Protects Employer's future expansion options while optimizing Phase 1 investment

**Deliverable Classification:**
- Type: Report (General Arrangement Drawing + Engineering Memo)
- Discipline: Design
- Responsible: D&B Contractor

**Source:** _CONTEXT.md; Decomposition DEL-27.03; Decomposition Section 2 (OBJ-8)

## Principles

**Principle 1: Future Expandability as Design Objective (OBJ-8)**
- Phase 2 expandability is explicit project objective: "The design facilitates Phase 2 expansion with minimal disruption"
- Not optional "nice to have" — fundamental requirement driving Phase 1 design decisions
- Balance: Provide adequate Phase 2 provisions without over-designing Phase 1 (cost-effectiveness per OBJ-9)
- **Source:** Decomposition Section 2 (OBJ-8, OBJ-9)

**Principle 2: Phase 1-Phase 2 Interface Management**
- Clear identification and documentation of all Phase 1-Phase 2 interfaces is critical
- Interface types: Physical (piping, electrical, structural), Operational (mode transitions, simultaneous operations), Regulatory (permits, approvals)
- Interface provisions in Phase 1 prevent costly rework during Phase 2
- **Source:** Specification.md (FR-2); **ASSUMPTION**: Interface management best practice

**Principle 3: Risk-Based Provision Strategy**
- Not all Phase 2 provisions have equal value; prioritize based on cost-to-change analysis:
  - **High priority (must provide in Phase 1):** Difficult-to-change items: underground utilities, foundations, structural upsizing, footprint reservations
  - **Medium priority (should provide if feasible):** Moderate-difficulty items: spare piping connections, electrical capacity margins, control system scalability
  - **Low priority (defer to Phase 2):** Easy-to-change items: above-ground piping routing, instrumentation additions, procedure updates
- **Source:** **ASSUMPTION**: Risk-based provision strategy balances future flexibility and Phase 1 cost

**Principle 4: Operational Continuity During Phase 2 Construction**
- Phase 2 construction must not shut down Phase 1 operations for extended periods (OBJ-5: Terminal Continuity applies to Phase 2 as well)
- Design for minimal-duration tie-ins: pre-fabrication, quick connections, phased commissioning
- Independent construction access and laydown areas for Phase 2
- **Source:** Decomposition Section 2 (OBJ-5, OBJ-8); **ASSUMPTION**: Operational continuity during expansion

## Considerations

**Phase 2 Scope Uncertainty:**
- Phase 2 scope may not be fully defined during Phase 1 design (business case, market conditions, regulatory environment evolve)
- Document range of Phase 2 scenarios (e.g., 1.5× to 3× Phase 1 capacity); design provisions for reasonable upper bound
- Flexibility: Provisions should accommodate range of Phase 2 concepts, not lock into single rigid plan
- **TBD** — Phase 2 scope definition from Employer; if uncertain, define planning scenarios
- **Source:** **ASSUMPTION**: Phase 2 scope uncertainty typical for long-term expansion planning

**Site Constraints:**
- Fraser Surrey Terminal is existing marine terminal with space constraints
- Phase 2 expansion limited by: available land, existing facilities, property boundaries, rail/marine access, utilities, environmental setbacks
- Site layout optimization: Phase 1 facilities positioned to maximize Phase 2 expansion options
- **TBD** — Site constraints from site investigation, terminal master plan, geotechnical suitability
- **Source:** Decomposition Section 1.1; **ASSUMPTION**: Existing terminal site constraints typical

**Multi-Discipline Coordination:**
- Phase 2 provisions must be coordinated across all disciplines:
  - Civil: Footprint reservations, utility corridors, access roads, drainage upsizing
  - Structural: Foundation upsizing for future tank loads, pipe rack extensions, equipment pad capacity margins
  - Mechanical: Piping upsizing, spare nozzles/connections, pump capacity margins, tank expansion pad
  - Electrical: Transformer capacity margin, spare breakers, cable tray/conduit capacity, substation expansion provisions
  - Controls: Spare I/O capacity, network scalability, control room expansion space
- Single-discipline provision without others creates bottleneck (e.g., piping provision useless if no electrical capacity)
- **Source:** Specification.md (IR-1); **ASSUMPTION**: Coordinated multi-discipline provisions essential

**Cost-Benefit Analysis:**
- Phase 2 provisions increase Phase 1 capital cost; Employer must approve cost-benefit trade-off
- Incremental Phase 1 cost for provisions << Phase 2 rework cost if provisions omitted
- Example: Oversizing underground piping in Phase 1 adds ~10-20% to pipe cost; replacing underground piping in Phase 2 costs 5-10× original cost plus operational disruption
- Order-of-magnitude cost estimates for Phase 2 provisions and Phase 2 rework scenarios support decision-making
- **TBD** — Cost estimates for provisions and Phase 2 expansion
- **Source:** Decomposition Section 2 (OBJ-9); **ASSUMPTION**: Lifecycle cost optimization considers Phase 2

## Trade-offs

**Trade-off 1: Phase 2 Provision Level (Under-Provide vs. Over-Provide)**
- **Minimal provisions:** Design Phase 1 with minimal Phase 2 consideration; defer most provisions to Phase 2
  - Advantages: Lowest Phase 1 cost; maximum flexibility for Phase 2 design changes
  - Disadvantages: High Phase 2 rework cost; long shutdown durations for tie-ins; operational disruption
- **Extensive provisions:** Design Phase 1 for full Phase 2 capacity; upsize everything
  - Advantages: Easy Phase 2 expansion; minimal rework; short tie-in durations
  - Disadvantages: High Phase 1 cost; potential over-design if Phase 2 defers or scope changes
- **Recommendation:** Targeted provisions for high-value items (underground, foundations, footprint); defer low-value provisions; document rationale
- **Source:** Decomposition Section 2 (OBJ-8, OBJ-9); **ASSUMPTION**: Balanced provision strategy

**Trade-off 2: Phase 2 Concept Definition (Detailed vs. Conceptual)**
- **Detailed Phase 2 concept:** Define Phase 2 design in detail during Phase 1 (equipment sizes, layouts, specifications)
  - Advantages: Very specific Phase 1 provisions; high confidence in adequacy
  - Disadvantages: High Phase 1 engineering cost; Phase 2 concept may change before execution; may lock in suboptimal Phase 2 design
- **Conceptual Phase 2 concept:** High-level Phase 2 definition (capacity ranges, general layouts, interface locations)
  - Advantages: Lower Phase 1 engineering cost; flexibility for Phase 2 optimization; adequate for provisions
  - Disadvantages: Less precision in provisions; may need adjustments during Phase 2 detailed engineering
- **Recommendation:** Conceptual Phase 2 definition adequate for DEL-27.03 scope; detailed Phase 2 engineering is separate future project
- **Source:** Specification.md (scope boundaries); **ASSUMPTION**: Conceptual-level Phase 2 planning appropriate for expansion documentation

## Examples

**Example 1: Phase 2 Piping Provisions (Typical)**

Phase 1 piping design provisions for Phase 2 tank addition:
- **Upsizing:** Main transfer piping sized for combined Phase 1 + Phase 2 flow (e.g., 16" pipe instead of 12" if Phase 2 doubles capacity)
- **Spare connections:** Install blind-flanged nozzle on main header for future Phase 2 tank connection (nozzle size based on Phase 2 tank capacity estimate)
- **Valve isolation:** Install isolation valve upstream of Phase 2 tie-in point for future shutdown-free connection
- **Pipe rack extension:** Extend pipe rack past Phase 1 equipment with structural capacity for future Phase 2 piping
- **Footprint reservation:** Reserve land adjacent to Phase 1 tank farm for Phase 2 tank pad; do not build permanent obstructions in reserved area

**Cost impact (typical):** Upsizing main piping ~10-20% cost increase; spare connection ~$5k-20k per connection; footprint reservation ~$0 (land cost already sunk)

**Phase 2 benefit:** Avoid replacing main underground piping ($$$ cost + long shutdown); short tie-in duration (~1-2 days vs. weeks); no excavation/backfill disruption

**Example 2: Phase 2 Electrical Provisions (Typical)**

Phase 1 electrical design provisions for Phase 2 capacity increase:
- **Transformer sizing:** Install transformer with capacity margin for Phase 2 loads (e.g., 2 MVA transformer vs. 1.5 MVA if Phase 2 adds 0.5 MVA)
- **Spare breakers:** Include spare breaker positions in Phase 1 MCCs/switchgear for future Phase 2 loads (typically 20-30% spare capacity)
- **Conduit/cable tray:** Size cable trays and install spare conduits with capacity for future Phase 2 circuits
- **Substation footprint:** Size substation pad and fence to accommodate future transformer/switchgear additions

**Cost impact:** Transformer upsizing ~10-15% cost increase; spare breakers/conduit ~5-10% electrical cost increase

**Phase 2 benefit:** Avoid transformer replacement or second substation ($$$ cost); simple breaker installation and cable pulls in Phase 2

**Example 3: Phase 2 Footprint Reservation (Typical)**

Phase 1 site layout provisions for Phase 2 expansion:
- **Tank pad extension:** Size Phase 1 tank pad foundation for future additional tank (e.g., 4-tank pad built in Phase 1, only 3 tanks installed)
- **Pipe rack alignment:** Align Phase 1 pipe racks toward anticipated Phase 2 expansion direction for easy extension
- **Access roads:** Locate Phase 1 access roads to avoid crossing Phase 2 expansion area
- **Laydown area:** Designate and preserve Phase 2 construction laydown area (graded, drained, but not paved or obstructed)
- **Utility corridors:** Reserve corridors for future Phase 2 utilities (fire water, electrical, instrument air, drainage)

**Cost impact:** Minimal; primarily planning and site layout coordination

**Phase 2 benefit:** Eliminates need to demolish/relocate Phase 1 facilities to make room for Phase 2; efficient Phase 2 construction logistics

**Source for Examples:** **ASSUMPTION**: Typical Phase 2 provisions for transload facility expansion; cost impacts are order-of-magnitude estimates
