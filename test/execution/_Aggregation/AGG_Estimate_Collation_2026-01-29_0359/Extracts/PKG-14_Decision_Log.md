# Decision Log

## PKG-14 Process Piping Estimate

| ID | Decision Statement | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | How to Override |
|----|-------------------|---------|----------|------------------|-----------------|-----------------|
| D-001 | Currency set to CAD (Canadian dollars) | Default selection required | Project location: Fraser Surrey Terminal, Surrey, BC, Canada per decomposition Section 1 | All | All amounts | Set `currency` in _CONFIG.md |
| D-002 | Piping assumed to be shop prefabricated with field assembly | Fabrication approach clarification | Industry standard for quality control on large diameter process piping | MAT, CD | Shop vs field labor split | Confirm fabrication strategy in DEL-14.02 |
| D-003 | Welding assumed per ASME B31.3 with coded welders | Welding code clarification | Process piping for petroleum/chemical service | CD | Welder qualification costs | Confirm code requirements in DEL-14.02 |
| D-004 | NDE assumed 100% RT on headers, spot RT on smaller lines | Inspection level clarification | Typical for process headers vs utility piping | CD | NDE costs ~$125,000 | Confirm NDE requirements in DEL-14.02 |
| D-005 | Productivity factor set to 1.0 (BC lower mainland baseline) | No site-specific productivity data | Project location in established industrial port area | PKG-14 / CD | Labor rates | Provide site-specific productivity factors |
| D-006 | Site access assumed via established industrial roads | Access clarification | Fraser Surrey Terminal is operating facility with road access | PKG-14 / CD | Logistics costs | Confirm access restrictions |
| D-007 | Working hours assumed standard 8-10 hour shifts | No shift schedule provided | Typical industrial construction | PKG-14 / CD, CI | Labor productivity | Provide project schedule/shift requirements |
| D-008 | All pricing via allowances (fallback typical model) | No vendor quotes or rate tables available | Source index search returned no pricing sources | All | 100% allowance basis | Provide vendor quotes or rate tables |
| D-009 | Total piping quantity assumed ~1,700 lm across all systems | No P&IDs or piping GAs available | Parametric estimate based on 32 unloading stations, 3 tanks, terminal layout | MAT, CD | Quantity basis for all pipe lines | Complete DEL-14.01 P&IDs and GAs |
| D-010 | Indirects factors applied per fallback typical model (CI 18%, PM 6%, P 2%, COM 3%) | No project-specific indirects data | Fallback typical model per AGENT_ESTIMATING STRUCTURE | CI, PM, P, COM | $835,000 indirects | Provide project-specific indirects |
| D-011 | Contingency rates elevated due to 100% allowance-based estimate (+10% on direct CBS, +5% on factors) | High uncertainty in allowance-based estimate | Per AGENT_ESTIMATING fallback contingency method | CONT | 26.2% weighted contingency | Reduce allowance share with quotes |
| D-012 | Escalation mode set to NONE | Default selection | Pricing date is current (January 2026) | All | No escalation | Set `escalation_mode` in _CONFIG.md |
| D-013 | Rail unloading header sized at 16-20 inch based on 32 station throughput | No hydraulic calculations available | 32 stations × typical 150-200 m³/hr per station = 4,800-6,400 m³/hr total | MAT | Header sizing | Complete DEL-14.03 pipe sizing calculations |
| D-014 | Export piping sized at 12-16 inch based on marine loading rate | No loading rate defined | 1,000,000 MT/annum throughput divided by operating hours | MAT | Export pipe sizing | Confirm loading rate from ER |
| D-015 | Nitrogen distribution assumed 400 lm covering tanks, headers, marine loading | No N2 P&ID available | Blanketing and purge requirements for canola oil service | MAT, CD | N2 system quantity | Complete N2 distribution in DEL-14.01 |
