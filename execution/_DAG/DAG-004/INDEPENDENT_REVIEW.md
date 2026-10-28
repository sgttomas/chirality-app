# V25 — independent review of the DAG-004 candidate

**Reviewer:** node V25, a Type 2 TASK (Claude Code subagent; no delegation).
This is the separate review instance that `project-dag` method Stage 4 step 3
and graph-version.md "Independent review" require. V25 wrote none of the
reviewed files. Git was used read-only and no network was used. The only file
written is this one. Scratch: `$TMPDIR/V25/` and the session scratchpad
(`v25_place.py`, sha256 prefix `b3daccb51d58d1ea`).

**Reviewed:** HEAD `4ca22437f7` (clean tree). Between the frozen basis
`75764184b9` and HEAD, `git diff --name-only` shows changes only inside this
run folder: `DAG_PREP/` (new), plus the V25 brief appended to `BRIEFS.md` and
the D1 row appended to `DISPATCH.md`. No register, ScopeOfWork, `_DAG/`,
`_Evaluation/` or case file changed after the basis.

**Read:** `BRIEFS.md` (common rules, D1, V25); `OWNER_DECISIONS.md`
(DECISION-1, DECISION-2); `DISPATCH.md`; all of `DAG_PREP/`;
`DX/DX_SCC-CHECK.md`; `AMENDMENT_PACKET/ARC_EFFECT.md`; `_DAG/DAG-003/`
(GRAPH_BASIS, HANDOFF_STATE, the edge files, the manifests);
`workflows/project-dag` (WORKFLOW, graph-version.md, method.md, currency.md);
the model V15 (`APP-V4-SCA002-20260929/reviews/V15.md`).

## Verdict

**READY FOR CHECKPOINT C.** There are no BLOCKING and no MAJOR findings.

- Every mechanical claim in `CHECKPOINT_C.md`, `REVIEW_PACKET.md`, the
  candidate's `GRAPH_BASIS.md`, `ASSEMBLY_RUN.md` and `Evidence/`, the closure
  snapshot and the currency snapshot reproduced, either from my own
  independent placement script or from reruns of the registered tools on
  copies.
- There are four MINOR findings (m-1…m-4) and two observations. None of them
  needs a change to a candidate byte before the owner decides.

## Counts

| Check | Result |
|---|---|
| Packet hashes | All 74 SHA-256 rows of `REVIEW_PACKET.md` (33 candidate files and 41 supporting records) equal the bytes at HEAD. The candidate holds exactly 33 files: DAG-003's file set less the five publication-time files. The six hashes in `CHECKPOINT_C.md` §7 also match (6/6) |
| Basis | `SOURCE_MANIFEST.sha256` (`03aa668b…`): `shasum -c` from E gives **130/130 OK**. Its paths and their order are identical to DAG-003's. There are **59** changed members: 19 `ScopeOfWork.md`, 20 `Dependencies.csv` and 20 `_DEPENDENCIES.md`, with DEL-05-02 as the only register without a SoW change. Nothing else changed. This is the set ARC_EFFECT §4 predicts |
| **Assembly rerun** | I copied `tools/`, `workflows/`, `AGENTS.md`, the execution root and the worktree's `.git` pointer to `$TMPDIR/V25/repo` and ran `python3 -B <candidate>/Evidence/assemble_graph.py` there. It exits **0**, result PASS, with 729 protected inputs unchanged. **32 of 33 candidate files are byte-identical**, including `AssemblyChecks.json`. `Evidence/Tool_Run.json` differs only in `finished_at` and in the `selected_context` hashes of `BRIEFS.md` and `DISPATCH.md`. Those two hashes still equal the files' bytes at `75764184b9`; the files were appended later (m-3) |
| **Strict audit** | I ran `audit_dag.py --dag-dir <copy> --canonical --strict` from the repository root (tool sha256 `830d0d53…3449a`). It exits **0** with 129 edges, 41 nodes, 0 canonical findings, 0 endpoint issues, 0 SCCs, 0 duplicates and 0 bidirectional pairs. My JSON equals `Evidence/dag_audit.json` in every key except the two path keys. The non-strict audits of `CandidateEdges.csv` (83) and `Evidence/admissible_edges.csv` (212) also exit 0 and equal `candidate_audit.json` and `admissible_audit.json`. Each shows six SCCs, of sizes 2/2/2/2/3/13 |
| **Independent placement** | My script re-read the 41 live registers and applied SR-2, SR-6 and SR-7 itself, with its own Tarjan pass. It does not reuse `assemble_graph.py`, `reapply_selection.py`, `audit_dag.py` or the analyzer. The registers have 929 rows: 355 ACTIVE ANCHOR, 7 RETIRED and **567 ACTIVE EXECUTION**. Of those, 359 have a deliverable target, giving **212 arcs**: **129 admitted** and **83 held**. The other rows split into 208 NOT_TOPOLOGICAL, 145 MIRROR and 2 SAME_ARC. **All 567 keys are placed exactly as expected:** 0 placement mismatches, 0 missing, 0 extra, 0 duplicates. Every MIRROR and SAME_ARC row's `RepresentedBy` is the right representative's locator. `SourceRegisterSHA256` and `SourceRecord` are correct on every row |
| Fidelity | All 212 admitted and held rows equal their source in all 29 core columns. `Explicitness`, `SatisfactionStatus` and `Confidence` are non-blank on all 212. All 212 `EvidenceQuote` values are exact substrings of their current `ScopeOfWork.md`. All 83 held rows are `SCC_UNRESOLVED` with the right `SCCRef` and `CaseRef` (SCC-004→CASE-005, SCC-005→CASE-006 and SCC-006→CASE-007, as in DAG-003). Each case's `OpenQuestion` equals DAG-003's text |
| Nodes | `DeliverableNodes.csv` is byte-equal to DAG-003's (`102eee1a…`). `_LATEST_ACCEPTED.md` still names GROUP3 |
| **Departure** | Against DAG-003's edge files, **exactly 10 arcs are added** and 0 removed. No existing arc changes layer. Admitted: NR-05 (DEP-01-04-020), NR-07 (-021), NR-01 (DEP-02-03-028), NR-02 (DEP-03-03-015) and NR-04 (DEP-02-02-020). Held in SCC-002: NR-08 (DEP-01-04-022), NR-09 (-023), NR-4 (-024), R2-04-03-e (DEP-04-03-034) and R20-10 (-035). Every arc is in its ARC_EFFECT §1.1 layer. All ten are UPSTREAM INTERFACE rows at INITIALIZED, with satisfaction TBD on seven and PENDING on three (DEP-03-03-015, DEP-04-03-034 and -035) |
| Representative changes | Exactly 7 changes, matching GRAPH_BASIS and MirrorAssessment row for row: 5 held arcs (DEP-02-03-029, DEP-03-02-034, DEP-03-03-016, DEP-03-03-017, DEP-04-03-036) and 2 admitted arcs (DEP-05-01-026, DEP-09-06-035). On both admitted arcs the old and new representatives have the same RequiredMaturity and SatisfactionStatus, so no verdict changes |
| SCCs and pairs | The six SCCs have the same members as DAG-003, and SCC-002 keeps its 13. There are 27 reciprocal pairs, 21 of them inside SCC-002 (DAG-003: 24 and 18). SCC-002's internal account is 128 rows, 71 arcs and 48 new rows, as the CASE-002 draft states |
| Guards | DEL-01-02 reaches only {DEL-01-01, DEL-01-05, DEL-04-01}, and DEL-01-03 reaches only those three and DEL-01-02, so R17-10 holds. DEL-01-05 reaches only SCC-001. None of the three suppliers reaches SCC-002. DEL-04-01 has 0 suppliers. DEL-09-06's consumers are only DEL-03-04 and DEL-09-07, and it reaches 20 deliverables. N-12, N-B8, NR-03, NR-06, NR-10, the reverse-citation arcs and both REQ-008 source-wording arcs are absent (the script asserts these; my reachability agrees) |
| DAG pending | The ends of the added arcs are the 11 deliverables named: DEL-01-02, 01-03, 01-04, 01-05, 02-01, 02-02, 02-03, 02-04, 03-03, 04-02 and 04-03. This equals `dag_pending.csv`, the currency report §5 and ARC_EFFECT §4 |
| **Currency** | I reran the registered analyzer (`2b8de3cb…`) with the recorded arguments on the scratch copy. Against DAG-003 it reports `DEPARTURE` with the same 10 arcs, 0 removed and the same 11 pending. Maturity changes on existing representatives (DEP-03-03-008, DEP-09-06-015) are correctly treated as drift, per currency.md |
| **Successor precheck** | On a scratch copy (execution root without `_Evaluation` and `_Coordination`), I installed the candidate as `_DAG/DAG-004/` and wrote `_DAG/_LATEST.md` from `PROPOSED_LATEST.md` with a date filled in. The analyzer reports **`NO_DEPARTURE_FOUND`**, 0 pending and 0 added or removed arcs, which reproduces `successor_currency_precheck.json` |
| Closure snapshot | The analyzer rerun with `--output-dir` reproduces **13 of 14** Evidence files byte for byte. In `closure_summary.json`, only the absolute `accepted_dag` paths and the `comparison` basis differ. `scc_summary.csv` is byte-identical to the SCA-V4-002 closure's |
| Recorded hashes | All 112 path/sha256 pairs in `SOURCE_BASIS.json` verify, as do those in the currency and closure `Tool_Run.json`. In the candidate's `Tool_Run.json`, 25 of 27 verify; the two that do not are `BRIEFS.md` and `DISPATCH.md` (m-3) |
| Mirror findings | Representative and mirror differ in RequiredMaturity on exactly three arcs, all TBD consumer against INITIALIZED supplier: DEL-06-01 → DEL-01-01 (DEP-06-01-013 / DEP-01-01-030), DEL-09-01 → DEL-01-01 (-019 / -031) and DEL-08-02 → DEL-02-01 (DEP-08-02-006 / DEP-02-01-037). DAG-003's two differences are now both INITIALIZED. The type pairs over the 91 new comparisons are exactly MirrorAssessment's: INTERFACE/HANDOVER 58, PREREQUISITE/HANDOVER 17, INTERFACE/INTERFACE 12, PREREQUISITE/INTERFACE 3 and CONSTRAINT/HANDOVER 1 |
| Unextracted mirrors | Each of the five arcs exists through a consumer UPSTREAM row: DEL-02-04 → DEL-01-01 (DEP-02-04-010, admitted), DEL-04-03 → DEL-01-01 (DEP-04-03-027, admitted), DEL-01-01 → DEL-01-05 (DEP-01-01-024, held in SCC-001), DEL-03-01 → DEL-03-02 (DEP-03-01-026, held) and DEL-02-03 → DEL-03-03 (DEP-02-03-026, held). So none has a graph effect, as stated |
| DEL-01-03 TargetLocation | 14 rows carry the absolute personal path: 001…010 are ANCHOR rows; 011 and 012 are admitted representatives (DAG-003's copies carry the same bytes); 013 is a MIRROR; 014 is NOT_TOPOLOGICAL with a PACKAGE target. This matches CHECKPOINT_C §5 and Accounting.md |
| Untouched | `_DAG/_LATEST.md` still says `Latest: DAG-003`. `_DAG/` and `_Evaluation/` have no commit since DAG-003's publication and the SCA-V4-002 closure audit. DAG-003, DAG-002 and DAG-001 `MANIFEST.sha256` verify 37/37, 37/37 and 61/61. `_Evaluation/DAGCurrency/_LATEST.md` still names the 2026-09-29 CURRENT observation, as disclosed. `PROPOSED_LATEST.md` is in §11.2 form, differing from the live pointer only in identity, date placeholder, basis, `Supersedes: DAG-003` and the cited audit |
| CASE-002 draft | It is evidence only (no ruling, remedy or closure). It appends after the existing heading "Successor observation, 2026-09-29 (DAG-003 candidate…)" (line 43). It continues the existing numbering: E5-* follows E4-*, and F-048 follows F-047. Its counts (128/71/21; +48 = 5 + 2 + 5 + 36) match my recomputation |

## Semantic examination (graph-version rules)

- **The edge semantics fit the objective.** Each of the ten new representative
  rows quotes a sentence in which the consumer receives or consumes a named
  contribution for a stated part of its work. Examples: "composes the turns it
  sends, including the collaboration mode supplied by App DEL-01-03"; "a run
  in the chain ends only as DEL-01-02 defines ending a run". None rests on an
  ownership or exclusion sentence. The quotes are exact. One existing arc's
  new representative is the exception (m-1).
- **Rule applications.** There are no `OUTSIDE_INVENTORY`, `UNRESOLVED_TARGET`,
  `INVALID_ROW` or `TYPE_NOT_SELECTED` rows, and no DELIVERABLE-typed row
  falls outside SR-2. NOT_TOPOLOGICAL is 208 (151 EXTERNAL, 26 DOCUMENT,
  17 PACKAGE, 14 UNKNOWN), DAG-003's 207 + 2 new EXTERNAL − 1 retired PACKAGE
  row. No scope-boundary question hides in the exclusions.
- **Admitted layer.** Four SCC-002 members gain direct admitted suppliers, as
  stated: DEL-01-04 (DEL-01-03, DEL-01-05) and DEL-02-02, DEL-02-03, DEL-03-03
  (DEL-01-02). The layer stays acyclic.
- **Isolated nodes and hubs.** There are 0 isolated nodes. Hub degrees rise
  for DEL-04-03 (27 → 29), DEL-02-03 (23 → 25) and DEL-02-01 (20 → 21);
  DEL-04-01 stays at 20 (m-2).
- **Candidate reasons and limitations** are stated per SCC with the work they
  leave without input. No ruling is cited beyond CP1-20260928. The carried
  rules, cases and guards are presented as carried, not re-decided.
- **CHECKPOINT_C** matches the evidence in every count and table. Nothing on
  the page, in the pointer draft or in `_DAG/` implies acceptance. The rejection
  path is stated honestly. The recommendations (C-1…C-7, questions 1–4) are
  sound and decidable.

## Findings

No BLOCKING. No MAJOR.

| # | Severity | Finding | Disposition |
|---|---|---|---|
| m-1 | MINOR | **A gating representative now says it takes no requirement.** On the existing admitted arc DEL-05-01 → DEL-01-05, SR-6 now selects DEP-05-01-026, which is UPSTREAM INTERFACE, INITIALIZED/PENDING. Its Statement says it receives DEL-01-05's capability handoff "as information … no requirement of this contract is taken from them". That is the P1-10 sentence the owner accepted at K1. The former representative, DEP-01-05-014, is a supplier HANDOVER row saying DEL-01-05 "supplies … requirements … to DEL-05-01 receiving". The verdict is unchanged: the maturity and satisfaction are the same, and DAG-003 already admitted the arc. However, the consumer's own row now characterizes as informational an arc that gates DEL-05-01. Under graph-version.md, a statement-level disagreement between representative and mirror is listed in GRAPH_BASIS and routed to both owners, and the human may direct that the arc be held. The point is disclosed only in `Evidence/MirrorAssessment.md`. It does not appear in GRAPH_BASIS's "Findings routed to owners" or in CHECKPOINT_C | Present it to the owner with C-4/C-5 as an open matter: does DEL-05-01 → DEL-01-05 remain a gating input, or should the register owners reconcile the type or statement through `dependency-extract`? Carry it in `HANDOFF_STATE.md`. No candidate byte change |
| m-2 | MINOR | **The hub change is not carried.** The closure report records the hub degrees (DEL-04-03 29, DEL-02-03 25, DEL-02-01 21, DEL-04-01 20). GRAPH_BASIS and CHECKPOINT_C do not mention them, although DAG-003's HANDOFF_STATE carried the hub note | Add a hub line to DAG-004's `HANDOFF_STATE.md` at publication |
| m-3 | MINOR | **The reproduction note is incomplete.** `REVIEW_PACKET.md` says a rerun reproduces everything "except `Evidence/Tool_Run.json` (`finished_at`) and possibly … `protected_input_count`". A rerun now also changes `Tool_Run.json`'s `selected_context` hashes for `BRIEFS.md` and `DISPATCH.md`, because those run records were appended after D1. The basis bytes at `75764184b9` still match. `Tool_Run.json` will therefore differ from any later rerun in more than its timestamp | Disclosure only. Publish the packet bytes, as the packet already directs |
| m-4 | MINOR | **V15 O-3 recurs.** `REVIEW_PACKET.md`, `ASSEMBLY_RUN.md` and `GRAPH_BASIS.md` say `INDEPENDENT_REVIEW.md` "is added to the candidate when returned", which would make 34 files against the packet's 33. CHECKPOINT_C §6 and the DAG-003 precedent add it only at publication, in `_DAG/DAG-004/` | Follow CHECKPOINT_C §6: copy this file as `INDEPENDENT_REVIEW.md` into `_DAG/DAG-004/` at Stage 5. Keep the 33-file packet, and keep `_Candidates/DAG-004/` byte-equal to it |

### Observations

| # | Observation |
|---|---|
| O-1 | **The C-3 advice list gains no new supplier.** The ten deliverables in C-3 and currency §7 (DEL-03-04, 09-02, 09-06, 09-07, 09-11, 10-03, 10-04, 11-01, 11-02, 11-03) already reached DEL-01-02 and DEL-01-05 through admitted links in DAG-003, and six of them also reached DEL-01-03. Their reach is identical in DAG-004: the new arcs add paths, not suppliers. The advice conforms to currency.md ("route runs through a changed arc"), but its consequence is small. New transitive admitted reach is limited to three deliverables: DEL-01-04 gains DEL-01-03 and DEL-01-05; DEL-02-03 and DEL-03-03 each gain DEL-01-02. DEL-02-02 already reached DEL-01-02 and DEL-01-03 under DAG-003, so NR-04 adds a direct wait but no new reach. The handoff may state this |
| O-2 | **Absolute home paths appear outside DEL-01-03.** Besides the 14 TargetLocation rows, absolute paths appear in analyzer outputs: `closure_summary.json` `accepted_dag.path` and `pointer`, and the currency `analyzer.stdout.json`. The precedent has the same pattern (the SCA-V4-002 closure). When the DEL-01-03 repair is routed, the owner may also want these noted. No graph effect |

## For the owner

- There is no blocking or major finding. The candidate is exactly DAG-003
  plus the ten links you accepted at Q-4, each in its predicted layer. Every
  register row is placed once (567), and the strict audit passes. Once
  installed, the analyzer reports no departure.
- Accepting changes sequencing in one respect only: DEL-01-04, DEL-02-02,
  DEL-02-03 and DEL-03-03 wait on DEL-01-02, DEL-01-03 or DEL-01-05 for the
  stated parts. The 11 pending deliverables clear.
- One point is worth adding to the open matters (m-1). DEL-05-01's own row now
  calls DEL-01-05's handoff "information" that sets no requirement, yet the
  link stays a sequencing link. Nothing changes from DAG-003, but you may want
  the register owners to reconcile it.
- m-2…m-4 are handoff and packaging notes for publication. None reopens a
  check.

## Tools and scratch

- **Scratch copies:** `$TMPDIR/V25/repo` (assembly rerun),
  `$TMPDIR/V25/audit` (strict, candidate and admissible audits),
  `$TMPDIR/V25/pre` (successor install) and `$TMPDIR/V25/closure` (closure
  rerun).
- **My script:** `v25_place.py` (Python 3.13.7). It does the placement,
  fidelity, provenance, departure, representative, guard, reachability,
  mirror, CASE-002 and TargetLocation checks.
- **Inline checks:** packet, SOURCE_BASIS and Tool_Run hash verification;
  the quote sweep; the manifest diff.
- **Repository writes:** none other than this file.
