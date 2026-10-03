# Basis and decomposition amendment — SCA-V4-003, node P1 (repaired at RP1)

**Status: PROPOSED. Nothing here is applied.** Basis: HEAD `897a107cc9`; the
files these edits target are unchanged at `423f65ca4f` (V23's candidate,
`git diff --name-only`). RP1 (after review V23, finding B-1) turned every
non-ScopeOfWork edit into exact bytes, so that "accept as recommended" fixes
every byte except the slots listed with their rules. The ScopeOfWork blocks
are in [SOW_REVISIONS_A.md](SOW_REVISIONS_A.md) and
[SOW_REVISIONS_B.md](SOW_REVISIONS_B.md); the register draft is
[Amendment_Actions.draft.csv](Amendment_Actions.draft.csv).

## Edits at a glance

| # | Target | Kind | When applied | Owner item | Ledger |
|---|---|---|---|---|---|
| B-01 | `_Decomposition/SOFTWARE_DECOMP.md`, `## Decision Log` | Change Register entry | After group-3 acceptance (acceptance-conditional) | Q-3 | DC-01 |
| B-02 | `_Decomposition/Open_Issues.csv` OI-009 `Status`, `Consequence` | Decided status and pointer | Candidate | Q-10 | SC3-01-05-8 |
| B-03 | `_Decomposition/Open_Issues.csv` OI-018 `Consequence` | Pointer; status unchanged | Candidate | Q-11 | OI-018-ptr |
| C-01 | `_ScopeChange/_LATEST.md` | Pointer move, SPEC §11.2 form | After group-3 acceptance (acceptance-conditional) | Q-3 | — |
| C-02 | `_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_{C02_UTC}_EFFECTIVE_STATE/EFFECTIVE_STATE.md` (new) | SCA-V4-002 effective-state note | After group-1 acceptance | Q-16 | — |
| D-01 | SCA-V4-003 `Supersession_Delta.csv` and `Supersession_Map.csv` | One row under Q-10 B | Candidate | Q-10 | SC3-01-05-8 |

## A. Accepted basis documents (`projects/chirality-app-v4/docs/`)

**None.** No basis text changes under the recommended dispositions, so
`_Decomposition/Consolidated_Coverage.csv` needs no recompute.

| Ledger ID | Item | Disposition | Why |
|---|---|---|---|
| P2-C1-B-B-1 | No accepted text decides the supplier's own start-up traffic | DROP | Answered by the owner (K-12 as revised, L-3); the ScopeOfWork route is SC3-01-05-5 |
| P2-C1-B-B-2 | Whether V4-HI-02 should name the catalog edition | DEFER | Observation for the basis owner, only if S-01-3 is accepted; no text proposed |
| P2-C1-B-B-3 | V4-HI-11 against R13-1 | DROP | Source proposes no change; recorded as a host non-conformance (SWBPIPE SQ-07) |
| P2-C1-C-B-1 | ARCHITECTURE §4 allow-list bullet: add the K1-5 rule | DEFER | Optional; the present text does not contradict K1-5; a basis edit would force a Consolidated_Coverage recompute. Next basis update |
| P2-C1-C-B-2 | V4-HI-70 / V4-HOST-02: whether boundary-refused destination requests are also recorded | DEFER | Owner phase-review question; narrowed by R16-1 |
| SIWC-custody | V4-ARC-04 custody rule for a ChatGPT plan grant | DROP | Recommendation superseded 2026-10-02; returns only if SIWC is reopened |

## B. Decomposition package (`execution/_Decomposition/`)

### B-01 · `SOFTWARE_DECOMP.md` — Change Register entry — acceptance-conditional

Insert after the SCA-V4-002 entry of `## Decision Log` (the old block occurs
once; checked by script):

```old
Snapshot: `../_ScopeChange/SCA-V4-002_2026-09-29_1901`.

## Checkpoint and next stage
```
```new
Snapshot: `../_ScopeChange/SCA-V4-002_2026-09-29_1901`.

- SCA-V4-003 ({ACCEPT_DATE}), requested by the owner (run APP-V4-DESIGN-PASS-3-20261001, start and closeout directions; run APP-V4-SCA003-20261002): MODIFY only. ScopeOfWork text of DEL-01-01, DEL-01-02, DEL-01-03, DEL-01-04, DEL-01-05, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-04-01, DEL-04-02, DEL-04-03, DEL-05-01, DEL-09-06 and DEL-09-09, carrying the contract proposals of design passes 2 and 3{Q5_CLAUSE}; {OI009_CLAUSE}{OI018_CLAUSE}{D021_CLAUSE}. No decomposition ID was added, retired, renumbered or moved (the ScopeOfWork files gain local IDs listed in their AX lines); 11 Packages, 41 Deliverables and 262 scope IDs are unchanged. Snapshot: `../_ScopeChange/{AMENDMENT_SNAPSHOT}`.

## Checkpoint and next stage
```

**Slot rules** (fixed by the group-2 decision; no "where accepted" text is
applied):

| Slot | Filled with | If not accepted |
|---|---|---|
| `{ACCEPT_DATE}` | the group-3 acceptance date | — |
| `{AMENDMENT_SNAPSHOT}` | the accepted snapshot folder name | — |
| `{Q5_CLAUSE}` | `, including the App act control in DEL-01-04` if Q-5 is accepted | the empty string |
| `{OI009_CLAUSE}` | Q-10 B: `Open_Issues OI-009 Status (RESOLVED_BY_OWNER_DECISION) and Consequence`; Q-10 A: `the Open_Issues OI-009 Consequence pointer` | — |
| `{OI018_CLAUSE}` | ` and the OI-018 Consequence pointer` if the OI-018 pointer (Q-11) is accepted | the empty string |
| `{D021_CLAUSE}` | `; and a Supersession_Delta row binding the GROUP3 OI-009 Status` under Q-10 B | the empty string |

A scratch copy filled with test values (all slots, recommended options) was
checked: the old block occurs once, no `{` remains, and nothing else in the
file changes.

### B-02 and B-03 · `Open_Issues.csv` OI-009 and OI-018

**Recommended status word (Q-10 option B): `RESOLVED_BY_OWNER_DECISION`.** It
follows the file's `RESOLVED_BY_<authority>` pattern (`RESOLVED_BY_SOURCE`,
`RESOLVED_BY_GROUP2`). No tool constrains the vocabulary: the audit script
counts any value other than `OPEN` as resolved (`BASELINE/audit_checks.py`
lines 350–351). Alternatives: `RESOLVED_FOR_CURRENT_DEFINITION_RUN` (the OI-017
precedent; it understates a product-level choice) or option A (keep `OPEN`).

Whole-field old → new (the edit is row-scoped; other fields and rows are
byte-identical):

| Row · column | Old field value (whole) | New field value (whole) |
|---|---|---|
| OI-009 · `Status` (option B) | `OPEN` | `RESOLVED_BY_OWNER_DECISION` |
| OI-009 · `Consequence` (option B) | `Do not silently carry current v3 overlay or Root behavior into new product choice. Required associated definition/receiving work is IN; this issue holds the unresolved detail, not the existence of the required result.` | `Do not silently carry current v3 overlay or Root behavior into new product choice. Required associated definition/receiving work is IN; this issue holds the unresolved detail, not the existence of the required result. Decided at choice level by APP-V4-DESIGN-PASS-3-20261001-DECISION-K3 K-1: the App's Codex shares the person's settings, providers and MCP servers and signs in separately, custodied by Codex in an App-owned home; taken by the Owner, who is also the App implementation owner (APP-V4-DESIGN-PASS-3-20261001-DECISION-L L-7), and recorded in DEL-01-05 Design/ACCOUNT_HOME_DECISION_RECORD.md. The mechanism was observed at Codex 0.158.0 without a credential (DEL-01-01 Design/OBS_2_0.158.0.md O-6); sign-in with a credential is not observed (DECISION-L L-6), and API-key behaviour stays with OI-010. Frozen Group3 retains the historical OPEN row.` |
| OI-009 · `Consequence` (option A; Status stays `OPEN`) | same | `Do not silently carry current v3 overlay or Root behavior into new product choice. Required associated definition/receiving work is IN; this issue holds the unresolved detail, not the existence of the required result. Decided at choice level by APP-V4-DESIGN-PASS-3-20261001-DECISION-K3 K-1: the App's Codex shares the person's settings, providers and MCP servers and signs in separately, custodied by Codex in an App-owned home; taken by the Owner, who is also the App implementation owner (APP-V4-DESIGN-PASS-3-20261001-DECISION-L L-7), and recorded in DEL-01-05 Design/ACCOUNT_HOME_DECISION_RECORD.md. The mechanism was observed at Codex 0.158.0 without a credential (DEL-01-01 Design/OBS_2_0.158.0.md O-6); sign-in with a credential is not observed (DECISION-L L-6), and API-key behaviour stays with OI-010. The row stays OPEN by the owner's choice (SCA-V4-003 Q-10 option A).` |
| OI-018 · `Consequence` (Q-11) | `Current owner direction settles manuals as core practice; exact mechanism remains open.` | `Current owner direction settles manuals as core practice; exact mechanism remains open. For the App, answered by DECISION-K3 K-9 as amended by DECISION-L L-2 (APP-V4-DESIGN-PASS-3-20261001); hosts and other instruction owners remain open.` |

- **CSV quoting and line endings.** The file uses CRLF. The OI-009
  Consequence is already quoted; the new OI-018 Consequence contains a comma
  and must be written quoted (`"…"`). Apply with a CSV writer that keeps the
  other rows' bytes and CRLF, or by row-scoped replacement of the quoted
  field, as the scratch check did.
- **Result hashes** (from the current file `a11782181531ce77…`, checked by
  re-parsing: only the named fields differ):

| Variant | Result sha256 | OPEN count |
|---|---|---|
| Q-10 B with the OI-018 pointer (recommended) | `9c2d916c277f8ce4b847c9c532822d0566e59517ba9e0a86b650fe0450f3515d` | 22 |
| Q-10 B without the OI-018 pointer | `23b5a8315a4d2d9003843f5844b4e243fd5c18390f19d1576162304762048dac` | 22 |
| Q-10 A with the OI-018 pointer | `a8be3024b481090c96b75d1f5c76e4fb1a603f009bb5bd78b4504191ca9d74d3` | 23 |
| Q-10 A without the OI-018 pointer | `418755dfe0ca3a9a3b665c9058aae33395652ef360a63c33760368e523f0af9c` | 23 |

- **Owner field** of OI-009 ("Owner with App implementation owner") is left
  as written: it names who owned the open question; L-7 is recorded in the
  Consequence and in the DEL-01-05 register refresh R3-01-05-c.
- **Telemetry:** `Coverage_Telemetry.json` stays STALE_REBUILD_REQUIRED; under
  option B its open-issue count differs by one more (pre-change audit COV-116).

**No other decomposition file changes.** `ScopeLedger.csv`, `Packages.csv`,
`Objectives.csv`, `Vocabulary_Map.csv`, `Deliverables.csv`, the other
registers, `Consolidated_Coverage.csv`, `checkpoint_snapshots/_LATEST_ACCEPTED.md`
and `_Decomposition/_LATEST.md` are unchanged (SCA-V4-002's reading rule
already covers a later amendment). Considered and not proposed: naming the act
control in DEL-01-04's `Deliverables.csv` Description; it does not contradict
SC3-01-04-1, and the pre-change audit's Check 5 is MATCH for all 32.

## C. Scope-change pointer and records

### C-01 · `_ScopeChange/_LATEST.md` — acceptance-conditional

Replace the whole file with (tokens filled at the act):

```text
Latest: {AMENDMENT_SNAPSHOT}
Updated: {ACCEPT_DATE}
Amendment: SCA-V4-003
Accepted predecessor: SCA-V4-002_2026-09-29_1901
Closure: {CLOSURE_VERDICT}

# Active SCOPE_CHANGE Snapshot

**Status:** `{CLOSURE_VERDICT}`
**Active snapshot:** `execution/_ScopeChange/{AMENDMENT_SNAPSHOT}/`
**Amendment:** `SCA-V4-003`, the contract proposals of App v4 design passes 2 and 3 (run `APP-V4-SCA003-20261002`)
**Accepted:** checkpoint group 3 on {ACCEPT_DATE} (`execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-3_{ACCEPT_DATE}/`); groups 1 and 2 (`execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-1_{G1_DATE}/`, `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-2_{G2_DATE}/`)
**Accepted predecessor:** `execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` (closure verdict: `OPEN_PENDING_DERIVATIVE_CLOSURE` per `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_{C02_UTC}_EFFECTIVE_STATE/EFFECTIVE_STATE.md`)
**Post-acceptance validation:** `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-003_{UTC}/`

SCA-V4-003 makes MODIFY actions only: ScopeOfWork text of 19 deliverables
(the six standalone-App deliverables DEL-01-02, DEL-01-03, DEL-01-04,
DEL-01-05, DEL-02-02 and DEL-02-04, and thirteen first-increment
deliverables), carrying the accepted contract proposals of design passes 2
and 3; Open_Issues OI-009 and OI-018; and the Change Register entry.
Topology is unchanged: 11 packages, 41 deliverables and 262 scope IDs.

Open, separately governed: the 19 ScopeOfWork REVISEs (`scope-of-work` MODE=REVISE, `STATUS_POLICY` `NO_STATUS_TOUCH`); the dependency-register UPDATE of 20 registers (`dependency-extract`); the DAG-003 departure and the DAG-004 candidate (owner acceptance); the Design re-pins after the REVISEs, GUIDE last; `_Decomposition/Coverage_Telemetry.json` (`STALE_REBUILD_REQUIRED`, owned by the decomposition owner; carried from SCA-V4-001); `audit-scope-closure` for SCA-V4-003.

It makes no release, publication or reliance claim.
```

| Slot | Filled with |
|---|---|
| `{AMENDMENT_SNAPSHOT}` | the accepted snapshot folder name (`SCA-V4-003_{YYYY-MM-DD}_{HHMM}`) |
| `{ACCEPT_DATE}` | the group-3 acceptance date |
| `{CLOSURE_VERDICT}` | the accepted closure verdict (expected `OPEN_PENDING_DERIVATIVE_CLOSURE`) |
| `{G1_DATE}`, `{G2_DATE}` | the dates in the group-1 and group-2 decision-snapshot folder names |
| `{C02_UTC}` | the UTC stamp of the C-02 folder |
| `{UTC}` | the UTC stamp of the post-acceptance validation folder |

**Parser check.** A scratch copy filled with test values was read by the
registered `validate_domain_decomposition_integrity._latest_pointer_target`:
it returns the snapshot name, and `_pointer_matches` is True.

### C-02 · SCA-V4-002 effective-state note — after group-1 acceptance (Q-16)

New file `_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_{C02_UTC}_EFFECTIVE_STATE/EFFECTIVE_STATE.md`:

```text
# SCA-V4-002 — effective state (update)

Record written: {C02_UTC}, by HELP_HUMAN, at HEAD {HEAD}, after the owner
accepted SCA-V4-003 checkpoint group 1. Append-only: it edits no SCA-V4-002
group-bound byte, moves no pointer and accepts nothing.

Since the record of 20260930T044342Z:
- The Design re-pins to the amended basis documents: done in run
  APP-V4-DESIGN-PASS-2-20260930 (Wave A); checked for SCA-V4-003 by review
  V23b: all 18 Design files that pin the basis documents carry their current
  hashes.
- The SWBPIPE handoff "local-first" line: replaced in that run (its closeout
  C1-C, "Confirmations": HANDOFF line 22 reads "on a model the person
  chooses, local or cloud, with no default"); not yet relayed.
- Still open: the Coverage_Telemetry.json rebuild (still Revision
  G3-draft-1), owner-deferred under APP-V4-BASIS-ALIGN-20260928 DECISION-8.

Closure verdict of the amendment record: OPEN_PENDING_DERIVATIVE_CLOSURE, for
Coverage_Telemetry.json only.
```

Slots: `{C02_UTC}` the UTC stamp of the folder; `{HEAD}` the commit at which
it is written.

## D. Supersession

- **Q-10 option B (recommended):** `Supersession_Delta.csv` is exactly:

```csv
AmendmentID,DecisionID,SupersededAuthorityRole,SupersededAuthorityPath,SupersededAuthorityRef,SupersededFactKey,SupersededFactTextOrValue,OverrideType,ReplacementFactTextOrValue,AppliesToRoots,AppliesToFacilities,AppliesToSections,Notes
SCA-V4-003,D-021,OTHER,projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Open_Issues.csv,"OpenIssueID OI-009, column Status",OPEN_ISSUES_OI_009_STATUS,OPEN,SUPERSESSION,RESOLVED_BY_OWNER_DECISION,,,,"APP-V4-DESIGN-PASS-3-20261001-DECISION-K3 K-1 and DECISION-L L-7 (owner, 2026-10-01/02); SCA-V4-003 action 21 (Q-10 option B). The Consequence field is appended, not superseded."
```

  The superseded value was checked: the GROUP3 canonical `Open_Issues.csv`
  row OI-009 has `Status` `OPEN`. Register action 21 then has
  `SupersessionBindingPresent` `YES`.
- **Q-10 option A:** no delta; action 21's `SupersessionBindingPresent` is `NO`
  and its Description reads "Consequence pointer appended; Status stays OPEN".
- **Map:** accumulated from SCA-V4-002's `Supersession_Map.csv` (29 rows) with
  `tools/coordination/accumulate_supersession_map.py`. Scratch runs: with the
  delta, exit 0, 30 rows, 0 findings; without a delta, exit 0, 29 rows.
- ScopeOfWork edits bind no row (IMPACT §7).
