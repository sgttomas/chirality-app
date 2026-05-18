# Assumptions Log -- EST_DEL-08-01_2026-02-18_1400

## Explicit Assumptions

| ID | Assumption | Source | Impact | Risk if Wrong |
|---|---|---|---|---|
| ASM-001 | Professional hourly rates reflect Alberta 2024 market rates for a Design-Build firm | Professional_Staff_Rates.csv (Basis=MARKET, Confidence=MEDIUM) | Rates may differ +/-20-30% from actual firm rates | Low-medium: estimate would shift proportionally; 30% rate variance = ~$1,400 swing on $4,620 total |
| ASM-002 | Level of effort for DEL-08-01 is 32 total hours (20 Scheduler + 8 PM + 4 CM) based on comparable $15-20M municipal DB proposal efforts | Level_of_Effort.csv (Basis=PARAMETRIC) | Hours may differ based on schedule complexity, number of disciplines, and cross-deliverable coordination needed | Medium: higher-complexity schedule with detailed Gantt could require 40-50 hours; lower-complexity could be 24-28 hours |
| ASM-003 | Scheduler role (R-17) is the primary production role for Gantt chart, critical path analysis, and milestone scheduling | Level_of_Effort.csv row DEL-08-01/R-17 Notes; BOE context | If Gantt production is done by PM or CM instead of dedicated Scheduler, rate and hours allocation shifts | Low: role assignment is a planning decision; total cost similar if redistributed among same-cost roles |
| ASM-004 | DEL-08-01 is a pure proposal production cost (professional hours only); no software licenses, printing, or external consultant costs included | INDEX.md notes: scheduling software costs embedded in R-17 rate | If external scheduling consultant or specialized software is needed, additional cost would apply | Low: Gantt production tools are typically included in overhead; specialized tools would be flagged |
| ASM-005 | The circular dependency between DEL-08-01 and DEL-04-01 does not affect the production cost estimate, only the content alignment process | BOE context (brief) | Production effort is the same regardless of which deliverable leads; iteration costs absorbed in the 32-hour total | Low: if significant iteration is required, additional hours would be needed, but this is captured in ASM-002 range |
