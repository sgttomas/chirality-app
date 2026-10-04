# Receipt — APP-V4-DESIGN-PASS-4-20261003, tranche 1

Design pass 4, tranche 1: eight App v4 deliverables designed to the 60%
level of `loop/LOOP_INIT.md`, reviewed and integrated. The run used the
owner's selected coordination method,
`bundled:chirality-root/coordinated-knowledge-work` (WORKFLOW.md sha256
`44049bcd…1b18`). Graph: [WORK_GRAPH.md](../../WorkGraphs/APP-V4-DESIGN-PASS-4-20261003/WORK_GRAPH.md).

## Owner acts

All are recorded with the owner's exact text in
[OWNER_DECISIONS.md](OWNER_DECISIONS.md):

- **Direction:** "1 yes, 2 no rewrite, 3 go, 4 A+C".
- **The download for the version check:** "yes, download it".
- **Coordination method:** use `coordinated-knowledge-work` as Agent 0.
- **Scope of owner questions:** "I don't want to expand governance
  structures and bring in human decision making where it doesn't belong."
  The ten questions first prepared (K-1…K-10) were then ruled by HELP_HUMAN
  instead.

No other owner decision was needed. The AGENTS.md instruction change
(D-GOV-52) awaits the owner's approval and is not in this run's commits.

## What landed

- **DEL-06-01** FR-v0.1 (fleet records, child index, delegation per R23-9)
  and **DEL-06-02** DECISION_VIEW and FV-v0.1 (queue, waiting, decision
  views; no invented examiner; a lost record never reads as ready).
- **DEL-09-01** EXP-v0.2: examination protocol, three record schemas,
  review protocol (V4-OPS-34), native route, SCC-003 milestones.
- **DEL-01-06** PKG-v0.2: signing option B (Codex keeps OpenAI's
  signatures; not relied on until FP-1/FP-3 pass on the first package),
  quarantined install witness, identity record.
- **DEL-09-02** SQ-v0.2: V4-EXM-10/11/12 step map over 65 supplier cases,
  declared stimuli ST-1…ST-5 (R23-27).
- **DEL-09-05** DAC (decision attribution case FW-04).
- **DEL-09-07** LHQ, TOP and DOS: four local-host cases, the traffic
  observation plan, the dossier and per-case SWBPIPE gap sheets. No
  SWBPIPE observation is claimed; host joins remain deferred.
- **DEL-09-11** RRM: the reader method and the examiner comparison, with a
  standing check that includes two independent accounts.
- **Shared rows:** A16 *decide* for a person's decision on a decision
  package (R23-8, R23-18, R23-24, R23-25), carried in:
  - ACT-POLICY-v0.10, RS-v0.10, AAC-v0.3 (with the offer-digest method
    `aac-offer-digest/0.1`), DEL-02-03's checkpoint schema (proposed-0.7,
    with `decisionPackageFile`) and GUIDE-v0.7;
  - NIR-v0.3, which carries Codex 0.160.0's `Turn.error` wording.
- **Codex 0.160.0:** checked and design-compatible
  (`VERSION_ADVANCE_0.160.0.md`). The definition pin stays 0.158.0 (R23-22).
- **Lifecycle:** the eight deliverables moved INITIALIZED → IN_PROGRESS
  (R23-28).
- **SCA-V4-003's derivative closure:** 21 of 23 Design files re-pinned to
  current ScopeOfWork (C1, C2, O-A). PIN_SPIKE stays as a dated record.

## The early path

One decision package, decided by the person, was carried all the way
through: package file, request record, act control, A16 record, decision
view, the FW-04 case, and reconstruction by a reader. Two isolated readers
given only the fixture files reconstructed the decision (RR-E, RR-F); the
second scored 9/9 with nothing referred. The path exposed three things that
reviews of separate parts had not:
- the request body's real home;
- my faulty R23-18 item 3, superseded by R23-24;
- an unspecified digest serialization.
It also exposed a comparison checker that agreed only with its own
author's constructed accounts.

## Checks

- **Standing reviewers:**
  - RV reviewed LHQ-U1, LHQ-U2, EXP-U1, E-1, E-2 and EP-05/EP-11;
  - RV2 reviewed PKG-U2 and SQ-U3.
  Every unit ended READY with no open BLOCKING or MAJOR finding. The
  reviewer who raised each finding confirmed its repair.
- **Integration closeout:** C1 handled 40 sibling and 17 ScopeOfWork
  re-pins, and repaired a DEL-09-06 W14 rehearsal that pass 4 had broken
  (now 44/0). C2 handled GUIDE-v0.7 (pin check 25/25), the ACCESS §13 row
  and the VERSION_ADVANCE note.
- **Pre-merge review P1** of `d150856784`: MERGE (0 BLOCKING, 0 MAJOR,
  2 MINOR, 5 NOTE). Every prototype count was rerun at the candidate.
- **Fences:** no ScopeOfWork, register, DAG, scope-change, decomposition or
  Open_Issues file changed; no home paths; every file is inside
  `projects/chirality-app-v4/execution`.

## Limits and carried items

- Nothing is implemented, built, signed or qualified. All evidence comes
  from fixtures and prototypes.
- **Carried to the next amendment (R23-11):** overtaken ScopeOfWork wording
  in all eight deliverables; DEL-04-01 REQ-002 naming A16; OI-011's
  register record (R23-26); the bundle-seam rows proposed by DEL-01-06.
- **Carried to owners' next revisions:** P1-F2 (TOP §7 times as instants);
  SQ-R-O (the ST-5 capture method); U-SQ-6 (the real Codex
  lost-acknowledgment capture, before RUN-A); FX-PIPE-01's adoption of
  L-LHQ-1/2 (R23-16).
- **Recorded limits (R23-29 item 4):** the 17 re-pinned files' register
  pins; pre-existing pins to older GUIDE and ACCESS versions in RELAY,
  ADAPTER and LOOP; VC.md's dated pin.
- **Coordinator lesson:** a working checkpoint taken mid-repair moved HEAD
  under owners' pins. Later checkpoints were taken at quiet points.
- **Tranche 2** (PKG-07, PKG-08, PKG-10, PKG-11, DEL-09-10, DEL-09-12)
  follows.
