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
