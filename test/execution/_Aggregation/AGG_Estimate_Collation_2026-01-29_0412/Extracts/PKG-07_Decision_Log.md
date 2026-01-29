# Decision Log

## PKG-07 Rail Works Estimate

| ID | Decision Statement | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | Override Method |
|----|-------------------|---------|----------|------------------|-----------------|-----------------|
| D-001 | Currency set to CAD | Config default validation | Project location: Surrey, BC, Canada per decomposition Section 1 | All | Currency basis | Update _CONFIG.md currency |
| D-002 | Track length estimated at 500m per new track (Tracks 6, 7) | No design drawings available | 32 railcar unloading stations at ~15m/car spacing per project parameters | PKG-07 / CD, MAT | Track cost basis (~1,000m total) | Provide track layout drawings |
| D-003 | Track 5 restoration length estimated at 300m | No design drawings available | Assumed 60% of new track length for partial restoration scope | PKG-07 / CD, MAT | Track 5 cost basis | Provide Track 5 condition assessment |
| D-004 | Ballast volume estimated at 1.5 m³/linear meter | No ballast design available | Typical rail track ballast section depth/width | PKG-07 / MAT, CD | Ballast cost basis (~1,950 m³ total) | Provide ballast design (DEL-07.03) |
| D-005 | End stops count set to 4 units | Engineering assumption | 2 new tracks × 2 ends each (Tracks 6, 7) | PKG-07 / MAT, CD | End stop cost basis | Confirm end stop requirements in ER |
| D-006 | Productivity factor set to 1.0 | No site-specific data | BC lower mainland baseline; rail work at operating terminal | CD, CI | Base labor rates | Provide site access constraints |
| D-007 | Rail work assumed during normal operations | No schedule constraints | Terminal operations coordination per PKG-34 | CD, CI | Base rates; no shutdown premium | Document operational constraints |
| D-008 | All pricing via allowances | No vendor quotes or rate tables found | Searched _RateTables/ and deliverable references | All | LOW confidence on all lines | Provide rail vendor quotes and rate tables |
| D-009 | Indirects factors applied from fallback model | No project-specific factors | CI=18%, P=2%, PM=6%, COM=3% per AGENT_ESTIMATING.md | CI, P, PM, COM | ~$200k indirect costs | Provide project factor schedule |
| D-010 | Contingency elevated for allowance-heavy estimate | 100% allowance-based | +10% above baseline per fallback model rules | CONT | ~30% average contingency | Improve pricing basis |
| D-011 | No escalation applied | Config setting | escalation_mode = NONE | All | $0 escalation | Update config if needed |
| D-012 | Rail type assumed as 115 RE or equivalent | No rail specification available | Typical heavy rail for industrial trackage | PKG-07 / MAT | Rail material cost basis | Provide rail specification (DEL-07.02) |
| D-013 | Track subgrade preparation included in PKG-02 | Scope split assumption | Earthworks package handles subgrade; rail works package handles ballast/track | PKG-07 / Scope | No subgrade cost in PKG-07 | Confirm scope split in ER |
| D-014 | Track drainage assumed in PKG-03 | Scope split assumption | Utilities package handles track drainage; rail works handles ballast only | PKG-07 / Scope | No drainage cost in PKG-07 | Confirm scope split in ER |
