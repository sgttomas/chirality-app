# Decision Log — EST_DEL-020-01_2026-02-27_0700

| DecisionID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used PARAMETRIC method for all line items | BASIS_OF_ESTIMATE=PARAMETRIC; all pricing sources are parametric rate tables and level-of-effort hours | Consistent method across all 18 lines; no mixed methods required |
| DEC-002 | Structured Items.csv with 8 labour line items (ITM-001 through ITM-008) and 10 activity-based items (ITM-009 through ITM-018) | Labour items directly map to Level_of_Effort.csv role allocations; activity items capture discrete commissioning work phases from Procedure Steps 1-11 | Activity items priced at $0 where labour is covered by role line items; avoids double-counting |
| DEC-003 | CBS categories assigned based on Professional_Staff_Rates.csv Category column | Rate table provides explicit category (Management, Construction, Admin, Specialty) for each role | Consistent CBS mapping; all activity-based items classified as Specialty (commissioning scope) except documentation (Admin) |
| DEC-004 | Crane load testing (DL-020-01-011) set to TBD rather than estimated | No third-party crane inspection pricing available in any provided source; FALLBACK_POLICY=ALLOW_PARAMETRIC does not help because no parametric model exists for third-party costs | TBD amount; flagged in QA; requires external quote or parametric source |
| DEC-005 | Safety Code inspection fees (DL-020-01-018) set to TBD | No fee schedule available; RFP S3.3.1 suggests permit fees are Owner responsibility | TBD amount; may be $0 if Owner-borne; flagged in QA |
| DEC-006 | Activity-based lump sum items (ITM-009 through ITM-017) priced at $0 | Labour for these activities is already captured in the role-based line items (ITM-001 through ITM-008); no separate material costs identified | Avoids double-counting; activities serve as scope documentation in Items.csv |
| DEC-007 | WBS_PackageID set to PKG-020 for all lines | DEL-020-01 belongs to PKG-020 per Decomposition S7 | Consistent WBS traceability |
| DEC-008 | UPDATE_LATEST_POINTER=FALSE; no pointer file modified | Per INIT-TASK brief instruction | No side effects on prior snapshots |
