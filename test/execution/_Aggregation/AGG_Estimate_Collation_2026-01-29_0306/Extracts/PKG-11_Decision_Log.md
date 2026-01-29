# Decision Log

## PKG-11 Marine Loading System Estimate

| ID | Decision Statement | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | How to Override |
|----|-------------------|---------|----------|------------------|-----------------|-----------------|
| D-001 | Currency set to CAD (Canadian dollars) | Default selection required | Project location: Fraser Surrey Terminal, Surrey, BC, Canada per decomposition Section 1 | All | All amounts | Set `currency` in _CONFIG.md |
| D-002 | Marine loading arm assumed as OEM-supplied package with Contractor installation | Procurement approach clarification | Industry standard for specialized marine loading equipment | MAT, CD | Equipment as single procurement; install separate | Confirm procurement strategy |
| D-003 | Loading arm foundation assumed in PKG-08 Marine Structures scope | Scope boundary clarification | Decomposition shows PKG-08 Marine Structures separate from PKG-11 | PKG-11 interface | Foundation excluded from PKG-11 | Include foundation if scope changes |
| D-004 | Productivity factor set to 1.0 (BC lower mainland baseline) | No site-specific productivity data | Project location in established industrial port area | PKG-11 / CD | Labor rates | Provide site-specific productivity factors |
| D-005 | Marine/jetty access assumed with coordination for terminal operations | Working conditions clarification | Active terminal with vessel operations | PKG-11 / CD, CI | Marine access logistics | Provide terminal coordination plan |
| D-006 | Working hours assumed standard 8-10 hour shifts; marine work may require tide windows | No shift schedule provided | Typical marine terminal construction | PKG-11 / CD, CI | Labor productivity | Provide project schedule/shift requirements |
| D-007 | All pricing via allowances (fallback typical model) | No vendor quotes or rate tables available | Source index search returned no pricing sources | All | 100% allowance basis | Provide vendor quotes or rate tables |
| D-008 | Indirects factors applied per fallback typical model (CI 18%, PM 6%, P 2%, COM 4%) | No project-specific indirects data | Fallback typical model per AGENT_ESTIMATING STRUCTURE; COM elevated to 4% for marine loading commissioning complexity | CI, PM, P, COM | $335,000 indirects | Provide project-specific indirects |
| D-009 | Contingency rates elevated due to 100% allowance-based estimate (+10% on direct CBS, +5% on factors) | High uncertainty in allowance-based estimate | Per AGENT_ESTIMATING fallback contingency method | CONT | 25.7% weighted contingency | Reduce allowance share with quotes |
| D-010 | Escalation mode set to NONE | Default selection | Pricing date is current (January 2026) | All | No escalation | Set `escalation_mode` in _CONFIG.md |
| D-011 | Double-walled pipe routing assumed at 150 lm from tank farm to berth | No layout drawings available | Typical routing for marine terminal with tank farm setback | MAT, CD | Pipe quantity basis | Provide DEL-11.01 with actual routing |
| D-012 | Loading arm size assumed 12-16 inch nominal for canola oil throughput | No loading rate specified | 1,000,000 MT/annum OBJ-2 implies ~2,000-4,000 m³/hr loading rate | MAT | Loading arm size/cost | Confirm loading rate from ER |
