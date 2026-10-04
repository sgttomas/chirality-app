# What each EU-F1 key answer rests on (RV3 EUF1-R3)

The three keys are frozen and not edited: `EU-F1.answer-key.json` (IS-FX-RP1-1), `EU-F1-2.answer-key.json` (IS-FX-RP1-2), `EU-F1-3.answer-key.json` (IS-FX-RP1-3). This file marks the ground of each answer, so that no answer reads as if a supplier had stated it when DEL-11-03's own owner (O-F) wrote it.

Grounds:
- **Supplier record:** a copy, under `supplied/`, of a record in another owner's file (SQ-EX-05 from DEL-09-02; the DOS example and the CIR from DEL-09-07). All of these are illustrative schema examples.
- **Packet rule:** derived from supplier records by DEL-11-03's rules RP-R1…RP-R8, so it is O-F's derivation and is checked by `check_rp.py` A-9.
- **O-F text:** the package's own wording, written by O-F (alternatives, purpose, terms).
- **First cut (O-F):** `supplied/continuity-handoff.json` (S-4) or `supplied/practitioner-standing.json` (S-5), written by O-F standing in for DEL-11-01 or DEL-09-12. These are not supplier records.

| Question | Ground | Notes |
|---|---|---|
| Q-1 decider, package id, act kind | O-F text | `reservedBy` quotes PRD §8 and EXAMINATION §7 |
| Q-2 revision | Supplier record (SQ-EX-05) | A placeholder string |
| Q-2 joined candidate, reconciliation | Supplier record (CIR, `not_supplied`) + packet rule RP-R3 | — |
| Q-3 elements, obligation, established, outside | Supplier record (SQ-EX-05) + packet rule RP-R1 | Key 1's Q-3 encoded RP-v0.1's defective rule (KEY-F1) |
| Q-4 journey fields | Supplier record (DOS example) + packet rule RP-R2 | Keys 1 and 2 used the pre-repair DOS example; key 3 uses O-C's repaired one |
| Q-5 complete | Packet rule RP-R4 | — |
| Q-6 gap ids, suppliers | Packet rule (gap derivation) | G-CONT and G-ADOPT come from first-cut S-4 and an absent DEL-11-02 input |
| Q-6 practitioner not a gap | Packet rule RP-R5 (R23-32 F-R3) | — |
| Q-7 alternatives | O-F text | Keys 1 and 2 inherit EUF1-R2's unclear release wording; key 3 asks whether the release act is performed or required |
| Q-8 decision state, owner act, v3.0.1 status | O-F text (the disposition) | `not_presented`: a fixture |
| **Q-9 practitioner standing, condition** | **First cut (O-F), S-5** | Not a DEL-09-12 record: none exists yet |
| Q-10 never established | O-F text (packet) | — |
| **Q-11 thesis identity** | **First cut (O-F), S-4**, observed by read-only `git` at `d2929fd62b` | Not a DEL-11-01 record; re-checked by `check_rp.py` A-10 |
| **Q-11 remote re-check, obligations, adoption** | **First cut (O-F), S-4** (and the absent DEL-11-02 input) | States what is not supplied or not run |
| Q-12 evidence standing | Packet rule | Illustrative because every supplier input is an example |
| Q-13 (key 3 only) | O-F text, applying R23-43 | — |
