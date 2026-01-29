# Decision Log

## PKG-04 Pavement & Surfacing Estimate

| ID | Decision Statement | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | How to Override |
|----|-------------------|---------|----------|------------------|-----------------|-----------------|
| D-001 | Currency set to CAD (Canadian dollars) | Default selection required | Project location: Fraser Surrey Terminal, Surrey, BC, Canada per decomposition Section 1 | All | All amounts | Set `currency` in _CONFIG.md |
| D-002 | Subgrade preparation assumed complete by PKG-02 Earthworks prior to PKG-04 | Scope boundary clarification | Decomposition shows PKG-02 Earthworks & Ground Improvement separate from PKG-04 | PKG-04 / CD | Excludes earthworks costs | Include subgrade if scope changes |
| D-003 | Drainage infrastructure assumed by PKG-03 Underground Utilities | Scope boundary clarification | Decomposition shows PKG-03 Underground Utilities & Drainage separate from PKG-04 | PKG-04 interface | Drainage tie-ins only | Include drainage if scope changes |
| D-004 | Productivity factor set to 1.0 (BC lower mainland baseline) | No site-specific productivity data | Project location in established industrial area | PKG-04 / CD | Labor rates | Provide site-specific productivity factors |
| D-005 | Site access assumed standard via Elevator Road | No access constraints identified | Decomposition Section 1 location description | PKG-04 / CD | No access premiums | Provide access study if constraints exist |
| D-006 | Working hours assumed standard 8-10 hour shifts | No shift schedule provided | Typical industrial construction | PKG-04 / CD, CI | Labor productivity | Provide project schedule/shift requirements |
| D-007 | All pricing via allowances (fallback typical model) | No vendor quotes or rate tables available | Source index search returned no pricing sources | All | 100% allowance basis | Provide vendor quotes or rate tables |
| D-008 | Indirects factors applied per fallback typical model (CI 18%, PM 6%, P 2%, COM 3%) | No project-specific indirects data | Fallback typical model per AGENT_ESTIMATING STRUCTURE | CI, PM, P, COM | $700,000 indirects | Provide project-specific indirects |
| D-009 | Contingency rates elevated due to 100% allowance-based estimate (+10% on direct CBS, +5% on factors) | High uncertainty in allowance-based estimate | Per AGENT_ESTIMATING fallback contingency method | CONT | 27% weighted contingency | Reduce allowance share with quotes |
| D-010 | Escalation mode set to NONE | Default selection | Pricing date is current (January 2026) | All | No escalation | Set `escalation_mode` in _CONFIG.md |
| D-011 | Survey and grade control allowance of $25,000 for layout and verification | No survey scope defined | Required for pavement construction quality | PKG-04 / CD | $25,000 | Provide survey scope/quote |
