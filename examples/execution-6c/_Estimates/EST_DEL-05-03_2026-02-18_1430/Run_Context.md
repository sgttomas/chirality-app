# Run Context: EST_DEL-05-03_2026-02-18_1430

## Run Configuration

| Field | Value |
|---|---|
| **RunID** | EST_DEL-05-03_2026-02-18_1430 |
| **AsOf** | 2026-02-18T14:30:00-07:00 |
| **Scope** | DEL-05-03 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 1 priced; 0 blocked; 0 TBD |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-05-03/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | EST_DEL-05-03 |

---

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-05-03 | PKG-02 | PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-03_PricingNarrativeAndAssumptions | TRUE | Pricing Narrative & Assumptions; T4; Narrative substance |

---

## Resolved Paths

| Input | Resolved Path |
|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates |
| Snapshot Folder | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates/EST_DEL-05-03_2026-02-18_1430 |
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| Dependencies.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-03_PricingNarrativeAndAssumptions/Dependencies.csv |
| Professional_Staff_Rates.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv |
| Level_of_Effort.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv |
| Assumed_Project_Parameters.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv |

---

## Defaults Applied

| Default | Value | Rationale |
|---|---|---|
| CBS mapping rule | RoleCategory from Professional_Staff_Rates.csv mapped to CBS codes: Management->MGMT, Financial->FIN | Deterministic mapping from role category; documented in Decision_Log.md |
| Method | RATE_TABLE for all lines | BASIS_OF_ESTIMATE = RATE_TABLE; ALLOW_MIXED_METHODS = FALSE; no fallback required |

---

## Upstream Context (from brief)

| Upstream Deliverable | Estimated Total | Production Cost | Construction Content |
|---|---|---|---|
| DEL-05-01 (Schedule A) | $10,738,960 | $9,960 (72 hrs) | $10,729,000 |
| DEL-05-02 (Schedule B) | $10,735,020 | $6,020 (44 hrs) | $10,729,000 |

Schedule A and Schedule B construction pricing content is fully reconciled at $10,729,000. DEL-05-03 documents the narrative and assumptions underlying those figures.

---

## Warnings

- [WARNING] OI-004 (FF&E treatment) is formally OPEN per decomposition, though assumed as $20,000 cash allowance (Additional Option 6) in upstream DEL-05-01/05-02 estimates. DEL-05-03 narrative must document this assumption.
- [WARNING] All upstream construction pricing content is PARAMETRIC (no vendor quotes). DEL-05-03 narrative must acknowledge parametric basis.
