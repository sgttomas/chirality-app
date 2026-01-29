# Guidance: DEL-14.03 Process Piping Design Calculations

## Purpose

Provides engineering calculations to size piping, verify stresses, and analyze thermal expansion per ASME B31.3 for PKG-14 Process Piping (scope: Specification.md Scope; attributes: Datasheet.md Calculation Type).

**Project context:** CSD canola oil transload facility, 1,000,000 MT/annum, Fraser Surrey Terminal BC (conditions: Datasheet.md Design Conditions; cross-reference DEL-14.01, DEL-14.02).

## Principles

**1. Pipe Sizing:**
- Hydraulic calculations using Darcy-Weisbach or equivalent (construction: Datasheet.md Construction item 1 - Methodology; requirements: Specification.md PR-1; standards: Specification.md Standards - Darcy-Weisbach; procedure: Procedure.md Step 1; examples: below - Typical pipe sizing)
- Balance pressure drop vs. capital cost (larger pipes = lower ΔP, higher cost) (requirements: Specification.md FR-2, FR-3; considerations: below - Pipe Sizing; trade-offs: below item 1)
- Typical liquid velocities: 1.5-3.0 m/s (avoid erosion and excessive pressure drop) (construction: Datasheet.md Construction item 1 - Outputs; requirements: Specification.md FR-3; verification: Specification.md Verification - Acceptance criteria; procedure: Procedure.md Step 1)
- Product viscosity affects pressure drop (canola oil viscosity varies with temperature) (conditions: Datasheet.md Product properties; requirements: Specification.md PR-4; procedure: Procedure.md Step 1; cross-reference DEL-14.02, DEL-14.04)

**2. Stress Analysis (ASME B31.3):**
- **Sustained loads:** Pressure + dead weight → allowable stress from material (code: Datasheet.md Design Code; construction: Datasheet.md Construction item 2; requirements: Specification.md FR-5, PR-6; standards: Specification.md Standards - ASME B31.3; procedure: Procedure.md Step 2; examples: below - Load Combinations)
- **Occasional loads:** Sustained + seismic/wind → 1.33 × allowable stress (code: Datasheet.md Design Code; requirements: Specification.md FR-5, PR-6, PR-7; procedure: Procedure.md Step 2; examples: below - Load Combinations)
- **Thermal expansion:** Range stress (expansion loads only) → f(1.25Sc + 0.25Sh) (code: Datasheet.md Design Code; construction: Datasheet.md Construction item 3; requirements: Specification.md FR-8, PR-6; procedure: Procedure.md Step 3; examples: below - Typical flexibility analysis)
- Software modeling (CAESAR II/AutoPIPE) typical for complex piping (attributes: Datasheet.md Software/Tools; construction: Datasheet.md Construction item 2 - Software; requirements: Specification.md PR-2; standards: Specification.md Standards - Software; considerations: below - Stress Analysis; procedure: Procedure.md Step 2; examples: below - Typical stress analysis)

**3. Flexibility Analysis:**
- Thermal growth = α × L × ΔT (coefficient × length × temp change) (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-8; procedure: Procedure.md Step 3; examples: below - Typical flexibility analysis)
- Accommodation: expansion loops, expansion joints, or spring hangers (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-10; considerations: below - Flexibility Analysis; trade-offs: below item 3; procedure: Procedure.md Step 3; cross-reference DEL-14.01, DEL-14.02)
- Equipment nozzle loads critical (must not exceed vendor allowables) (construction: Datasheet.md Construction items 2, 3 - Outputs; requirements: Specification.md FR-7, FR-9; interface: Specification.md IR-5; considerations: below - Stress Analysis, Flexibility Analysis; verification: Specification.md Verification - Acceptance criteria; procedure: Procedure.md Step 2, Step 3)

**4. Load Combinations:**
- Sustained: P + W (pressure + weight) (construction: Datasheet.md Construction item 2; requirements: Specification.md PR-6; procedure: Procedure.md Step 2; examples below)
- Occasional: Sustained + E (earthquake) or W (wind) (construction: Datasheet.md Construction item 2; requirements: Specification.md PR-6, PR-7; conditions: Datasheet.md Seismic criteria; procedure: Procedure.md Step 2; examples below)
- Thermal: Thermal expansion independent of sustained/occasional (construction: Datasheet.md Construction item 3; requirements: Specification.md PR-6; procedure: Procedure.md Step 3; examples below)

## Considerations

**Pipe Sizing:**
- Flow rates from process design (1M MT/annum total throughput) (conditions: Datasheet.md Flow rates; requirements: Specification.md FR-1, PR-4; procedure: Procedure.md Step 1; cross-reference DEL-14.01, DEL-14.04)
- Operational modes: direct rail-to-ship vs. through storage tanks (requirements: Specification.md FR-4; procedure: Procedure.md Step 1; cross-reference DEL-14.01)
- Multiple loading scenarios (single ship, multiple railcars, tank filling/emptying) (requirements: Specification.md FR-4; procedure: Procedure.md Step 1)
- Allowable pressure drop budget (pump capacity constraints) (requirements: Specification.md FR-2, FR-3; procedure: Procedure.md Step 1; cross-reference PKG-15)

**Stress Analysis:**
- Critical lines: large diameter, high pressure, high temperature, complex routing (construction: Datasheet.md Construction item 2 - TBD; requirements: Specification.md FR-5; quality: Specification.md QR-3; trade-offs: below item 2; procedure: Procedure.md Step 2)
- Seismic importance (BC location, NBC 2020) (conditions: Datasheet.md Seismic criteria; requirements: Specification.md PR-7; standards: Specification.md Standards - NBC 2020; procedure: Procedure.md Step 2; cross-reference DEL-14.01, DEL-14.02)
- Equipment nozzle protection (pumps, tanks, valves have load limits) (construction: Datasheet.md Construction item 2 - Outputs; requirements: Specification.md FR-7; interface: Specification.md IR-5; rationale: above item 3; verification: Specification.md Verification - Acceptance criteria; procedure: Procedure.md Step 2)
- Support spacing per ASME B31.3 Table 321.7.4 (requirements: Specification.md FR-6; standards: Specification.md Standards - ASME B31.3; procedure: Procedure.md Step 2; cross-reference DEL-14.01, DEL-14.02)

**Flexibility Analysis:**
- Temperature variation drives thermal expansion (conditions: Datasheet.md Operating temperature, Design temperature; construction: Datasheet.md Construction item 3; requirements: Specification.md FR-8; rationale: above item 3; procedure: Procedure.md Step 3)
- Long straight runs susceptible to high thermal stresses (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-8, FR-10; rationale: above item 3; procedure: Procedure.md Step 3)
- Mitigation: expansion loops (space-intensive), expansion joints (maintenance), spring hangers (cost) (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-10; rationale: above item 3; trade-offs: below item 3; procedure: Procedure.md Step 3; cross-reference DEL-14.01, DEL-14.02)

## Trade-offs

**1. Pipe Size Selection:**
- Smaller pipes: Lower capital cost, higher operating cost (pressure drop, pumping energy) (requirements: Specification.md FR-1, FR-2; rationale: above item 1; procedure: Procedure.md Step 1)
- Larger pipes: Higher capital cost, lower operating cost (requirements: Specification.md FR-1, FR-2; rationale: above item 1)
- **Guidance:** Lifecycle cost optimization (source: OBJ-9; requirements: Specification.md FR-1; rationale: above item 1; procedure: Procedure.md Step 1; cross-reference DEL-14.02); typically optimize for 5-10 year payback

**2. Stress Analysis Extent:**
- Analyze all lines: Conservative, high engineering cost (construction: Datasheet.md Number of Calculations; requirements: Specification.md FR-5; considerations: above - Stress Analysis; procedure: Procedure.md Step 2)
- Analyze critical lines only: Lower cost, requires engineering judgment to identify critical lines (construction: Datasheet.md Construction item 2 - TBD; requirements: Specification.md FR-5; quality: Specification.md QR-3; considerations: above - Stress Analysis; procedure: Procedure.md Step 2)
- **Guidance:** Risk-based approach (critical = large, high-pressure, high-temp, complex) (requirements: Specification.md FR-5; considerations: above - Stress Analysis; procedure: Procedure.md Step 2)

**3. Thermal Expansion Mitigation:**
- Expansion loops: No maintenance, consume space (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-10; rationale: above item 3; considerations: above - Flexibility Analysis; procedure: Procedure.md Step 3; cross-reference DEL-14.01)
- Expansion joints: Compact, require periodic maintenance/replacement (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-10; considerations: above - Flexibility Analysis; procedure: Procedure.md Step 3; cross-reference DEL-14.02)
- Spring hangers: Accommodate movement, higher cost than rigid supports (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-10; rationale: above item 3; procedure: Procedure.md Step 3; cross-reference DEL-14.01, DEL-14.02)
- **Guidance:** Expansion loops preferred (reliability, lifecycle cost); expansion joints where space limited (requirements: Specification.md FR-10; rationale: above item 3; considerations: above - Flexibility Analysis; procedure: Procedure.md Step 3; cross-reference DEL-14.02)

## Examples

**Typical pipe sizing calculation:**
- Input: Q (flow rate m³/h), ρ (density kg/m³), μ (viscosity cP), L (length m), fittings (conditions: Datasheet.md Flow rates, Product properties; interface: Specification.md IR-3; procedure: Procedure.md Step 1)
- Method: Assume diameter D → calculate velocity V = Q/A → Reynolds No. Re = ρVD/μ → friction factor f (Moody chart) → ΔP = f(L/D)(ρV²/2) + fittings (construction: Datasheet.md Construction item 1 - Methodology; requirements: Specification.md PR-1; standards: Specification.md Standards - Darcy-Weisbach; rationale: above item 1; procedure: Procedure.md Step 1)
- Iterate D until velocity and ΔP acceptable (requirements: Specification.md FR-2, FR-3; rationale: above item 1; verification: Specification.md Verification - Acceptance criteria; procedure: Procedure.md Step 1)
- Output: Recommended pipe size (NPS or DN) (construction: Datasheet.md Construction item 1 - Outputs; requirements: Specification.md FR-1; procedure: Procedure.md Step 1; cross-reference DEL-14.01, DEL-14.02, DEL-14.04)

**Typical stress analysis scope:**
- Model piping geometry in CAESAR II/AutoPIPE (attributes: Datasheet.md Software/Tools; construction: Datasheet.md Construction item 2 - Software; requirements: Specification.md PR-2; standards: Specification.md Standards - Software; interface: Specification.md IR-1; rationale: above item 2; procedure: Procedure.md Step 2; cross-reference DEL-14.01)
- Apply loads: pressure, weight, temperature, seismic (response spectrum), wind (construction: Datasheet.md Construction item 2 - Inputs; requirements: Specification.md PR-5, PR-6, PR-7; conditions: Datasheet.md Design Conditions; rationale: above items 2, 4; procedure: Procedure.md Step 2)
- Run analysis: sustained, occasional, expansion load cases (construction: Datasheet.md Construction item 2; requirements: Specification.md FR-5, PR-6; rationale: above items 2, 4; procedure: Procedure.md Step 2)
- Check: Stress ratios vs. ASME B31.3 allowables (code: Datasheet.md Design Code; requirements: Specification.md FR-5; quality: Specification.md QR-3; standards: Specification.md Standards - ASME B31.3; verification: Specification.md Verification - Acceptance criteria; procedure: Procedure.md Step 2, Step 4)
- Output: Support loads, nozzle loads, stress report (construction: Datasheet.md Construction item 2 - Outputs; requirements: Specification.md FR-6, FR-7; interface: Specification.md IR-5, IR-6; procedure: Procedure.md Step 2; verification: Specification.md Verification - Acceptance criteria)

**Typical flexibility analysis:**
- Long heated line (e.g., 100m, ΔT = 50°C) (construction: Datasheet.md Construction item 3 - TBD; conditions: Datasheet.md Operating temperature; requirements: Specification.md FR-8; considerations: above - Flexibility Analysis; procedure: Procedure.md Step 3)
- Calculate thermal growth: α = 12×10⁻⁶/°C (carbon steel), ΔL = 12×10⁻⁶ × 100,000mm × 50°C = 60mm (construction: Datasheet.md Construction item 3; requirements: Specification.md FR-8; rationale: above item 3; procedure: Procedure.md Step 3)
- Model with expansion loop or spring hangers to accommodate growth (construction: Datasheet.md Construction item 3 - Outputs; requirements: Specification.md FR-10; rationale: above item 3; trade-offs: above item 3; procedure: Procedure.md Step 3; cross-reference DEL-14.01)
- Verify thermal stresses and nozzle loads acceptable (requirements: Specification.md FR-8, FR-9; quality: Specification.md QR-3; verification: Specification.md Verification - Acceptance criteria; procedure: Procedure.md Step 3, Step 4)
