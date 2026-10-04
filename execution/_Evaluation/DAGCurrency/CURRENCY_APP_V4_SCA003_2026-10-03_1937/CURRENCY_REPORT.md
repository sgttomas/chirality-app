# DAG-003 currency audit — APP_V4_SCA003

**Result: `DEPARTURE`.** The current registers add **10 arcs** to the accepted DAG-003 and remove none. Five of the new arcs are **admitted** (they enter the sequencing layer) and five are **held** inside the unchanged 13-member SCC-002. The six SCCs and the 41-node inventory are unchanged. **11 deliverables are `DAG pending`** until the owner accepts the successor DAG-004 or rejects the change.

- **Audit:** `project-dag` `resources/currency.md`, run `APP-V4-SCA003-20261002`, node D1, 2026-10-03 19:37 MDT. Exact commands, exit codes and hashes: [Tool_Run.json](Tool_Run.json). Outputs: `Evidence/`.
- **Basis audited:** commit `75764184b99ab006cd46c1d1c328cf7d5c4d0c8d`, clean tree. That is after every register-changing brief of SCA-V4-003 returned: the 19 ScopeOfWork REVISEs (AK2 part 2, `2d5e6845c5`) and the `dependency-extract` UPDATE of 20 registers (DX, `0e3c55eec5`). One audit, as ARC_EFFECT §4 and DECISION-2 foresee.
- **Placement (departure from the model):** this snapshot sits in the run folder, `DAG_PREP/`, because the D1 brief fences writes there. Its contract home is `_Evaluation/DAGCurrency/`. **`_Evaluation/DAGCurrency/_LATEST.md` was not moved and still names the `CURRENT` observation of 2026-09-29.** Until an authorized node copies this snapshot there and moves that pointer, a consumer that reads only that pointer will not see the departure; the registered analyzer (§3) reports it directly.

## 1. The accepted version

`_DAG/_LATEST.md` is in SPEC §11.2 form: `Latest: DAG-003`, `Basis revision: 8cd783d8d…`, `Supersedes: DAG-002`. It resolves to `_DAG/DAG-003/` and its ACCEPTANCE_RECORD (DECISION-4 of run `APP-V4-SCA002-20260929`, covering project-dag checkpoints 1 and 2). No candidate later than DAG-003 exists under `_DAG/_Candidates/` (DAG-001…003 only), and no `REJECTION_RECORD.md` exists anywhere under `_DAG/`, so no departure has been rejected before.

## 2. Manifest checks

| Check | Result |
|---|---|
| `shasum -a 256 -c MANIFEST.sha256` in `_DAG/DAG-003/` | **37/37 OK**, exit 0. The accepted snapshot is intact |
| `shasum -a 256 -c _DAG/DAG-003/SOURCE_MANIFEST.sha256` in the execution root | **71 OK, 59 FAILED**, exit 1 (`Evidence/source_manifest.stdout.txt`) |
| `shasum -a 256 -c MANIFEST.sha256` in `_DAG/DAG-002/` and `_DAG/DAG-001/` (superseded) | 37/37 and 61/61 OK. History unchanged |

The 59 changed members are 19 `ScopeOfWork.md` (DEL-01-01…01-05, 02-01…02-04, 03-01…03-04, 04-01…04-03, 05-01, 09-06, 09-09), and 20 `Dependencies.csv` and 20 `_DEPENDENCIES.md` (the same 19 plus DEL-05-02). This is exactly the set ARC_EFFECT §4 predicts.

**Inventory.** `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` is byte-unchanged and names `GROUP3-20260928T001055Z`; its `canonical/Deliverables.csv` is unchanged. **No inventory change.** The scope-change pointer `_ScopeChange/_LATEST.md` moved to SCA-V4-003; it is not a manifest member and changes no node.

## 3. Scratch re-application of DAG-003's rules

[Evidence/reapply_selection.py](Evidence/reapply_selection.py) re-applied DAG-003's confirmed SR-1…SR-7 (carried unchanged from DAG-001) to the current registers and compared the result with DAG-003's edge and candidate files. It is not a graph version.

| Comparison | DAG-003 | Current | Change |
|---|---:|---:|---|
| Admitted arcs | 124 | 129 | **+5** |
| Held arcs (SCC holds) | 78 | 83 | **+5** |
| All arcs | 202 | 212 | **+10 added, 0 removed**; no existing arc changes layer |
| SCCs | 6 | 6 | identical member sets (2/13/2/3/2/2) |
| Reciprocal pairs | 24 | 27 | +3, all inside SCC-002 |
| Nodes | 41 | 41 | unchanged (GROUP3) |
| ACTIVE EXECUTION rows | 465 | 567 | +103 added, −1 retired |

The registered `audit_dag.py` (sha256 `830d0d53…3449a`) on the scratch admissible set: exit 0, 212 edges, 6 SCCs, 0 canonical findings.

**Analyzer cross-check.** The registered closure analyzer, run without `--output-dir` (`Evidence/analyzer.stdout.json`), reads the §11.2 pointer and reports `accepted_dag`: version DAG-003, result **`DEPARTURE`**, the same 10 added arcs, 0 removed, 11 `DAG pending`. The closure snapshot `../CLOSURE_APP_V4_SCA003_2026-10-03_1936` holds the same comparison.

**The added arcs against what the owner accepted** (OWNER_ITEMS Q-4, DECISION-1; ARC_EFFECT §1.1). Exactly the expected ten, none extra, none missing, each in the layer ARC_EFFECT predicted ([Evidence/added_arcs.csv](Evidence/added_arcs.csv)):

| Ledger | Consumer → supplier | Representative | Layer | Rows on arc | Reverse arc |
|---|---|---|---|---:|---|
| NR-05 | DEL-01-04 → DEL-01-03 | DEP-01-04-020 | **admitted** | 2 | — |
| NR-07 | DEL-01-04 → DEL-01-05 | DEP-01-04-021 | **admitted** | 1 | — |
| NR-01 | DEL-02-03 → DEL-01-02 | DEP-02-03-028 | **admitted** | 2 | — |
| NR-02 | DEL-03-03 → DEL-01-02 | DEP-03-03-015 | **admitted** | 2 | — |
| NR-04 | DEL-02-02 → DEL-01-02 | DEP-02-02-020 | **admitted** | 2 | — |
| NR-08 | DEL-01-04 → DEL-04-02 | DEP-01-04-022 | held, SCC-002 | 1 | — |
| NR-09 | DEL-01-04 → DEL-02-03 | DEP-01-04-023 | held, SCC-002 | 1 | X-1 (DEP-02-03-027) |
| NR-4 | DEL-01-04 → DEL-02-04 | DEP-01-04-024 | held, SCC-002 | 2 | — |
| R2-04-03-e | DEL-04-03 → DEL-02-01 | DEP-04-03-034 | held, SCC-002 | 1 | DEP-02-01-019 |
| R20-10 | DEL-04-03 → DEL-02-02 | DEP-04-03-035 | held, SCC-002 | 2 | DEP-02-02-017 |

All ten representatives are consumer-side UPSTREAM INTERFACE rows, RequiredMaturity INITIALIZED.

**Guards** (ARC_EFFECT §3; DAG-003 HANDOFF_STATE): absent are N-12, N-B8, NR-03, NR-06, NR-10, the DEL-09-06 reverse citations E-1, K-11, E-5, K-7 and K-6, and both arcs REQ-008's source wording would have produced (DEL-04-01 → DEL-01-04, DEL-04-03 → DEL-01-04). DEL-04-01 has 0 suppliers. No SCC-002 member consumes DEL-09-06; its consumers are still only DEL-03-04 and DEL-09-07. **R17-10 holds:** across both layers DEL-01-02 reaches only DEL-01-01, 01-05 and 04-01, and DEL-01-03 reaches those three and DEL-01-02.

## 4. Classification

**`DEPARTURE`**: arcs were added, five of them to the admitted layer. The SCCs and inventory did not change, so no SCC forms, changes or dissolves, and no case opens or closes. Drift alone (§6) would have been `CURRENT_WITH_EVIDENCE_DRIFT`.

## 5. `DAG pending` deliverables (11)

A pending deliverable gets no ready or blocked verdict from dependencies until the owner decides. Unaffected deliverables keep using DAG-003. **The decision awaited for every row is the same:** the owner's checkpoint decision on the successor candidate DAG-004 (staged at `_Coordination/AgentRuns/APP-V4-SCA003-20261002/DAG_PREP/DAG-004/`), to accept it or reject the change. Either answer clears the flag; a follow-up currency audit then records it.

"→" marks a new input the deliverable consumes; "←" a new consumer of it. A = admitted, H = held (SCC-002, SCC-CASE-002).

| Deliverable | In SCC-002 | New inputs it consumes | New consumers of it |
|---|---|---|---|
| DEL-01-02 | no | — | NR-01 ← DEL-02-03 (A); NR-02 ← DEL-03-03 (A); NR-04 ← DEL-02-02 (A) |
| DEL-01-03 | no | — | NR-05 ← DEL-01-04 (A) |
| DEL-01-04 | yes | NR-05 → DEL-01-03 (A); NR-07 → DEL-01-05 (A); NR-08 → DEL-04-02 (H); NR-09 → DEL-02-03 (H); NR-4 → DEL-02-04 (H) | — |
| DEL-01-05 | no (SCC-001) | — | NR-07 ← DEL-01-04 (A) |
| DEL-02-01 | yes | — | R2-04-03-e ← DEL-04-03 (H) |
| DEL-02-02 | yes | NR-04 → DEL-01-02 (A) | R20-10 ← DEL-04-03 (H) |
| DEL-02-03 | yes | NR-01 → DEL-01-02 (A) | NR-09 ← DEL-01-04 (H) |
| DEL-02-04 | yes | — | NR-4 ← DEL-01-04 (H) |
| DEL-03-03 | yes | NR-02 → DEL-01-02 (A) | — |
| DEL-04-02 | yes | — | NR-08 ← DEL-01-04 (H) |
| DEL-04-03 | yes | R2-04-03-e → DEL-02-01 (H); R20-10 → DEL-02-02 (H) | — |

These are the eleven ARC_EFFECT §4 predicted. **Unlike SCA-V4-002, this departure touches the admitted layer.** Four SCC-002 members (DEL-01-04, DEL-02-02, DEL-02-03, DEL-03-03) gain admitted suppliers outside the cycle (DEL-01-02, DEL-01-03, DEL-01-05). If the successor is accepted, the stated parts of those four that need the named contribution read a blocker from DEL-01-02, DEL-01-03 or DEL-01-05 at INITIALIZED; their satisfaction is read from the live registers (`SatisfactionStatus` TBD or PENDING on all five rows).

**Not pending.** DEL-01-01, DEL-03-01, DEL-03-02, DEL-03-04, DEL-04-01, DEL-05-01, DEL-05-02, DEL-09-06 and DEL-09-09 changed bytes without an added or removed arc (§6). They keep using DAG-003.

## 6. Evidence drift alongside the departure

These changes alter no arc, layer, SCC or inventory. They are read from the live files.

- **Rows.** +103 rows: the 10 new-arc rows, 91 mirror rows (81 mirror-group rows and the 15 Q-17 rows, less the 5 DX did not extract), and 2 new EXTERNAL rows (DEP-04-01-033, DEP-05-01-027). 1 row retired: DEP-03-01-022 (a PACKAGE-target row, R-01-2). Node DX's account (`DX/DX_SCC-CHECK.md`) agrees.
- **Representatives on existing arcs that change by rule (7).** Seven existing arcs were carried in DAG-003 only by the supplier's DOWNSTREAM row. SCA-V4-003 added the consumer's UPSTREAM row on each, and SR-6 now selects it: DEL-02-03 → DEL-04-02 (N-07, DEP-02-03-029), DEL-03-02 → DEL-04-02 (N-05, DEP-03-02-034), DEL-03-03 → DEL-02-01 (N-20, DEP-03-03-017), DEL-03-03 → DEL-04-02 (N-06, DEP-03-03-016), DEL-04-03 → DEL-02-04 (DEP-04-03-036, R22-7), DEL-05-01 → DEL-01-05 (DEP-05-01-026) and DEL-09-06 → DEL-09-01 (DEP-09-06-035). The former representatives become mirrors. Arc and layer are unchanged in each case.
- **Field changes on existing representatives (120 of 195 unchanged representatives):** 83 `LastSeen` only; 11 `Notes`; 22 `Statement` (with `SourceRef` or `EvidenceQuote` in 12); 2 `EvidenceQuote` or `SourceRef` only; 2 `RequiredMaturity` (DEP-03-03-008 and DEP-09-06-015, TBD → INITIALIZED).
- **Mirror maturity.** The two differences DAG-003 routed to owners (DEL-03-03 → DEL-04-01 and DEL-09-06 → DEL-04-03) are now reconciled, both rows INITIALIZED. Three new mirror pairs differ: DEL-06-01 → DEL-01-01 (DEP-06-01-013 TBD / DEP-01-01-030 INITIALIZED), DEL-08-02 → DEL-02-01 (DEP-08-02-006 TBD / DEP-02-01-037 INITIALIZED) and DEL-09-01 → DEL-01-01 (DEP-09-01-019 TBD / DEP-01-01-031 INITIALIZED).
- **Text.** The ScopeOfWork text of 19 deliverables (the SCA-V4-003 MODIFY actions).

## 7. Advice: renewed examination (not `DAG pending`)

The five admitted additions change admitted routes. Through admitted arcs, these deliverables reach a consumer of an added admitted arc, so their routes now also run to DEL-01-02, DEL-01-03 or DEL-01-05: **DEL-03-04, DEL-09-02, DEL-09-06, DEL-09-07, DEL-09-11, DEL-10-03, DEL-10-04, DEL-11-01, DEL-11-02 and DEL-11-03** (`reapplication_result.json` `advice_renewed_examination`). Re-examine their routes when they next rely on those inputs. They are not `DAG pending` on that account. DAG-003's advice list stands.

## 8. What follows

A successor is prepared for these decisions only: DAG-004 (project-dag TRIGGER=SUCCESSOR, CURRENCY_REPORT = this audit), staged at `DAG_PREP/DAG-004/`. This audit does not edit DAG-001, DAG-002, DAG-003, either pointer, any case or any local file. It establishes currency only. It does not establish satisfaction, readiness or lifecycle.
