# Assumptions Log — EST_DEL-02-07_2026-02-18_1600

## Active Assumptions

### ASM-001: Generator Runtime = 72 Hours

| Field | Value |
|---|---|
| **Assumption** | Generator is sized for 72-hour continuous runtime on essential loads. |
| **Source** | PP-26 in Assumed_Project_Parameters.csv; Addendum 03 functional program notes |
| **Confidence** | MEDIUM |
| **Impact if Wrong** | Fuel tank sizing and potentially generator capacity would change. Longer runtime = larger fuel tank = higher cost. EQ-04 range ($120k-$180k) may not cover significantly longer runtimes. |
| **Resolution Required** | Owner (Town of Penhold) must confirm runtime requirement (DEP-0207-E006, PENDING). |

### ASM-002: Generator Size = 100-150 kW

| Field | Value |
|---|---|
| **Assumption** | Essential loads (kitchen, meeting/command room, 2 bathrooms, emergency lighting, door backup mechanisms) require a generator in the 100-150 kW range. |
| **Source** | EQ-04 description in Equipment_Pricing.csv |
| **Confidence** | LOW |
| **Impact if Wrong** | If essential loads list expands or specific loads are larger than assumed, a larger generator would be required, pushing cost toward or beyond the $180k upper range. |
| **Resolution Required** | Essential loads analysis during design (DEL-02-07 Procedure Phase A). |

### ASM-003: Diesel Fuel Type

| Field | Value |
|---|---|
| **Assumption** | Generator is diesel-fueled per functional program notes. |
| **Source** | SOW-0222; Addendum 03 section 1.15 |
| **Confidence** | HIGH |
| **Impact if Wrong** | Natural gas generator would have different pricing, fuel storage, and permitting requirements. |
| **Resolution Required** | None expected; diesel is specified. |

### ASM-004: Single Generator (Not Redundant)

| Field | Value |
|---|---|
| **Assumption** | One (1) generator system serves all essential loads. No redundancy or paralleling required. |
| **Source** | EQ-04 Quantity_Assumed=1; SOW-0222 states "at minimum" essential loads |
| **Confidence** | MEDIUM |
| **Impact if Wrong** | Redundant or paralleled generators would approximately double equipment costs. |
| **Resolution Required** | Confirm during design that single generator meets reliability requirements for this facility type. |

### ASM-005: Emergency Distribution Scope

| Field | Value |
|---|---|
| **Assumption** | Emergency distribution from generator to essential loads includes: 1 dedicated sub-panel, branch circuits to kitchen, meeting/command room, 2 bathrooms, and emergency lighting circuits. Estimated at $18,000. |
| **Source** | Brief cost ownership rules; DEC-EST-003 |
| **Confidence** | LOW |
| **Impact if Wrong** | If essential loads are more extensive or if distribution routing is longer than typical, costs would increase. |
| **Resolution Required** | Building electrical design (DEL-02-06 interface) must define distribution routing. |

### ASM-006: Door Backup Mechanism — 8 Doors at $2,000 Each

| Field | Value |
|---|---|
| **Assumption** | All 8 main building overhead doors (4 fire + 4 PW) require backup power mechanism integration. Mechanism assumed to be battery backup unit or UPS for door opener motor, at $2,000 per door. |
| **Source** | PP-13 (8 doors confirmed); SOW-0216; DEC-EST-004 |
| **Confidence** | LOW |
| **Impact if Wrong** | If mechanism is generator-fed circuit only (no battery backup), cost per door may be lower ($500-$1,000). If a more sophisticated system is required, cost could be $3,000-$3,500 per door. |
| **Resolution Required** | Door backup mechanism type to be determined during design. Requires door specification from DEL-02-04. |

### ASM-007: Installation Labour Hours

| Field | Value |
|---|---|
| **Assumption** | Site-specific installation requires approximately: Electrician 60 hours, Millwright 40 hours, Crane Operator 2 days (16 hours). Total incremental labour ~$12,000. |
| **Source** | Construction_Labour_Rates.csv (T-07, T-13, T-14); DEC-EST-005 |
| **Confidence** | LOW |
| **Impact if Wrong** | If vendor quote includes full turnkey installation, this line item should be removed. If site conditions are difficult, labour could increase. |
| **Resolution Required** | Vendor quote scope clarification. |

### ASM-008: Design Fee Basis

| Field | Value |
|---|---|
| **Assumption** | Generator-specific electrical engineering design fees estimated at 2.5% of DEL-02-07 construction cost (~$196,000), yielding ~$5,000. |
| **Source** | Professional_Design_Fees.csv / DF-05 (2.5% recommended) |
| **Confidence** | LOW |
| **Impact if Wrong** | If generator design is bundled into overall electrical design fees (DEL-02-06), this line may be a double-count. If generator is a specialty sub-consultant, fees could be higher. |
| **Resolution Required** | Confirm whether generator design is included in or separate from overall electrical engineering fee. |
