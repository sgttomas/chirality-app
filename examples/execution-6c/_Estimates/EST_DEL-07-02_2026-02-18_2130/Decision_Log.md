# Decision Log — EST_DEL-07-02_2026-02-18_2130

## Decisions Applied During This Run

### DEC-EST-001: CBS Assignment Rule

- **Decision:** Assign CBS = `ADMIN` to all DEL-07-02 line items.
- **Rationale:** Both roles (R-26 HR Coordinator, R-22 Proposal Coordinator / Writer) are categorized as `Administrative` in Professional_Staff_Rates.csv. DEL-07-02 is an administrative deliverable (resume compilation, formatting, availability coordination) with no design, construction, or financial content.

### DEC-EST-002: Scope Resolution

- **Decision:** DEL-07-02 resolves to exactly 2 line items based on Level_of_Effort.csv rows for this deliverable (R-26: 12 hr, R-22: 8 hr).
- **Rationale:** Level_of_Effort.csv is the authoritative source for labour hours per deliverable per role. No additional roles are listed for DEL-07-02 in this source. No fallback pricing was needed (all hours and rates were available).

### DEC-EST-003: No Fallback Required

- **Decision:** FALLBACK_POLICY = STRICT was satisfied without invoking fallback.
- **Rationale:** Both line items have complete basis evidence from the two primary rate table sources (rates + hours). No TBD amounts were produced.

### DEC-EST-004: Dependency Evidence Not Used for Pricing

- **Decision:** Dependencies.csv was read for blocker detection only; no dependency rows were used as pricing evidence.
- **Rationale:** Per non-negotiable invariant: "Dependencies are not pricing evidence." All 4 EXECUTION dependencies are coordination interfaces or handover relationships that do not affect unit rates or quantities.
