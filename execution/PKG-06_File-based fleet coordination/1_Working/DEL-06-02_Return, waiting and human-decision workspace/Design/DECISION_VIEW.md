# Decision view (decision packages)

- Contribution: DEL-06-02/DV-v0.1 (new). Covers the decision-package part of
  OUT-002 and its fixtures (OUT-003). The return-review queue and waiting
  views (OUT-001) are a later file.
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. The prototype that exercises it is in the run folder
  (`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/E/`), not here; it is
  not product code and no App candidate exists.
- Run and owner: `APP-V4-DESIGN-PASS-4-20261003`, owner O-A (Type 2 TASK,
  Claude Opus 5.5, high effort), early path E; written 2026-10-03.
- Basis (sha256): this deliverable's `ScopeOfWork.md`
  3f6bb7b8344a83158530758dea6c7f69e797c30147458a8ae506359589c8ded7 (INIT
  contract; SCA-V4-001/002/003 changed no block of it, so R23-5's re-pin has
  no block to read); `docs/PRD.md` bb6e786f… (V4-PM-03…06, V4-AUT-03,
  V4-REC-02/03/05); `docs/HOST_INTEGRATION.md` d4331c39… (V4-HI-25, 30–33,
  61–63); rulings R23-2, R23-3, R23-7, R23-8, R23-18 and R23-21 (cited by ID, R23-21 item 1).
- Suppliers read, by label and section (this file adopts the versions that
  carry A16, R23-21 item 3): DEL-04-01/ACT-POLICY-v0.10 §2.1 (A8, A16), §2.3,
  §4.7, §9; DEL-04-03/RS-v0.10 §3, §6.1, §6.2 HA-11, §7, §13.6 and
  `RS_RECORD.schema.json`; DEL-02-03 `checkpoint-record-entries.schema.json`
  0.7 (CE-4 with the package elements; CE-10 `actRef` with A16;
  `$defs/decisionPackageFile`, R23-24);
  DEL-01-04/AAC-v0.3 §1.2, §2 (AI-9), §5, AK-a…AK-f; DEL-01-02/RECOVERY-v0.2
  §2 and §7 ("Shown as").
- Supplier pin (R23-3): nothing here depends on a Codex fact; the same text
  holds at 0.158.0 and 0.160.0.
- Labels: **SETTLED**, **DERIVED**, **INTEGRATION**, **PROPOSED** as R9.

## 1. What this view is

The person's place to see the decisions waiting for them and the decisions
they have made, each shown from its files. **DERIVED** from V4-PM-04 and
R23-8:

- A **decision package** is an A8 request recorded as an RS `act_request` with
  two further elements, **alternatives** and **consequences** (RS §13.6). The
  agent writes the package **file** in the project (DEL-02-03
  `$defs/decisionPackageFile`: package id, act requested, subject, purpose,
  the basis reserving the decision, alternatives with consequences; nothing
  the recorder supplies, no self-hash). The App writer records the request,
  citing that file by path and content identity, by the mapping RS §13.6
  states (R23-24). No PKG-06 record holds the package (R23-8 item 1).
- The person's **decision** is the act the package names: A16 *decide* for a
  reserved coordination decision, or an existing kind (A4–A7, A10, A12, A13,
  A15). It is captured by that kind's surface, A16 by DEL-01-04's App act
  control, and recorded under RS HA-1.
- The view **derives** both from those records (V4-PM-06). It writes nothing,
  performs no act and is never evidence of one.

## 2. Inputs

| Input | Owner | Used for | When it is missing |
|---|---|---|---|
| RS `act_request` entries carrying `alternatives` (packages) | DEL-04-03 format; body DEL-02-03 CE-4 | One row per package | No row; nothing is inferred |
| The package file each request cites (`evidence.ref`, `claimedIdentity`) | The project (an App file the agent wrote) | Showing current content; lapse | "package file not available"; lapse *unknown (unavailable)* |
| RS `human_act` entries whose `relations.requestRef` names a package | DEL-04-03; captured by the kind's surface | The decision | The row stays *pending* |
| RS record states (partial, read limited, refused, nonconformant) | DEL-04-03 §3, §14.2 | Limits on the view | Shown as limits, never used |

Not inputs, ever (**SETTLED** by CAP-7, HA-1, OF-2): conversation text,
including an agent's statement that the person decided; native Codex status;
answers to supplier questions; PEC projections.

## 3. Derivation rules (PROPOSED; the prototype implements DV-1…DV-9)

- **DV-1 Rows.** One row per `act_request` that carries `alternatives`. A
  request without them is an ordinary A8 and belongs to the queue and
  waiting views, not here.
- **DV-2 Package checks** (reader rules the schema cannot express):
  alternative identities are unique; every consequence names an alternative of
  the package; an alternative without a stated consequence is shown "no
  consequence stated". Each failure is a limit on the row, not a repair.
- **DV-3 The file now.** The view reads the package file's current content
  identity. If it differs from the identity the request recorded, the row
  says so; if the file is absent, it says "not available".
- **DV-4 What decides a package.** Only a `human_act` of the **kind the
  package names** whose `relations.requestRef` is the package's record. An act
  of another kind citing the package is listed and is not its decision.
- **DV-5 A16's chosen alternative.** It must be one the package names
  (`relations.alternativeChosen`). Otherwise the act is listed "not counted"
  with that rule and the row stays *pending*.
- **DV-6 Several decisions (R23-25, owner O-A's decision).** A later act of
  the named kind on the same package is a new decision by the person. It
  supersedes the earlier one for current standing, as a later established
  A12 does (RS §7 L-0; ACT §2.1 A16 row). The view shows the latest and lists
  each earlier act as "superseded by ‹act›" with its chosen alternative.
  Nothing is erased. A correction (RS OF-5: a new entry with `corrects`) is
  not a new decision: the corrected entry is listed "corrected by ‹entry›"
  and the correcting entry stands in its place. Prototype cases: RV-8 and
  RV-9.
- **DV-7 Lapse** (RS §7, unchanged): the package is an App file, so L-1 uses
  its file content identity. Equal → *not lapsed*; different → *lapsed — the
  package changed after the decision*; unobtainable → *unknown
  (unavailable)*. A lapse never deletes or hides the decision (L-8).
- **DV-8 Attribution.** The decision shows the decision actor as RS records
  them, with "identity not verified" (K1-4), and the recorder separately
  (OF-8, HA-2); recording mode and capture evidence references are shown.
- **DV-9 Derived only.** Rendering or rebuilding writes no file and no record;
  the input files' hashes are the same before and after (VER-005).

## 4. Row states

| State | Entered when | Shown as |
|---|---|---|
| *pending* | A package row exists and no act passes DV-4/DV-5 | "pending — awaiting the person's decision", with the exact act requested, subject, purpose, scope, alternatives and their consequences |
| *decided* | An act passes DV-4/DV-5 | The alternative chosen and its statement, "decided by ‹person› (identity not verified) · recorded by ‹recorder›", capture time, lapse state |
| (limits) | DV-2, DV-3, DV-4 or DV-5 finds something | Listed on the row; they never change the state by themselves |

Wording follows ACT §9: "decide" for A16; "accept" only for A5, never
"approve" for a proposal (REQ-003).

## 5. The route to the act (R23-2; INTEGRATION)

At the person's click on a pending row, the App opens DEL-01-04's act control
with the package as a **runtime value**: the package file reference and
content identity, the request record identity, the act kind, scope, purpose,
and the alternatives with their consequences. The view captures nothing;
nothing opens the control except the person (AAC AK-a, AK-b). There is **no
register row** from DEL-06-02 to DEL-01-04: such a row is cycle-safe in that
direction, but R23-2 chose the runtime value, and a row the other way would
form a cycle (S1-A S-6). If the package changes between the offer and the
person's confirmation, AAC AK-c captures nothing.

## 6. Failure behaviour

| Failure | Behaviour |
|---|---|
| Record log line torn or unreadable | Row data from readable entries only; "partial entry (not read)" listed (RS §3 record states) |
| Request of a newer minor or unknown major version | RS R-3: read limited or refused; a refused request gives no row, and the limit is listed |
| Package file absent or changed | DV-3 and DV-7 |
| Act citing an unknown request | Not shown on any row; listed as a view limit |
| Two packages for the same matter | Two rows; the view does not merge them |
| PEC absent, stale or failing | No effect: PEC is not an input (REQ-006) |

## 7. Interfaces

- **Consumed** (register rows already admitted): DEP-06-02-010 → DEL-04-03
  (records, states, lapse); DEP-06-02-009 → DEL-04-01 (act names, label
  rules). The package's form and body come through DEL-04-03's container from
  DEL-02-03 (CE-4, schema 0.7). The package file is its own shape,
  `$defs/decisionPackageFile`; the request record cites it, and the mapping
  between them is RS §13.6 (R23-24, superseding R23-18 item 3).
- **Offered** (runtime value, no row): the package to DEL-01-04's act control
  (§5).
- **To DEL-09-05 and DEL-09-11:** the fixture FX-DP1 and its manifest (run
  folder `E/fixtures/FX-DP1/`), for DEL-09-05's VER-004 case and DEL-09-11's
  reader.

## 8. Verification (designed; prototype results are not candidate evidence)

| VER | Case | Prototype (run_e.py) |
|---|---|---|
| VER-003 | Pending package shown with exact act, subject/basis, alternatives, consequences | D: PKG-2 pending row |
| VER-004 | Positive faithful case (person's A16 through the act control, actor ≠ recorder, lapse visible); negatives: agent message claiming a decision, an act of another kind, a chosen alternative outside the package | D, RV-1, RV-2, RV-3, RV-5, RV-6 |
| VER-005 (part) | Rebuild leaves the inputs unchanged | D: hashes before and after |

## 9. Open matters

| Matter | Owner | Point of need |
|---|---|---|
| ~~CE-4, CE-10 and AAC schema rows (PR-1…PR-13)~~ | Closed: applied under R23-18 (EXEC schema 0.7, AAC-v0.3); the package file's shape and its mapping to the request record follow R23-24 (`$defs/decisionPackageFile`; RS §13.6); R23-18 item 3 is superseded | — |
| Content-identity method (RS U-04): the prototype uses sha-256 of the file bytes as a TEST VALUE | Owner with DEL-04-03 (carried) | Before lapse is relied on |
| The return-review queue and waiting views (OUT-001), and decision packages in waiting causes | O-A, next unit | — |
