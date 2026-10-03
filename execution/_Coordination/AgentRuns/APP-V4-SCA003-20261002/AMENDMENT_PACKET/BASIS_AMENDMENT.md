# Basis and decomposition amendment — SCA-V4-003, node P1

**Status: PROPOSED. Nothing here is applied.** Basis: HEAD `897a107cc9`.

## A. Accepted basis documents (`projects/chirality-app-v4/docs/`)

**None.** No basis text changes in SCA-V4-003 under the recommended
dispositions. PRD, ARCHITECTURE, HOST_INTEGRATION and EXAMINATION are
unchanged, so `_Decomposition/Consolidated_Coverage.csv` needs no recompute.

The six basis items in the ledger (all from the sources; none proposes text
except where stated):

| Ledger ID | Item | Disposition | Why |
|---|---|---|---|
| P2-C1-B-B-1 | No accepted text decides the supplier's own start-up traffic | DROP | Answered by the owner: K-12 as revised, L-3; the ScopeOfWork route is SC3-01-05-5 (P3RUN C1-B §4.4) |
| P2-C1-B-B-2 | Whether V4-HI-02 should name the catalog edition | DEFER | Observation for the basis owner, only if S-01-3 is accepted; no text proposed |
| P2-C1-B-B-3 | V4-HI-11 against R13-1 | DROP | Source proposes no change; recorded as a host non-conformance (SWBPIPE SQ-07) |
| P2-C1-C-B-1 | ARCHITECTURE §4 allow-list bullet: add the K1-5 rule (text given at source) | DEFER | Optional; the present text does not contradict K1-5; a basis edit would force a Consolidated_Coverage recompute of the ARCHITECTURE rows. Next basis update |
| P2-C1-C-B-2 | V4-HI-70 / V4-HOST-02: whether boundary-refused destination requests are also recorded | DEFER | Owner phase-review question; narrowed by R16-1 (a person's decline is SETTLED through DEL-04-03 CLM-004) |
| SIWC-custody | V4-ARC-04 custody rule for a ChatGPT plan grant | DROP | Recommendation superseded 2026-10-02; returns only if SIWC is reopened (ACCESS §20 triggers) |

If the owner reverses a DEFER here (OWNER_ITEMS Q-12), the edit becomes an
`OTHER` action on the basis file with a Consolidated_Coverage RECOMPUTE of
that file's rows, as SCA-V4-002 A-01/B-01 did.

## B. Decomposition package (`execution/_Decomposition/`)

| # | Target | Edit | When | Owner item |
|---|---|---|---|---|
| B-01 | `SOFTWARE_DECOMP.md`, `## Decision Log` | The SCA-V4-003 amendment entry (ID, date, description, requested by the owner), as SCA-V4-002 B-04 (ledger DC-01) | After group-3 acceptance (acceptance-conditional; slot rule for the date as SCA-V4-002) | Q-3 |
| B-02 | `Open_Issues.csv`, OI-009 `Status` and `Consequence` | Option B (recommended): Status OPEN → the owner's chosen decided value; Consequence cites DECISION-K3 K-1, DECISION-L L-7 and OBS-2 O-6, and that sign-in with a credential is unobserved (L-6). Option A: Status stays OPEN; Consequence gains the same pointer (ledger SC3-01-05-8) | Candidate | Q-10 |
| B-03 | `Open_Issues.csv`, OI-018 `Consequence` | Append: "For the App, answered by DECISION-K3 K-9 as amended by DECISION-L L-2 (APP-V4-DESIGN-PASS-3-20261001); hosts and other instruction owners remain open." Status stays OPEN (ledger OI-018-ptr; text from P3RUN C1-B §4.2) | Candidate | Q-11 |

The exact old bytes of B-02 and B-03 are the current rows (OI-009 Status
`OPEN`, Owner "Owner with App implementation owner"; OI-018 Status `OPEN`,
Consequence "Current owner direction settles manuals as core practice; exact
mechanism remains open."). P2 or the candidate step writes them as exact
old → new, with a dry-run, once Q-10 is answered.

**No other decomposition file changes.**
- `ScopeLedger.csv`, `Packages.csv`, `Objectives.csv`, `Vocabulary_Map.csv`,
  `Allocation_Rationale.csv`, `Source_*.csv`, `Scope_Classification.csv`,
  `ContextBudgetQA.csv`, `External_Dependencies.csv`, `Companion_Inventory.csv`,
  `Consolidated_Coverage.csv`: unchanged.
- **`Deliverables.csv`: unchanged.** Considered: naming the App act control in
  DEL-01-04's Description. Not proposed: the Description ("native request,
  response, turn/outcome and attachment interactions … PKG-04 supplies act
  distinctions") does not contradict SC3-01-04-1, and the obligation lives in
  the Scope of Work, where K1-4 placed it. Likewise DEL-01-05 ("account-home
  and API-key details are decided before dependent implementation"), DEL-02-02
  and DEL-02-04 read consistently with the pass-3 items.
- **Pointers:** `checkpoint_snapshots/_LATEST_ACCEPTED.md` and
  `_Decomposition/_LATEST.md` unchanged; SCA-V4-002's reading rule ("read this
  snapshot as amended by the active scope-change snapshot") already covers a
  later amendment.
- `Coverage_Telemetry.json`: STALE_REBUILD_REQUIRED, carried; outside
  SCA-V4-003.

## C. Scope-change pointer and records

| # | Target | Edit | When |
|---|---|---|---|
| C-01 | `_ScopeChange/_LATEST.md` | Pointer move to the SCA-V4-003 snapshot, in SPEC §11.2 form (as SCA-V4-002 C-01) | After group-3 acceptance |
| C-02 | `_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_{UTC}_EFFECTIVE_STATE/EFFECTIVE_STATE.md` (new, append-only) | Effective-state note for SCA-V4-002: pass 2 re-pinned the Design files and fixed the HANDOFF line; `Coverage_Telemetry.json` still open | After group-1 acceptance (OWNER_ITEMS Q-16) |

## D. Supersession

- **Delta:** empty under Q-10 option A. Under option B, one `SUPERSESSION`
  row, `DecisionID` `D-021` (action 21 of IMPACT §3):
  `SupersededAuthorityPath`
  `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Open_Issues.csv`,
  ref "OpenIssueID OI-009, column Status", original `OPEN`, replacement the
  owner's chosen value.
- **Map:** accumulated from SCA-V4-002's `Supersession_Map.csv` (29 rows) with
  `tools/coordination/accumulate_supersession_map.py`; without a delta the
  prior rows are carried forward through the same tool.
- ScopeOfWork edits bind no row (IMPACT §7).
