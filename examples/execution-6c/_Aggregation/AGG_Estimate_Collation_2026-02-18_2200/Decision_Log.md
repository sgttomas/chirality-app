# Decision Log

**Snapshot:** AGG_Estimate_Collation_2026-02-18_2200
**Date:** 2026-02-18

---

## Decisions Made During Aggregation

### DEC-AGG-001: Snapshot Selection

**Decision:** Use the 2026-02-18 estimate snapshots (not the archived 2026-02-04 snapshots).

**Rationale:** The 2026-02-18 snapshots are the most recent and are the ones explicitly listed in the aggregation brief. The 2026-02-04 snapshots are in `_Archive/` and represent a prior iteration.

### DEC-AGG-002: Construction Content Counted Once

**Decision:** DEL-05-01 and DEL-05-02 both report $10,729,000 in construction pricing content. This is counted ONCE in project totals.

**Rationale:** Per brief double-counting warning and BOE Section 7.2. Schedule A is the summary view; Schedule B is the detail view of the same construction pricing. They are not additive.

### DEC-AGG-003: Bond/Insurance Premium Treatment

**Decision:** DEL-01-03 bond/insurance premiums ($537,534) are NOT added to the production total. Only the production cost ($2,060) and broker fee ($3,500) from DEL-01-03 are counted as PKG-01 additive costs.

**Rationale:** Per brief double-counting warning. The premiums documented in DEL-01-03 represent the same economic costs carried within DEL-05-01/05-02 construction content (L-021: $474,000 bonds/insurance). The slight difference ($537,534 vs $474,000 = $63,534) is due to different calculation approaches (item-by-item percentages vs blended 5.45% rate).

### DEC-AGG-004: DEL-05-02 Transparency Rows

**Decision:** DEL-05-02 lines L-095 (temp facilities) and L-096 (temp power) are marked as GR transparency rows and NOT added to the construction total.

**Rationale:** Per the estimate's own notes in Detail.csv, these lines are "part of the GR breakdown and is NOT additive to base construction. Shown for Schedule B detail transparency only."

### DEC-AGG-005: Evaluation Weight Split for DEL-02-02

**Decision:** DEL-02-02's 80 hours are estimated to split approximately 50/50 between "Design Brief" (5 pts) and "Durability/Maintenance" (15 pts) evaluation categories.

**Rationale:** DEL-02-02 covers 5 SOW items. SOW-013 (Durability/Maintenance) is one of five; however, it is weighted 15 points vs 5 points for the remainder. A 50/50 split is a conservative estimate given that durability content (materials selection, maintenance strategies, lifecycle cost considerations) requires comparable effort to the combined design brief + accessibility + adaptability content. Actual split depends on authoring emphasis.

### DEC-AGG-006: Risk Register Sparse Coverage

**Decision:** Only 1 of 21 snapshots (DEL-08-01) contains a Risk_Register.md. The project-level risk collection reflects this sparse coverage.

**Rationale:** The AGENT_ESTIMATING instructions treat Risk_Register.md as optional ("optional; only if risks are explicitly stated or implied by missing inputs"). Most deliverable estimates did not produce one. This is logged as a QA warning rather than a failure.

### DEC-AGG-007: DEL-05-02 L-078 Environmental Overlap

**Decision:** Accepted the DEL-05-02 Detail.csv as written (L-078 at $74,000 and L-106 at $22,000), flagging the potential $22k overlap in QA.

**Rationale:** The estimate's own notes on L-106 state that L-078 was conceptually reduced to $9,500 and the $22k consultant fee moved to L-106. However, the Detail.csv as published carries $74,000 for L-078. AGGREGATION does not modify source data; it flags the discrepancy. The net impact on the $10,729,000 construction total is immaterial at this accuracy level (+/-20-50%).
