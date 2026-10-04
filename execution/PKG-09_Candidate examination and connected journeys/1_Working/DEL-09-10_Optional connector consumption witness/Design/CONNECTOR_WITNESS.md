# Optional connector consumption witness

- **Contribution:** DEL-09-10/CW-v0.2. It supersedes CW-v0.1 (sha256
  `f836c7462286aa3197256c75b9fbb36cdd2e465b86a694a3e05876e0834e44f3`, the
  EU-D1 freeze RV2 reviewed), repaired for RV2-EUD1 (EUD1-R1, R5, R6, R7;
  R23-40); see "Changes". Owner O-D, run
  `APP-V4-DESIGN-PASS-4-20261003`, early unit EU-D1. Serves OUT-001 (the
  suite: §2, §3) and OUT-002 (the witness account: §4, §5).
- **Status:** PROPOSED. The suite is defined and its limited cases are
  rehearsed on constructed inputs. The qualified joined witness (AC-001) is
  not run: no qualified PEC release and no App adoption exist.
- **Basis:** ScopeOfWork sha256 `a976bf18fba98d137086628102b9995d0b0018346019b8b64a89eb52a4c166aa`
  (INIT; no SCA revision); Dependencies.csv `98b586fb2c9432ac2d2383db800676315f15a424f3590d6f4f408a5dc406c146`.
  EXAMINATION V4-EXM-01…05, V4-EXM-30, §7. Records follow DEL-09-01
  EXP-v0.2 (`exam.result-record.schema.json`, rules EXP-R1…R9; outcome
  labels per R23-1, R23-20). Rulings: R23-19 (parts not applicable), R23-20
  (`blocked`, `not-run`), R23-27 (conditions as declared stimuli), R23-34.
- **Register note (R23-34 item 8):** this register has no upstream row for
  DEL-09-01; DEP-09-01-027 is admitted from DEL-09-01's side. For the
  register owners.

## 1. Subject and consumer

The selected receiving consumer is the App ("The App is the first intended
PEC consumer", V4-EXM-30). The coordination question is DEL-07-01's Q1
(PRC-v0.1 §2). Domains' research question QD (DRC-v0.1 §5) carries the
original absent-PEC/stale-Domains combination. Standing is read in DEL-07-02's
vocabulary (CFB-v0.1 §2).

## 2. Cases

| Case | Criterion | Parts | Declared stimuli (R23-27) |
|---|---|---|---|
| CW-QC | AC-001 | QC-1 qualified joined trace (one actual source pin → qualified PEC response → permitted App receiving action); UQ-1 unqualified delivery reported as such; QA-1 adopted-current receiving; QA-2 a relied report of READY nodes establishes no readiness to start (Q1 asked at S) | None for QC-1 (needs a real release); P1, P2, P7 for the rehearsal parts |
| CW-LC | AC-002 | LC-1 absent (no response); LC-2 stale; LC-3 partial; LC-4 failing; LC-5 a record-tier citation that does not resolve; all on Q1 | PEC stopped; pin before a change to the cited file; feed partly parsed; fallback signal set; an anchor missing from the cited file |
| CW-OC | AC-003 | OC-1 PEC absent + Domains index older than its sources; IA-1 PEC with Domains absent… IA-3 both absent (IA-2 rehearsed in EU-D1) | PEC stopped; a source revised after indexing; Domains query unavailable |
| CW-RB | AC-004 | Binding of every result to candidate, configuration and date; reopening on candidate change (EXP §6.2) | — |
| CW-BD | AC-005 | Custody: release/adoption evidence, D108, owners of excluded acts; no act fabricated | — |

No part is declared not applicable in this version.

## 3. Pass conditions per part

A part passes only if, for its condition:
1. the standing has the expected envelope and condition, with reasons;
2. no item that CS-R1 excludes is relied on;
3. the named unsupported conclusions appear (CS-R3);
4. no prohibited conclusion appears anywhere (CS-R2);
5. the question is answered from the route where reliance is not
   supported, and the route account's facts match the sources;
6. (OC/IA) each connector's standing equals its standing with the other
   connector's inputs removed (CS-R4).

On a candidate, "the App shows" replaces "the record holds"; interface
scenarios run in WebKit and Chromium with a packaged smoke (EXP §8;
V4-EXM-04).

## 4. Records and standing of evidence

- **Rehearsal (now):** EXP records with `run_basis: rehearsal`, the fixture
  as the double. They stand for no scenario (EXP-R3).
  - Evidence carries its own standing per source (RV2 EUD1-R6): connector
    receiving records are `constructed`; the route accounts are derived
    from real bytes (no fixture standing); the work graphs they read are
    cited as `recorded` (`git show` bytes, provenance `static_inspection`).
  - The record date is the build constant of the deterministic build,
    labelled `record_timestamp` with a limit saying so, never
    `observed_clock` (RV2 EUD1-R5). A rehearsal on a later day still
    carries that constant, so it is not a statement of when anything was
    observed.
- **Candidate (later):** a `candidate` record names the App candidate, Codex
  pin, route, model and model server (EXP-R2), the PEC release and the App
  adoption account (DEL-07-01 OUT-004). Only then can a record stand for
  V4-EXM-30.
- **QC-1 now:** `not-run`, with missing inputs "qualified, released PEC
  response" (PEC owning project, DEP-002) and "App release-level adoption"
  (App receiving owner). It becomes `blocked` only if attempted and stopped
  (R23-20). An applicable `not-run` part beside passing parts aggregates to
  `inconclusive` (EXP-R1), which is the honest state of CW-QC today.
- **CW-QC stays visibly a rehearsal (RV2 EUD1-R7).** Its record carries the
  limit "AC-001 is not examined … do not read this record as a candidate
  result". The dossier (§5) carries that limit forward wherever CW-QC's
  outcome is cited, so `inconclusive` is never read as a candidate result.

## 5. Dossier (OUT-002; outline)

Per candidate: the case records; a PEC gap sheet (release, qualification
evidence, adoption, OI-022 terms still open, D108 as stated) and a Domains
gap sheet (contract, admitted sources, OI-023/OI-026), in DOS-v0.1's
pattern; the owners of excluded acts (REQ-006); and the independent review
(EXP §7).

## 6. EU-D1 rehearsal

`RUN/D/` builds three records, CW-EUD1-LC, CW-EUD1-OC and CW-EUD1-QC,
validated against EXP's schema and rules. `OWNERS/O-D.md` lists the results
and file hashes.

## 7. Open

| Matter | Owner | Point of need |
|---|---|---|
| QC-1 joined witness | PEC owning project (release); App receiving owner (adoption) | After a qualified PEC release |
| IA-1, IA-3 rehearsal | O-D | Next unit |
| CW-RB, CW-BD case detail | O-D | Next unit |
| Domains cases on admitted sources (V4-EXM-32 is DEL-08-02's) | Domains receiving owners | Domains-enabled increment |

## Changes

| Finding (ruling) | Change | Where |
|---|---|---|
| RV2 EUD1-R1 (R23-40) | Part QA-2 (P7: Q1 asked at S; relied report of READY nodes; readiness to start named unsupported) | §2 |
| OD-F1 (owner) | Part LC-5 (P8: unresolvable citation) | §2 |
| RV2 EUD1-R5 | Record dates labelled as the build constant | §4 |
| RV2 EUD1-R6 | Per-source fixture standing in evidence | §4 |
| RV2 EUD1-R7 | CW-QC's rehearsal limit carried into the dossier | §4, §5 |

