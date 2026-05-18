# Decision Log — EST_DEL-015-03_2026-02-27_0148

| Decision ID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used App B-Elec conceptual drawing quantities as the basis for receptacle counts | IFC drawings (DEL-004-05) are not yet available; conceptual drawing is the best available source for quantity takeoff | Quantities may change +/- 20% at IFC; impacts all material and some labour lines |
| DEC-002 | Treated 50A/240V welding receptacles using ES-04 all-in installed rate ($950/EA) | Electrical_System_Rates.csv provides a direct parametric rate for 50A welding receptacles installed; avoids double-counting labour + material | L-005 amount = $5,700; L-011 set to $0 to avoid duplication |
| DEC-003 | Separated material costs from labour costs for non-50A receptacles | ES-04 only covers 50A class; no equivalent installed rates for 15A/20A/30A; separate material + labour approach provides better transparency | Material lines (L-001 to L-004, L-006 to L-015) + labour lines (L-017 to L-020) |
| DEC-004 | Used fully burdened electrician rate ($96/hr) from Construction_Labour_Rates.csv T-04 | Direct rate source with burden multiplier already applied (1.6x); PARAMETRIC basis with MEDIUM confidence | All trade labour lines use this rate |
| DEC-005 | Professional staff hours taken directly from Level_of_Effort.csv without adjustment | LoE.csv provides role-specific hours for DEL-015-03; treated as a parametric model output | 6 professional staff lines totalling 38 hours |
| DEC-006 | Added design coordination line item (L-028) not explicitly in LoE.csv | Procedure Phase 1 requires IFC drawing review, RFI resolution, and welder spec confirmation; this effort is beyond routine PM oversight | $1,200 parametric allowance for coordination |
| DEC-007 | Permit fee estimated as parametric allowance at $1,500 | No permit fee schedule in price sources; Alberta Safety Codes permit fees for commercial electrical work typically range $1,000-$2,000 | LOW confidence; actual fee depends on project valuation and municipal authority |
| DEC-008 | FALLBACK_POLICY = ALLOW_PARAMETRIC applied to all items without direct rate evidence | Brief authorizes parametric fallback; 57% of lines use parametric-only pricing | No TBD amounts; all items priced |
| DEC-009 | UPDATE_LATEST_POINTER = FALSE; no pointer file modified | Per brief instruction | No _LATEST.md file written or modified |
