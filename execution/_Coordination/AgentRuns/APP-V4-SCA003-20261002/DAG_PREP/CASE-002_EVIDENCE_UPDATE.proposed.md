# SCC-CASE-002 — proposed evidence update for the DAG-004 candidate (not applied)

**Status: DRAFT, NOT APPLIED.** ARC_EFFECT §4 foresees that "CASE-002 gains evidence rows for the five held arcs", and the DAG-003 precedent wrote such an update into the case files at this stage. The D1 brief fences writes to `DAG_PREP/`, so no file under `_DAG/cases/` was written. An authorized node should apply this through `scc-resolution-case` (evidence update only: no ruling, remedy, closure or membership change) before or at publication, then run the case validator, as the precedent's run record did. The DAG-004 candidate cites the case by `CaseRef` only and does not depend on this update.

## Proposed datasheet section (append after "Successor observation, 2026-09-29 (DAG-003 candidate; evidence update only)")

```markdown
## Successor observation, 2026-10-03 (DAG-004 candidate; evidence update only)

- **Matched snapshot:** `_Coordination/AgentRuns/APP-V4-SCA003-20261002/DAG_PREP/CLOSURE_APP_V4_SCA003_2026-10-03_1936` (to be copied to `_Evaluation/DepClosure/` at publication), positional **SCC-002**. Member set identical to the confirmed 13 members: **no membership change**; the case continues by member-set matching. Source `75764184b99ab006cd46c1d1c328cf7d5c4d0c8d`; frozen manifest SHA-256 `03aa668b88cb1cb32e1d26a15fb64afdf85e0af6fbb61ec89f833eaf5893a8ef`.
- **Why the account changed:** the accepted scope change SCA-V4-003 (run `APP-V4-SCA003-20261002`, DECISION-1 and DECISION-2) revised 19 SoWs and the `dependency-extract` UPDATE (node DX) refreshed 20 registers. Five of the ten new links lie inside this component.
- **Internal account:** 128 source rows / 71 arcs (was 80 / 66); 21 reciprocal pairs inside the component (was 18). +48 rows, all new: the 5 representatives of the new held arcs; 2 mirrors on them (DEP-02-04-019 on NR-4, DEP-02-02-024 on R20-10); 5 consumer-side rows that become the SR-6 representative of an existing held arc (DEP-02-03-029 on DEL-02-03 → DEL-04-02, DEP-03-02-034 on DEL-03-02 → DEL-04-02, DEP-03-03-017 on DEL-03-03 → DEL-02-01, DEP-03-03-016 on DEL-03-03 → DEL-04-02, DEP-04-03-036 on DEL-04-03 → DEL-02-04), whose former representatives become mirrors; and 36 further mirror rows on existing internal arcs.
- **New held arcs** (consumer → supplier; all held `SCC_UNRESOLVED` in the DAG-004 `CandidateEdges.csv`, citing this case; labels from `APP-V4-SCA003-20261002/AMENDMENT_PACKET/ARC_EFFECT.md`):

| Label | Arc | Representative | RequiredMaturity / Satisfaction | Reciprocal with |
|---|---|---|---|---|
| NR-08 | DEL-01-04 → DEL-04-02 | DEP-01-04-022 UPSTREAM INTERFACE | INITIALIZED / TBD | — |
| NR-09 | DEL-01-04 → DEL-02-03 | DEP-01-04-023 UPSTREAM INTERFACE | INITIALIZED / TBD | X-1 (DEP-02-03-027): new pair |
| NR-4 | DEL-01-04 → DEL-02-04 | DEP-01-04-024 UPSTREAM INTERFACE | INITIALIZED / TBD | — |
| R2-04-03-e | DEL-04-03 → DEL-02-01 | DEP-04-03-034 UPSTREAM INTERFACE | INITIALIZED / PENDING | DEP-02-01-019: new pair |
| R20-10 | DEL-04-03 → DEL-02-02 | DEP-04-03-035 UPSTREAM INTERFACE | INITIALIZED / PENDING | DEP-02-02-017: new pair |

- **Admitted arcs leaving the component:** four members gain admitted suppliers outside it: DEL-01-04 → DEL-01-03 (NR-05) and → DEL-01-05 (NR-07); DEL-02-03, DEL-03-03 and DEL-02-02 → DEL-01-02 (NR-01, NR-02, NR-04). None of the suppliers reaches the component (R17-10 holds), so the membership is unchanged.
- **Withheld and guarded:** N-12, N-B8, NR-03, NR-06 and NR-10 are absent; REQ-008's source-wording arcs (DEL-04-01 → DEL-01-04, DEL-04-03 → DEL-01-04) are absent; none of the SCC-enlarging arcs E-1…E-5 or reverse citations K-1…K-12 checked by the DAG-004 assembly is present; DEL-04-01 keeps 0 suppliers; no member consumes DEL-09-06. The component therefore still excludes DEL-09-06, DEL-03-04, DEL-04-01, DEL-01-02, DEL-01-03 and DEL-01-05.
- **What this does not do:** no ruling, remedy, closure, merge, satisfaction or readiness claim. The CP1-20260928 ruling carries forward unchanged. CaseState stays EVIDENCE_ACCUMULATING. The held arcs are non-gating. The DAG-004 candidate is unaccepted until the owner decides.
```

## Proposed Evidence_Register rows (IDs E5-*)

| EvidenceID | SourcePath | Supports |
|---|---|---|
| E5-SCC | the closure snapshot's `Evidence/scc_summary.csv` (sha256 as at copy) | Same 13-member set at `75764184b9`; matched by member set |
| E5-CLOSE | the closure snapshot's `Dependency_Closure_Report.md` | 128 internal rows / 71 arcs; 10 arcs added overall, 5 inside SCC-002; 0 removed |
| E5-PAIR | the closure snapshot's `Evidence/bidirectional_pairs.csv` | 21 reciprocal pairs inside SCC-002 (was 18): DEL-01-04↔DEL-02-03, DEL-02-01↔DEL-04-03, DEL-02-02↔DEL-04-03 new |
| E5-HELD | DAG-004 `CandidateEdges.csv` | 71 held arcs citing this case |
| E5-DEPART | DAG-004 `Evidence/DepartureAccount.json` | 10 added (5 held here), 0 removed, 7 representative changes (5 here), guards |
| E5-CURR | the currency audit's `CURRENCY_REPORT.md` | DEPARTURE against DAG-003; 11 pending |
| E5-ARC | `RUN/AMENDMENT_PACKET/ARC_EFFECT.md` | Predicted arcs, layers and SCC neutrality |
| E5-DX-SCC | `RUN/DX/DX_SCC-CHECK.md` | Register UPDATE result: 212 arcs; SCCs byte-identical |
| E5-OWNER | `RUN/OWNER_DECISIONS.md` | DECISION-1 (Q-4, Q-15, Q-17) and DECISION-2 |

Hashes are to be taken at the time of applying, from the copied locations.

## Proposed Task_Findings row

`F-048`, type `SUCCESSOR_HELD_ARCS_EVIDENCE`, affected DEL-01-04; DEL-02-01; DEL-02-02; DEL-02-03; DEL-02-04; DEL-04-02; DEL-04-03. Summary: closure at `75764184b9` matches this case by the unchanged 13-member set; SCA-V4-003 adds 5 held arcs inside it (NR-08, NR-09, NR-4, R2-04-03-e, R20-10) and 4 members gain admitted suppliers outside it; internal account 128 / 71 / 21 (was 80 / 66 / 18); 5 internal representatives change by SR-6; guards hold; no ruling, remedy or closure. Status `EVIDENCE_RECORDED_NO_RULING`.
