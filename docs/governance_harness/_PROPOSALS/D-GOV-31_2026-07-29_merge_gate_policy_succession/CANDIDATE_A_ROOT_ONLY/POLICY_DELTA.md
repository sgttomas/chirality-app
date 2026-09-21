# Policy Delta — Candidate A (ROOT-ONLY)

Artifact class: proposal companion; non-authoritative (K-AUTH-1). This file
is the human-readable delta declaration for the Candidate A subject,
`PRD_ROOT_REV7_CANDIDATE.md` in this folder. It rules nothing,
performs no propagation, and is complete on its own — it does not depend on
the Candidate B package.

Live preimage: `docs/PRD_ROOT.md` at
`main@4f7808acb2802443370d045efa198152934c1674`, SHA-256
`0e36a03abc16b86f99024aa2a17c467ae7f4303f9740be3a6ba2e9dd1dfb2f2d`.

## 1. Exact superseded row and exact successor row

Superseded (live `docs/PRD_ROOT.md`, line 454, verbatim):

```text
| **D-8** | Git closeout runs through the change-management role with human-gated PRs; **never self-merge**. | TRANSCRIBED — `execution/_Coordination/LOOP_INIT.md` §7; standing workplan §Closeout; K-MERGE-1 |
```

Successor (candidate line 462, verbatim):

```text
| **D-8** | Root-loop Git closeout runs through the change-management role with human-gated PRs as the standing default; a bounded owner grant, recorded before or at exercise, may authorize merge execution under the merge-gate policy in annex §5.3.1, which preserves K-MERGE-1 and the four closeout identities. Other loops' merge discipline is unchanged and remains under their own instruments. | **PROPOSED (Rev 7)** — successor to the Rev 6 TRANSCRIBED row ("never self-merge"); default source `execution/_Coordination/LOOP_INIT.md` §7; invariant K-MERGE-1; owner policy intent recorded in the D-GOV-31 packet |
```

The label moves from TRANSCRIBED to PROPOSED because the successor changes
doctrine: `execution/_Coordination/LOOP_INIT.md` §7 (line 126) still says
"never self-merge" at this basis, so the successor cannot be transcribed
from any accepted source. No other provenance label is retroactively
changed.

## 2. Policy content (carried in candidate annex §5.3.1)

1. **Default unchanged** — human-gated PRs remain the default; permission
   to merge is required absent a live grant.
2. **Bounded owner grant** — may authorize merge execution; every grant
   defines authoring actor, merge executor, scope (exact PRs/branches/
   paths or a bounded work stretch), duration, expiry, and exclusions;
   recorded before or at exercise (OD-style transcription or PR-carried),
   never after.
3. **Key sentence** (in the annex verbatim): "A bounded owner grant may
   authorize merge execution within its recorded scope and term. It never
   constitutes semantic approval of future unknown content. Each merge
   still requires a human approval vehicle bound to the exact source HEAD,
   verification that HEAD remains unchanged, and a separately recorded
   effective merge identity."
4. **Four identities** preserved in every closeout: semantic approval;
   approved source SHA; merge authorization; effective merge SHA. The
   prior corpus conflated these — no merger-versus-author test ever
   existed as a deterministic check; the identity separation is the
   successor to "never self-merge".
5. **Owner token grammar** lives in the policy (never in transcription
   records): short tokens (`APPROVE <ID>`,
   `RATIFY <IDs> AS ENUMERATED IN <RECORD> <SHA8>`, `SELECT <OPTION>`) are
   lawful only where the exact candidate, SHA, scope, and effect are
   pre-fixed in an immutable record the token names.
6. **Exclusions** — expressly prohibited: agent-authored semantic
   auto-approval; content mutation after approval; force push, rebase, or
   invented conflict resolution; authority beyond the named scope and
   expiry; lifecycle or issuance authority merely from merge permission.
7. **K-MERGE-1 unchanged, evidencing strengthened** — the approved source
   SHA must be pinned in a durable record before merge so the invariant is
   falsifiable; cures the NOT_EVIDENCED failure mode in
   `execution/_Evaluation/MERGE_APPROVAL_MATRIX_2026-07-28_85EA0628/`.
8. **Scope (Candidate A)** — Root-loop Git closeout only. No other loop's
   merge discipline is amended; App, PEC, Piping, and any later registered
   loop remain governed by their own instruments.

## 3. Declared changed-line set (candidate vs. live preimage)

The candidate is byte-identical to the live preimage except these five
regions. `diff` of preimage against candidate reproduces exactly the hunks
listed; no hunk exists outside them.

| Region | Live lines | Candidate lines | Change |
|---|---|---|---|
| R1 | 3–48 | 3–56 | Document-control header blockquote reconciled to Rev 7 (status, accepted Rev 6 basis, adopting instrument D-GOV-31, minimal change envelope, provenance statement, Rev7AmendmentBasis, composite SourceCorpusBasis, revision history, date). Diff hunks: `4c4`, `6c6`, `8,9c8,9`, `13,16c13,18`, `18,24c20,25`, `27,30c28,33`, `35c38,41`, `38,40c44,46`, `45,48c51,56` |
| R2 | 62 | 70 | Provenance-key PROPOSED row updated: O-11 recorded as accepted by D-GOV-28; the D-8 successor recorded as the sole Rev 7 PROPOSED item. Diff hunk: `62c70` |
| R3 | 454 | 462 | D-8 row superseded (§1 above). Diff hunk: `454c462` |
| R4 | insertion after 470 | 478–545 | New annex `#### 5.3.1 Merge-gate policy — the D-8 successor [PROPOSED]` (contiguous heading-to-end block at candidate lines 479–544; diff aligns the neighboring blank lines as `469a478,485` and `470a487,545`) |
| R5 | 951–1004 | 1026–1081 | §10.3 replaced by "Revision 7 amendment mechanics"; §10.4 document-control table reconciled (adopting instrument, predecessor, bases, revision history, change envelope, provenance counts 32 TRANSCRIBED / 5 CLARIFIED / 6 PROPOSED-origin of 43, PROPOSED inventory 19, adoption condition). Diff hunks: `951c1026`, `953,955c1028,1032`, `958,961c1035,1039`, `963,978c1041,1051`, `980,983c1053,1059`, `989,992c1065,1068`, `994,995c1070,1072`, `997,998c1074,1075`, `1000,1004c1077,1081` |

## 4. Propagation obligations on adoption — enumerated, not performed

These are follow-on obligations that Candidate A's adoption would create.
They are Step-4 work owned as listed; nothing here performs them, and no
ordering beyond the stated dependency (adoption first) is implied. All
locations verified at basis `4f7808acb2802443370d045efa198152934c1674`.

| # | Surface | Verified location | Obligation on adoption | Owner |
|---|---|---|---|---|
| 1 | Root scope ledger row SOW-042 | `execution/_Decomposition/chirality_root_scope_ledger_v1_0.csv` line 43 | Restate the SOW-042 obligation text from "never self-merge" to the successor policy, preserving the stable ID and D-8 traceability | SCOPE_CHANGE |
| 2 | DEL-04-06 scope of work | `execution/PKG-04_Developmental_Machinery_and_Change_Control/1_Working/DEL-04-06_Change_Management_and_Human_Gated_Closeout/ScopeOfWork.md` — REQ-001 at lines 62–66, plus seven more no-self-merge occurrences (lines 20, 22, 38, 44, 56–58 CLM-002, 77, 100) | Reconcile requirement, output, and evidence definitions to the four-identity discipline and bounded-grant policy | Downstream contract owner (DEL-04-06 via WORKING_ITEMS) |
| 3 | Loop protocol closeout rule | `execution/_Coordination/LOOP_INIT.md` §7, line 126 ("use CHANGE for Git closeout; never self-merge.") | Amend to the successor default-plus-grant formulation, concordant with the adopted PRD row | HELPS_HUMANS via a human-gated M2 tranche |
| 4 | Deterministic G4 check | `tools/validation/validate_instruction_tranche_manifest.py` — self_merge must-be-false check at lines 304–308 (schema comment line 40; `REQUIRED_M2_KEYS` line 123) | Extend semantics so a recorded bounded grant is representable without weakening the default (see row 6); never silently delete the check | HELPS_HUMANS via a human-gated tools tranche |
| 5 | G4 check test | `tools/validation/test_validate_instruction_tranche_manifest.py` — `test_block_on_self_merge` at lines 228–234 | Update in the same tranche as row 4, preserving a failing test for undeclared self-merge | Same tranche as row 4 |
| 6 | Tranche-manifest schema semantics | `instruction-tranche-manifest/v1`, `m2_gate.self_merge` (must-be-false) | Define how a bounded owner grant is declared (e.g. a grant-reference field naming the durable grant record) so `self_merge: false` remains the default and any exception is explicit and falsifiable | HELPS_HUMANS |
| 7 | Practitioner harness invariant map | `tools/practitioner_harness/harness_common.py` line 78 (`"K-MERGE-1": "RATIFIED"`) | Verify the K-MERGE-1 ratification mapping remains accurate under strengthened evidencing; no change expected unless `docs/CONTRACT.md` §1.8 enforcement wording is amended | HELPS_HUMANS |

**Note on task-brief anchors.** The dispatch brief cited the validator check
at line 307 and its test at line 234; at this basis the check spans lines
304–308 and the test function spans lines 228–234. The table above records
the verified anchors.

**Expressly a non-obligation:** SHA-pinned historical mirrors, frozen
proposal and evidence packages (including the D-GOV-28 and D-GOV-30
packages and the OD7-G1 manifests), `LOOP_RECEIPTS.md` receipts, and OD
transcription records are NOT rewritten. Historical statements of the old
rule remain historical statements.

## 5. Candidate A / Candidate B divergence declaration

The two candidates are independently complete and differ in exactly seven
lines, all scope-bearing: the header status line, the header
change-envelope scope phrase, the D-8 row, the annex Scope paragraph, the
§10.3 scope-limit propagation tail, and the §10.4 Status and Change
envelope rows. Candidate A carries no shared-CHANGE or M6 obligation.
