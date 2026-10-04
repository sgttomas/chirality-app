# SCC-CANDIDATE-N13 — DEL-09-07 ↔ DEL-09-11 (2026-10-04)

- **Standing.** This is pre-case evidence, not a case. `workflows/scc-resolution-case` opens a case only for a registered row. N13 is not a register row, so this folder is a candidate folder: no `Case_Contract.md`, CaseState or `Ruling_Register.csv`. It is evidence for HELP_HUMAN and the owner's checkpoint, not a ruling. Every move below is a **proposal**. Cut and merge are the owner's (`docs/CYCLE_DRIVEN_RESOLUTION.md` §2 rule 3). Nothing is changed by this file: no row, register, ScopeOfWork, Design file, DAG version or existing case file.
- **Run.** `APP-V4-GRAPH-CLOSURE-20261004`, working to `CASE_BRIEF_COMMON.md` (committed at `b459b4f2d1`). Author: O-C, a Type 2 TASK agent (Claude Opus 5.5) dispatched by HELP_HUMAN. It does not delegate. O-C designed both Design files examined here (DOS and RRM, pass 4), so this analysis is the design agent's own proposal and needs independent review. Branch `claude/app-v4-graph-closure`; read at HEAD `b459b4f2d1` through `0c815a8cdf`. No file read here changed between those commits (`git diff --stat`).
- **Paths.** `E/` is `projects/chirality-app-v4/execution/`. `P9/` is `E/PKG-09_Candidate examination and connected journeys/1_Working/`.
- **Scope.** One pair: G2's N13 (DEL-09-07 → DEL-09-11, not registered) against the admitted DEP-09-11-006 (DEL-09-11 → DEL-09-07).

## 0. Basis and checks

| File | sha256 |
|---|---|
| `E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/CASE_BRIEF_COMMON.md` | `c83e0f86ca55c26ddc6abd2cfa817256fd6ed42f6013a926b72016825c703468` |
| `…/SURVEY/G1.md` (r3, commit `4575bc1649`) | `3d6543bc2a05e5e62cb9673c1d3177386f484de38d9058a0b396eee9299f0a45` |
| `…/SURVEY/G2.md` | `24cc2a6fcb00e466775647ce14590cb91914b6132aab6a441e79576c22efa87b` |
| `…/GC_RULINGS.md` (GC-1…GC-4) | `27265cc9245fd7c2d93096dd8f2978376b51c48daf0e77fc110ced4c7c3318dc` |
| `docs/CYCLE_DRIVEN_RESOLUTION.md` | `bbd41a8d091c7fa81fce6462c1d5e976832e5879b6ab8c3c74147e2df55e514f` |
| `workflows/dependency-extract/resources/brief.md` | `b51a8166eda6131302c64dcbc893e375c028dd8931f9d49d64b4a0fb8cb49fde` |
| `E/_DAG/DAG-004/DependencyEdges.csv` | `c43033742df768a6fb493701d25b1d73240366172c05b1d0caa143650690966e` |
| `E/_DAG/DAG-004/CandidateEdges.csv` | `2bfff10e3094d7fd86da563006c965694563ec10d0fc78e9b1d9958fefa42025` |
| `P9/DEL-09-07…/ScopeOfWork.md` | `813ef0f3ebcbc000df3a54093f15a0cfe9b2a75c8f6bb69a6648b1eec8e0395a` |
| `P9/DEL-09-07…/Dependencies.csv` | `9010b0aa3e1c7d1edf8644003ed278224aec4d17200a427b64b8fd2b295d1c78` |
| `P9/DEL-09-07…/Design/QUALIFICATION_DOSSIER.md` (DOS-v0.1) | `b4de982f84e8f77aea1678084d40fae23e3a40bbb5614ab111fd2f5482cfd1fe` |
| `P9/DEL-09-07…/Design/lhq.dossier-manifest.schema.json` | `88cd994821c25422507ca45a901e4cd8ed5c31d847ecdbbd8475ad1ebd7d7e88` |
| `P9/DEL-09-11…/ScopeOfWork.md` | `e4ee1a5779af66fe085fefd12cf3b91dad2c8fdedcad6211ea613f2d188f09ae` |
| `P9/DEL-09-11…/Dependencies.csv` | `ccc0817502711be66f49b345fda0e600aa8087ce7f6016561fe58c262bd307b5` |
| `P9/DEL-09-11…/Design/READER_METHOD.md` (RRM-v0.1) | `3e24df2764bf881d40dda3c7e31588a5fccc16a68a4886b9aab449ce47316d33` |
| `P9/DEL-09-11…/Design/rrm.input-set-manifest.schema.json` | `a1f03a374b5b69d267b9dd6a0b4c2ccee3fe52ca306c2b2efe420b06b07ad15e` |
| `E/_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/reviews/RV-LHQ-U2.md` (U2-R2) | `61e76a9c40776c388569b6a85c367dbbcc868e864764bac619e49be39aad2095` |

Both Design files are "DRAFT DEFINITION", PROPOSED and not accepted.

**Checks run.** The scripts are scratch files under `$TMPDIR`, not in the repository.

| Check | Result |
|---|---|
| DAG-004 arcs | 212 arcs, consumer → supplier, with DOWNSTREAM rows reversed. Each one has a G1 r3 kind, parsed from G1 §2 and Appendix A. None is missing |
| Baseline SCC counts | O-1 6, O-2 4, O-3 2, O-4 2. These reproduce G1 §1.3 |
| Arcs between the pair | One: DEP-09-11-006 (DEL-09-11 → DEL-09-07), kind P. DEL-09-07's register has no row naming DEL-09-11 (grep). DEL-09-07's only outgoing arcs go to DEL-09-01 and DEL-09-06. No arc enters DEL-09-11 |
| Other paths DEL-09-07 ⇝ DEL-09-11 | None in DAG-004. None either when every other G2 item (§4 N and K rows, §5 A items; 42 arcs) is added at O-1. So N13 alone closes the cycle |
| N13 added | Under each of O-1…O-4 it forms exactly {DEL-09-07, DEL-09-11}. No other SCC changes. This reproduces G1 §2b.2 reading 2 |

## 1. The two rows of the exchange

| Row | From → To | Kind (G1 r3) | EvidenceQuote / Design sentence | Statement or citation | Mirror |
|---|---|---|---|---|---|
| DEP-09-11-006 (admitted) | 09-11 → 09-07 | **P** (K-4; K-5 does not apply because the witness is DEL-09-11's OUT-001; G1 case 6, RVG G1-m2) | EQ: "supplies the actual identified V4-EXM-20 journey evidence and host receipt references through its connected-activity examination owner." | ST: "Consume App DEL-09-07 actual identified V4-EXM-20 host-run evidence and host receipt references, including the source journey date needed for the week-later witness." Notes: "Only the relevant journey contribution is consumed, not an automatic pass of every DEL-09-07 scenario." | None. DEL-09-07 has no DOWNSTREAM mirror (LHQ F-4; G2 §6 G-15) |
| N13 (G2 §4; **not a row**) | 09-07 → 09-11 | **I** (K-2; G1 §2b.1) | DOS §5: "**Withheld items**, each with identity and kind, using DEL-09-11's input-set classes" | G2: "the input-set standings, and 'the input-set manifest DEL-09-11 gives its reader (RRM §3)'" | G2 §7 sizes it as "C N13†" in DEL-09-07 and "M N13†" in DEL-09-11 |

**ScopeOfWork.**
- **DEL-09-11, CLM-001** (the source of DEP-09-11-006): "App `DEL-09-07` supplies the actual identified V4-EXM-20 journey evidence and host receipt references through its connected-activity examination owner." REQ-001: "The witness shall use one identified V4-EXM-20 host-run record set from App DEL-09-07 …".
- **DEL-09-07: no sentence names DEL-09-11** (grep on `ScopeOfWork.md`, `813ef0f3…`).
  - OUT-002 names DEL-11-03 as its receiver: "supplies the local-host evidence to App `DEL-11-03`".
  - LHQ F-4 already records the gap: "DEL-09-07's ScopeOfWork names DEL-11-03 as its only receiver, although DEL-09-11 consumes it (DEP-09-11-006, admitted) … A receivers sentence is listed for the next amendment (R23-11)".
  - **No ScopeOfWork sentence of DEL-09-07 says that it consumes anything from DEL-09-11.**

## 2. The Design text on both sides

**DEL-09-07, DOS-v0.1 §5 "Handoff to DEL-09-11 (DEP-09-11-006): the source-journey record".**
- The withheld row: "**Withheld items**, each with identity and kind, using DEL-09-11's input-set classes (`harness_session`, `host_agent_conversation`, `app_conversation`, `author_memory`, `derived_view`): the run's sessions and conversations; the run authors' working memory; and, as `derived_view`, **the dossier's case results, the examiner's reconstruction and its review record**".
- The record-set row: "**Record set**: the run's **primary** project records only — host run record, act records, findings, and receipt references — each with path, sha256 and its input-set standing (`record`, `project_file`, `host_evidence`, `not_authority`). The agent's own run summary (LHQ 20-13, *agent-prepared*) is listed as `not_authority`". Its "why" column reads: "The input-set manifest DEL-09-11 gives its reader (RRM §3)".
- DJ-1: "The record set lists the run's primary project records only, each with its standing. … are named under withheld, never supplied (DEL-09-11 REQ-004; RRM §3). The agent's run summary may be supplied only as `not_authority`."
- The dossier schema encodes both enums. `handoff_del_09_11.record_set[].standing` is `["record", "project_file", "host_evidence", "not_authority"]`, described as "DEL-09-11 input-set standing (RRM §3)". `withheld[].kind` is the five RRM classes, described as "Kinds are DEL-09-11's input-set classes (RRM §3)".
- History: these enums entered DOS through review finding **U2-R2** (MAJOR, RV-LHQ-U2). Its repair said: "Name the dossier's results, the examiner's reconstruction and review, and the agent's summary as withheld, or as `not_authority`, using DEL-09-11's input-set classes."

**DEL-09-11, RRM-v0.1.**
- §1 roles: the **Assembler** "Builds the input set from the source journey's handoff, arranges the reader, records the dates".
- §3, "Built by the assembler from the source journey's handoff (DOS §5 for a V4-EXM-20 journey)", defines the item standings `record`, `project_file`, `host_evidence`, `definition` and `not_authority`, and the **withheld** list.
- The schema `rrm.input-set-manifest.schema.json` defines the enums `items[].standing` (`record`, `project_file`, `host_evidence`, `not_authority`, `definition`) and `withheld[].kind` (the five classes).
- §2 uses DOS §5's run-author list: "absent from the source journey's run-author list (DEL-09-07 DOS §5)". That use runs DEL-09-11 → DEL-09-07, the direction of the existing arc.

**What each side owns, by its own text.**
- The enums are defined in RRM and its schema. DOS copies them and says so.
- The run-author roles (`person_requester` … `examiner`) and the host-evidence kinds (`host_run_record`, `host_receipt`, `origin_mark`, `content_identity`, `act_record`, `destination_record`, `findings`) are DOS's own enums, in DOS's schema.
- The date-source enum (`observed_clock`, `record_timestamp`, `stated_by_person`) is shared by both sides from DEL-09-01's EXP schema. It is not DEL-09-11's.

## 3. Real contradiction or projection artefact

**Part order, from the Designs.**
1. RRM §3 defines the input-set standings and withheld kinds. It was designed and rehearsed on the early-path fixture FX-DP1, with no DEL-09-07 input.
2. DOS §5 defines the handoff and uses (1). It also defines the run-author list and the host-evidence kinds.
3. RRM §2 and §3 use (2): the run-author list for reader separation, and the handoff as the assembler's input.
4. LHQ-20 runs and produces the journey evidence, the content of DEP-09-11-006 (P).
5. DEL-09-11's assembler builds the input set and the reader reconstructs. This is the witness, DEL-09-11 OUT-001.

No part depends on a later part. The deliverable-level 2-cycle is a **projection artefact**: a design-time vocabulary flow (1 → 2) runs against a design-time and production flow (2 → 3 → 5, with 4 → 5).

**Rule-bearing or carry-only (case-002 §1 discriminator).** DOS's use of the RRM enums is **rule-bearing**. DJ-1 sorts the run's items with them, and the dossier schema validates against them. So GC-1 (a) fails on the current text: "The consumer's Design uses no field, state value or identity scheme that the supplier defines" is false for DOS. GC-3 does not apply, because these are enumerated classes with meaning, not uninterpreted identifiers. As the Design stands, N13 is a real I relationship.

## 4. Should N13 be a row?

**Not as things stand, and not after the proposed move.**
- **Extraction source.** `dependency-extract` extracts from `ScopeOfWork.md` by default: "`DEFAULT` uses `ScopeOfWork.md` as both anchor and execution source when present" (brief, `DOC_ROLE_MAP`). Every register row carries `EvidenceFile` `ScopeOfWork.md` and an `EvidenceQuote` from it. DEL-09-07's ScopeOfWork has no sentence naming DEL-09-11 (§1), and DEL-09-07's `_DEPENDENCIES.md` declares nothing about DEL-09-11 (grep). So a default UPDATE cannot produce N13. Registering it would take one of two things:
  - a ScopeOfWork sentence in DEL-09-07, added by an amendment the owner accepts;
  - a DECLARED entry.
  
  G2 found N13 in Design text only. Its §7 marks the row "†": "they need an owner ruling or an `scc-resolution-case` decision before extraction".
- **But the Design does state it.** A missing ScopeOfWork sentence is not a reason to keep the relationship. The Design consumes RRM's classes today (§3). The honest remedy is to remove the consumption, not to rely on the register missing it.
- **The pending F-4 sentence.** The receivers sentence LHQ F-4 lists for the next amendment (R23-11) must be worded as **supply only**, for example: "DEL-09-07 supplies DEL-09-11 the identified V4-EXM-20 journey evidence and host receipt references (DEP-09-11-006)". It must not be worded as "using DEL-09-11's input-set classes". Otherwise that amendment would itself give N13 a ScopeOfWork basis.

## 5. Proposed move M-01: invert the handoff vocabulary by design rewording (brief step 4 (i))

**The move.** DEL-09-07 states its handoff in its own classes, and DEL-09-11's assembler maps them into its input-set classes. The vocabulary then flows DEL-09-07 → DEL-09-11 as a contribution consumed by DEL-09-11, which is the direction of the existing arc. In the doctrine's words, the dependency is inverted "behind a contract/interface so the edge reverses". It reverses onto an arc that already exists, so no new arc is created.

**DEL-09-07: DOS §5, DJ-1 and the dossier schema.** Design agent: O-C, the DEL-09-07 owner.
- Record-set items carry DOS's own **host-evidence kind** from DOS §1's index (`host_run_record`, `host_receipt`, `origin_mark`, `content_identity`, `act_record`, `destination_record`, `findings`). They also carry a DOS-owned mark `agent_prepared` (true only for LHQ 20-13's run summary, which LHQ already labels *agent-prepared*). They do not carry RRM's `standing`.
- Withheld items carry a DOS-owned `class`, defined in DOS from LHQ's own run elements:
  - the harness session;
  - the host agent's conversation (LHQ's K-7 identity);
  - the App conversation;
  - the run authors' working memory;
  - a dossier product (the EXP case results, the examiner's reconstruction, its review record).

  They do not carry RRM's `kind`.
- DJ-1 is restated in DOS's own terms. This keeps U2-R2's protection whole:
  - primary records only;
  - every dossier product and session withheld, by identity;
  - the agent's summary never authority.

  Its citations of DEL-09-11 REQ-004 and R23-6 stay as citations of the receiver's stated need, which is basis text, not a Design contribution. RRM §3 is no longer cited as the source of the classes.
- `handoff_del_09_11` in `lhq.dossier-manifest.schema.json` replaces the two RRM enums with the DOS enums above. The valid and invalid examples follow, including U2-R2's invalid example (a derived view in the record set). `dos_check.py` is unaffected; it reads only receipts and outcomes.

**DEL-09-11: RRM §3, §9 and the input-set schema.** Design agent: O-C, the DEL-09-11 owner.
- RRM §3 gains the assembler's map from DOS §5 classes to input-set standings and kinds:

  | DOS class | Input-set standing or kind |
  |---|---|
  | `act_record` | `record` |
  | `host_run_record`, `host_receipt`, `origin_mark`, `content_identity`, `destination_record` | `host_evidence` |
  | `findings` | `project_file` |
  | any item marked `agent_prepared` | `not_authority` |
  | harness session | `harness_session` |
  | host-agent conversation | `host_agent_conversation` |
  | App conversation | `app_conversation` |
  | working memory | `author_memory` |
  | dossier product | `derived_view` |

- RRM §9 gains one failure row: a handoff item whose class does not map stops assembly; the witness is *blocked* (R23-20), and the item is returned to DEL-09-07. This is DEL-09-11 checking its own input, read at its point of need.
- `rrm.input-set-manifest.schema.json` is unchanged.

**GC-1 test after the move.**
- **(a)** DOS then uses no field, state value or identity scheme that DEL-09-11 defines. Its enums are its own, and RRM is cited only as the receiver.
- **(b)** Conformance of the handoff to DEL-09-11's input set is checked outside DOS. DEL-09-11's assembler maps the handoff and validates the assembled manifest against `rrm.input-set-manifest.schema.json`; a failure is RRM's new failure row.

The existing direction (DEL-09-11 consumes DOS §5) gains the class map. It is already covered by DEP-09-11-006's arc, so no new arc arises.

**What does not move.**
- No ScopeOfWork-assigned ownership moves, so the move code is IV, not IV-O. Neither ScopeOfWork assigns the handoff classes:
  - DEL-09-11 CLM-001 assigns integration of the witness to the App evidence examination owner, and RRM's assembler is that owner's role;
  - DEL-09-07 REQ-009 keeps DEL-09-07 out of other deliverables' acts, and the mapping is DEL-09-11's.
- **ScopeOfWork effect: none.** No ScopeOfWork sentence states N13, so none is reworded. The F-4 amendment wording (§4) is a condition, not a change made by this move.

**Residual.** None from N13. DEP-09-11-006 (P) stays, unchanged, as the one arc of the pair.

**Rejected alternatives.**
- **Invert or cut DEP-09-11-006.** It is the witness's production input: the journey evidence is the material DEL-09-11 reconstructs (K-4). Cutting it would leave OUT-001 without its subject, and inverting it has no meaning. Not proposed.
- **Treat the RRM classes as opaque in DOS (GC-3).** They are enums whose meaning DJ-1 applies, so (a) cannot hold. Not available.
- **Drop all classes from DOS and let the assembler classify from free text.** This satisfies GC-1, but it weakens U2-R2: the classification would rest on prose. M-01 keeps a closed enum on DEL-09-07's side instead.

## 6. Rulings and findings the move would amend (GC-4)

- **Integrator rulings: none.** No R23 or GC ruling requires DOS to use RRM's classes. R23-6 (the purpose of the week-later test) and R23-10 (reader separation, shown against DOS's run-author list) are unaffected.
- **Review finding U2-R2 (RV-LHQ-U2, MAJOR), repair wording.** "using DEL-09-11's input-set classes" is superseded in form, and its substance is kept. The reviewer of the rewording should confirm U2-R2 stays closed:
  - the record set holds primary records only;
  - dossier products and sessions are withheld by identity;
  - the agent's summary is never authority;
  - an invalid example rejects a derived view in the record set.
- **Self-review limit.** O-C wrote DOS, RRM and this proposal. Applying it is a revision of pass-4 frozen units, so it needs its own authorized brief and an independent reviewer (AGENTS.md "independent checking").

## 7. Closure under O-1…O-4 (G1 r3 kinds)

Computed by a scratch Tarjan pass over DAG-004's 212 arcs, filtered per option by G1 r3 primary kind (O-2 drops V; O-3 drops V and L; O-4 keeps P and I only):

| Option | SCCs, DAG-004 | With N13 added (I) | With M-01 (N13 not a relationship) | DEP-09-11-006 under the option |
|---|---|---|---|---|
| O-1 | 6 | 7: adds {09-07, 09-11} | 6. The pair is in no SCC | P, sequences |
| O-2 | 4 | 5: adds {09-07, 09-11} | 4. The pair is in no SCC | P, sequences |
| O-3 | 2 | 3: adds {09-07, 09-11} | 2. The pair is in no SCC | P, sequences |
| O-4 | 2 | 3: adds {09-07, 09-11} | 2. The pair is in no SCC | P, sequences |

What remains after M-01: nothing for this pair, under every option. DEL-09-07 reaches DEL-09-11 by no other path, even with every other G2 item added at O-1 (§0). So M-01 does not depend on how the other G2 items are settled.

## 8. Owner acts needed

| Option | With M-01 accepted | If M-01 is declined and N13 is registered |
|---|---|---|
| O-1 | None. The move is an agent design rewording, reviewed | One of: per-edge **cut** of N13 (an I row, so a cut reclassifies an interface contribution as out-of-objective), or **merge** {09-07, 09-11}. Either is an owner ruling. Before that, registering N13 needs a ScopeOfWork sentence in DEL-09-07, through an amendment the owner accepts |
| O-2 | None | As O-1. N13 is I, so it does not leave with V |
| O-3 | None | As O-1 |
| O-4 | None | As O-1 |

The owner should not be asked to cut DEP-09-11-006 under any option. It is P, and it is DEL-09-11's reason to exist.

## 9. Verdict

- **N13 ↔ DEP-09-11-006: projection artefact.** A design-time vocabulary use runs against the journey-evidence flow, and the parts order cleanly (§3).
- **Proposed:** M-01, an invert by design rewording of DOS §5 and RRM §3, which meets GC-1 (a) and (b). After it, N13 is not a relationship and is not registered, and no `scc-resolution-case` opens.
- **The component closes** under O-1…O-4 with no owner act.

## 10. Not established

- That `dependency-extract` would run with its default sources. A run given `SOURCE_DOCS` that includes `Design/` could extract N13 from the current text. The brief allows `SOURCE_DOCS` overrides, and I did not check whether any planned UPDATE uses one.
- The DOS-class names in §5 are proposals. Their final names, and whether the host-agent conversation class needs a host-specific identity form, are for the rewording, not this analysis.
- That RV, or another reviewer, accepts that a DOS-owned enum which maps one-to-one onto RRM's classes is an inversion and not a relabelling. The test applied is GC-1 (a), "uses no … state value … that the supplier defines". DOS would define the values, and DEL-09-11 would map them.
- No DAG version, register or Design file was changed or re-read for drift after HEAD `0c815a8cdf`.

## 11. 2026-10-04 note: RVG-N13 minors recorded as conditions on M-01

RVG reviewed this analysis and marked it READY, with BLOCKING 0, MAJOR 0, MINOR 2 and NOTE 3 (`E/_Coordination/AgentRuns/APP-V4-GRAPH-CLOSURE-20261004/reviews/RVG-N13.md`, sha256 `24f1f51f043afa2c784fc5d6441c0ababcb472b5a56051dc5e7c6840af5620e7`, committed at `e987d34d2c`). It agrees that M-01 is a genuine inversion. Nothing above is changed. The two minors are conditions on the rewording, in addition to those in §5 and §6:

1. **N13-m1.** Every record-set item keeps a required DOS `class`. Both U2-R2 invalid examples stay:
   - "U2-R2: a record-set item without its input-set standing" is restated as "a record-set item without its DOS class";
   - "U2-R2 / DJ-1: a derived view (the dossier's case result) supplied in the record set" stays as written.
2. **N13-m2.** RRM §9's new failure row is worded as DEL-09-11 blocking its own witness and reporting the unmappable item (R23-20). It does not say the item is "returned to DEL-09-07", and it states no act or receipt by DEL-09-07. Otherwise it would create a runtime row that re-closes the cycle. Any repair of the handoff stays DEL-09-07's ordinary design work. This replaces §5's wording "the item is returned to DEL-09-07".

The LHQ F-4 "supply only" condition (§4) is carried into the R23-11 amendment list by HELP_HUMAN, not by this file.
