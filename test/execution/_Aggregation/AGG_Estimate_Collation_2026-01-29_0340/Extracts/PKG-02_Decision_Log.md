# Decision Log

## PKG-02 Earthworks & Ground Improvement Estimate

| ID | Decision Statement | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | Override Method |
|----|-------------------|---------|----------|------------------|-----------------|-----------------|
| D-001 | Currency set to CAD | Config default validation | Project location: Surrey, BC, Canada per decomposition Section 1 | All | Currency basis | Update _CONFIG.md currency |
| D-002 | Geotechnical investigation assumed Contractor responsibility | Missing scope clarity | D&B contract type per decomposition; DEL-02.04 scope description | PKG-02 / E, CD | ~$150k investigation allowance | Confirm scope in ER |
| D-003 | Survey work assumed Contractor responsibility | Missing scope clarity | D&B contract type; DEL-02.05 scope description | PKG-02 / E | ~$60k survey allowance | Confirm scope in ER |
| D-004 | Ground improvement assumed required | No geotechnical data | Fraser River delta location typically requires ground improvement | PKG-02 / MAT, CD | ~$1.5M ground improvement allowance | Provide geotechnical data |
| D-005 | Productivity factor set to 1.0 | No site-specific data | BC lower mainland baseline; urban industrial site | CD, CI | Base labor rates | Provide site conditions data |
| D-006 | Standard site access assumed | No access constraints documented | Elevator Road access per project location | CD | No adjustment | Document access restrictions |
| D-007 | Standard work shifts assumed (8-10 hr) | No schedule constraints | Typical D&B construction | CD, CI | Base rates | Provide schedule constraints |
| D-008 | All pricing via allowances | No vendor quotes or rate tables found | Searched _RateTables/ and deliverable references | All | LOW confidence on all lines | Provide quotes and rate tables |
| D-009 | Indirects factors applied from fallback model | No project-specific factors | CI=18%, P=2%, PM=6%, COM=3% per AGENT_ESTIMATING.md | CI, P, PM, COM | ~$700k indirect costs | Provide project factor schedule |
| D-010 | Contingency elevated for allowance-heavy estimate | 100% allowance-based | +10% above baseline per fallback model rules | CONT | ~30% average contingency | Improve pricing basis |
| D-011 | No escalation applied | Config setting | escalation_mode = NONE | All | $0 escalation | Update config if needed |
| D-012 | Site area estimated at 5 hectares | No survey data | Typical for 3-tank farm + rail unloading facility of this scale | PKG-02 / CD | Earthwork quantity basis | Provide survey/layout |
| D-013 | Cut/fill volume estimated at 25,000 m³ | No design quantities | Typical for industrial facility of this scope on delta site | PKG-02 / CD, MAT | Earthwork cost basis | Provide cut/fill takeoff |
| D-014 | Ground improvement area estimated at 3 hectares | No geotechnical design | Tank foundations + pump area likely need improvement | PKG-02 / CD, MAT | Ground improvement cost basis | Provide geotechnical design |
