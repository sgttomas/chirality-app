# Blockers Report

## DEL-05-04: Option -- Security & Camera System

### Blockers to Final Pricing (not blocking this parametric run, but blocking a QUOTE-basis run)

| # | Blocker | Evidence | Impact | Resolution Path |
|---|---|---|---|---|
| B-01 | No vendor quote for camera system | Brief note: "No vendor quote exists"; BASIS_OF_ESTIMATE=QUOTE but no quote available | Cannot produce QUOTE-method pricing; parametric fallback used | Obtain competitive quotes from 2-3 security system vendors |
| B-02 | Camera count is assumed (16 locations) | PP-29 (LOW confidence); DEP-0504-003 (prerequisite: DEL-02-01 floor plan) | System price varies with camera count; OPT-08 is based on 16-camera assumption | Finalize architectural layout (DEL-02-01) and confirm camera placement plan |
| B-03 | IT/network infrastructure scope boundary not yet detailed | DEP-0504-004 (interface: DEL-02-06 IT/telecom) | Camera system requires PoE switches, VLAN configuration -- unclear what is included in OPT-08 vs DEL-02-06 | Coordinate with DEL-02-06 estimate to confirm scope split for network equipment |

### Dependencies with Estimating Impact (from Dependencies.csv)

| DependencyID | Type | Target | Statement | Estimating Impact |
|---|---|---|---|---|
| DEP-0504-003 | PREREQUISITE | DEL-02-01 | Camera placement requires architectural layout | Camera count and locations TBD until layout finalized; affects system pricing |
| DEP-0504-004 | INTERFACE | DEL-02-06 | IT/telecom infrastructure compatibility (PoE, VLAN) | Scope boundary for network equipment; potential double-count risk if not coordinated |
| DEP-0504-006 | INTERFACE | DEL-05-03 | Conditional integration with access control | If both elected, integration cost may be additive; not priced in this snapshot |

### Dependencies Without Direct Estimating Impact

| DependencyID | Type | Target | Notes |
|---|---|---|---|
| DEP-0504-001 | ANCHOR | SOW-0503 | Scope traceability; no pricing impact |
| DEP-0504-002 | ANCHOR | OBJ-010 | Objective traceability; no pricing impact |
| DEP-0504-005 | PREREQUISITE | RFP Appendix H | Pricing format requirement; no pricing impact |
