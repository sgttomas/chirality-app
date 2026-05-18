# Source Index

## Run: EST_DEL-02-06_2026-02-18_1500

### Price Sources

| # | File | Source Type | Items Used | Coverage | Notes |
|---|------|-----------|-----------|----------|-------|
| 1 | Electrical_System_Rates.csv | Rate table | ES-01, ES-02, ES-03, ES-04, ES-06, ES-07, ES-09, ES-10, ES-11, ES-13, ES-14 | 11 of 15 items used | Primary pricing source; ES-05 (cold storage) not in DEL-02-06 scope; ES-08 (fire alarm) excluded per DEC-RC-02; ES-12 (cold storage electrical) not in scope |
| 2 | Equipment_Pricing.csv | Rate table | EQ-11, EQ-12 | 2 of 15 items used | EQ-11 (bay displays) cross-referenced with ES-10; EQ-12 (PA system) cross-referenced with ES-09; other items not in DEL-02-06 scope |
| 3 | Construction_Labour_Rates.csv | Rate table | T-07 | 1 of 15 items used | T-07 Electrician fully-burdened rate ($80/hr) used for commissioning labor |
| 4 | Professional_Design_Fees.csv | Rate table | DF-05 | 1 of 8 items used | DF-05 Electrical engineering design fees (2.5% of construction cost) |
| 5 | Assumed_Project_Parameters.csv | Parameters | PP-05, PP-11, PP-12, PP-27 | 4 of 29 items used | PP-05 (18,000 sf building footprint); PP-11/PP-12 (bay counts); PP-27 (45 data drops) |

### Decomposition Source

| File | Version | Items Used |
|------|---------|-----------|
| Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md | v1.0 (Phase 7) | DEL-02-06 deliverable definition; PKG-002 package mapping; SOW-0203, SOW-0208, SOW-0224-0228 scope item linkage |

### Dependency Source

| File | Schema | Items Used |
|------|--------|-----------|
| DEL-02-06 Dependencies.csv | v3.1 | 19 rows (10 ANCHOR + 9 EXECUTION); used for blocker detection and scope boundary validation |

### Items Not Used (from sources in scope)

| Source | ItemID | Reason |
|--------|--------|--------|
| Electrical_System_Rates.csv | ES-05 | Cold storage lighting; not in DEL-02-06 scope (belongs to DEL-04-04) |
| Electrical_System_Rates.csv | ES-08 | Fire alarm system; not mapped to DEL-02-06 in decomposition (DEC-RC-02) |
| Electrical_System_Rates.csv | ES-12 | Cold storage electrical; not in DEL-02-06 scope (belongs to DEL-04-04) |
| Equipment_Pricing.csv | EQ-01 through EQ-10, EQ-13-EQ-15 | Not in DEL-02-06 electrical scope |
| Construction_Labour_Rates.csv | T-01 through T-06, T-08 through T-15 | Not applicable to electrical commissioning |
| Professional_Design_Fees.csv | DF-01 through DF-04, DF-06 through DF-08 | Not electrical discipline |
| Assumed_Project_Parameters.csv | All except PP-05, PP-11, PP-12, PP-27 | Not required for DEL-02-06 pricing |
