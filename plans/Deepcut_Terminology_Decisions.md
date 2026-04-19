# Deepcut Terminology Decisions

## Campaign Reference
- Amendment: SCA-003
- Snapshot: `domain-test/domains/West_Doe_Deepcut_DBM/_ScopeChange/SCA-003_2026-04-19_0900/`
- Date: 2026-04-19

## Normalized Shared Terms

| Term | Canonical Form | Prior Deepcut Form | Prior C&L Form | Matrix Row |
|---|---|---|---|---|
| West Doe Complex | West Doe Complex | West Doe (informal) | TBD | AUTH-001 |
| Tourmaline Oil Corporation | Tourmaline Oil Corporation (TOU) | TOU | TBD | AUTH-001 |
| NorthRiver Midstream | NorthRiver Midstream (NRM) | NRM | TBD | AUTH-001 |
| Millenia Engineering | Millenia Engineering (MLE) | MLE | TBD | AUTH-001 |
| LACT | Lease Automatic Custody Transfer (LACT) | LACT | TBD | AUTH-001 |
| NRM NEBC Connector | NRM NEBC Connector | Pembina HVP Pipeline (legacy) | TBD | AUTH-001 |
| Sales Gas | Pipeline Quality Sales Gas | Sales Gas | TBD | AUTH-011 |
| NGL | NGL (C3+) | LPG (legacy, corrected by SCA-001/003) | TBD | AUTH-011 |
| C3+ | Propane Plus (C3+) | C3/C4 (legacy partial) | TBD | AUTH-011 |
| C5+ | Pentane Plus / Condensate (C5+) | C5+ Condensate | TBD | AUTH-011 |
| Stabilized Condensate | Stabilized Condensate | Stab Condensate | TBD | AUTH-018 |
| Raw Condensate | Raw Condensate | Unstabilized Condensate | TBD | AUTH-018 |
| Produced Water | Produced Water | PW / Sour Water | TBD | AUTH-008/018 |
| Cross-Facility | Cross-Facility | Cross-Fence (corrected: Cross-Fence denotes outside-project flows) | TBD | AUTH-018 |
| SOC | Stabilizer Overheads Compressor (SOC) | SOC | TBD | AUTH-018 |
| VRU | Vapour Recovery Unit (VRU) | VRU | TBD | AUTH-018 |
| MPFS | Medium Pressure Flash Separator (MPFS) | MPFF (legacy) | TBD | AUTH-018 |
| Dual Flare Stack | HP/Cryo and LP Dual Flare Stack | Flare Stack | TBD | AUTH-021 |
| Incinerator | Incinerator | Incinerator | TBD | AUTH-022 |
| Fuel Gas | Fuel Gas | Fuel Gas | TBD | AUTH-004/023 |
| Instrument Air | Instrument Air | Instrument Air | TBD | AUTH-004/023 |
| Heat Medium | Heat Medium System | Heat Medium | TBD | AUTH-023 |
| Emergency Generator | Natural Gas Emergency Generator | Emergency Generator | TBD | AUTH-004/023 |
| Buyback Gas | Buyback Gas | Buyback Gas | TBD | AUTH-023 |
| Acid Gas Disposal Well | Acid Gas Disposal Well (02-25) | Acid Gas Disposal Well | TBD | AUTH-025 |
| Enbridge Meter Station | Enbridge Meter Station | Enbridge Meter Station | TBD | AUTH-026 |
| Metering Independence | Independent Metering | Metering Independence | TBD | AUTH-026 |
| NGL Mercaptan Treating | NGL Mercaptan Treating | LPG Mercaptan Treating (Future, non-regenerative) — corrected by SCA-003 | TBD | AUTH-003/017/020 |
| NGL Molecular Sieve Dehydration | NGL Molecular Sieve Dehydration | LPG Mole Sieve Dryers (Future, 2-tower) — corrected by SCA-003 | TBD | AUTH-003/017/020 |

## SHARED_INTERFACE Resolution Summary

| AuthorityRef | Resolution | Deepcut Action | C&L Implication |
|---|---|---|---|
| AUTH-001 | Project framing normalized to cleaned source §1 | KTY-01-01, KTY-01-02 enriched with TOU/MLE/commercial framework | C&L must carry consistent project framing |
| AUTH-004 | Shared utilities described as 03-25/04-25 shared | KTY-01-04, KTY-05-01, KTY-05-02, KTY-05-07, KTY-12-04 updated | C&L must mirror shared utility descriptions |
| AUTH-005 | Site parameters verified against canonical CSV | KTY-02-01 verified; seismic values corrected (+60-70%) | C&L must carry identical site design parameters |
| AUTH-006 | Well blending philosophy aligned with §3.1 | KTY-03-01 enriched | C&L must describe compatible blending methodology |
| AUTH-011 | Product routing verified (sales gas + NGL from 04-25, C5+ from 03-25) | KTY-03-02 verified and enriched | C&L must describe compatible product definitions |
| AUTH-018 | Cross-fence flows normalized (5 flows) | 7 KTYs updated with cross-facility routing | C&L must mirror each cross-fence flow description |
| AUTH-021 | Dual flare stack at 03-25, shared | KTY-05-05 updated with AUTH-021 pointers | C&L must resolve ISS-006-003 to ISS-006-007 (live sensitivity) |
| AUTH-022 | Incinerator at 03-25, shared | KTY-05-05 updated with AUTH-022 pointers | C&L must resolve same ISS series |
| AUTH-023 | Utilities infrastructure normalized | 6 KTYs updated with shared framing | C&L must mirror utility descriptions; KTY-05-03 retired in C&L |
| AUTH-025 | Acid gas disposal interface normalized | KTY-04-10, KTY-04-11 updated | C&L must carry compatible acid gas scope delineation |
| AUTH-026 | Sales gas pipeline/metering verified | KTY-01-03, KTY-04-15 updated | C&L must carry metering independence statement |

## Open Issues Affecting Comp & Liquids

1. **AUTH-021/AUTH-022 (flare/incinerator):** ISS-006-003 through ISS-006-007 remain unresolved in Comp & Liquids. Deepcut has normalized the wording; C&L must resolve the boundary question before Phase 7 conformity gate.

2. **AUTH-008 (produced water):** Deepcut records outbound flow (04-25 PW to 03-25 at 60/240 m3/d). C&L owns the Liquids Hub storage and H2O2 treatment scope. Flow rates and treatment basis must align.

3. **AUTH-009 (condensate):** Deepcut records outbound stabilized condensate (04-25 to 03-25 Liquids Hub). C&L owns the receiving/treatment/blending scope. Composition and flow basis must align with canonical CSV `table_03_03_02_condensate_flow_rates.csv`.

4. **AUTH-024 (product storage):** Canonical CSV `table_05_03_product_storage_summary.csv` governs both facilities. C&L must verify its 03-25 storage figures match the canonical table.

5. **KTY-05-08 residual LPG terminology:** Outside the frozen SCA-003 amendment scope but carries "LPG Mole Sieve (Future)" in moisture analyzer context. Should be addressed in C&L's Phase 5 SCOPE_CHANGE or a future Deepcut amendment.

6. **NGL pipeline naming (CONFLICT-01): RESOLVED.** Canonical pipeline/offtake destination term is **NRM NEBC Connector** per the cleaned source (Process_DBM_fixed.md §1 line 110, §3.5.2 line 438) and the frozen allocation matrix (AUTH-001, AUTH-013). "Pembina HVP Pipeline" is retained only as legacy prior-DBM wording and must not be used as the current destination label. "Pembina" remains valid only when referring to the propane-plus specification basis (e.g., "Pembina propane plus specification").

7. **Seismic values:** KTY-02-01 corrected seismic parameters upward by 60-70% per canonical CSV. Both roots must carry identical values. C&L should verify alignment.
