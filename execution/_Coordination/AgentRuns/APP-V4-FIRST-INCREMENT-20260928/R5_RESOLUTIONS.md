# R5 final integration rulings — V3 residuals

Integrator: HELP_HUMAN. Inputs: [V3-A](reviews/V3-A.md) and
[V3-B](reviews/V3-B.md), both **MERGE AS DRAFTS** (0 BLOCKING; 10 MAJOR and 26
MINOR in total), and [R5_CANDIDATES.md](R5_CANDIDATES.md). R1–R4 stand unless
amended here.

This is the last alignment pass before the Wave-2 PR. Version bumps:

| Files | New version |
|---|---|
| Wave-1 files | v0.5 |
| EXEC and ADAPTER | v0.3 |
| W9 files (CA, RELAY, XT) | v0.3 |
| GUIDE | v0.2, dispatched after the others return |

For MINOR items addressed to your file, apply the reviewer's proposed fix
unless it contradicts a ruling below.

## R5-1 One hold-support value set (V3-A MAJOR-1; V3-B MAJOR-5) — owner of values: DEL-02-03 EXEC §3.6

Each checkpoint on each surface takes exactly one value:

| Value | Meaning | Workflow requirement check |
|---|---|---|
| **enforced by the host loop** | Embedded route: the host loop holds the run (LOOP §2.4.4) | passes (holds are subject to host evidence, DEP-001) |
| **enforced on the host route** | The host holds or refuses the operation through a *host-held* constraint (R5-2), evidenced by the host's answer to SQ-02 and a candidate | passes |
| **not established** | Depends on a host answer not yet given (SQ-02) or on unagreed exposure | *not established* (never a pass, and never "unsupported") |
| **not enforceable** | No mechanism exists on this surface in this increment. Examples: App-only steps with no host operation (R4-2 / D6), or a constraint carried only as model-supplied | *unsupported* (R4-8 reason) |

Consequences:

- E1 run from the App through the external channel (surface X): `CP-accept` →
  **not established** (awaiting SQ-02); any App-only checkpoint → **not
  enforceable**.
- EXEC-v0.1's five values and "held after observation" are retired
  everywhere.

## R5-2 Carriage assurance, final (Y-1, Y-8; V3-B MAJOR-1)

- **Host-held:** the constraint is held on the host side, whether the host
  derived it from its own resolved copy of the declaration or received it and
  then verified it against its own copy. The host loop's own evaluation
  (LOOP §6.2) is host-held.
- A constraint the host merely **received** from an outside caller keeps its
  source's assurance: *model-supplied* or *App-assured*.
- **App-assured** is *not available in this increment* (R4-2: interposed App
  code is not adopted).
- Only host-held carriage satisfies R2-12.
- P §3.3/§4.4 remove the host loop from *App-assured*. ACT §4.4 and WD-EX R-5b
  stop presenting App-assured as available.

## R5-3 Grant-setting subject (Y-2, amended per V3-A)

- The **declared** setting content always binds, and the declaration must
  always name it. A declaration that names no setting content is invalid,
  unconditionally.
- An A8 may present that content but never changes the subject. An A12 made
  on different content satisfies nothing at that checkpoint.
- A run-dependent scope is declared as a binding rule resolved at arrival
  (e.g. "targets of the held call"). It is never chosen by an A8.
- Files: WD §4.3.1/§4.3.6, ACT §4.2 (fixes V3-A m-5), LOOP §2.4.2, PANEL W-5a,
  EXEC §4.10.

## R5-4 Model destination (Y-3, amended; attribution per V3-A m-11 / V3-B)

- Record the destination **per turn** where the supplier reports it,
  including reroutes (HOSTING §8.3). Keep requested and effective destinations
  separate. Turns that are not observed are *unknown*.
- The run-level value is the set of destinations observed. A switch starts no
  new run.
- EXEC CR-14 shows the destination at report time.
- **Attribution:**
  - "Host content may flow to the selected model; no gating" is SETTLED by
    DECISION-2.
  - "Record and show the destination" is the recorder's reading of
    DECISION-2. Label it **INTEGRATION (DECISION-2 reading)**, not SETTLED.
- Relabel wherever it appears.

## R5-5 Undo and re-hold (Y-4, amended)

- EXEC RH-8 is generalized: a lapse re-holds whatever caused it, including the
  person's own undo.
- The person's undo is never recorded as "action during hold".
- An undo never re-holds an A5 arrival.

## R5-6 Person's own operations (Y-5, confirmed with precision)

- A person's own A1/A2 are run-record (R7) operations, not human-act records.
- An operation that **performs a reserved act** (OP-C6/C7/C8, the A12/A13
  controls) produces the human-act record, and the R7 entry references it.

## R5-7 Grant change after checkpoint arrival (Y-6, amended; V3-A MAJOR-3/MAJOR-5)

- C §10 adds a named variant, **V-GR1**: a run of E1d in which CP-grant
  arrives at r15, T15's A12 is captured *after* the arrival, and the held call
  is then dispatched unchanged as T16.
- The main timeline is unchanged. Run 12 (⟨rev-3⟩) declares no CP-grant, and
  WD-EX R-16(i) stays correct.
- ACT CP-3, L-LOOP-C11, L-PANEL-2, L-WDEX-11, L-AS-7/8 and EXEC CH-12…14
  re-point to V-GR1 and agree that T15-before-arrival does **not** count.
- Owner-visible cost, recorded under U-E4/U-31: SP-6 can make the person
  repeat a grant change whose content is already in force.

## R5-8 App-run hold over-claim (V3-A MAJOR-2)

RS E10/VC-17 remove "held after observation" and "run stops". They show hold
support **not enforceable** (App-only) or **not established**, and record
action during hold.

## R5-9 Citation and staleness pass (Y-7; V3-A MAJOR-4, m-1…m-3, m-12; V3-B list)

- Re-point every citation to the current sibling versions and section
  numbers. The following are **substantive**, not mechanical:
  - EXEC's L-WDEX-n citations: re-point by case content, not by number;
  - GUIDE's matrix: GUIDE v0.2;
  - ADAPTER SQ-13 → SQ-28, and its hold-support values → R5-1;
  - HOSTING: stop citing the withdrawn EXEC U-E20, and add HP-4;
  - P: "confirms at W7" becomes "confirmed by DEL-02-03";
  - XT IN-07 → ACT-v0.4 or later;
  - ACT FX-50: stop citing the retired ADAPTER U-X3.
- Statements that C lacks App-side subjects are now false. C-v0.4 has LIB-A1,
  LIB-A2 and AF-1, and FXA-5 declares CP-accept **and** CP-check. EXEC
  L-EXEC-19, ⟨fx-app-import⟩ and U-E21 re-point.
- Cite **FXA-n**, not FA-n.

## R5-10 Relay corrections before the owner relays (Y-9; V3-B MAJOR-3/MAJOR-4)

- **SQ-02 "Why it matters":** the answer decides holds for checkpoints on
  **host operations** only. App-only checkpointed workflows remain
  **not enforceable** whatever SWBPIPE answers; that is a separate D6
  follow-up for the owner.
- **SQ-28** gates the whole external channel, including every live XC case.
- **SQ-16:** stop over-crediting D5 (per R5-4).
- **SQ-09:** "outcome unknown" does not apply to reads.
- **Coverage:** add an SQ, or a "Not included — reason", for each of C U-C4,
  U-C6, U-C10; P U-P6; AS U-04; RS U-12; WD U-09, U-10; ACT U-06.
