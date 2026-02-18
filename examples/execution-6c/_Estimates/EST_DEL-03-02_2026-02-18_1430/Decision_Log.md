# Decision Log: EST_DEL-03-02_2026-02-18_1430

## Defaults Applied

| ID | Decision | Rationale |
|---|---|---|
| DEC-RUN-01 | BASIS_OF_ESTIMATE = RATE_TABLE | Per BOE Section 4 (PKG-05 table, DEL-03-02 row). Validated against enum. |
| DEC-RUN-02 | FALLBACK_POLICY = STRICT | Per run brief. No fallback pricing was needed; all items have direct rate table + LOE evidence. |
| DEC-RUN-03 | ALLOW_MIXED_METHODS = FALSE | Per run brief. All lines are RATE_TABLE; no mixing required. |
| DEC-RUN-04 | ROUNDING = DOLLAR | Per run brief. All amounts are whole dollars (no fractional cents in computed results). |
| DEC-RUN-05 | CBS = MGMT for all lines | Design Manager and Project Manager hours on a plan/narrative deliverable map to Management/Coordination. Consistent with DEL-03-01 (sibling deliverable in PKG-05). |

## Scope Resolution Decisions

| ID | Decision | Rationale |
|---|---|---|
| DEC-SCOPE-01 | DEL-03-02 confirmed as sole in-scope deliverable | Per run brief SCOPE = DEL-03-02. Validated against decomposition Section 8 and Section 7 (PKG-05). |
| DEC-SCOPE-02 | Cost ownership boundary applied per BOE Section 4 (PKG-05 rules) | Design docs plan (milestones, coordination, QA/QC) in DEL-03-02; design methodology narrative in DEL-03-01; construction QC in DEL-09-01. No double-counting. |

## Fallback Uses

None. All items priced from primary sources.
