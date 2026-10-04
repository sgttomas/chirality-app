# MR-MANUAL — independent review of the 60% gate manual revisions

**Reviewer:** MR, a Chirality Type 2 TASK dispatched by HELP_HUMAN. Model: Claude Opus 5.5 (`claude-opus-5-5`). I did not write any of the reviewed text. I used read-only git and no network. This file is the only thing I wrote.

**Candidate:** branch `claude/app-v4-graph-closure` at `a8d835ad7b`.

| File | sha256 (prefix) |
|---|---|
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Consolidated_v8.md` (new) | `e434d546e3a1…` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `f09bca8d2c49…` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `d5b215c6044c…` |
| v7, unchanged (checked) | `0aafefb12e9a…f095032` |
| Sources: `LESSONS_60PCT.md` / `OWNER_DECISIONS.md` / `GC_RULINGS.md` / `MANUAL_CHANGES.md` | `6b29584f4d11…` / `cefeef46fc17…` / `e375cabecebe…` / `05780483d444…` |

**Method.**
- Diffs: `git diff --no-index -U0` from v7 to v8, and `git diff a8d835ad7b~1 a8d835ad7b` for the field book and the Agent User Manual (AUM).
- Governing texts read: SPEC §5.3–§5.4; `docs/CYCLE_DRIVEN_RESOLUTION.md` (CDR, in full); `workflows/project-dag` (WORKFLOW.md, `resources/contract.md`, `resources/currency.md`, `resources/graph-version.md` SR-1–SR-7); `construct-local-work-graph` (WORKFLOW.md); `loop/LOOP_INIT.md`; Root `AGENTS.md`; `coordinated-knowledge-work` section headings and the cited passages.
- App v4 records checked directly:
  - `_DAG/DAG-004/DeliverableNodes.csv`: 41 rows.
  - `_DAG/DAG-004/CandidateEdges.csv`: 83 rows, all `SCC_UNRESOLVED`, across six `SCCRef`s and six `CaseRef`s.
  - `_DAG/DAG-00{1..4}/ACCEPTANCE_RECORD.md` and `GRAPH_BASIS.md`: dates and triggers.
  - `_Evaluation/DAGCurrency/_LATEST.md`.
  - `SURVEY/G2b.md` §4.1, and `DISPATCH.md` row G2b.
  - The WorkGraph `WORK_GRAPH.md`, which records the redirection and B0 as DROPPED.
  - `POSITION_60/POSITION_STATEMENT.md` §C.
- Link definitions and anchors checked with grep and `test -e`.

## Summary

Most of the revision is sound. The App v4 counts are right: 41 Deliverables, 83 held rows in six SCCs, groups A–E in the order A → {B, C} → D → E, and the one counter-order dependency. The owner quotes are exact. The AUM states the SPEC §5.4 departure path correctly and explicitly. The gate is presented throughout as the human's act. All link targets exist.

There are two MAJOR problems.
- **The planning merge.** The revision adds a "merge for planning purposes" under which an SCC counts as "resolved" for the gate while its rows stay held. That collides with the governing meanings of *merge* and *resolved*.
- **When a successor is needed.** v8 narrows the occasions for a successor DAG to a changed Deliverable set or group order. That understates SPEC §5.4. It also contradicts App v4's own record: three successors were accepted during its 60% phase, and each one only added arcs.

Neither problem blocks drafting, but both need repair before v8 is relied on.

## Findings

### MAJOR-1: "Merge for planning purposes" and "resolved for the gate" redefine governed terms

**Evidence.**
- What the governing texts say:
  - CDR §2 rule 3: "**Merge** the cluster and accept it as one indivisible unit."
  - CDR §2 rule 4: edges "stay non-gating until resolved".
  - CDR §4: cycles "live only in a non-gating candidate layer pending resolution".
  - project-dag `graph-version.md` SR-4: a merge ruling removes arcs "internal to a ruled merge group" as `MERGE_GROUP_INTERNAL`, citing the ruling. The merge group is recorded in `GRAPH_BASIS.md` with its combined inputs, responsibility and examination.
  - SPEC §5.4, Blockers table: "Edges the version holds as unresolved-cycle candidates stay non-gating".
- What the App v4 record shows:
  - All 83 rows in DAG-004 remain `SCC_UNRESOLVED`, each with an open `CaseRef`.
  - `WORK_GRAPH.md`: "B0 Merge page … DROPPED".
  - No merge ruling exists in any graph version.
- What the revised text says:
  - v8 §4.12: "This is a merge applied for planning and execution. Like any merge, it requires the human's decision. The Deliverables keep their identities … Their cycle-participating relationships remain held in the non-gating candidate layer … For the purpose of the gate, an SCC is resolved when its work has such a treatment: a recorded move, or a group whose combined undertaking the human has accepted."
  - v8 §3.11 (added): "Late in detailed development, a merge can be applied for planning and execution: co-designed Deliverables keep their identities and contracts while one undertaking develops them together."
  - AUM §5 `#gate-60`: "Grouping co-defined members into one undertaking is itself a merge for planning purposes, and the human rules on it."
  - AUM §8 (added) calls this "a merge for planning purposes". The sentence just before it, which is unchanged, says "**Merge** treats the coupled work as one indivisible unit".
  - Field book: "Co-designed groups taken as one undertaking by human decision (a merge)."

**Consequence.** The manuals bring in a third kind of treatment and give it the name of a doctrinal move. Under project-dag a merge is a recorded ruling that changes graph selection (SR-4) and so produces a successor version. The App v4 grouping did neither: the SCCs stay unresolved and held in DAG-004. A reader can now go wrong in two ways.
- **Record a merge ruling.** Under SR-4 that moves the 83 rows into exclusions as `MERGE_GROUP_INTERNAL`, closes cases and calls for a successor.
- **Treat the SCCs as resolved.** Rule 4 releases an edge from non-gating status once its SCC is resolved, so held rows could then be read as gating.

v8 guards against the second error in one sentence, but the terms themselves still conflict. This is the kind of quiet amendment of governing texts that the manuals must avoid.

**Proposed fix.** Rename the treatment and say what it does and does not do.
- Call it "grouping for development", or "a grouped undertaking".
- State that it is a planning arrangement that the human accepts, typically with the gate.
- State that it is not a merge ruling under CDR §2 rule 3 or project-dag SR-4. The SCCs remain unresolved in the DAG's terms, with their rows held as `SCC_UNRESOLVED` and their cases open, and the group's work graph orders the parts.
- Say that if the human wants a recorded merge, that follows the merge rules and produces a successor.
- Keep the owner's word "resolved" only as the owner's criterion, read as "each SCC has a treatment under which its work can proceed". v8 already says this in its opening paragraph. Drop "an SCC is resolved when…".
- Apply the same wording in v8 §3.11 and §4.12, the field book DISCERN list, and AUM §5 and §8.

### MAJOR-2: v8 narrows when a successor DAG is warranted, contrary to SPEC §5.4 and App v4's own record

**Evidence: the governing rule.**
- SPEC §5.4: a local file departs "when its evidence adds an edge, removes an edge, or creates a cycle". The departure is flagged stale, a candidate is prepared, and "The human accepts it or rejects the change."
- `currency.md`: a `DEPARTURE` includes "an SCC formed, changed, or dissolved". It also says "Several departures may be decided in one successor."

**Evidence: App v4's own record.** App v4's 30% gate was DAG-001 (2026-09-28). During 60% three successors followed, and each came from a scope amendment, a register update and a currency `DEPARTURE` in which "SCCs and inventory [were] unchanged":
- DAG-002 (2026-09-29): SCA-V4-001, 37 arcs added;
- DAG-003 (2026-09-29): SCA-V4-002, 4 arcs added;
- DAG-004 (2026-10-03): SCA-V4-003, 10 arcs added, 5 of them held.

None changed the Deliverable set. G2b §4.1 lists 62 dependencies that no DAG-004 arc carries, 23 of them SCC-forming under at least one option. When those are registered, they are departures by definition.

**Evidence: the v8 sentences that narrow the rule.**
- §1.7 (C1): "Findings during 60% can warrant successor versions of the project DAG when they change its structure: the Deliverables it contains, or the order in which groups of them can be completed."
- §3.12 (C2) and the chapter 4 introduction (C3): "commonly" becomes "can".
- §4.7 (added): "A finding about how two closely coupled Deliverables refer to each other usually is not; the local work graph and the change control on their agreed contracts can carry it."
- §4.12, after the level table: "A finding of the other kinds changes the work within it; such findings are expected throughout the 90% phase and are no reason to withhold the transition." The "other kinds" include the register-update row.
- §4.12, App v4 paragraph: "The same project then passed the gate on the DAG accepted before that attempt began. No successor was needed."

**Evidence: the passages that are correct.**
- v8 §4.12, the "Registers updated…" paragraph: "The project's adopted rules govern how a departure from the accepted graph is treated, including any candidate successor and the human's decision on it."
- The field book: "Successor DAG only on a structural event or as the adopted departure rules require."
- The AUM, step 4 (quoted under ruling 1).

**Consequence.**
- **v8 is inconsistent with itself and with SPEC §5.4.** A reader of §1.7 or §4.7 alone would conclude that a newly registered dependency inside a group needs no departure decision.
- **C1–C3 remove an accurate statement.** "Commonly" was true of App v4's 60% phase. The sources cited for the change, L§1 and L§2, concern graph closure at detail level, not how often successors occur.
- **The trigger has been redefined.** LESSONS' "structural event" is CDR §4's trigger: "a decomposition revision / scope change (SCA)". The manuals turned it into "a changed Deliverable set or group order".
- **The 90% phase is understated.** This is the over-correction the brief asked about: the manuals now understate that successors will still be needed during 90%, App v4's included.

**Proposed fix.**
1. **§1.7, §3.12 and the chapter 4 introduction.** Restore "commonly", or cite the App v4 rate. Separate two things:
   - a *structural change*, meaning the Deliverable set or the group order, which bears on the gate;
   - a *departure* under the project's adopted rules, such as an added or removed production relationship or a changed SCC. A departure still needs the human's decision on a candidate successor, even within a group, but it does not by itself reopen the gate.
2. **§4.7 (added paragraph).** Append: "If the finding adds or removes a production relationship that the accepted graph does not represent, the project's departure rules still apply."
3. **§4.12 table follow-up.** Rephrase: "…changes the work within it. Some still require a decision under the project's departure rules. None is a reason to withhold the transition unless it crosses the group order or closes a cycle between groups."
4. **"No successor was needed."** Change to "No successor was needed to pass the gate; the dependencies found in the designs are carried through the departure rules as the loops register them."
5. **Describe the proportionate path once, in the §4.12 handoff paragraph.**
   - Batch the register updates for each scope amendment.
   - Run one currency audit.
   - Prepare one small successor whose checkpoints are decided together. App v4's DAG-002 to DAG-004 are the worked example, and `currency.md` permits this.
6. **AUM step 4.** Add that a ScopeOfWork change goes through the project's scope-amendment route, as App v4's SCAs did, before `dependency-extract` and the currency audit. Add the batching sentence.

### MINOR-1: The field book DISCERN list asks for open structural matters to be "settled", which App v4 did not do

**Evidence.**
- The field book says: "any that could add or remove a Deliverable or reverse the group order is settled."
- v8 says only that such matters "bear on the gate".
- `POSITION_STATEMENT.md` §C records that the SWBPIPE host joins could still bring structural changes (AC-004 of DEL-03-01, placement OI-013/014, OI-021 and receipts). The gate passed with these as contained residual risks.

**Consequence.** The checklist is stricter than both the source and v8.

**Fix.** Use: "…is settled, contained as a residual risk with an owner, or accepted by the human as a stated qualification."

### MINOR-2: The field book drops the "identified join" clause from check 4

**Evidence.**
- The field book says: "each residual risk contained, with an owner."
- v8 check 4 says: "within a group, or at an identified join that follows the group order".
- The AUM says: "the group or identified join".

**Consequence.** The checklist does not match the method it summarises, and would have failed App v4's SWBPIPE case.

**Fix.** Use: "each residual risk contained in a group or at an identified join that follows the group order, with an owner."

### MINOR-3: The field book places the grouping decision before the gate

**Evidence.**
- The field book lists, under DISCERN: "[ ] Co-designed groups taken as one undertaking by human decision (a merge)."
- In App v4 the only explicit grouping approval was for the contract core: the owner's "Yes you can take this approach…". For groups B–E, the human decision is the gate acceptance itself, given on an assessment that named the groups. The B0 merge page was dropped.

**Consequence.** The checklist implies a separate decision made earlier. App v4 had none for B–E.

**Fix.** Use: "Groupings proposed for the human's decision, which may be given with the gate." See also MAJOR-1 on the word "merge".

### MINOR-4: A field book reference points to the sentence that v8 corrects

**Evidence.** Field book line 80: "Reference: [Manual §1.7](…v7.md#ch_1_7); for the 60% gate, [Manual v8 §4.12](…)". v7 §1.7 still says "Findings during 60% commonly warrant successor versions…", the sentence corrected as C1. The new subsection directly above that reference line takes the other view.

**Consequence.** One line sends the reader to two editions that disagree on the same point.

**Fix.** Either point this one reference at v8 §1.7, or wait until the edition decision (ruling 4) and leave the line as it was before this change.

### MINOR-5: Two pinned manuals were edited in place without a revision mark

**Evidence.**
- The AUM header still reads "Version 3 · 22 September 2026 · repository source basis `b3e2ce4…`" and "companion to version 7". The new body cites 2026-10-04 records and v8.
- The field book has no edition line.
- `LOOP_INIT.md` pins both files by name, and v7 by name with section numbers (PM Manual §§1.7, 3.12, chapter 4).
- The PM manual became a new edition, v8, but the other two changed in place.

**Consequence.** App v4's adopted guidance basis changes silently when this lands, and readers cannot tell which text they were given.

**Fix.**
- Add a dated revision line to the AUM header (for example, "revised 4 October 2026: 60% gate guidance") and update the renderer basis date when the HTML is regenerated.
- Do the same for the field book's metadata.
- Notify the App v4 loop of the change, following the notice practice in Root AGENTS.md. Alternatively, issue new editions of both.

### MINOR-6: GC-5 is stated as general practice without its edge-semantics premise

**Evidence.**
- GC-5 rests on DAG-004's part-level edge semantics. Its sources include "DAG-004 edge semantics".
- CDR §2 rule 1 makes every edge relative to an objective and to edge semantics.
- v8 §4.12 states the rule without qualification: "A design's use of another Deliverable's content is a dependency when the consumer needs that content to define or produce its own part…".
- The AUM "Rulings worth carrying" does the same.

**Fix.** Qualify it: "under edge semantics such as App v4's (the consumer requires the supplier's contribution before the stated part of its work)".

### MINOR-7: §4.12 reordering moves the phase-names paragraph and Figure 4.10 under the wrong subsection

**Evidence.** In v7 these sit under "Examine what could still change the route". In v8 they come after the App v4 acceptance quote, inside "Prepare the assessment and obtain the decision".

**Consequence.** The general paragraph on organisational phase names now interrupts the account of obtaining the decision.

**Fix.** Move "Prepare the assessment and obtain the decision" so that it follows the figure. Alternatively, move the phase-names paragraph and the figure back to the end of "Examine…".

### MINOR-8: The method relies on a "group order", but neither the manuals nor App v4 say where the groups are recorded

**Evidence.**
- v8 and the AUM say each loop builds its work graph "from the DAG's group order". The DAG does not record groups.
- In App v4 the group membership is held only in the session transcript, which `OWNER_DECISIONS.md` names as custody. No committed file lists the members of groups B–E. LESSONS gives only A's count.
- v8 asks for a record of "how the groups are to be taken up", but not of the groups themselves.

**Consequence.** Loops cannot reproduce or check the basis they are told to build from.

**Fix.**
- Change "the DAG's group order" to "the group order accepted at the gate".
- Add to "Record the effect of the decision": "the groups, their members, the order between them and the result of the grouping test".
- Separately for HELP_HUMAN, not as a manual fix: App v4 should commit its A–E membership before the loops fan out.

### MINOR-9: The AUM paraphrase strengthens the owner's criterion

**Evidence.** The owner said "without many or any conflicting outcomes". The AUM `#gate-60` says "without conflicting outcomes".

**Fix.** Use "with few or no conflicting outcomes".

### MINOR-10: The App v4 residual-risk sentence is vague where the sources are specific, and the sources disagree

**Evidence.**
- v8: "Each was placed with identified groups".
- LESSONS §3: "SWBPIPE host joins: A and D"; placement: A; the policy deliverable: A.
- `OWNER_DECISIONS.md` gives HELP_HUMAN's assessment as "Residual risks are contained within single groups", which conflicts with LESSONS.

**Fix.** In v8, write: "the host-side joins touched the core and the fleet group, which lie in group order. The placement question and the policy Deliverable's reach lay within the core. The unregistered dependencies became register updates." Report the disagreement between the sources to HELP_HUMAN; it is noted under ruling 2.

### MINOR-11: The general reference now carries dense repository-specific figures

**Evidence.**
- v7 keeps "the general management explanations in this manual and the detailed repository procedures in the companion user manual" (v7 l.20). Its examples are constructed.
- v8 adds survey figures such as "10,584 cross-Deliverable uses on 536 pairs".

**Consequence.** These figures sit awkwardly in a measured general reference. The owner quotes and the 41/83/six/five-group outline do earn their place.

**Fix.** Keep the outline and the quotes. Reduce the survey figures to "each survey found more coupling (83 held rows, then 30, then 62 unregistered dependencies)", or move the detail to the AUM.

### NOTE-1: "towards" against the book's "toward"

v7 uses "toward" 24 times and "towards" never. v8 introduces "towards" twice, in §4.12 and §4.12 "Recognise…". Use "toward" for consistency.

### NOTE-2: Who recorded the owner's words

v8 says the owner "received the grouping assessment, and recorded: 'I am accepting…'". The owner wrote the words, and HELP_HUMAN recorded them. Use "and replied".

### NOTE-3: Duplication

The structure-versus-detail distinction is now stated in §1.7 (two paragraphs), §3.12, the chapter 4 introduction, §4.7, §4.12 (twice, plus the table) and the Figure 4.10 caption. That is tolerable in a reference work. The second paragraph of §1.7 and the §4.7 paragraph could each be reduced to one sentence and a pointer.

### NOTE-4: Generated editions and README

- The AUM and field book HTML files are now stale.
- README "Current editions" lists v7 with its Word and PDF files. The README asks that a later management-manual revision carry Word and PDF regeneration.

This belongs to the publication step (ruling 4), not to this change.

### NOTE-5: Anchors

- `#gate-60` is defined once (AUM l.201), and both internal references resolve to it.
- `v8#ch_4_12` exists (v8 l.2314). `v8#ch_1_7` exists.
- The new AUM link definitions resolve to existing files: `human-manual-v8`, `ckw`, `app-v4-loop` and `app-v4-gc-rulings`. So do the reused ones: `spec`, `project-dag`, `scope-change`, `scc-case`, `cycles`, `dependency-extract` and `construct-graph`.
- The coordinated-knowledge-work citations §1, §2 and §4 match those sections.
- I found no broken anchor.

### NOTE-6: Faithful content

- The AUM summaries of GC-1, GC-3, GC-5 and GC-6 are faithful.
- The skeleton description matches `WORK_GRAPH.md`: four steps, measured as code under automated tests, with contract issues logged with file and section.
- The pre-move SCC range of 16–26 matches the G2b row in `DISPATCH.md`.

## Rulings on the four flagged uncertainties

**1. SPEC §5.4 and "successor only on a structural event".** The required path is: a ScopeOfWork or register update under a scope amendment, then a currency audit, then a `DEPARTURE` with the affected deliverables `DAG pending`, then a candidate successor that the human accepts or rejects. Batching is allowed: "Several departures may be decided in one successor."

- **The AUM states this correctly**, in step 4: "A row that adds or removes an edge, or creates a cycle, is a departure under SPEC §5.4: the affected deliverables are DAG pending until the human accepts a candidate version or rejects the change. A further row on an edge the version already represents leaves it current. Otherwise successors are event-driven, under the doctrine's §4." It should add batching and the scope-amendment step.
- **The field book is acceptable:** "Successor DAG only on a structural event or as the adopted departure rules require."
- **v8 is inconsistent.** Its handoff paragraph defers correctly ("The project's adopted rules govern how a departure from the accepted graph is treated…"). But four passages imply that registering rows inside a group is free of the departure rule:
  - §1.7, "when they change its structure: the Deliverables it contains, or the order…";
  - §4.7, "usually is not; the local work graph and the change control … can carry it";
  - §4.12, "A finding of the other kinds changes the work within it…";
  - §4.12, "No successor was needed."

  This requires repair under MAJOR-2.
- **On LESSONS.** Its "structural event" is CDR §4's trigger, a decomposition revision or SCA, not "a changed Deliverable set or group order".

**2. Check 4 wording.** **Confirmed, with conditions.** "Within a group, or at an identified join that follows the group order" fits App v4: the SWBPIPE host joins touch A and D, and A precedes D. Three conditions apply:
- the field book must carry the same clause (MINOR-2);
- the v8 worked example should say so plainly (MINOR-10);
- HELP_HUMAN should note that `OWNER_DECISIONS.md` describes all residual risks as "contained within single groups", which disagrees with LESSONS §3.

**3. The merge record.** **Honest as to App v4, but the framing needs repair.** No manual claims that a separate merge record exists. Three problems remain:
- calling the grouping a "merge" conflicts with CDR §2 rule 3 and project-dag SR-4 (MAJOR-1);
- the field book checklist implies a decision before the gate, which App v4 did not have for B–E (MINOR-3);
- the group membership itself is unrecorded (MINOR-8).

The accurate statement is this. The core grouping was approved explicitly with change control. Groups B–E were accepted through the gate acceptance, on an assessment that named them. No merge ruling was recorded in any graph version, and the SCCs remain held.

**4. Repointing links to v8.** **This is a separate decision and should not be part of this change.** Making v8 the current edition requires four things:
- review and acceptance of v8;
- an update to README "Current editions", with the Word and PDF regeneration the README requires;
- repointing about 11 field book references, the AUM header ("companion to version 7") and the AUM `[human-manual]` link;
- a change to App v4's `LOOP_INIT.md`, which pins v7 by file and by section numbers. That change is the loop's own adoption decision, made on notice.

There is one exception within this change. The field book reference that sends readers to v7 §1.7, beside the new gate subsection, should be repointed or reverted (MINOR-4). Separately, MINOR-5 asks for in-place edits to the pinned AUM and field book to be marked and notified.

## Verdict

**REPAIR.**

| Severity | Count |
|---|---|
| BLOCKING | 0 |
| MAJOR | 2 |
| MINOR | 11 |
| NOTE | 6 |

Both MAJOR repairs are wording changes in v8, with matching edits in the field book and AUM. They need no new sources. Once MAJOR-1 and MAJOR-2 are repaired, the manuals will be consistent with the governing texts and faithful to the App v4 record. The MINOR items are recommended in the same pass.

---

## Addendum A: confirmation of repairs (2026-10-04)

**Reviewer:** MR, the same Claude Opus 5.5 instance (`claude-opus-5-5`). I used read-only git and no network, and I edited only this file.

**Candidate:** `db25aa3256`, on the same branch. The diffs I checked are `a8d835ad7b..HEAD` for the three manuals and `OWNER_DECISIONS.md`, and `b935a016a6..HEAD` for this review file, which was unchanged until I appended this addendum.

| File | sha256 (prefix) |
|---|---|
| v8 | `ebae260fd5ac…` |
| Field book | `60634b937881…` |
| AUM | `858e1a822eeb…` |
| `OWNER_DECISIONS.md` | `21c781f92244…` |
| v7, still unchanged | `0aafefb12e9a…` |

The map I checked against is `MANUAL_CHANGES.md` §5.

### MAJOR-1 ("grouping for development"): repaired

- **v8 §4.12, SCC paragraph.** It now names **grouping for development** and says the human accepts it, "typically together with the gate". It also says the grouping "is not a merge ruling under the cycle-resolution doctrine, and it does not resolve the component in the graph's terms". Held rows stay non-gating, "their resolution cases remain open", and "a recorded merge, cut, or other move … follows the doctrine's rules and produces a successor graph". The gate asks for "an accepted treatment … not that every SCC be resolved". "An SCC is resolved when…" has been removed.
- **v8 §3.11.** It now contrasts a merge with grouping, "which leaves the cycle unresolved in the graph".
- **v8 §4.7.** "…while the component remains unresolved in the graph".
- **v8 Figure 4.10.** "their relationships still held and their cases open".
- **Field book.** DISCERN reads "Grouping is not a merge ruling: SCC rows stay held and their cases stay open", and §4 reads "Grouping co-designed members for development is not a merge".
- **AUM.** `#gate-60` names CDR §2 rule 3, project-dag selection and `SCC_UNRESOLVED`, and §8 reads "leaves the SCC held and is not a merge ruling".
- **Leftover terms.** A grep for "planning purposes", "for planning" and "an SCC is resolved" finds no remaining use in the 60% guidance. The two hits at v8 l.456 and l.616 are unrelated text that was already there.
- **Consistency.** The repaired text is now consistent with CDR §2 rules 3–4, project-dag SR-4 and SR-7, and the SPEC §5.4 blockers row. It also describes App v4 truly: DAG-004 holds 83 rows as `SCC_UNRESOLVED` with open cases, and B0 was dropped.

### MAJOR-2 (SPEC §5.4 path): repaired in all four quoted passages and the related ones

1. **§1.7.** "commonly" is restored. The passage now reads: "An added or removed production relationship, or a changed cycle, is a departure from the accepted graph; the human decides it under the project's adopted rules, and several departures can be decided together in one successor. Keep that distinct from a structural change…". The second paragraph adds: "Departures in finer relationships continue to arrive and are decided as before."
2. **§4.7.** "…usually is not, although a relationship it adds or removes is still a departure under the project's rules."
3. **§4.12, after the level table.** This now uses my proposed wording exactly: "Some still require a decision under the project's departure rules. None is a reason to withhold the transition unless it crosses the group order or closes a cycle between groups."
4. **§4.12, App v4 example.** "No successor was needed to pass the gate; the dependencies found in the designs are carried through the departure rules as the loops register them."

Related passages:
- §3.12 reads "commonly … several successor DAGs".
- The chapter 4 introduction reads "are common".
- The structural-change paragraph in §4.12 and the chapter 5 introduction now carry the departure statement.
- The §4.12 handoff paragraph sets out the proportionate path: batch per scope amendment, examine currency once, and prepare one small successor.

I checked the App v4 claim in the handoff paragraph against the records. It says three successors were accepted "during its 60% phase, each adding relationships without changing the Deliverable set". The `GRAPH_BASIS.md` files of DAG-002, DAG-003 and DAG-004 record 37, 4 and 10 added arcs, with inventory unchanged, after DAG-001 completed 30% on 2026-09-28.

AUM step 4 now puts the scope-amendment route first, then `dependency-extract` and the currency audit, and adds batching with the DAG-002 to DAG-004 example. The field book handoff block and §5 step 2 now state the departure rule, with batching.

Ruling 1 is therefore satisfied. All three manuals now say that registering a row inside a group can be a departure for the human to decide. None implies that registering rows is free of that rule.

### MINOR and NOTE items

| Item | Status | Evidence |
|---|---|---|
| MINOR-1 | Repaired | Field book DISCERN: "…is settled, contained as a residual risk with an owner, or accepted by the human as a stated qualification." |
| MINOR-2 | Repaired | Field book check 4 now carries the "identified join that follows the group order" clause. |
| MINOR-3 | Repaired | Field book: "Groups and members recorded; grouping for development proposed for the human's decision, which may be given with the gate." |
| MINOR-4 | Repaired | The field book's §1 references now point to v8 `#ch_1_7` and `#ch_4_12`; both anchors exist (v8 l.240 and l.2314). The other v7 links are left for the edition decision, as ruling 4 advised. |
| MINOR-5 | Repaired | Both manuals now carry a dated revision line. The AUM's line names §5 and §8 and says the rest of its basis is unchanged. The notice to the App v4 loop is still listed for HELP_HUMAN. |
| MINOR-6 | Repaired | The edge-semantics premise is added in the v8 handoff and in the AUM's ruling summary. |
| MINOR-7 | Repaired | Order in §4.12: "Examine…", then the phase-names paragraph (l.2387), then Figure 4.10 (l.2423), then "Prepare the assessment…" (l.2425), then "Hand the work into 90%". |
| MINOR-8 | Repaired | Every manual now says "the group order accepted at the gate". Groups and their members are in the assessment, in the decision record (v8 and the AUM), in Figure 4.10 and in the field book DISCERN list. Committing App v4's own A–E membership remains with HELP_HUMAN. |
| MINOR-9 | Repaired | The AUM now reads "with few or no conflicting outcomes". |
| MINOR-10 | Repaired | The v8 example now says the host joins touched the core and the fleet group, in group order, and that the other two risks lay within the core. |
| MINOR-11 | Repaired | The 10,584/536 figures and the 16–26 range are removed. The outline and the quotes are kept. |
| NOTE-1 | Repaired | No "towards" remains in the new text. The only remaining instance is the title of the Polanyi entry in the bibliography. |
| NOTE-2 | Repaired | "replied". |
| NOTE-3 | Repaired | §1.7 and §4.7 are shortened to a pointer. |
| NOTE-4 | Open, as intended | Rendering and the README belong to the publication step. |
| NOTE-5, NOTE-6 | No change needed | Anchors rechecked for the new links. |

**`OWNER_DECISIONS.md` correction.** It is appended below the existing entries and leaves the owner's quoted words unchanged. It places the SWBPIPE joins at A and D, in group order, and placement OI-013/014 and DEL-04-01 within A, which matches LESSONS §3 and ruling 2. It is labelled as HELP_HUMAN's correction, not as an owner statement.

**Residual note (R-1, NOTE, not a condition).** The opening paragraph of v8 §4.12 still reads the owner's "resolved" as "a treatment under which each SCC's work can proceed". The repaired SCC paragraph says "accepted treatment". Changing "a treatment" to "an accepted treatment" would make the two consistent. The current wording is not wrong.

### Verdict

**READY.** Both MAJOR findings and all eleven MINOR findings are repaired, and no new defect was found. The rendering and Word/PDF production may proceed.

This verdict covers the content of the guidance only. Making v8 the current edition is still a separate decision, as ruling 4 said: that means README "Current editions", the remaining v7 links and App v4's `LOOP_INIT` pin. Three items remain with HELP_HUMAN:
- commit App v4's A–E group membership;
- send the notice to the App v4 loop;
- make the edition decision.

---

## Addendum B: recheck after the owner's direction on structure versus detail (GC-7)

**Reviewer:** MR, the same instance (Claude Opus 5.5, `claude-opus-5-5`). I used read-only git and no network, and I edited only this file.

**Candidate:** `0c45aba0e9`. I checked the diff `db25aa3256..HEAD` for the three manuals against:
- `OWNER_DECISIONS.md`, section "Structure versus detail after 60%";
- `GC_RULINGS.md` GC-7;
- `GROUPS.md`;
- `MANUAL_CHANGES.md` §6.

| File | sha256 (prefix) |
|---|---|
| v8 | `d0de0b1ec4da…` |
| Field book | `9adac4b575f0…` |
| AUM | `30d6ec602b13…` |
| `GC_RULINGS.md` | `058cf8c8b027…` |
| `GROUPS.md` | `7d3bfb79ae4f…` |
| `OWNER_DECISIONS.md` | `7b04069a49e8…` |
| v7, still unchanged | `0aafefb12e9a…` |

### 1. Faithful to GC-7 and the owner's words: yes

**Recording.** All three manuals carry GC-7 items 2 and 3 in the same form. A found relationship is recorded "where those who depend on it will see it":
- within a group, in the group's work graph;
- across groups, in a shared list that every loop reads.

Registers and Scope of Work are updated "when their wording would otherwise mislead". These updates are decided by the human "in batches at natural boundaries" under the departure rules. The places are v8 §4.12 (handoff and level table), AUM step 4, and the field book's handoff block and §5 step 2.

**The in-the-moment triggers** match GC-7 item 4 in all three manuals, and "In doubt, ask" is kept. The triggers are:
- a relationship that seems to run against the group order;
- a cycle across groups;
- a change to the Deliverable set;
- a change that would make another group's finished work wrong;
- any sign that the grouping is wrong.

**Lightness and stated limits.** No tiers, names or thresholds are introduced. Each manual says the guidance comes from one project and sets no thresholds:
- v8: "This guidance comes from one project's experience. It sets no thresholds or fixed tiers, and leaves judgment to the moment."
- AUM: "(App v4 ruling GC-7); it sets no thresholds or fixed tiers".
- Field book: "(From one project's experience; no thresholds.)"

This fits the owner's "better to leave some things underdefined and seek human judgment in the moment".

**Superseded GC-5 item 3.** The AUM's ruling summary now states it historically, accurately: "App v4 first required … its later ruling GC-7 relaxed that…".

### 2. Consistency with SPEC §5.4: yes

The departure rule still applies once a change reaches the registers:
- v8 §4.12: "When such changes reach the dependency registers, the project's departure rules apply, and the human can decide them in batches."
- AUM step 4 keeps the explicit statement: "SPEC §5.4 still governs the registers: a row that adds or removes an edge, or creates a cycle, is a departure, and the affected deliverables are DAG pending…". It also keeps the batching example.
- Field book §5 step 2: "as the adopted departure rules require when the dependency records change".

No passage says the registers may knowingly stay misleading. The rule for updating them is stated as the opposite: update them when wording would otherwise mislead. The earlier MAJOR-2 repair still holds in substance:
- "commonly" is retained in §1.7, §3.12 and the chapter 4 introduction;
- §1.7 keeps "several can be decided together in one successor";
- §4.12 keeps "None is a reason to withhold the transition unless it crosses the group order or closes a cycle between groups".

The sentences that called every finer edge a departure have been removed. That removal follows GC-7 and does not narrow SPEC §5.4. SPEC acts on the local files, and GC-7 governs when a found relationship is put into them.

### 3. No new obscuring: one gap to close (MINOR-B1)

**MINOR-B1: say that DAG-derived readiness does not cover relationships held outside the registers.**

**Evidence.**
- Under SPEC §5.4, blockers come "from the accepted current version's edges".
- `construct-local-work-graph` reads readiness from the DAG and the dependency records.
- Under GC-7, a known relationship may now live only in a group's work graph or in the cross-group list.

So a ready or blocked verdict computed from the DAG will not reflect such a relationship. A cross-group one in group order is the likely case: a D deliverable reported ready while the A input it needs, recorded only in the list, has not been produced. The unchanged AUM §8 sentence warns of exactly this: "An omitted dependency can make the topology look cleaner while making execution less reliable" (AUM l.337). App v4 runs in `FULL_GRAPH` mode, and DAG-004's `GRAPH_BASIS.md` declares "Completeness FULL for the selected semantics". That completeness claim is now qualified by the relationships held outside the registers.

**Consequence.** A readiness claim made from the DAG alone could be unsupported. This is the risk the owner asked about. The texts do make the list visible to every loop, but they do not say that readiness must consult it.

**Proposed fix.** Add one sentence to the v8 handoff paragraph and to AUM step 4, and optionally to the field book: "A ready or blocked verdict from the project DAG does not cover relationships recorded only in a work graph or the shared list; read those before declaring work ready." For App v4 (HELP_HUMAN, close-out), qualify DAG-004's FULL completeness claim in the handoff, pointing to the shared list. This is a MINOR item and not a condition of the verdict. It is a one-sentence change and is worth making before rendering.

**Clarity of the triggers.** They are stated identically in the three manuals and in GC-7.

### 4. Consistency and anchors: intact

- The unchanged §3.12 text ("Each departure is decided as the project's rules require…") and the §4.7 renewal paragraphs remain compatible with the revised text.
- §4.7 now reads "Distinguish detail from structural change … record it where those who depend on it will see it, as §4.12 describes". It is consistent with §4.12.
- The new AUM link `[app-v4-groups]` resolves to the committed `GROUPS.md`. The AUM points at `CROSS_GROUP_RELATIONSHIPS.md` only by name, through GROUPS.md, which is appropriate while the file does not exist.
- The field book fence count is balanced at 4, and the new "ASK THE HUMAN AT ONCE" block lies inside the fenced block.
- No other link or anchor changed.
- The revision lines in the AUM (§5, §8) and the field book (§§1, 4, 5) still describe the edited sections correctly.

### Notes for HELP_HUMAN (records, not manual text)

- **N-B1.** `GROUPS.md` gives the in-the-moment triggers more narrowly than GC-7. It omits "suggests the grouping is wrong", and it says "makes finished work wrong" where GC-7 says another group's finished work. Align it with GC-7.
- **N-B2.** `GROUPS.md` places `CROSS_GROUP_RELATIONSHIPS.md` "in the handoff location". Name the exact path when the list is created in the close-out, and seed it from the sorted G2b items, so that the v8 sentence "the dependencies found in the designs are recorded for the loops that need them" is true when the loops start.
- **N-B3.** An uncommitted `SURVEY/GROUP_SORT.md` (RVG, untracked in this worktree) reports two things:
  - a second cross-group arc, DEP-09-01-027 (DEL-09-10 in C consumes DEL-09-01 in B), which orders C after B;
  - a possible move of DEL-09-10 to group D.

  I did not review that file. If the grouping changes, recheck the App v4 example in v8 §4.12 ("core → {packaging, connectors} → fleet → practice") and GROUPS.md.

### Verdict

**READY.** The revision is faithful to GC-7 and the owner's direction. It is light and states its limits. It stays consistent with SPEC §5.4, and it introduces no contradiction or broken anchor.

| Severity | Count |
|---|---|
| BLOCKING | 0 |
| MAJOR | 0 |
| MINOR | 1 (MINOR-B1, a one-sentence readiness caveat, recommended before rendering) |
| NOTE | 3 (N-B1 to N-B3, for HELP_HUMAN's records) |

---

## Addendum C: manual changes after Addendum B (GC-8, current edition, AUM additions)

**Reviewer:** MR, the same instance (Claude Opus 5.5, `claude-opus-5-5`). I used read-only git and no network.

**Candidate:** the local commit `1e930cb16e`, under the owner's merge hold. I checked `git diff a61372eb4c 1e930cb16e -- docs/alignment-manual` against GC-8, GC-9, `MANUAL_CHANGES.md` §8–9 and the owner's directions from "How LOOP_INIT steers agents…" onward.

| File | sha256 (prefix) |
|---|---|
| AUM | `2671c22edb8a…` |
| Field book | `fe1136c5bf51…` |
| v8 | `aec310aba8f1…` |
| README | `ab70ed20c865…` |

The companion review of the LOOP_INIT drafts is `reviews/MR-LOOPINIT.md`.

### Checks

**GC-8 wording: accurate.** v8 §4.12 (the level table and the handoff paragraph), AUM §5 step 4, and the Field Book (HAND OFF block and §5 step 2) now say three things:
- a cross-group relationship is recorded in each affected loop's work graph;
- where the other group has no graph yet, it is recorded in the finding loop's graph and carried over;
- no new standing list is created.

The readiness caveat is kept. No text still mentions the shared list or `CROSS_GROUP_RELATIONSHIPS.md`.

**Current edition and links: correct.**
- README "Current editions" names v8, and v7 is first in the Archive table, with targets that exist.
- The Field Book has 18 links to v8 and none to v7.
- The AUM's `[human-manual]` points to v8; `[human-manual-v8]` is removed and its three uses are rewritten.
- The header now reads "the current edition".

**Edition pinning: none unwanted.** Edition numbers survive only in file names, which links must use, and in history: "since version 7" and the kept anchor `#v7-adoption`. A repository-wide grep finds the remaining references to `Consolidated_v7` outside the alignment-manual sources only in dated records. Those are App v4's definition-run basis files, which are scoped historical records, and the governance tranche and decision records.

**Anchors: resolved.**
- All 31 internal fragment links in the AUM resolve, including `#app-v4` and `#gate-60`.
- Every reference-style link is defined, and every link-definition target exists.
- All Field Book fragment links into v8 resolve to explicit `<a id>` anchors.

**A1, the receipt content (§13): accurate.** It matches construct §3 on the location and bounded-reconciliation §5 on the PR-description use. It defines content and limits that were previously stated only in LOOP_INIT. It adds no time-sensitive state.

**A5, decision recording (§13): accurate and general.** "Imply no review the human did not perform" is consistent with Root AGENTS.md's "never imply personal owner review".

**A3, the gate sentence (§5): true only after the close-out.** "Reserves each stage-gate assessment" matches the proposed LOOP_INIT ("The owner assesses each stage gate."). The live LOOP_INIT, which `[app-v4-loop]` links to, still says only "The human assesses the 60% position". See MINOR-C3.

**A2, the App v4 entry (§14): it does not duplicate LOOP_INIT.** It routes to the init prompt and LOOP_INIT and separates App v4 from the App v3 material. It holds no phase, group or DAG state. It has one current-state clause (MINOR-C2). The proposed LOOP_INIT's App v3 line now conflicts with it (MR-LOOPINIT MINOR-L2), so the repair belongs on the LOOP_INIT side.

### Findings

**MINOR-C1: README links to v8 Word and PDF files that do not exist yet.**
- *Evidence:* a link check finds `Project_Management_for_Human_Agent_Teams_Consolidated_v8.docx` and `.pdf` missing. `MANUAL_CHANGES.md` §8 says HELP_HUMAN will produce them or remove the entries.
- *Fix:* produce them, or remove the two entries, before the change is merged.

**MINOR-C2: A2 states a current-state fact that will go stale.**
- *Evidence:* "App v4 has no project `AGENTS.md`." This becomes false if one is established.
- *Fix:* "Read a project `AGENTS.md` if App v4 establishes one; its `LOOP_INIT.md` binds it to…". Alternatively, drop the sentence, since AUM §2's entry already tells the agent to read a project AGENTS.md where one exists.

**MINOR-C3: Sequence A3 with the LOOP_INIT replacement.**
- *Evidence:* until the close-out replaces `loop/LOOP_INIT.md`, the AUM states something about the App v4 loop that the linked file does not yet say.
- *Fix:* land the AUM change and the LOOP_INIT replacement in the same PR. The merge hold makes this easy.

**MINOR-C4: The manuals do not say who carries a cross-group relationship into a graph built later.**
- *Evidence:* AUM step 4 says "record it in the finding loop's graph and carry it over when that graph is constructed". v8 says "carrying it into a group's graph when that graph is constructed". Neither says that the loop constructing the graph reads the other groups' graphs. The finding loop may have closed by then.
- *Fix:* add a clause to both: "the loop that constructs a group's graph reads the other groups' graphs for relationships recorded against it". This is the general counterpart of MR-LOOPINIT MAJOR-L1.

**NOTE-C1.** The HTML editions of the AUM and the Field Book are stale until they are rendered. The README's render commands carry the old `--basis-date` and `--basis-revision` values for both. Update them when you render.

### Verdict for part A

**READY**, with four MINOR items and one NOTE.
- MINOR-C1 must be closed before merge.
- MINOR-C4 is a one-clause change that should travel with MR-LOOPINIT MAJOR-L1.
- MINOR-C2 and MINOR-C3 can be fixed in the same pass.

Rendering and producing the Word and PDF files can proceed.
