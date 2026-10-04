# RVG review of SCC-CANDIDATE-N13 (O-C) — APP-V4-GRAPH-CLOSURE-20261004

- **Reviewer:** RVG, a Type 2 TASK executor (Claude Opus 5.5, `claude-opus-5-5`). No delegation. I did not author DOS, RRM or the analysis. O-C did, and says so. Read-only git, no network.
- **Subject:** commit `5785eeebec`:
  - `E/_DAG/cases/SCC-CANDIDATE-N13/PAIR_ANALYSIS_2026-10-04.md`, sha256 `d4187515c91aa0a6608231f2319f17f214ee3fa434f0ef6da09feb781e875673`;
  - `MOVES_PROPOSED_2026-10-04.csv`, sha256 `17f5fd3554ec00dfa42460664b2531de53a63992b60c9708f7eb049004e05260`.
- **Read at source:**
  - DOS-v0.1 §5 (l.118) and DJ-1 (l.124), with the changes row for U2-R2 (l.154);
  - `lhq.dossier-manifest.schema.json` and its invalid examples;
  - LHQ F-4 (l.351);
  - DEL-09-11 ScopeOfWork REQ-004 and AC-004;
  - `RV-LHQ-U2.md` U2-R2, in full;
  - `R23_RESOLUTIONS.md` R23-11;
  - DAG-004's arcs at and around the pair.
- **Scripts:** `$TMPDIR/rvg/`.
- **Paths:** `E/` is `projects/chirality-app-v4/execution/`.

## 1. What holds

- **Arcs.** DEP-09-11-006 (DEL-09-11 → DEL-09-07, kind P under G1 r3) is the only arc between the pair, and DEL-09-07 has no outgoing arc toward DEL-09-11.
- **Reach.** I added all 42 other G2 items (N, K and A rows) to DAG-004's 212 arcs at O-1. DEL-09-07 still does not reach DEL-09-11; its reach stops at the SCC-002 cluster, 01-0x, 09-01, 09-06 and 09-09. So N13 alone closes the cycle, under every option, as G1 r3 §2b states. **Confirmed.**
- **No ScopeOfWork basis today.** DEL-09-07's ScopeOfWork names no DEL-09-11 consumption, and LHQ F-4 records that its only receiver is DEL-11-03. A default `dependency-extract` UPDATE therefore cannot produce N13. **Confirmed.**
- **Current kind.** As DOS stands, N13 is a real interface relationship. DJ-1 and the schema's two enums are rule-bearing on RRM's classes, so GC-1 (a) fails today and GC-3 does not apply. **Confirmed.** The analysis is candid about this.
- **Part order.** RRM §3 (rehearsed on FX-DP1, with no DEL-09-07 input) → DOS §5 → RRM §2 and §3 assembly → LHQ-20 evidence → the witness. This is a projection artefact. **Confirmed.**

## 2. Inversion or relabelling? (the question O-C flags)

GC-1 (a) asks whether the consumer's Design "uses no field, state value or identity scheme that the supplier defines". Read literally, M-01 passes once DOS's enums are its own. A one-to-one renaming could pass that letter while the meaning still comes from RRM, so I applied three further tests.

| Test | Result after M-01 |
|---|---|
| **(i) Definitions in the supplier's own domain.** Are DOS's classes defined from LHQ's own run elements, not as RRM's kinds renamed? | **Record set: yes.** The seven host-evidence kinds already exist in DOS's schema as DOS's index (`host_run_record` … `findings`), and they map **many-to-one** onto RRM's standings. `agent_prepared` is LHQ's own label for 20-13. **Withheld: yes, if written that way.** The five classes are LHQ run elements (harness session, the host agent's conversation with its K-7 identity, App conversation, working memory, dossier product). They match RRM's five kinds one-to-one because RRM was designed for the same journey. The rewording must define each in DOS's terms, with no "= RRM `harness_session`" glosses |
| **(ii) DJ-1's rule grounded in basis, not in RRM's Design** | **Yes.** DJ-1's substance (primary records only; sessions, memory and derived views never authority) is DEL-09-11 ScopeOfWork REQ-004: "Private agent memory, a harness transcript/session store, and a derived view … shall not become authority". That is accepted basis, the same treatment SCC-002 gives basis-owned content (P3). R23-6's purpose ("whether the files and host receipts stand on their own") is also basis. RRM §3 stops being cited as the source |
| **(iii) Change propagation** | **Runs the right way.** If RRM changes its standings or kinds, DOS needs no change. If DOS adds a class, RRM's map must follow, along the existing arc DEP-09-11-006. An unmappable item blocks assembly at DEL-09-11 (RRM §9 new row) |

**Verdict on the question: a genuine inversion, not a relabelling.** It qualifies provided the withheld classes are defined in DOS's own terms, per test (i). The many-to-one map on the record set shows the DOS vocabulary is not a renaming of RRM's.

## 3. U2-R2 stays closed in substance, under two conditions

U2-R2 (RV-LHQ-U2, MAJOR) required four things. Each survives M-01 as follows:
- **Record set limited to primary project records** (host run record, act records, findings, receipt references). The closed DOS host-evidence enum cannot name a dossier case result, a reconstruction or a review, so the schema itself excludes them. Holds, **if `class` is required on every record-set item**, as `standing` is today.
- **Dossier products, the examiner's reconstruction and review, and sessions withheld by identity.** Holds through the DOS "dossier product" and session classes.
- **The agent's summary never authority.** Holds through `agent_prepared` → `not_authority`. DJ-1 must keep "supplied only as `agent_prepared`, never as authority".
- **"Add an item class to `record_set` and an invalid example."** DOS's U2-R2 repair actually added **two** invalid examples:
  - "U2-R2: a record-set item without its input-set standing";
  - "U2-R2 / DJ-1: a derived view (the dossier's case result) supplied in the record set".

  M-01 mentions only the second (§5: "U2-R2's invalid example (a derived view in the record set)").

**N13-m1 — MINOR.** The rewording must keep both invalid examples, the first restated as "a record-set item without its DOS class", and must keep `class` required. Otherwise U2-R2's item-class protection lapses silently.

## 4. LHQ F-4 condition: holds and is necessary

- **F-4** (LHQ l.351) is "carried under R23-11". R23-11 lists overtaken ScopeOfWork wording "for the next amendment, which reaches the owner at its own checkpoints". No sentence has been drafted yet.
- I searched the run folders for "input-set classes". It appears only in DOS's schema (and a vendored copy in `APP-V4-DESIGN-PASS-4-20261003/F/vendor/`), RV-LHQ-U2, G1 and G2. It appears in no pending amendment text.
- O-C's condition is right and necessary: the receivers sentence must state supply only. As worded ("DEL-09-07 supplies DEL-09-11 the identified V4-EXM-20 journey evidence and host receipt references (DEP-09-11-006)"), it yields a DOWNSTREAM mirror on the existing arc and creates no new arc.
- The condition should be carried into the R23-11 amendment list, not left only in this case file.

## 5. Other findings

| ID | Severity | Finding | Consequence |
|---|---|---|---|
| N13-m2 | MINOR | RRM §9's new failure row says the unmappable item "is returned to DEL-09-07". If the rewording states that DEL-09-07 must receive and act on returns, that is a runtime flow DEL-09-11 → DEL-09-07, read consumer → supplier as DEL-09-07 → DEL-09-11. Under K-3 that is an E row, and it would re-close N13's cycle under O-1…O-3. This is the pattern of RVG-C2 B2-M1 | Word the row as DEL-09-11 blocking and reporting its own witness (R23-20). Any repair is DEL-09-07's ordinary maintenance of its handoff, not a stated consumption by DEL-09-07 |
| N13-n1 | NOTE | Before M-01 is applied, an UPDATE run whose `SOURCE_DOCS` include `Design/` could extract N13 from today's DOS text (§10, first item) | Sequence the application before any such run, or exclude Design for DEL-09-07 until then |
| N13-n2 | NOTE | `APP-V4-DESIGN-PASS-4-20261003/F/vendor/lhq.dossier-manifest.schema.json` is a vendored copy in a completed run's evidence | It is historical evidence. The rewording changes only the live Design file |
| N13-n3 | NOTE | O-C authored DOS, RRM and this proposal. This review is the independent check of the proposal. Applying it to pass-4 frozen units needs its own brief and its own independent review, as O-C states | — |

## 6. Verdict

**READY.**
- **The pair is a projection artefact.** M-01 is a genuine inversion by design rewording that meets GC-1 (a) and (b), and N13 then has no Design basis and is never registered.
- **No owner act** is needed under any of O-1…O-4.
- **Folded into M-01's application brief:**
  - the two minors: both U2-R2 invalid examples with `class` required (N13-m1), and RRM §9 worded as block-and-report (N13-m2);
  - the test (i) requirement that the withheld classes are defined in DOS's own terms;
  - the F-4 condition (supply-only wording), carried into the R23-11 amendment list.
- **Fallbacks.** M-02 (cut) and M-03 (merge) are correctly labelled fallbacks, needed only if M-01 is declined and N13 is registered.

**Counts.** BLOCKING 0, MAJOR 0, MINOR 2, NOTE 3.
