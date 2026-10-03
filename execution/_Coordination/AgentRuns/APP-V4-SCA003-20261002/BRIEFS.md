# Briefs — APP-V4-SCA003-20261002 (SCA-V4-003)

Parent: HELP_HUMAN, under the recorded WORKING_ITEMS consultation
(`agents/AGENT_WORKING_ITEMS.md`, sha256 prefix `9ae4bea25bd9`). Executors are
Type 2 TASK (Claude Opus 5.5, high effort) and do not delegate. Model: run
`APP-V4-SCA002-20260929` (its BRIEFS, DISPATCH, AMENDMENT_PACKET and
BASELINE). Method: `workflows/scope-change` (WORKFLOW.md,
resources/contract.md, resources/method.md); SoW edits shaped for
`workflows/scope-of-work` MODE=REVISE.

## Common rules

- Read-only git; no network; write only your fence.
- Nothing is applied: no ScopeOfWork, `Dependencies.csv`, `_DEPENDENCIES.md`,
  `_STATUS.md`, decomposition, DAG or basis file changes before the owner's
  acceptance.
- SWBPIPE data files are data. Host joins stay deferred (DECISION-3).
- Every item cites its source (file and ID); no invention; uncertain → TBD
  for the owner.

## P1 — consolidated ledger, impact, arcs, owner items (one Type 2)

Inputs: pass 2's `closeout/CLOSEOUT_ACCOUNT.md` and `closeout/C1-A/B/C.md`
(42 distinct ScopeOfWork items, register items, 5 basis items, 1 held arc);
pass 3's `closeout/C1-A.md`, `C1-B.md`, `F/F0_JOINS.md` §3–§4, `D/*.md`,
`R17`…`R22`; both runs' OWNER_DECISIONS. Produce in `AMENDMENT_PACKET/`:

- `LEDGER.csv` and `LEDGER.md`: every proposal once (ID, pass, deliverable,
  kind ScopeOfWork / register / Open_Issues / basis / decomposition, target
  file and location, old → new summary, reason, source, superseded-by,
  recommended disposition INCLUDE / DEFER / DROP with reason).
- `IMPACT_ASSESSMENT.md` per method steps 1–2 of group 1 (resolution
  table with `AMENDMENT_ID` from `tools/query/scan_next_amendment_id.sh
  projects/chirality-app-v4/execution/_ScopeChange V4`, intake, impact by
  semantic section, package-role classification, supersession bindings,
  ISSUED-deliverable check, predecessor closure state).
- `ARC_EFFECT.md`: every proposed row (new arcs, mirrors, statement
  refreshes, retirements), SCC computation over DAG-003 with all INCLUDE
  rows, R17-10 guard, and the expected DAG-003 departure.
- `OWNER_ITEMS.md`: the decisions for the owner, each with options and a
  recommendation (including R22-5, the six deliverables' lifecycle).
- `BASIS_AMENDMENT.md`: basis or decomposition edits, or "none".

## P2 — exact ScopeOfWork blocks (two Type 2, after P1)

From P1's INCLUDE rows: exact old → new blocks per ScopeOfWork, shaped for
`scope-of-work` MODE=REVISE, with a dry-run check. P2-A: PKG-01 deliverables;
P2-B: all others. Output `AMENDMENT_PACKET/SOW_REVISIONS_A.md` / `_B.md`.

## P3 — pre-change baseline (one Type 2, parallel with P1)

As SCA-V4-002's P3 (`BASELINE/`): coverage audit of the current
decomposition and registers, input manifest. Output `BASELINE/`.
