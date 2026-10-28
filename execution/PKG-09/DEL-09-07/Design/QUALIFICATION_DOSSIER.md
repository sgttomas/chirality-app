# Local host qualification dossier — structure, applicability and handoffs

- Contribution: DEL-09-07/DOS-v0.1 (unit LHQ-U2, with `TRAFFIC_OBSERVATION_PLAN.md`; repaired in place for RV-LHQ-U2)
- Status: DRAFT DEFINITION — proposed, not assembled. No dossier exists; no case has run.
- Run and node: `APP-V4-DESIGN-PASS-4-20261003`, owner O-C, 2026-10-03.
- Serves: OUT-002 (the one durable joined dossier); REQ-007, REQ-008, REQ-009; AC-007, AC-008; VER-007, VER-008. It also supplies DEL-11-03 (DEP-11-03-007) and DEL-09-11 (DEP-09-11-006).
- Schemas beside this file (JSON Schema 2020-12, PROPOSED; valid and invalid examples beside each): `lhq.candidate-identification.schema.json` (LHQ §3; pinned at LHQ-v0.2's schema, sha256 3fb8f586b0bc1ca32c2ba4e82008e384109d3adc1189a0bf5091d598c46b5fc5 (LHQ2-R2, R23-42 item 4). A CIR carrying `app_candidate_subject` validates only under this schema, not the v0.1 schema `194f8419…`. Every dossier CIR is validated against this one), `lhq.traffic-observation.schema.json` (TOP §6), `lhq.dossier-manifest.schema.json` (§1–§5 here).
- **Consumed, not redefined: DEL-09-01's examination records, EXP-v0.2 (adopted under R23-21 item 3; RV-LHQ-U2 U2-R3).** This file relies on v0.2's `parts_not_applicable` (R23-19) and its change kind `case_definition`, so it pins the refrozen v0.2: `EXAMINATION_PROTOCOL.md` sha256 ff0187dafd9e1f0268a19f9266914bdba64f39e0c8befdcaf20d3da7a7206a93 (EXP-v0.2 with U-EXP-1 closed in place; re-pinned at pass-4 closeout C1 under R23-21 item 4 from `fc5b8230…20d`: no rule, schema or example changed); `exam.result-record.schema.json` (`…exam-result-record:0.2`, `format` EXP-v0.2) f7871c96cef25bb974aea73feca009ed3caf843db5077d80612f13b130af2081; `exam.change-impact.schema.json` b8fcb4586aa8d844fd9700d660f8eb66ccd66893724215b0a5d9cd468500f82f; `exam.review-record.schema.json` b3294a402197ffa67ba1beb85847b60a7cf8d7bf1edf0006703f94faf7344508. Each LHQ case or part result is an EXP result record. Its `subject.identification_record` cites the CIR (the slot EXP names for "the journey's own candidate identification record"), and its `configuration.host_profile` names the host-loop configuration. Reopening uses EXP change-impact records, and independent review uses an EXP review record. DEL-09-07 adds no outcome vocabulary of its own: EXP uses HOSTING §9.3's labels (R23-1), and LHQ's EXAMINATION spellings map one to one (*passed* → `pass`, *failed* → `fail`, *not run* → `not-run`). An LHQ record on a candidate takes `codex_pin: not_applicable` where no Codex is involved, `model_server.kind: local_provider` with `home: not_applicable`, and route `seam_live` (RV checked such a record against v0.2; EXP's example EXP-EX-08 has the same shape).
- Other inputs: `LOCAL_HOST_QUALIFICATION.md` (LHQ-v0.2, sha256 d59a1ea011fd860139603fb78c20a3f66b04984f1bc2501ac0af74083876b8f1; re-pinned at the tranche-2 closeout under R23-21 item 4 from LHQ-v0.1 `20361a0b…`. The version step v0.1→v0.2 changes only §3 (CI-5, with LHQ2-R1 and LHQ2-R2). The cases, §2.1, CI-4 and §7 that this file relies on are unchanged. v0.2 is pinned because the dossier's CIRs may now carry `app_candidate_subject`); rulings cited by ID (R23-21): R23-6 as revised, R23-10, R23-15, R23-16); DEL-04-03/RS-v0.9 (committed bytes at `cec590c5c3`, sha256 a91882e74064495c5758110deae4cbc7280f3b2a12d0df8592f5238d1afd16e5; the version relied on; nothing here relies on the A16 rows added under R23-18, so the pin stays (R23-21 item 3)) §9 (resolution status), §3 (who records a host-agent run); DEL-11-03 `ScopeOfWork.md` (0177354357b07ea177491cffc2b1c75ffac578e179ba96e63e91d6ba34dcf5b6; OUT-002, REQ-002, VER-002); DEL-09-11 `ScopeOfWork.md` (REQ-001, REQ-002, TBD-001).
- **Pin basis.** Either pin (R23-3). The App candidate's actual Codex version is a CIR element.

## 1. Dossier contents (the manifest)

The dossier is a set of files linked by one **dossier manifest**. Evidence is linked, never copied: host truth stays in the host's store (V4-REC-01; V4-HI-71).

| Element | Content | Rule |
|---|---|---|
| Identity and version | Dossier identity; version; date | A new version for every added or superseded record; earlier versions are kept |
| CIRs | Every candidate-identification record the cases cite | At least one. A later CIR names the one it supersedes (LHQ CI-4) |
| Case results | Per case LHQ-20…23: the EXP result record(s), for the case and its parts | Every planned case and part has a record, including *not run* (R23-20 item 3). Parts declared not applicable before the run are listed with their reason and left out of aggregation (R23-19). Outcomes as the EXP record states them; nothing re-labelled here |
| Traffic observations | The traffic observation record(s) for LHQ-23 | Raw captures are not in the dossier (TOP §6) |
| Host evidence index | Every host run record, receipt, origin mark, content identity, act record and destination record the results cite, each with its RS §9 resolution status at write: *resolved*, *unresolvable* or *not supplied* | Status at read is added by each reader; a reference never becomes resolved by being listed |
| Act and owner account | Every excluded act of REQ-009 with its owner, and every human act cited, with actor ≠ recorder | Nothing is claimed discharged by this dossier (AC-008) |
| Interface and native coverage | Per route (WebKit and Chromium interface examination; development and packaged native) which evidence exists for the host panel and the App candidate, or that it is absent | REQ-008; browser evidence never stands for a required native witness (V4-EXM-04) |
| Applicability map | §2 | — |
| Independent examination | The EXP review record of the examiner's reconstruction (§3) | Required before the dossier is handed to DEL-11-03 |
| Limitations | Every limit from the results and observations, in its owner's vocabulary (RS R11, TOP, EXP) | Kept with the result it limits |
| Handoffs | §4 to DEL-11-03; §5 to DEL-09-11 | — |

**Cross-reference rules (EUF1-S1; RR-EUF3, R23-49; checked by `prototype/dos_check.py`, sha256 c845bed87d155ab5f1a047c456d923c48c33e8495f38c0c3f6bfca47f60cdb6e).** A schema cannot compare one part of the manifest with another, or with the EXP records it cites, so these are checked by script:

- **DX-1** Every receipt named in either hand-over (§4 `receipts`, §5 `receipt_refs`) is listed in the host-evidence index as a `host_receipt`, with the same resolution status at write.
- **DX-2** When both hand-overs are present, they carry the same receipt set, because both concern the one LHQ-20 journey.
- **DX-3** A not-run case names no run. Only LHQ-20 has hand-overs. When every EXP result the manifest cites for LHQ-20 has outcome `not-run`:
  - there is no DEL-09-11 hand-over, because its required journey, run authors and record set would name a run;
  - the DEL-11-03 hand-over names no acceptance act and no receipt, and does not count as the completed witness.

  The script reads the outcomes from EXP result records passed with `--outcomes`. When an outcome is not supplied, it reports DX-3 as not checked rather than passing it. Its exit status is 1 for a broken rule, 2 when DX-3 could not be checked, and 0 only when every rule was checked and none is broken (RV3 N8).

The manifest examples satisfy all three:
- `DOS-EXAMPLE-INVENTED` (no case run) names no receipt and no run, and has no DEL-09-11 hand-over.
- `DOS-EXAMPLE-INVENTED-POPULATED` (only LHQ-20 run, inconclusive) lists RC-1, *unresolvable*, in the index and in both hand-overs.

Their outcomes are in `lhq.dossier-manifest.exp-outcomes.examples.json` (sha256 15d9ae2d1a1698a13a75d18c7fbc1c614d84f4b9969c1bf99a5cf26abd2880b8): invented stubs carrying only `record_id` and `outcome`, not EXP records.

`lhq.dossier-manifest.dx-violations.examples.json` holds five schema-valid violations, and `dos_check.py` reports each one:
- the EUF1-S1 example, which named RC-1 only in the DEL-09-11 hand-over and also named a run for a not-run LHQ-20;
- a resolution that differs from the index;
- a receipt missing from the DEL-11-03 hand-over;
- a not-run LHQ-20 with a DEL-09-11 hand-over (the example before RR-EUF3);
- a not-run LHQ-20 whose DEL-11-03 hand-over names an acceptance act and a receipt.

## 2. Applicability map (CI-4; V4-EXM-03, V4-EXM-05)

When something a result relied on changes, an EXP change-impact record reopens the affected cases. Earlier results stay attached to their own subject as historical. This table is DEL-09-07's reliance map: EXP's "reliance map used" (`unaffected_basis`). The rows are derived from the elements each EXP record carries (EXP §6.2 rule 2): a case is reopened when the changed thing appears in its record.

| Changed | EXP change kind | Cases reopened |
|---|---|---|
| Host candidate (build or configuration) | `candidate_code` | LHQ-20, 21, 22, 23 |
| App candidate | `candidate_code` | LHQ-20 and LHQ-23 where the App contributes to the embedded run; all four while that contribution is unknown (OI-013/014; an unknown reliance counts as affected, EXP) |
| Local model server or model | `configuration` | LHQ-20, 21, 22, 23: every LHQ case runs the embedded agent on it, and every candidate record carries `configuration.model` and `model_server` (EXP §6.2 rule 2) |
| Adopted operation policy | `configuration` | LHQ-20, LHQ-22 |
| Initial allow list | `configuration` | LHQ-23 |
| Observation tooling, OS version or snap length | `configuration` | LHQ-23 |
| Operation binding (OI-021) | `case_definition` (the binding table is part of the case definition) | Every case using the changed slot (LHQ §2.1) |
| Invented material | `fixture` | All |
| Codex pin of the App candidate | `codex_pin` | LHQ-23 (attribution of the App's Codex traffic); others only through the App candidate row |
| Case definition (steps, binding table, parts declared not applicable before the run; R23-19) | `case_definition` | The case whose definition changed |

A change of criterion is never made here. A criterion disposition is cited, never made (EXP; V4-EXM-05).

## 3. Independent examination (VER-007)

An examiner other than the dossier's assembler and the run's participants takes the dossier manifest and the linked evidence only. The examiner reconstructs:

1. the request and its basis;
2. the proposals, the stale refusal and the re-draft;
3. the human acts, each with actor and recorder;
4. the changes with their receipts;
5. the solve and the checks;
6. the autonomy settings and checkpoint;
7. the traffic and the comparison;
8. the recovery.

The examiner then compares this reconstruction with each result's claims. Their findings and standing go into an EXP review record (reviewer per V4-OPS-34, R23-12). A finding returns to the owning case. The dossier is not handed to DEL-11-03 while a finding against P20-A is open.

This is the dossier's own review, at the time of assembly. The week-later reconstruction is DEL-09-11's (VER-007 says so).

## 4. Handoff to DEL-11-03 (DEP-11-03-007)

DEL-11-03 OUT-002 consumes "the actual App DEL-09-07 joined dossier", preserving "the App/host/model configuration, applicable original basis, outcomes, receipts and attributable human acceptance". Its VER-002 checks that "source-only traces, independent component passes, stale/unknown outcomes or operation receipts without a human act cannot pass the required journey".

The handoff block names:

- the dossier identity and version;
- the CIR;
- the EXP result record for **P20-A** and its outcome;
- whether P20-A counts as the completed V4-EXM-20 witness;
- the human acceptance acts cited (act record references, actor, recorder);
- the receipts with their resolution status at write;
- the limits;
- the independent review record.

**Rules (PROPOSED).**

- **DH-1** P20-A counts only when its EXP outcome is `pass`, its run basis is `candidate`, it has no open review finding, and it names a local model server (LHQ LR-1, LR-2). Every other outcome is handed over as truthful evidence that does not complete the witness (REQ-008).
- **DH-2** The handoff states that it is not a replacement decision, a release or professional reliance (AC-007). The owner decides replacement (V4-REP-01).

## 5. Handoff to DEL-09-11 (DEP-09-11-006): the source-journey record

DEL-09-11 consumes "the actual identified V4-EXM-20 host-run evidence and host receipt references, including the source journey date needed for the week-later witness". Its reader must be a named reader separate from the run's author, person or agent (R23-10). The reconstruction happens "a week after V4-EXM-20" (EXAMINATION V4-EXM-31, kept as written, R23-6). Its purpose is that the run's sessions and its author's working context are gone. So the source-journey record supplies:

| Element | Why DEL-09-11 needs it |
|---|---|
| Journey identity (the LHQ-20 run) and its CIR | The one identified record set (DEL-09-11 REQ-001) |
| Journey date(s), with their source | The week-later observation is examined against them (REQ-001) |
| **Run authors**, each with identity and role: the person who requested and acted, the host agent's conversation or session, the recorder(s), the dossier assembler, the examiner | The reader's separation from the run's author is shown against this list (R23-10) |
| **Withheld items**, each with identity and kind, using DEL-09-11's input-set classes (`harness_session`, `host_agent_conversation`, `app_conversation`, `author_memory`, `derived_view`): the run's sessions and conversations; the run authors' working memory; and, as `derived_view`, **the dossier's case results, the examiner's reconstruction and its review record** | So DEL-09-11 can show they were not supplied to the reader (DEL-09-11 REQ-004; RRM §3). The reader must reconstruct from the run's own files, not from earlier reconstructions or results (R23-6's purpose) |
| **Record set**: the run's **primary** project records only — host run record, act records, findings, and receipt references — each with path, sha256 and its input-set standing (`record`, `project_file`, `host_evidence`, `not_authority`). The agent's own run summary (LHQ 20-13, *agent-prepared*) is listed as `not_authority` | The input-set manifest DEL-09-11 gives its reader (RRM §3) |
| **Host receipt, hash and origin references**, each with resolution status at write | Resolved again by the reader; an *unresolvable* reference stays so (RS §9; CA CAF-37). Against SWBPIPE's current answers, every receipt is session-only (SQ-09 (c); LHQ §7), so this handoff would carry *unresolvable* references |

**Rules (PROPOSED).**

- **DJ-1** The record set lists the run's primary project records only, each with its standing. Harness transcripts, session stores, private memory, **the dossier's case results, the examiner's reconstruction and review, and any other derived view** are named under withheld, never supplied (DEL-09-11 REQ-004; RRM §3). The agent's run summary may be supplied only as `not_authority`.
- **DJ-2** The handoff makes no schedule and no date of its own; DEL-09-11 arranges the reader (TBD-001 there).
- **DJ-3** It hands over the evidence of the journey's actual acceptance and change. It does not certify every other DEL-09-07 case (DEP-09-11-006 notes: "not an automatic pass of every DEL-09-07 scenario").

## 6. Failure behaviour

| # | What fails | Record left | Next |
|---|---|---|---|
| DF-1 | A linked record cannot be resolved at assembly | Index entry *unresolvable* or *not supplied* | Kept as such; the result it supports keeps its own outcome and gains the limit |
| DF-2 | The independent examiner finds a reconstruction that disagrees with a result | EXP review finding | Returned to the case; the handoff to DEL-11-03 waits for P20-A findings only |
| DF-3 | A case result is superseded by a rerun | New EXP record; change-impact record | Manifest version advances; the earlier result is kept as historical |
| DF-4 | Assembly happens with some cases not run | Their EXP records with `not-run` and reasons | The dossier is complete as a record and incomplete as qualification; it says which |
| DF-5 | The source journey's receipts are session-only | *unresolvable* in the §5 handoff | Handed over as unresolvable; DEL-09-11 records the gap (its AC-004) |

## Findings for other owners (returned, not applied)

- **D-F1 — closed by EXP-v0.2.** `configuration.host_profile` names the host-loop configuration; `codex_pin` and `home` take `not_applicable`; route `seam_live` (RV-LHQ-U2 U2-R3 validated such a record). Observation tooling stays in the CIR.
- **D-F2 — closed by EXP-v0.2's change kind `case_definition`.** An operation-binding change is a change to the case definition's binding table, so §2 reports it as `case_definition`.

## UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| The App candidate's role in an embedded run (OI-013/014) | Shared contract owner with SWB owner | Applicability map row "App candidate" | Treated as affected while unknown |
| Host run recording (RS §3: external owner) | SWBPIPE owner; host joins deferred | Before the host evidence index has entries | None now |

## Changes at repair (review RV-LHQ-U2; in place, version label unchanged)

| Finding | Repair |
|---|---|
| U2-R2 (MAJOR) the handoff could pass derived content | §5 and DJ-1 limit the record set to the run's primary project records, each with its DEL-09-11 input-set standing. The dossier's case results, the examiner's reconstruction and its review are withheld as `derived_view`, and the agent's run summary is supplied only as `not_authority`. The schema replaces `session_identities` with `withheld` (RRM kinds), requires a standing on every record-set item, and gains two invalid examples |
| U2-R3 (MINOR) EXP-v0.1 pinned, v0.2 relied on | EXP-v0.2 is adopted and pinned (R23-21 item 3). D-F1 and D-F2 are closed by v0.2 (`host_profile`; `case_definition`). The "EXP-v0.1 in progress" row is removed from UNRESOLVED |
| U2-R4 (MINOR) applicability map narrower than EXP | The map is derived from the elements each record carries (EXP §6.2 rule 2). The model row reopens all four cases. A case-definition row is added, and an operation-binding change is reported as `case_definition`. The schema's change kinds equal EXP-v0.2's (checked by script) |
| U2-R12 (NOTE, from the confirmation) | The duplicate `operation_binding` value is removed from the schema's `applicability.changed` enum |
| EUF1-S1 (O-F, via the coordinator; tranche 2) | The example's DEL-09-11 hand-over named RC-1 while the index and the DEL-11-03 hand-over were empty. DOS §1 already required the index to list every cited receipt, but nothing checked it. The not-run example now names no receipt. A second, populated example lists RC-1 (*unresolvable*) in all three places. The new rules DX-1 and DX-2 are checked by `prototype/dos_check.py`, with three violation examples. The schema-invalid examples, derived from the old example, no longer carry the inconsistency, so each fails only for its stated rule |
| RR-EUF3 (R23-49; tranche 2) | `DOS-EXAMPLE-INVENTED` recorded LHQ-20 as not run, yet its DEL-09-11 hand-over named a journey run, its record set and its run authors. That hand-over is removed, and a limitation says why. New rule DX-3 (a not-run case names no run) is checked by `dos_check.py --outcomes`. Two violation examples and an outcome-stub file are added. The populated example and the schema-invalid examples now cite the run (inconclusive) LHQ-20 result, so their limitation and withheld labels no longer say that no case has run, and each fails only for its stated rule. The schema is unchanged |
| RV3 N8 (Addendum 5; tranche 2) | Run without `--outcomes`, `dos_check.py` printed "DX-3 not checked" but exited 0. It now exits 2 when DX-3 could not be checked. Exit 1 still means a rule is broken, and 0 means every rule was checked and none is broken |
| Tranche-2 closeout pins (R23-21 item 4; LHQ2-R2, R23-42 item 4) | LHQ pin moved from v0.1 (`20361a0b…`) to v0.2, after reading v0.2's diff. Only §3 changed, and additively. The CIR schema is now pinned explicitly at v0.2 (`3fb8f586…`), because mapped CIRs fail the v0.1 schema. This was decided by the owner, not re-pinned by script |
