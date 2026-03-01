# Decision Log — EST_DEL-014-03_2026-02-27_0901

| DecisionID | Decision | Rationale | Source |
|---|---|---|---|
| DEC-001 | Use PARAMETRIC basis for all line items | BASIS_OF_ESTIMATE=PARAMETRIC; FALLBACK_POLICY=ALLOW_PARAMETRIC; no vendor quotes available in PRICE_SOURCES | Run brief |
| DEC-002 | Apply Underground_Utility_Rates.csv UU-01 ($130/m) for fill line piping | Best available rate for installed water line piping; acknowledges above-grade portion may differ but rate includes installation | Underground_Utility_Rates.csv; Decision to use closest available rate |
| DEC-003 | Use fully burdened labour rates from Construction_Labour_Rates.csv | T-05 Plumber ($92.80/hr) and T-08 Labourer ($65.10/hr) include burden multiplier; this is the correct rate for estimating | Construction_Labour_Rates.csv |
| DEC-004 | Professional staff LOE derived directly from Level_of_Effort.csv x Professional_Staff_Rates.csv | 6 roles, 38 total hours; calculation: PM 6h@$165=$990 + CPM 8h@$155=$1,240 + Supt 10h@$145=$1,450 + Est 4h@$135=$540 + QA 6h@$135=$810 + HSE 4h@$140=$560 = $5,590 | Level_of_Effort.csv; Professional_Staff_Rates.csv |
| DEC-005 | Estimate covers cistern replenishment direction only (not extraction) | RFP language "for external filling" interpreted as filling the cistern from delivery vehicle; bidirectional ambiguity flagged as Conflict C-003 in Guidance.md; conservative scope interpretation | Guidance.md Conflict Table C-003 |
| DEC-006 | Fill line run length assumed at 15 m | Based on building layout context (utility room to north exterior wall in ~13,000 sqft building); no IFC routing available | Parametric assumption; Appendix B conceptual drawing context |
| DEC-007 | Plumber labour estimated at 56 total hours (40 hr rough-in + 16 hr completion) | Scope includes all Procedure Phases 1-4: layout, wall penetration, pump rough-in, fill line, cistern connection, exterior point, freeze protection, stub-out, inspections, final connections, pressure test, flush | Procedure.md; parametric |
| DEC-008 | Labourer support at 24 hours | Approximately 0.4:1 ratio of labourer to plumber hours; material staging, excavation support, general assist | Procedure.md; parametric |
| DEC-009 | Commissioning activities priced as separate line items per Procedure Phase 5 steps | Four distinct commissioning activities identified in Procedure.md; each priced independently for traceability | Procedure.md Steps 5.1-5.5 |
| DEC-010 | Safety Codes permit fee set at $1,500 allowance | No specific fee schedule available; two inspections (rough-in + final) plus permit; rural Alberta context | Parametric allowance |
