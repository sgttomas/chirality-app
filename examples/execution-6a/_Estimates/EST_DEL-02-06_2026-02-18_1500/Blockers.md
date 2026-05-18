# Blockers Report

## Run: EST_DEL-02-06_2026-02-18_1500

## Summary

- **Blocking dependencies affecting pricing:** 0
- **Blocking dependencies affecting execution (future):** 4 upstream prerequisites with TBD satisfaction status
- **Impact on this estimate run:** NONE -- rate-table pricing uses area/quantity parameters from Assumed_Project_Parameters.csv and does not require resolved upstream deliverables

## Upstream Dependencies (from Dependencies.csv)

### Prerequisites (TBD satisfaction)

| DependencyID | Target | What is Needed | Blocking for Estimate? | Notes |
|-------------|--------|---------------|----------------------|-------|
| DEP-0206-E01 | DEL-02-01 (Architectural Program) | Floor plan, room schedule, IT room location/sizing | NO | Needed for detailed design, not rate-table pricing; ASM-001 area split covers estimate needs |
| DEP-0206-E02 | DEL-02-02 (Firehall Apparatus Bays) | Apparatus bay layout for electrical service location | NO | Bay count (4 fire) is confirmed (PP-11); layout needed for design, not rate-based pricing |
| DEP-0206-E03 | DEL-02-05 (Mechanical/Plumbing) | HVAC loads and door opener electrical requirements | NO | Mechanical loads are embedded within the per-sf rate for electrical distribution |
| DEP-0206-E08 | Functional Program (Appendix B) | Meeting room EM workstation layout | NO | Data drop count (45 including 15 EM workstations) is assumed per PP-27 |

### Interfaces (TBD satisfaction)

| DependencyID | Target | What is Needed | Blocking for Estimate? | Notes |
|-------------|--------|---------------|----------------------|-------|
| DEP-0206-E04 | DEL-02-07 (Emergency Power) | ATS location and essential loads list | NO | Normal-side distribution is priced; ATS/generator scope is in DEL-02-07 |
| DEP-0206-E06 | DEL-03-04 (Site Utilities) | External electrical service from site utility tie-ins | NO | Service entrance (ES-14) is priced within DEL-02-06; site-side tie-in is DEL-03-04 scope |
| DEP-0206-E07 | DEL-02-04 (Structure/Envelope) | Ceiling height and structural clearance for fixture mounting | NO | Rate-based pricing does not require specific fixture mounting heights |

## Conclusion

No dependencies block the production of a meaningful rate-table estimate. All upstream prerequisites and interfaces are relevant to detailed design execution but not to area/quantity-based rate application. The estimate is valid for budgeting purposes with the assumptions documented in Assumptions_Log.md.
