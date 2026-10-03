# Arc effect — SCA-V4-003, node P1

**Status: PROPOSED.** This file lists every register row the ledger proposes,
classes each against the accepted graph, computes the SCC effect of the rows
recommended INCLUDE, checks the guards, and states the departure from DAG-003
that the next currency audit should find. Nothing here writes a register or a
DAG file.

- **Basis:** HEAD `897a107cc9`. Accepted graph `E/_DAG/_LATEST.md` → **DAG-003**
  (accepted 2026-09-29; currency `CURRENT`, 0 pending, per
  `_Evaluation/DAGCurrency/_LATEST.md`).
- **Edges read:** `_DAG/DAG-003/DependencyEdges.csv` (sha256
  `4716ca287d23835c…`, 124 admitted arcs) and `CandidateEdges.csv`
  (`07b969209e273310…`, 78 held arcs); 41 nodes; 202 arcs; the two layers do
  not overlap. Same hashes as pass-3 F0 read.
- **Method:** a script in scratch (`$TMPDIR/p1/scc.py`, not in the
  repository) reads both files with the `csv` module, keeps rows whose
  `TargetType` is `DELIVERABLE`, forms consumer → supplier arcs (UPSTREAM:
  From → Target; DOWNSTREAM: Target → From), and runs Tarjan's algorithm.
  The base result reproduces F0 §3 and both pass-3 C1 records: six SCCs,
  sizes 2, 2, 2, 2, 3 and 13; the admitted layer alone has no SCC; 24
  reciprocal pairs (SCA-V4-002's figure after its four arcs).

SCC-002 (13): DEL-01-04, 02-01, 02-02, 02-03, 02-04, 03-01, 03-02, 03-03,
04-02, 04-03, 05-01, 05-02, 09-09. The others: {01-01, 01-05} (SCC-001),
{01-06, 09-01}, {10-02, 10-04}, {11-01, 11-03}, {07-01, 07-02, 08-01}.

## 1. Every proposed row, by graph class

Totals of the ledger's register kind: 89 items. INCLUDE 81 items standing for
140 rows: **10 new arcs**, 30 mirror items (80 rows), 41 statement, notes,
maturity or label items (50 rows). DEFER 3, DROP 5 (listed in §1.4).

### 1.1 New arcs (no row in either direction today; checked ABSENT in both edge files)

| Ledger ID (aliases) | Register | Consumer → supplier | Layer if added | Grounding ScopeOfWork item | Disposition |
|---|---|---|---|---|---|
| R2-04-03-e (ARC_ANALYSIS K-8) | DEL-04-03 | DEL-04-03 → DEL-02-01 | held (both in SCC-002) | SC2-04-03-2 | INCLUDE |
| R20-10 (F-C §4) | DEL-04-03 | DEL-04-03 → DEL-02-02 | held | **P1-05** (no source proposes one) | INCLUDE |
| NR-08 (D3 NR-1) | DEL-01-04 | DEL-01-04 → DEL-04-02 | held | SC3-01-04-5 | INCLUDE |
| NR-09 (D3 NR-2) | DEL-01-04 | DEL-01-04 → DEL-02-03 | held | SC3-01-04-5 | INCLUDE |
| NR-4 (D3 R2.5; adopted R22-1) | DEL-01-04 | DEL-01-04 → DEL-02-04 | held | SC3-01-04-11 | INCLUDE |
| NR-05 (D2; adopted R18-1 C-06) | DEL-01-04 | DEL-01-04 → DEL-01-03 | **admitted** | SC3-01-04-10 | INCLUDE |
| NR-07 (D3 NR-3 = D4 NR-1) | DEL-01-04 | DEL-01-04 → DEL-01-05 | **admitted** | SC3-01-04-6 (amended at C1-A) | INCLUDE |
| NR-01 (D1 NR-D1-1) | DEL-02-03 | DEL-02-03 → DEL-01-02 | **admitted** | **P1-01** (R22-4) | INCLUDE |
| NR-02 (D1 NR-D1-2) | DEL-03-03 | DEL-03-03 → DEL-01-02 | **admitted** | **P1-02** (R22-4) | INCLUDE |
| NR-04 (D5 NR-1) | DEL-02-02 | DEL-02-02 → DEL-01-02 | **admitted** | **P1-03** (R22-4) | INCLUDE |
| NR-03 (D1 NR-D1-3) | DEL-09-09 | DEL-09-09 → DEL-01-02 | admitted | — | **DROP** (R22-4: dropped, not grounded) |

"Layer if added": an arc whose two ends lie in one existing SCC is held; any
other arc is admitted if the admitted layer stays acyclic (§2).

**R22-4 statement (required by that ruling), for each of NR-01…NR-04:**

- **NR-01 — add the sentence.** EXEC-v0.7 §2.7, AE-6 and RE-4 consume
  DEL-01-02's custody events and run-tag lookup; DEL-02-03's ScopeOfWork names
  DEL-01-02 0 times (checked). P1-01 adds the consumption to DEL-02-03 CLM-002's
  "consumes, and does not define" list (the locus SC2-02-03-3 also uses).
- **NR-02 — add the sentence.** ADAPTER-v0.7 PI-6 and XF-41 consume the
  in-flight item state and the relaunch fact; DEL-03-03's ScopeOfWork names
  DEL-01-02 0 times. P1-02 adds it to CLM-002's consumption list (where S-03-2,
  S-03-3 and S-03-5 also edit).
- **NR-03 — drop the row.** XT XC-06 reaches DEL-01-02's facts through
  ADAPTER-v0.7 PI-6 (F-E1 FT-01), which NR-02 covers; the row was optional at
  its source (D1, F0, C1-A). XT keeps the reliance as a labelled
  cross-reference.
- **NR-04 — add the sentence.** WR-v0.2 SQ-X (App-start reconciliation) and
  chaining (R19-2 (a): "The person ends run A (DEL-01-02 DEF-4)") rest on
  DEL-01-02's definitions; DEL-02-02's ScopeOfWork names DEL-01-02 0 times.
  P1-03 adds it beside SC3-02-02-10 (chaining).

### 1.2 Mirror rows (the arc already exists; no topology change)

Each mirror was checked present in DAG-003, with its layer.

| Ledger ID (aliases) | Register | Rows | Arcs mirrored (consumer → supplier), layer | Supplier-side grounding |
|---|---|---:|---|---|
| R2-04-01-a | DEL-04-01 | 1 | 09-06 → 04-01 admitted | SC2-04-01-1 |
| R2-04-02-a..c | DEL-04-02 | 3 | 03-04, 09-06 → 04-02 admitted; 09-09 → 04-02 held | SC2-04-02-1 |
| R2-04-03-a..d | DEL-04-03 | 4 | 02-01, 02-03, 03-01 → 04-03 held; 03-04 → 04-03 admitted | SC2-04-03-1 |
| R2-02-01-a..f | DEL-02-01 | 6 | 02-03, 03-02, 05-01, 05-02 held; 03-04, 09-06 admitted | SC2-02-01-2 |
| R2-02-03-a | DEL-02-03 | 1 | 02-03 → 04-02 held (consumer side) | SC2-02-03-3 |
| R2-02-03-b..i | DEL-02-03 | 8 | 02-01, 03-03, 04-02, 04-03, 05-01, 05-02, 09-09 held; 03-04 admitted | SC2-02-03-6 |
| R2-01-04-a (F0 M-7) | DEL-01-04 | 1 | 02-03 → 01-04 held (X-1) | SC3-01-04-1 consumer list |
| R-01-1 | DEL-03-01 | 11 | 8 held, 3 admitted | **P1-06** (DEL-03-01 SoW names 2 of 11) |
| R-02-1 | DEL-03-02 | 1 | 03-01 → 03-02 held | already named |
| R-02-2 | DEL-03-02 | 6 | 4 held, 2 admitted | **P1-07** (names 1 of 6) |
| R-02-3 | DEL-03-02 | 1 | 03-02 → 04-02 held (consumer side, N-05) | S-02-2 |
| R-03-1 | DEL-03-03 | 4 | 2 held, 2 admitted | **P1-08** (names 1 of 4) |
| R-03-4 | DEL-03-03 | 2 | 03-03 → 04-02, 03-03 → 02-01 held (consumer side) | S-03-3 |
| R-11-1 (incl. F0 M-6) | DEL-01-01 | 10 | all admitted | **P1-09** (names 3 of 10) |
| R-0501-4 (F0 M-5) | DEL-05-01 | 1 | 05-01 → 01-05 admitted (consumer side) | **P1-10** (DEL-05-01 SoW names DEL-01-05 0 times) |
| R-0906-3 | DEL-09-06 | 1 | 09-06 → 09-01 admitted (consumer side) | S-0906-3 |
| R3-01-02-a, -b (M-1, M-2) | DEL-01-02 | 2 | 01-03, 09-02 → 01-02 admitted | SC3-01-02-8 |
| R3-01-02-e, -f, -h | DEL-01-02 | 3 | mirrors of NR-01, NR-02, NR-04 (new admitted) | SC3-01-02-8 completion |
| R3-01-03-a..c (M-3) | DEL-01-03 | 3 | 06-01, 09-02, 09-05 → 01-03 admitted | SC3-01-03-8 |
| R3-01-03-d | DEL-01-03 | 1 | mirror of NR-05 (new admitted) | SC3-01-03-8 |
| R3-01-04-b | DEL-01-04 | 1 | 09-02 → 01-04 admitted | SC3-01-04-13 |
| R3-01-05-a (M-4) | DEL-01-05 | 1 | 01-01 → 01-05 held (SCC-001) | already named |
| R3-01-05-b | DEL-01-05 | 1 | 09-02 → 01-05 admitted | SC3-01-05-12 |
| R3-02-02-a..c | DEL-02-02 | 3 | 01-04, 02-03 → 02-02 held; 09-06 → 02-02 admitted | SC3-02-02-12 |
| R3-02-02-d | DEL-02-02 | 1 | mirror of R20-10 (new held) | SC3-02-02-12 |
| R3-02-04-a, -b | DEL-02-04 | 2 | 03-04, 10-03 → 02-04 admitted | SC3-02-04-9 |
| R3-02-04-c | DEL-02-04 | 1 | mirror of NR-4 (new held) | SC3-02-04-9 |

**Grounding finding (this node).** Every register here records CONSERVATIVE
extraction from `ScopeOfWork.md` only (each `_DEPENDENCIES.md` Run Notes;
pass-2 C1-A "Registers follow the ScopeOfWork"). Pass 2's C1-A paired each of
its mirror groups with a receivers sentence; pass 2's C1-B and C1-C did not.
A script counted consumer IDs in the supplier ScopeOfWork bytes: R-01-1,
R-02-2, R-03-1 and R-11-1 lack a naming sentence for 24 of their 31 rows, and
R-0501-4 lacks a consumer-side sentence. P1-06…P1-10 add them. The
alternative is a human-declared row in each `_DEPENDENCIES.md` "Declared"
section (OWNER_ITEMS Q-15).

### 1.3 Statement, notes, maturity and label items (non-topological)

41 INCLUDE items (50 rows). None adds or removes an arc. By register:
DEL-04-01 R2-04-01-c (new EXTERNAL constraint row); DEL-04-03 R2-04-03-f, -g
(with DEL-09-06), -h (`_DEPENDENCIES.md` label); DEL-02-01 R2-02-01-g, -h;
DEL-02-03 R2-02-03-j; DEL-03-01 R-01-2 (retire or retarget the package row
DEP-03-01-022), R-01-3 (edition part); DEL-03-03 R-03-2, -3, -5, -6; DEL-03-04
R-04-1, -2; DEL-01-01 R-11-2, R-11-3 (extended in pass 3); DEL-05-01 R-0501-1,
-2, -3, R-0501-5 (new EXTERNAL handover row); DEL-05-02 R-0502-1 (7
statements); DEL-09-06 R-0906-1, -2; DEL-09-09 R-0909-1, -2, -3; DEL-01-02
R3-01-02-c, -d; DEL-01-03 R3-01-03-e, -f; DEL-01-04 SC3-01-04-9 (ST-1),
R3-01-04-a; DEL-01-05 R3-01-05-c, -d, -e; DEL-02-02 SC3-02-02-6 (ST-2), -7
(ST-3), -9 (with DEP-02-03-010); DEL-02-04 SC3-02-04-8 (ST-4), R3-02-04-d.

**Retirements and refreshes.** R-01-2 retires or retargets DEP-03-01-022 at
extraction. R3-01-03-e refreshes DEP-01-03-017 to the OI-001 residue and
records OI-002 as ruled (split and retire, or note), as SCA-V4-002 did for
DEL-01-04's twin rows. Any row whose quoted SoW text changes is re-quoted, or
retired `source_revised` with its successor named, as in SCA-V4-002. None of
these is topological.

### 1.4 Rows not carried

| ID | Class | Disposition | Why |
|---|---|---|---|
| NR-03 | new admitted arc | DROP | R22-4 (above) |
| R3-01-02-g | mirror of NR-03 | DROP | follows NR-03 |
| NR-06 | new admitted arc DEL-02-04 → DEL-01-03 | DROP | withdrawn (R18-1 C-07) |
| NR-10 | new held arc DEL-02-04 → DEL-02-02 | DROP | withdrawn (R19-7) |
| R-0906-4 | maturity | DROP | duplicate of R2-04-03-g |
| R2-04-01-b | new EXTERNAL row | DEFER | follows SC2-04-01-2 (A12 mapping) |
| R-0502-2 | statements | DEFER | follows S-0502-1 option A |
| R-02-4 | value convention | DEFER | cross-register convention (DAG-003 open matter P2 O-6) |

## 2. SCC computation

| | DAG-003 now | With the 10 INCLUDE arcs | With all 11 (NR-03 too) |
|---|---:|---:|---:|
| Arcs | 202 | **212** | 213 |
| Admitted | 124 | **129** | 130 |
| Held | 78 | **83** | 83 |
| SCCs | 6 | 6, **identical membership** | 6, identical |
| Admitted layer acyclic | yes | **yes** | yes |
| Reciprocal pairs | 24 | **27** | 27 |

- **Singly, in pairs and together:** each of the 10 INCLUDE arcs alone, all
  45 pairs and all 10 together leave the SCC set unchanged. With NR-03 added,
  the 11 singly, in all 55 pairs and together also leave it unchanged.
- **Why certain for the five held arcs:** both ends already lie in SCC-002,
  and an arc between members of one SCC cannot change any SCC.
- **Why the five admitted arcs stay admitted:** none of their suppliers
  (DEL-01-02, DEL-01-03, DEL-01-05) reaches a member of SCC-002 or their
  consumers. The script's reachability over the final graph: DEL-01-02 reaches
  only DEL-01-01, DEL-01-05 and DEL-04-01; DEL-01-03 reaches those three and
  DEL-01-02.
- **New reciprocal pairs:** R2-04-03-e (DEL-02-01 → DEL-04-03 exists), NR-09
  (X-1, DEL-02-03 → DEL-01-04, exists) and R20-10 (DEL-02-02 → DEL-04-03
  exists). All three are inside SCC-002 and held, like the others.
- **Negative controls** (rows not proposed): DEL-01-05 → DEL-01-02 forms
  {DEL-01-01, DEL-01-02, DEL-01-05}; DEL-01-03 → DEL-02-04 pulls DEL-01-03 into
  SCC-002; DEL-01-02 → DEL-02-04 pulls DEL-01-02 and DEL-01-03 into SCC-002.
  This reproduces F0 §3 and C1-A. The withdrawn NR-06 and NR-10 change no SCC;
  they were withdrawn on design grounds, not graph grounds.

## 3. Guards

- **R17-10 cycle guard** (DEL-01-02 and DEL-01-03 must not consume DEL-01-04,
  DEL-02-02, DEL-02-03, DEL-04-02, DEL-04-03 or DEL-06-01): no proposed row has
  DEL-01-02 or DEL-01-03 as consumer of any of them, and in the final graph
  neither reaches any of them (reachability above). **Holds.**
- **DEL-04-01 gains no supplier** (SCA-V4-002 guard): DEL-04-01 is a consumer
  in no arc of the final graph. **Holds.** R2-04-01-c adds an EXTERNAL row only.
- **No SCC-002 member depends on DEL-09-06** (SCA-V4-002 guard): none in the
  final graph. **Holds.**
- **N-12 and N-B8 stay absent:** no proposed row names them.

## 4. Expected DAG-003 departure

After the ScopeOfWork REVISEs and the `dependency-extract` UPDATEs, the next
currency audit should find:

- **Arcs:** +10 (5 admitted: NR-01, NR-02, NR-04, NR-05, NR-07; 5 held:
  R2-04-03-e, R20-10, NR-08, NR-09, NR-4), 0 removed, no SCC change. The
  admitted additions are a real departure in the admitted layer: SCC-002
  members DEL-01-04, DEL-02-02, DEL-02-03 and DEL-03-03 gain admitted
  suppliers DEL-01-02, DEL-01-03 or DEL-01-05, so those three come before
  SCC-002 in the admitted order. (SCC-002 already reaches SCC-001 through
  admitted arcs such as DEL-02-01 → DEL-01-01.)
- **DAG pending** (ends of added arcs, 11): DEL-01-02, DEL-01-03, DEL-01-04,
  DEL-01-05, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-03, DEL-04-02,
  DEL-04-03. The flags clear when the successor graph is accepted.
- **Rows:** at least 10 new arc rows and at least 80 mirror rows, plus the
  statement and notes changes (§1.3). An extractor may split one arc into
  several rows; the arc set is what counts.
- **Changed bound files without an arc change:** the ScopeOfWork, register and
  `_DEPENDENCIES.md` of every deliverable the INCLUDE rows touch: 19
  ScopeOfWork files (DEL-01-01…01-05, 02-01…02-04, 03-01…03-04, 04-01…04-03,
  05-01, 09-06, 09-09) and 20 registers (the same plus DEL-05-02). All are
  bound in DAG-003's `SOURCE_MANIFEST.sha256` (130 paths).
- **Route:** `project-dag` currency audit → `DEPARTURE` → TRIGGER=SUCCESSOR
  prepares **DAG-004** for the owner's acceptance, as DAG-003 followed
  SCA-V4-002. Cases: CASE-002 gains evidence rows for the five held arcs.
- **If the owner drops new arcs:** remove the grounding sentence with the row.
  With no new arc left, only evidence drift remains; a currency audit is still
  needed after the REVISEs and UPDATEs, but no successor graph on arc grounds.

## 5. Considered and not proposed

- The supplier-side mirrors pass 2 noted "outside mirrors noted, not
  proposed": DEL-04-01 → DEL-01-02, 01-04, 02-02; DEL-04-03 → DEL-01-04, 02-02;
  DEL-02-01 → DEL-02-02, 02-04; DEL-02-03 → DEL-02-02. F0 §1.14 notes they are
  proposable now; no node proposed them, and both pass-3 C1 records keep them
  "as noted". They would add no arc. Not in this ledger; a later amendment or
  the register owners may take them.
- Consumer rows owed by DEL-04-03 for DEP-02-04-012 and by DEL-11-02 for
  DEP-02-04-013 (P3RUN C1-B §3.4, §7 item 4): returned to the graph by C1-B,
  not proposed. No arc change.
- SCC-forming rows (§2 negative controls): not proposed; their needs stay
  runtime values (`assess live work`, the K-10 standing).
