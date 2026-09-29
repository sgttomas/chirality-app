# Arc effect — SCA-V4-002, node P1: N-18, N-21, N-24 and X-1

**Status: PROPOSED.** This file recommends, for each of the four arcs the
owner routed to SCA-V4-002 (`APP-V4-BASIS-ALIGN-20260928` DECISION-10,
option A), whether to keep it, and gives the exact "consumes" sentence. It
then computes the effect on the graph. Nothing here writes a register or a
DAG file.

**Basis:** commit `102f09c1a`. The graph is DAG-002 (`_DAG/_LATEST.md`).

## 1. Recommendation: keep all four

For each arc, the consumer SoW today names the supplier only as an owner. The
registers read ownership sentences as non-edges, so no row was extracted
(CHECKPOINT_C §4). The question is whether the consumer really uses the
supplier's output. For all four, both the consumer's and the supplier's
Design files say it does, in the current phase. The Design files are used
here only as evidence of that; no row is taken from them.

| Arc | Consumer → supplier | Consumer-side evidence | Supplier-side evidence | Phase | Keep? |
|---|---|---|---|---|---|
| **N-18** | DEL-02-01 → DEL-03-02 | WD-v0.6 §8 "Expected **from** suppliers", row DEL-03-02: "P §9; change-item content identity; item dispositions, all-decided, item-left events; governing checkpoint constraint; applied-outcome object identities", used in WD §4.2.2, §4.3.6, §4.3.7, §4.6. WD §4.3.7: "DEL-03-02 supplies per-item dispositions, the "all items decided" indication and item-left events (P §4.3)" | P-v0.6 §13 "Provide to DEL-02-01 / DEL-02-03": per-item dispositions, item-left events, all-items-decided indication, resulting objects for subject binding | Current phase (subject binding §4.3.6 and item decisions §4.3.7). Only the constraint element is governance phase | **Keep.** WD cannot define subject binding or item-level decisions without these outputs |
| **N-21** | DEL-02-03 → DEL-03-02 | EXEC-v0.4 §9.1 row DEL-03-02: per-item dispositions; item-left events; all-items-decided; change-item content identity; applied outcome with resulting objects; stale and application-error outcomes; retry precedence. Used in §4.4, §4.11 (confirms WD §4.3.7), §4.12 (interruption and replay) | P-v0.6 §13, the same "Provide to DEL-02-01 / DEL-02-03" row | Current phase: recording, and REQ-002's "interrupted or replayed history" | **Keep** |
| **N-24** | DEL-02-03 → DEL-03-03 | EXEC §9.1 row DEL-03-03: "§7.7 checkpoint observation on X", used in CH-22 and CH-27 (two-part cases) | ADAPTER-v0.4 §7.7: "**Phase 1 (R8-1).** The adapter observes arrivals and act records and passes them to DEL-02-03 for recording." §11 "Provide to DEL-02-03: External-channel observations (§7.7)" | Current phase (recording on the external channel). The carriage assurance and hold-support inputs are governance phase | **Keep.** Without them, DEL-02-03 cannot record checkpoint arrivals and acts on the external channel |
| **X-1** | DEL-02-03 → DEL-01-04 | EXEC §9.1 row DEL-01-04 (later, D1): "App act control (CAP-2) and person identity", used in §5. EXEC §5: "Construction of the control is DEL-01-04's (later undertaking, D1). App-side positive capture cases are therefore **AWAITING INPUT** (CH-23)"; U-E8 "App person identity scheme; App act control construction — DEL-01-04 … Before App capture fixtures" | DEL-01-04 has no Design file yet (INITIALIZED, later undertaking). Its SoW owns the native act presentation (REQ-005) | Current phase, but only for the App-side positive capture fixtures (OUT-003, VER-003) | **Keep, narrowly.** The owner already kept X-1 (DECISION-6). The sentence ties it to the fixtures that wait for DEL-01-04, not to DEL-02-03's definition work |

**Why not drop X-1.** It is the weakest of the four, because DEL-01-04 is a
later undertaking and its control is built to EXEC §5's requirements. But
EXEC's own positive capture case (CH-23 (ii)) cannot run without it, and that
is a real input. The arc sits inside SCC-002, so it is held and gates
nothing (§3). Dropping it (option D in CHECKPOINT_C) would also reverse the
owner's DECISION-6 answer "keep X-1".

## 2. The sentences

Each sentence goes in the consumer's CLM-002, after its ownership clauses.
They use the "consumes …; does not define" form that this repository's
extractors read as UPSTREAM (compare DEP-02-01-026). The exact old → new
blocks are F-0201-01 and F-0203-01 in [SOW_REVISIONS.md](SOW_REVISIONS.md).

**DEL-02-01, CLM-002 (N-18)**, appended after "These are receiving
interfaces, not transferred implementation assignments.":

> Checkpoint subject binding and item-level decisions consume `DEL-03-02`'s
> change-item content identities, per-item dispositions, all-items-decided
> indication, item-left events and applied-outcome object identities; this
> contract does not define them.

**DEL-02-03, CLM-002 (N-21, N-24, X-1)**, appended after "`DEL-01-04` (later
undertaking) constructs the App act control.":

> This slice consumes, and does not define: `DEL-03-02`'s per-item
> dispositions, item-left events, all-items-decided indication, change-item
> content identities and applied outcomes with their resulting objects, for
> checkpoint recording and interrupted or replayed history (REQ-002,
> REQ-003); `DEL-03-03`'s observations of checkpoint arrivals and act records
> on the external channel, which this slice records (REQ-002, REQ-003); and
> `DEL-01-04`'s App act control and person identity, for the App-side
> positive capture fixtures (OUT-003, VER-003), which await that later
> undertaking.

The ID-shaped text in these quotations is a proposed SoW sentence, shown for
review.

**Guards.**
- Neither sentence names DEL-04-01 or DEL-09-06. No other edit in the packet
  names a deliverable that its SoW does not already name (the mention check
  in `sow_dryrun.py`: 0 new IDs in 9 files).
- No edit makes DEL-04-01 consume anything. DEL-04-01 keeps 0 suppliers.
- No supplier SoW gains a sentence. Any reverse arc would be a separate
  change and would need its own SCC check.

## 3. SCC computation

`arcs.py` (scratch `P1-002/`, sha256 `954f6a82…`) read all 41 live
`Dependencies.csv` at `102f09c1a`. It kept ACTIVE `EXECUTION` rows with a
`DELIVERABLE` target. UPSTREAM rows give From → Target and DOWNSTREAM rows
give Target → From. It then ran Tarjan's algorithm, first on the current
arcs and then on the current arcs plus the four.

**Current state** (reproduces V12 and DAG-002): 41 registers; 462 ACTIVE
EXECUTION rows, 254 with a deliverable target; 198 arcs; 6 SCCs.

| | Now (DAG-002) | With the four arcs |
|---|---:|---:|
| Arcs | 198 | **202** |
| Held (inside an SCC) | 74 | **78** |
| Admitted | 124 | 124 |
| SCC-002 internal arcs | 62 | **66** |
| Reciprocal pairs (all / in SCC-002) | 22 / 16 | **24 / 18** |
| SCCs | 6 | 6, **identical membership** |

SCC-002 stays the same 13 members: DEL-01-04, 02-01, 02-02, 02-03, 02-04,
03-01, 03-02, 03-03, 04-02, 04-03, 05-01, 05-02 and 09-09. The other five
are {07-01, 07-02, 08-01}, {01-01, 01-05}, {01-06, 09-01}, {10-02, 10-04}
and {11-01, 11-03}.

| Arc | Already present? | Reverse row present? | Both ends in SCC-002 now? | Changes the partition on its own? |
|---|---|---|---|---|
| N-18 DEL-02-01 → DEL-03-02 | no | yes, DEP-03-02-027 (N-B3) | yes | no |
| N-21 DEL-02-03 → DEL-03-02 | no | no | yes | no |
| N-24 DEL-02-03 → DEL-03-03 | no | yes, DEP-03-03-014 (N-27) | yes | no |
| X-1 DEL-02-03 → DEL-01-04 | no | no | yes | no |

**Why the result is certain, not just observed.** An arc between two members
of the same SCC cannot change any SCC: the members already reach each other.
All four arcs are of that kind.

**Guard checks after adding the four:**
- DEL-04-01 as a consumer: none.
- An SCC-002 member depending on DEL-09-06: none.
- N-18 and N-24 each form a reciprocal pair. They join the 16 already in
  SCC-002 and are held, like the others.

## 4. Expected DAG-003 departure

After REVISE and the `dependency-extract` UPDATE, the next currency audit will
find a small departure from DAG-002. What it should find:

- **Arcs:** +4 added, all held (candidate layer, `SCC_UNRESOLVED`, citing
  CASE-002). 0 removed. 0 admitted arcs change. No SCC changes. The strict
  audit condition (no SCC in the admitted layer) is unaffected.
- **Rows:** at least 4 new UPSTREAM INTERFACE rows (DEL-02-01: 1; DEL-02-03:
  3). An extractor may split an arc into more than one row, but the arc set
  is what counts. Several EXTERNAL rows change quote or wording (IMPACT §5).
  These are not topology.
- **DAG pending** (the endpoints of added arcs): **DEL-02-01, DEL-02-03,
  DEL-03-02, DEL-03-03 and DEL-01-04**. All five are in SCC-002, so each is
  already held for those arcs. The flag clears when DAG-003 is accepted.
- **Changed bound files, no arc change** (evidence drift only, not pending):
  - the SoWs and registers of DEL-10-03, DEL-09-07 and DEL-02-02, plus
    DEL-04-02 and DEL-01-01 if Q-6 is accepted. DEL-03-03 and DEL-01-04 also
    change bytes for their text edits, but they are already pending as arc
    endpoints;
  - the registers of **DEL-04-01, DEL-04-02 and DEL-04-03**, re-quoted
    exactly (ASC-ISS-008; V12 F1: 34 quotes). Their arcs do not change. For
    DEL-04-01 the guard applies: the UPDATE adds no row that makes it
    consume anything;
  - `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`, if Q-12
    option (a) is accepted (BASIS_AMENDMENT B-06a; ASC-ISS-006). It is bound
    in DAG-002's `SOURCE_MANIFEST.sha256`, so its edit is timed to fall
    inside this same departure rather than cause a second one.
- **DAG-003's source manifest** re-binds all of these files, which are 130
  paths today.
- **Route:** the currency audit (`project-dag`) records `DEPARTURE`, then
  `project-dag` TRIGGER=SUCCESSOR prepares DAG-003 for the owner's
  acceptance. This is step 4 of the owner's accepted order (APP-V4-SCA002
  OWNER_DECISIONS). CASE-002 gains evidence rows only.
- **If the owner drops an arc at Q-4:** remove it from the sentence. With
  all four dropped, only evidence drift remains, and there is no DAG pending
  and no need for DAG-003 on these grounds. A currency audit is still needed
  after the SoW and register changes.

## 5. Not proposed

- **N-05 and N-07 consumer-side wording** (V12 F6). Both arcs are already in
  DAG-002, carried by DEL-04-02's supplier-side rows. Adding consumer
  sentences would change no arc. They are outside the decided scope. Not
  proposed.
- **Any supplier-side sentence** in DEL-03-02, DEL-03-03 or DEL-01-04 naming
  DEL-02-01 or DEL-02-03 as a receiver. It is not needed for the arcs, and it
  would add mirror rows only.
