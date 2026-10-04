# Manual changes — the 60% gate and the handoff to 90%

**What this is.** This is a TASK (MW) change summary for HELP_HUMAN, dated 2026-10-04. It answers the owner's request, quoted in `LESSONS_60PCT.md`: "Can you add to the richness and accuracy of the Project Management manual and Agent User Manual around this transitionary phase and how to discern it, what criteria to watch for, and how to pass through it and handoff to the 90% phase?"

The manuals are guidance. Nothing here amends AGENTS.md, a workflow, SPEC or a project's adopted basis. No .html, .docx or .pdf file was edited, and v7 is unchanged. The v7 sha256 `0aafefb1…f095032` was checked before and after the edits.

**Sources**, all in this run folder unless a path is given:
- `LESSONS_60PCT.md` (cited as L§n);
- `OWNER_DECISIONS.md`;
- `GC_RULINGS.md`;
- `../../WorkGraphs/APP-V4-GRAPH-CLOSURE-20261004/WORK_GRAPH.md`;
- `docs/CYCLE_DRIVEN_RESOLUTION.md`;
- `projects/chirality-app-v4/loop/LOOP_INIT.md`;
- `docs/SPEC.md` §5.4;
- `workflows/coordinated-knowledge-work/WORKFLOW.md` §§1, 2, 4;
- `workflows/construct-local-work-graph/WORKFLOW.md` §§1–3.

**Counts checked against the records:**
- 41 deliverable folders.
- 83 rows in `_DAG/DAG-004/CandidateEdges.csv` (86 lines, less the header) and in G1.
- Six SCCs (G1 l.27).

**Owner quotations.** All are exact text from `OWNER_DECISIONS.md`. The spelling "enmass" is the owner's and is kept.

## 1. Project_Management_for_Human_Agent_Teams_Consolidated_v8.md (new)

This is a byte copy of v7 with the edits below. v7's front matter has no edition or "v7" label, so no edition naming changed. The authorship section is untouched.

| Section | Change | Source |
|---|---|---|
| §1.7, "60%: develop the details…" | Corrected (see C1). Successors follow structural findings. Finer relationships go to local work graphs. The gate does not require a DAG free of every cross-reference or cycle-closing relationship, and a coupled group can pass as a group. A pointer to §4.12 is added. | L§1; owner, "the graph will never stop changing in minute details…" |
| §3.11, Merge paragraph | Added: late in development a merge can apply for planning and execution, with deliverables keeping their identities and contracts. Points to §4.12. | Brief; doctrine §2 rule 3; L§3 |
| §3.12, "Keep graph change deliberate" | Corrected (see C2). Added the distinction between structure and detail. | L§1, L§2 |
| Chapter 4 intro | Corrected (see C3). "Broader structure" is defined as the deliverables and the order between groups. Detail goes to the work graphs. | L§1 |
| §4.7, "Renew the project DAG…" | Added two things. First, grouping co-designed SCC members as a remedy. Second, a paragraph on keeping renewal at DAG level, which says that chasing coupling the work requires is the wrong level. | L§2, L§3 |
| §4.12 (main revision) | Corrected the opening sentence (C4) and the "no further DAG change" sentence (C5). Added these subsections: **Distinguish structure from detail**, with a five-row level table and SCC treatment by grouping as a planning merge under the human's decision; **Test whether the structure is settled**, giving the four-check grouping test in general form with the App v4 worked example and its numbers; **Recognise work at the wrong level**, giving five warning signs and the App v4 wrong turn with its numbers and the owner's redirect quote; **Prepare the assessment and obtain the decision**, covering the gate as the human's act, exact words with custody, and the owner's acceptance quote; **Hand the work into 90%**, giving five practices. "Examine what could still change the route" is extended with the thin-design inventory, open matters sorted by who closes them, and evidence standing. | L§§1–6 |
| Figure 4.10 | Updated in place. Added a "Coupled work" block covering grouping, held rows, the group order and residual risks, and an "Evidence standing" block. Extended "Project basis", "Developed detail" and "Local execution". The caption gains one sentence. No new figure was added. | L§§3–4, L§6 |
| Chapter 5 intro | Corrected (see C6). | L§1 |
| §5.1, "Confirm the route remains suitable" | Added one sentence: a contract found wrong follows the change control set up at the transition. | L§6 |
| §5.10 | Corrected (see C7). | L§1 |
| Working vocabulary | Added the entry **Walking skeleton**. | L§6; WORK_GRAPH "Redirection to build" |

### Sentences corrected (old v7 wording)

- **C1, §1.7.** Old: "Findings during 60% commonly warrant successor versions of the project DAG. Carry each through the applicable source amendments, dependency examination, and human decisions." The new text says successors are warranted "when they change its structure: the Deliverables it contains, or the order in which groups of them can be completed". **Why:** "commonly warrant" implied that ordinary findings each need a new DAG, and the lessons show the opposite (L§1, L§2). No text stated that the DAG must be free of cross-references, but the old wording invited that reading, so the new text says so explicitly.
- **C2, §3.12.** Old: "During 60%, design findings commonly produce that need, and several successor DAGs may be required before the route settles." The new text reads "can produce that need, and more than one successor DAG may be required", and adds the structure/detail distinction. App v4 did have DAG-001 to DAG-004, so the possibility is kept.
- **C3, chapter 4 intro.** Old: "Such revisions are common during this phase … The project approaches the end of 60% when it expects to complete the remaining development without further changes to that broader structure." The new text uses "can occur" and defines the broader structure.
- **C4, §4.12.** Old: "the team should expect to carry the remaining work through without another change to the project DAG." The new text reads "without another structural change". **Why:** the old text was inaccurate against the owner's own words: "the graph will never stop changing in minute details".
- **C5, §4.12.** Old: "The expectation of no further DAG change remains revisable." The new text reads "no further structural change".
- **C6, chapter 5 intro.** Old: "and further changes to the project DAG are no longer anticipated." The new text reads "further structural changes", and adds that finer relationships are ordered in the work graphs.
- **C7, §5.10.** Old: "The absence of anticipated DAG changes at the end of 60%". The new text reads "anticipated structural DAG changes".

## 2. Project_Management_for_Human_Agent_Teams_Field_Book_v1.md (edited in place)

| Section | Change | Source |
|---|---|---|
| §1, positions table, 60% row | Extended. Old: "Developed design and interfaces; an execution route for which further structural changes are no longer anticipated." The new row adds "(the Deliverable set, the order between groups)" and "each SCC treated so its work can proceed". | L§1 |
| §1, new subsection "The 60% gate" | Two framing sentences, then one fenced checklist with three parts: DISCERN, STOP ANALYSING AND BRING THE GATE WHEN, and HAND OFF TO 90%. A closing line says the gate is the human's act, recorded as exact words with custody. Reference link to v8 §4.12. | L§§2–6 |
| §4, "Establish the dependencies" | One sentence added: grouped co-designed members keep their held rows non-gating, and the work graph orders the parts. | Brief; doctrine §2 rule 4 |
| §5, step 2 | Extended. Old: "Renew the project DAG when its governing relationships change." The new text names the deliverable set or group order, or what the adopted departure rules require. Finer ordering belongs to the work graph. | L§6; SPEC §5.4 |

## 3. CHIRALITY_AGENT_USER_MANUAL_v3.md (edited in place)

| Section | Change | Source |
|---|---|---|
| §5, route table, "Work toward 60%" row | The useful-basis column adds "structure settled at DAG level, with each SCC treated so its work can proceed", with a link to the new subsection. | L§1 |
| §5, new subsection "Discern and pass the 60% gate" (`#gate-60`) | Covers: <br>• the definition at DAG level against work-graph level; <br>• who assembles the assessment, and what TASK may do; <br>• a six-part assessment table: design inventory with thin designs, grouping test, residual-risk containment, open matters, evidence standing, continuation; <br>• the treatment when the test fails, and grouping as a merge for planning purposes ruled on by the human; <br>• five stop-analysing signs; <br>• the gate as the human's act, with exact words, source and custody in `OWNER_DECISIONS.md`; <br>• five steps for setting up the 90% loops, with the SPEC §5.4 departure rule stated as governing; <br>• three rulings as general practice: opaque references (GC-1 and GC-3), Design uses as dependencies (GC-5) and no narrowing (GC-6). | L§§1–7; GC_RULINGS |
| §8, four-moves paragraph | One sentence added, pointing to `#gate-60` for grouping near the gate. | L§3 |
| Link definitions | Added `[human-manual-v8]`, `[ckw]`, `[app-v4-loop]` and `[app-v4-gc-rulings]`. All targets were checked to exist. Existing `[human-manual]` still points to v7. | — |

## 4. Matters for HELP_HUMAN

- **Edition links.** The Field Book and the Agent User Manual still point their existing links at v7, and the AUM header still says "companion to version 7". Only the new text links to v8. LOOP_INIT also pins v7. Repointing those links, or adopting v8, is left to HELP_HUMAN and the loop.
- **SPEC §5.4 and the lessons.** SPEC §5.4 treats any added or removed edge, or a new cycle, as a departure: the DAG goes pending and the human decides. L§6 says a successor comes "only on a structural event". The manuals defer to the adopted rules. Registering the roughly 60 design-level dependencies may therefore set some App v4 deliverables to DAG pending, even inside a group.
- **Check 4 of the grouping test.** L§3 lists "SWBPIPE host joins: A and D" under "contained in one group". The general check 4 therefore allows containment "within a group, or at an identified join that follows the group order". This should be confirmed.
- **Grouping as a merge in App v4.** The owner explicitly approved merging the contract core under change control. For groups B–E, the record of the human decision is the gate acceptance itself, which followed the owner's "a valid decision to start grouping items together". The B0 merge page was dropped. The manuals say grouping requires the human's decision. They do not claim a separate merge record was made.

## 5. Repair after review MR-MANUAL (REPAIR: 2 MAJOR, 11 MINOR)

**Basis.** These repairs answer `reviews/MR-MANUAL.md`, committed at `b935a016a6` against candidate `a8d835ad7b`. They are made in place in v8, the field book and the Agent User Manual. v7 is still unchanged (sha256 `0aafefb1…f095032`).

The repair supersedes parts of §§1–4 above:
- corrections C1–C3 are reverted where they narrowed when a successor is needed;
- "merge for planning purposes" is withdrawn everywhere.

### Findings and changes

| Finding | Repair |
|---|---|
| **MAJOR-1** "merge" and "resolved" | The gate-time treatment is now called **grouping for development**. It is a planning arrangement that the human accepts, typically with the gate. Each manual says plainly that it is not a merge ruling under CDR §2 rule 3 or project-dag SR-4: held rows stay `SCC_UNRESOLVED`, their cases stay open, and the local work graph orders the parts. A recorded merge, cut or other move remains available through the doctrine and project-dag, and it produces a successor. "An SCC is resolved when…" is removed; the gate asks that every SCC have an *accepted treatment* under which its work can proceed. "Resolved" appears only in the owner's quoted criterion and its reading. Places changed: v8 §3.11 (Merge paragraph), §4.7 (SCC sentence), §4.12 (SCC paragraph), Figure 4.10 "Coupled work"; the field book §1 DISCERN list and §4; AUM §5 `#gate-60` and §8. |
| **MAJOR-2** do not narrow SPEC §5.4 | Restored "commonly" in v8 §1.7, the chapter 4 intro and §3.12 (C1–C3 reverted). The text now separates two things: a *departure* (an added or removed relationship, or a changed cycle), which the human decides under the adopted rules and which can be batched into one successor; and a *structural change* (the Deliverable set or the order between groups), which is what the gate expects not to happen. Fixed the four passages MR quoted: §1.7, §4.7, §4.12 after the level table (now MR's wording), and §4.12 "No successor was needed" (now "…needed to pass the gate; the dependencies found in the designs are carried through the departure rules as the loops register them"). The §4.12 opening paragraph and the chapter 5 intro gain the departure statement. The §4.12 handoff paragraph now sets out the proportionate path once: batch per scope amendment, one currency examination, one small successor. It cites App v4's three successors accepted during 60% (DAG-002 to DAG-004, checked in each ACCEPTANCE_RECORD) and the future departures from G2b. The field book §1 framing, the handoff block and §5 step 2 are restated on the departure rule. In AUM step 4 the scope-amendment route comes first, followed by batching and the DAG-002 to DAG-004 example. |
| **MINOR-1** "settled" | Field book DISCERN now reads: "…is settled, contained as a residual risk with an owner, or accepted by the human as a stated qualification." |
| **MINOR-2** check 4 | Field book: "contained in a group or at an identified join that follows the group order, with an owner." |
| **MINOR-3** grouping before the gate | Field book: "grouping for development proposed for the human's decision, which may be given with the gate." The DISCERN list no longer implies a prior decision. |
| **MINOR-4** v7 §1.7 reference | The field book reference beside the gate subsection is repointed to v8 §1.7 and §4.12. The other v7 links are left for the v8 adoption decision. |
| **MINOR-5** revision marks | Added a dated revision line to the field book (after its title) and to the AUM header. The AUM line names §5, §8 and the v8 citation, and says that the rest is unchanged. |
| **MINOR-6** GC-5 premise | v8 §4.12 handoff and the AUM ruling now say "Under (part-level) edge semantics such as App v4's (the consumer requires the supplier's contribution before the stated part of its work)…". |
| **MINOR-7** placement | In v8 §4.12, the phase-names paragraph and Figure 4.10 now end "Examine what could still change the route". "Prepare the assessment and obtain the decision" follows the figure. |
| **MINOR-8** where groups are recorded | "The DAG's group order" becomes "the group order accepted at the gate" in v8, the field book and the AUM. The decision record now includes "the groups, their members, the order between them, and the result of the grouping test". The assessment and Figure 4.10 list the groups with their members. |
| **MINOR-9** owner's criterion | AUM: "with few or no conflicting outcomes" ("without many or any" in the owner's words). |
| **MINOR-10** residual risks | v8 example: the host-side joins touched the core and the fleet group, which lie in group order; the placement question and the policy Deliverable's reach lay within the core; the roughly 60 dependencies became register updates. |
| **MINOR-11** dense figures | Removed from v8: "10,584 … 536 pairs" and the 16–26 range. The text now reads "Each survey found more coupling: the 83 held relationships, then 30…, then 62…". The 41/83/six/five-group outline and the quotes are kept. |
| **NOTE-1** "towards" | Both instances changed to "toward". |
| **NOTE-2** "recorded" | Changed to "replied". |
| **NOTE-3** duplication | v8 §1.7's second paragraph is shortened to one statement and a pointer. The §4.7 paragraph is tightened to the departure/structure distinction and a pointer. |
| NOTE-4, -5, -6 | No manual change. NOTE-4 (stale HTML, README editions) belongs to the publication step. |

### Words added against the original baselines

| Document | Before | After this repair | Added |
|---|---|---|---|
| v8 against v7 | 69,271 | 72,227 | +2,956 |
| Field book | 2,631 | 3,116 | +485 |
| AUM | 17,033 | 18,745 | +1,712 |

### Still for HELP_HUMAN

- **Group membership.** App v4 should commit its group A–E membership before the loops fan out (MR MINOR-8). The manuals now ask for that record.
- **Residual-risk wording.** `OWNER_DECISIONS.md` says the residual risks are "contained within single groups". LESSONS §3 places the SWBPIPE joins at A and D. The v8 example follows LESSONS and MR's ruling 2.
- **Notice to the App v4 loop.** The pinned field book and AUM changed in place. The App v4 loop should be notified (MR MINOR-5).
- **Separate decision.** Adopting v8 and repointing the remaining v7 links, the README and LOOP_INIT is a separate decision (MR ruling 4).

## 6. GC-7 revision

**Why.** This revision follows the owner's later direction, under "Structure versus detail after 60%" in `OWNER_DECISIONS.md`. That direction includes: "It's probably better to leave some things underdefined and seek human judgment in the moment than take your limited experience too far and overconstrain things in the future leading to a problem that builds and isn't recognized." It also follows ruling GC-7 (`GC_RULINGS.md`) and `GROUPS.md`.

**What changed.** Passages that said every finer edge change is a departure for the human to decide now follow GC-7, lightly:
- **Record found relationships where those who depend on them will see them.** Within a group, the group's work graph is enough. Across groups, use a shared list that every loop reads. The register is not the only place.
- **Update registers and ScopeOfWork when wording would otherwise mislead.** The human decides these updates in batches at natural boundaries. SPEC §5.4 still governs the registers.
- **Ask the human in the moment** about anything that seems to run against the group order, forms a cross-group cycle, changes the deliverable set, would make another group's finished work wrong, or suggests that the grouping is wrong. In doubt, ask.
- **State the limits of the guidance.** It comes from one project's experience and sets no thresholds or fixed tiers.

No tier names are introduced. v7 is unchanged.

| File | Passage | Change |
|---|---|---|
| v8 | §1.7, first and second 60% paragraphs | The sentence calling every added or removed relationship a departure is removed. Successors are carried through the adopted rules, and several can be decided together. Finer relationships point to §4.12. |
| v8 | Chapter 4 intro | Removed "departures in it are still decided under the project's rules". |
| v8 | §4.7, "Distinguish…" paragraph | Now reads "Distinguish detail from structural change". Coupling detail is recorded where those who depend on it will see it (§4.12). |
| v8 | §4.12, opening "Structural change…" paragraph | The departure rules apply when changes reach the registers, decided in batches. |
| v8 | §4.12, reading of "resolved" | Now "an accepted treatment" (MR's last point). |
| v8 | §4.12, level table, last row | Recording place: work graph within a group, shared list across groups, register where wording would otherwise mislead. |
| v8 | §4.12, sentence after the table, and the App v4 "No successor…" sentence | Aligned with the recording practice. |
| v8 | §4.12 handoff, "Registers updated…" | Replaced by "Found relationships recorded where they will be seen". This brings in the GC-7 points, the in-the-moment triggers, "In doubt, ask", and the one-project, no-threshold statement. The batching and DAG-002…004 detail is removed. |
| v8 | Figure 4.10 caption, chapter 5 intro | Brought into line, lightly. |
| Field book | §1, gate framing sentence | Finer relationships are recorded where those who depend on them will see them. |
| Field book | §1, handoff block | Gains the recording places and batched register updates. Adds a new short block "ASK THE HUMAN AT ONCE" with the triggers, "In doubt, ask" and "From one project's experience; no thresholds". |
| Field book | §5, step 2 | The departure rule applies when the dependency records change. Finer relationships go in the work graph, or in a shared list across groups. |
| AUM | §5 `#gate-60`, opening paragraph | The departure clause is replaced by a pointer to step 4. |
| AUM | §5, step 4 | Rewritten to GC-7. Names `CROSS_GROUP_RELATIONSHIPS.md` via a new `[app-v4-groups]` link to `GROUPS.md`. Keeps SPEC §5.4 and the batching example. Adds the in-the-moment triggers and the limits of the guidance. |
| AUM | "Rulings worth carrying", Design-uses bullet | The superseded GC-5 item 3 sentence is replaced: GC-7 relaxed carrying each dependency into ScopeOfWork and register to recording it where it will be seen. |

**Words added against the original baselines:**

| File | Words added |
|---|---|
| v8 against v7 | +2,902 |
| Field book | +523 |
| AUM | +1,772 |

## 7. MR Addendum B, MINOR-B1 (HELP_HUMAN, 2026-10-04)

One sentence was added in v8 §4.12 ("Found relationships recorded where
they will be seen"), in Agent User Manual §5 step 4, and in the field book's
HAND OFF block: a ready or blocked verdict read from the project DAG does
not cover relationships recorded only in a work graph or the shared list,
so read those before declaring work ready. GROUPS.md's trigger list now
matches GC-7 (N-B1).

## 8. GC-8, the current edition, and repointed links (MW, 2026-10-04)

**Basis.**
- The owner's directions in `OWNER_DECISIONS.md`: no new record types, no edition pinning, and the entry reading.
- Ruling GC-8 in `GC_RULINGS.md`.

v7 is unchanged. No HTML, DOCX or PDF file was edited.

**GC-8 wording.** The shared list is gone. A cross-group relationship is now recorded in the work graph of each affected loop, and the readiness sentence is kept. Changed passages:

| Document | Passage | Change |
|---|---|---|
| v8 | §4.12 level table, last row | Now reads "Work graphs or dependency records"; "across groups, the work graph of each affected loop". |
| v8 | §4.12 handoff, "Found relationships recorded where they will be seen" | Records cross-group relationships in the work graph of each affected loop, carried into a group's graph when that graph is constructed. Adds "No new standing list is needed." The readiness sentence now reads "relationships recorded only in work graphs". |
| Field book | §1 HAND OFF block | Now reads "the work graph of each affected loop across groups; read them before declaring work ready". |
| Field book | §5 step 2 | A relationship that crosses groups goes in the work graph of each affected loop. |
| AUM | §5 step 4 | Covers each affected loop's work graph and the carry-over when the other group has no graph yet. Says to create no new standing list and cites GC-8 and the groups record. The readiness sentence is kept. `CROSS_GROUP_RELATIONSHIPS.md` is no longer named. |

**Current edition (README.md).**
- "Current editions" now lists v8 with its Markdown, Word and PDF. The Word and PDF are named `Project_Management_for_Human_Agent_Teams_Consolidated_v8.docx` and `.pdf`; they do not exist yet, and HELP_HUMAN will produce them or remove the entries.
- v7 is moved to the top of the Archive table, with its Markdown, Word, PDF and the `plans/evidence/2026-09-22_manual_v7/` evidence link. All three of those targets exist.
- In "Maintain the management-manual formats", the v7 evidence is now described as the retained layout's preparation. A link to this change summary records the v8 text revisions.

**Links repointed: 18.**
- **Field book: 16 links** from v7 to v8 (one bare link and 15 with anchors), plus one label "Manual v8 §1.7" changed to "Manual §1.7".
- **AUM: 2 links**, the header link and the `[human-manual]` definition.
  - The `[human-manual-v8]` definition is removed. Its three uses become "[Human manual §4.12][human-manual]".
  - The header now reads "An operational companion to the current edition of *Project Management for Human–Agent Teams*".
  - The revision line says the links now point to the current edition.
  - Two unrequested edits remove edition pinning in passing. "Version 7 develops…" becomes "The management manual, since version 7, develops…". The source-map label "v7 route and adoption boundary" becomes "route and adoption boundary". The anchor `#v7-adoption` is kept so links do not break.
- **Not changed:** the AUM `[guide-sources]` and `[guide-conflicts]` evidence links under `manual_v7`. They record the guide's source basis.

**Anchors.**
- All 17 fragment links from the field book into v8 resolve to explicit `<a id>` anchors. These are `ch_1_6`, `1_7`, `1_9`, `1_10`, `2_1`, `2_9`, `3_1`, `3_9`, `4_1`, `4_3`, `4_7`, `4_12`, `5_2`, `5_5`, `5_6`, `5_9` and `ch_6`.
- All 30 internal fragment links in the AUM resolve to its own explicit anchors.
- No anchor is unresolved. The anchors are explicit ids, not ids derived from headings, so the changed headings do not affect them.

## 9. LOOP_INIT audit additions, per GC-9 (MW, 2026-10-04)

The source is `LOOP_INIT_MAPPING.md`, "Additions needed elsewhere", as decided by ruling GC-9. The drafted text was applied verbatim to `CHIRALITY_AGENT_USER_MANUAL_v3.md`.

| Item | Placement | Change |
|---|---|---|
| A1 | §13, "Index the run without duplicating its decisions", before the MEMORY table | Receipt content paragraph: a single central receipt at the location named by the method, as a derivative account. |
| A2 | End of §14, new subsection "Enter App v4 development", anchor `#app-v4` | App v4 entry and its separation from App development. The `[app-v4-loop]` link definition already existed and was reused, not duplicated. The README's AUM description now reads "across App, App v4, Piping, Runtime, and PEC". |
| A3 | §5 `#gate-60` | "reserves the 60% assessment" now reads "reserves each stage-gate assessment to the human". |
| A5 | §13, after "silence is no ruling." | Each decision is recorded with the human's exact words, source and custody, kept apart from the agent's interpretation, and implying no review the human did not perform. |
| Revision line | AUM header | Now also names §13 (receipt content and decision recording) and the App v4 entry in §14. |

A4 and A6 were not applied, as GC-9 directs.

**Checks.**
- All internal anchors in the AUM resolve, including `#app-v4`.
- Every reference-style link is defined.
- Code fences are balanced.
