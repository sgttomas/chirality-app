# LOOP_INIT mapping: where each current rule belongs

Prepared by a Type 2 TASK (LI) for HELP_HUMAN, run
`APP-V4-GRAPH-CLOSURE-20261004`. This is analysis and proposal only. No
existing file was edited.

**Basis.** The owner's decisions in `OWNER_DECISIONS.md`, last two
sections: "How LOOP_INIT steers agents…" and "What LOOP_INIT is…". A
sentence stays in LOOP_INIT only if it is specific to App v4, is an
instruction, and is stated nowhere else.

**Subject.** `projects/chirality-app-v4/loop/LOOP_INIT.md` as committed at
HEAD `3a7fd0ef76`: 253 lines, 15,570 characters. Line numbers below refer to
that file. The draft is in `LOOP_INIT_PROPOSED.md`, and the init prompt in
`DEV_LOOP_INIT_PROMPT_PROPOSED.md`.

**Method.** Each quotation below was checked verbatim with `grep -F`, after
joining wrapped lines, against the working tree at the time of writing.
That working tree carries another agent's uncommitted GC-8 edits to the
Agent User Manual (AUM), the Field Book (FB) and Consolidated v8. None of
the sentences quoted here comes from those edits.

**Classes.**
- **(a)** Carried elsewhere. The row gives the destination and a quote.
- **(b)** Project-specific; it stays as a single line. The row names the
  draft section.
- **(c)** Load-bearing and general, and found nowhere else. The row gives
  the proposed home and draft text.
- **(d)** Obsolete or superseded. The row gives the reason.

"construct" means `workflows/construct-local-work-graph/WORKFLOW.md`, and
"ckw" means `workflows/coordinated-knowledge-work/WORKFLOW.md`.

## Mapping table

| # | Current text (lines) | Class | Destination, quote, or reason |
|---|---|---|---|
| 1 | Resolve `REPO_ROOT`; set `WORKING_ROOT`; paths are relative (3–4) | b | Kept in the draft's opening, with the same convention. |
| 2 | "Enter through `init/dev-loop-init-prompt.md` with the selected role and the human's steering." (5–6) | a | The init prompt itself is the entry. AUM §2: "Establish the project and active role, read the applicable entry instructions, and recover the current undertaking before creating replacement work." |
| 3 | "This file owns the recurring development-loop procedure" (6) | d | Superseded by the owner's accepted reading: LOOP_INIT binds the project to the general layers. The procedure now lives in the workflows and manuals. |
| 4 | Root `AGENTS.md`, the active role and the accepted basis supply responsibilities and boundaries (7–8) | a | AGENTS.md: "Ordinary selective context consists of this Root `AGENTS.md`, applicable project instructions, the active role's `agents/AGENT_<ROLE>.md`, and available skill names and descriptions." The draft's opening names these layers in one clause. |
| 5 | "Read project `AGENTS.md` if one is subsequently established" (8–9) | a | AUM §2. Its orientation block lists `cat "$WORKING_ROOT/AGENTS.md"`, and the section says "read the applicable entry instructions". |
| 6 | "do not substitute another project's instructions" (9) | a + b | AUM §1: "Do not export one project's newest loop into its siblings without their adoption." The App v3 case stays as b (draft, "App v3"). |
| 7 | "Keep this file evergreen…; execution state lives in the selected work graph." (10–12) | a | construct §4: "Keep undertaking-specific paths and state out of reusable loop instructions." Construct's introduction: "The human's steering selects the undertaking". |
| 8 | Loop steps 1–4: recover, select, commission and integrate, update the graph (16–21) | a | FB §5, subsections 1–4: "Orient and recover", "Construct or revise the route", "Commission ready work", "Produce, examine, repair, and integrate". Construct §§1–4. |
| 9 | Step 5: continue; prepare reserved decisions while independent work proceeds; pause dependent work at its boundary (22–24) | a | FB §7: "Hold dependent production. Advance work whose inputs and authority are sufficient." Construct §3: "Keep blockers and uncertainty truthful while independent authorized work proceeds." |
| 10 | Step 6: closeout and final review; missing work returns to the graph (25–27) | a | Construct §3: "After the intended implementation/evidence PRs, plan one final bounded closeout stage." bounded-reconciliation §5: "If missing implementation or evidence is found, repair that graph work and recheck only the affected comparisons before completing this closeout." |
| 11 | Step 7: merge the final PR, report and stop; another undertaking needs steering (28–29) | a | AUM §18: "Its final merge ends that loop." FB §5, subsection 6: "A new objective requires new steering". |
| 12 | **"An intermediate PR, child return or session boundary does not end the loop."** (31) | a | Confirmed in AUM §18: "Earlier substantive merges remain intermediate results."; "an open required node, review hold or unmerged final PR leaves the undertaking open"; "no separate handoff or receipt is required solely because a session ends". Construct §3: "The final PR merge is the terminal condition". On a child return, AUM §10: "Distinguish usable partial work from completion." |
| 13 | On interruption, preserve the graph, active operations, evidence and the next safe action (32–33) | a | FB §7: "Preserve actual state, active operations, ownership, blockers, and next action." AUM §18, continuation account. |
| 14 | "The sections below define this recurring procedure; they are not a one-time reading checklist." (33–34) | d | Those sections are removed, and the methods carry the procedure. |
| 15 | Three manual links that name editions: Consolidated v7, AUM v3, Field Book v1 (38–42) | d | Superseded by the owner: "No don't pin to editions." The draft's "Entry reading" takes editions from `docs/alignment-manual/README.md`. |
| 16 | "Consult the sections needed…: PM Manual §§1.7, 3.12 and chapter 4; Agent User Manual §§2–5, 7–13 and 18; Field Book §§4–5." (44–45) | d | Superseded by the owner: "No routers." The draft replaces it with the headings-based entry and the principles paragraph. |
| 17 | "Read the manuals with the project's actual accepted basis and subsequent human steering." (45–46) | a | AUM Status: "Follow the actual human direction, applicable adopted instructions, selected method, brief, and host permissions." |
| 18 | "Their examples and dated App-v3 entry pointers are not v4 product requirements…" (46–48) | a + b | The examples: AUM §20, "The following examples are constructed teaching cases. They report no real authorization, execution, test, acceptance, or current project status." The App v3 entry (AUM §14) stays as b (draft, "App v3"). |
| 19 | "A guide describes practice; actual decisions, selected methods, briefs and host permissions bound execution." (48–49) | a | AUM Status: "It does not amend instructions, adopt a workflow, activate project work…". Alignment-manual README: "Applicable instructions, accepted decisions, and current source records govern actual project work." The draft's principle sentence restates this because the brief asks for it. |
| 20 | "Keep the undertaking proportionate. A small correction does not require a new PRD…" (51–53) | a | AUM §1: "A small authorized documentation correction does not require a new PRD, a new decomposition, a project-wide dependency audit, or a replacement work graph." |
| 21 | "Proceed on routine authorized work and prepare concrete alternatives for consequential human decisions." (53–54) | a | AUM §1: "An agent may act and make routine choices within clear authorization. It should prepare consequential human decisions, rather than multiply prompts…". AUM §13: "Prepare human decisions as concrete reviewable packages." |
| 22 | "Do not add a checkpoint after every contribution or PR." (54) | a | AUM §9: "advance ready authorized work without requesting approval for every routine node". Construct §3: "A PR boundary alone requires neither a formal reconciliation pass nor a Task Management intake." |
| 23 | Purpose and seed: PRD and companions through the ACCEPTANCE, plus later owner decisions (58–60) | b | Draft, "Basis". |
| 24 | "`conceptual/DECISIONS.md` preserves originating decisions; it does not override later accepted directions." (60–61) | a | The project README lists accepted commitments as "Original conceptual choices plus later accepted amendments, qualifications and continuation". AUM §4: "an older header does not cancel a later accepted adoption". |
| 25 | Decomposition pointer `_LATEST_ACCEPTED.md` (62) | b | Draft, "Decomposition". |
| 26 | "Follow accepted scope amendments if subsequently established; do not assume an `execution/_ScopeChange/_LATEST.md` exists." (63–64) | d | Stale. `execution/_ScopeChange/_LATEST.md` exists (SCA-V4-003), and the reading rule in `_LATEST_ACCEPTED.md` names it. The draft replaces this with a pointer (b). |
| 27 | DAG pointer, its handoff, and the DAGCurrency pointer (65–66) | b | Draft, "DAG". |
| 28 | "Read actual input satisfaction from local `Dependencies.csv` and `_DEPENDENCIES.md`." (66–67) | a | Construct §2: "Read satisfaction from the dependency records and treat held candidate edges as non-gating." |
| 29 | Deliverable paths: ScopeOfWork, dependencies, `_STATUS.md`, run indexes (68–69) | b | Draft, "Deliverables". `Design/` and `MEMORY.md` are added, since both now exist across deliverables. |
| 30 | "INITIALIZED establishes checked-contract maturity, not delivered inputs or completed implementation." (69–70) | a | `execution/_Coordination/_COORDINATION.md`, accepted rules: "INITIALIZED never implies any of those inputs exist or are fit for reliance." |
| 31 | Operating basis: `CURRENT_EXECUTION_BASIS.md` and `_COORDINATION.md` (71–72) | d + b | `CURRENT_EXECUTION_BASIS.md` is a "Manager-recorded selection for this App-v4 project-definition run". It pins manual hashes, contrary to "No don't pin to editions", so it is dropped. `_COORDINATION.md` is kept (draft, "DAG": setup rules). |
| 32 | "The selected PM Manual, Field Book and Agent User Manual are located through that basis." (72–73) | d | No edition pinning. Editions come from the alignment-manual README. |
| 33 | "Preserve `foundation/thesis/` unchanged." (73–74) | b | Draft, "Thesis". It is also recorded in `foundation/README.md` ("carried forward unchanged at the owner's direction (OD-07)"). It is kept as a write fence, because an agent would otherwise meet that record only after writing. |
| 34 | `HANDOFF_30_PERCENT.md` pointer and "work toward 60%" (75–78) | d | The 60% gate is passed: "I am accepting the 60% gate cleared." The handoff's standing items keep their homes: the v3.0.1 fallback is in the project README, and the archive is in `reference/archives/ARCHIVES.md`. |
| 35 | SWBPIPE handoff pointer; SWBPIPE stays with its session; PEC optional; Domains later (79–81) | b + a | The pointer stays (draft, "SWBPIPE, PEC and Domains"). The detail is in the handoff: "PEC remains an independent optional coordination capability."; "Domains develops alongside the first activity and joins a subsequent increment." |
| 36 | Checks: ScopeOfWork verification methods, candidate tooling, repository CI (82) | a + b | AUM §11: "Select verification from the actual affected behavior and project requirements." The b part is draft "Code": `app/README.md` for the offline build and tests. |
| 37 | No v4 `software-workflow.json`; "do not borrow v3 commands or report unconfigured checks as performed" (83–84) | b + a | The missing profile is draft "Code"; the v3 commands are draft "App v3". On unconfigured checks, AUM §11: "Record skipped, unavailable, interrupted, failed, and passed separately." and "An empty selection or exit-zero result supports no broader conclusion than the operation actually performed." |
| 38 | Task Management: federation preflight; no register assumed; no sweep created (85–87) | a + b | task-management, step 2: "Perform the invocation-local federation preflight". AUM §13: "Ordinary development has no standing sweep, service or register gate." The loop's intake permission is b (draft, "Methods"), because task-management says "A loop may authorize bounded intake under its own stated conditions", and bounded-reconciliation §4 says "when the calling loop permits it". |
| 39 | "`chirality-app-dev` remains a historical exemplar and fallback, not this loop's working root…" (89–90) | b | Draft, "App v3". |
| 40 | "Recover current owner decisions through their real records rather than assuming the v3 `_DECISIONS/_REGISTER.md` structure exists here." (90–92) | b | Draft, "Basis": `Acceptances/` and each run's `OWNER_DECISIONS.md`; no central register. |
| 41 | The steering establishes purpose and phase; recover the graph from the supplied references (96–98) | a | Construct §1: "Read the init steering, subsequent human directions and relevant decisions." and "Recover a continuing undertaking through the current graph". |
| 42 | Read the graph, contracts, MEMORY pointers, dependencies, implementation and evidence; give a concise reading and proceed (98–100) | a | Construct §2, source table. Construct §1: "State the reading of the undertaking briefly, distinguishing direction from interpretation. Proceed where intent is clear." |
| 43 | Verify branch and worktree state, partial edits, active workers and prior integration (102–103) | a | AUM §18: "Inspect the selected cursor, branch and worktrees, staged and unstaged changes, outputs, still-running workers, and shared resources." |
| 44 | Preserve unrelated edits; transfer shared-file and test-resource ownership explicitly (103–105) | a | AUM §18: "Establish that prior workers have stopped or explicitly transfer ownership before reassigning their files or application state." AUM §11: "Preserve unrelated user work." |
| 45 | Missing or stale pointers require recovery; they are not permission to restart (105–106) | a | AUM §18: "If a pointer is missing or contradictory, search the pertinent records and history for the intended target." Construct §1: "A missing target requires recovery; a previous proposal or paused assignment is not new authorization." |
| 46 | Use `construct-local-work-graph` when no graph exists or it needs revision (110–111) | a + b | The method is in the workflow. Its selection for App v4 is b (draft, "Methods"). |
| 47 | Relate the outcome to the DAG, the deliverables and present work (111–112) | a | Construct §2, table: "Locate the intended contribution, required upstream inputs and affected downstream consumers." |
| 48 | "Before the first DAG exists, follow the phase steering and applicable dependency/cycle-resolution method." (112–113) | d | Obsolete: DAG-004 is accepted. |
| 49 | Establish currency before relying on an accepted graph (113–114) | a | Construct §2: "audit its currency when the dependency records may have changed since its basis". |
| 50 | SCCs stay non-gating; identify the actual missing input without holding whole groups (114–116) | a | AUM §8: "Unresolved cycle-participating edges stay non-gating". AUM §5: "the group's local work graph orders the parts by the specific inputs each needs". |
| 51 | "Graph revision is driven by changed relationships or scope, not session entry." (117) | a | AUM §8: "A newly opened session does not warrant rebuilding a still-current accepted DAG." AUM §9: "If the same undertaking continues, revise its useful graph instead of creating another because the conversation is new." |
| 52 | Graph at `WorkGraphs/<undertaking>/WORK_GRAPH.md`; commit early; keep current; preserve historical graphs (119–123) | a + b | Construct §4: "save the current graph exactly at `execution/_Coordination/WorkGraphs/<undertaking>/WORK_GRAPH.md`" and "Preserve historical graphs at their original paths." The adoption and path stay as a pointer (b, draft "Conventions"). |
| 53 | Plan PRs with their slice's documents; the contents of the final closeout stage; no formal pass after every node (125–131) | a | Construct §3: "Plan substantive PRs, each carrying the documentation, reconciliation and conditional Task Management consequences its slice needs. A PR boundary alone requires neither a formal reconciliation pass nor a Task Management intake." The next paragraph of construct §3 lists the closeout stage. |
| 54 | "For work toward 60%, develop how the selected Deliverables meet their requirements and interact…" (135–137) | d | The 60% gate is passed. |
| 55 | Read the local ScopeOfWork and fixed choices before selecting a solution (137–138) | a | AUM §11: "Start implementation from the accepted objective, current candidate, explicit write fence, exclusions, and checking basis." AUM §7: "Read `ScopeOfWork.md` as a production contract." |
| 56 | Identify the exchanged contribution, supplier, receiver, conditions and failure behavior (138–139) | a | FB §4: "For each relationship, identify the supplier, consumer, required contribution, point of need, source, and present satisfaction." AUM §11: "For a service, examine the request, response, state changes, failure behavior, and subsequent consumer operation." |
| 57 | Put technical details in their maintained artifacts; keep the ScopeOfWork at the level of obligations (140–141) | a | AUM §12: "A statement failing all three is implementation detail, kept in code, tests, or developer documentation and cited as supporting evidence when useful." |
| 58 | Bounded implementation and connected tests can resolve design questions; definitions, prototypes and observations have different standing (143–144) | a | ckw §1: "A bounded disposable experiment is appropriate when it resolves consequential uncertainty more cheaply." FB §3: "Keep prototypes and proposed solutions identifiable." (Citation improved per MR NOTE-L1; it was AUM §5, "Fixtures and prototypes are consistent with 60% when reported as such.") |
| 59 | Revisit commitments and the DAG only when findings warrant it (145–146) | a | AUM §8: "Re-derivation is event-driven by decomposition revision or scope change under the doctrine and the project's adopted triggers." AUM §5, step 4: the departure rule. |
| 60 | Coordinate coupled work; missing inputs limit only the work that needs them (146–148) | a | AUM §5, the grouping paragraph (see row 50). FB §7 (see row 9). |
| 61 | Do not require every SCC to be resolved; do not silently delete relationships (148–149) | a | AUM §5: "Do not treat the gate as requiring a deliverable-level DAG with every cycle-closing reference reworded away." AUM §8: "it is not a reason for a tool to auto-cut relationships until the drawing passes". AUM §5 rulings: "No narrowing to close a cycle." |
| 62 | "The human assesses the 60% position…" (151–152) | d + b | The 60% content is superseded, since the gate is accepted. The binding of who assesses is kept and generalised (b, draft "Standing constraints": "The owner assesses each stage gate."). AUM §5 says "The project loop states who assesses the position" and cites this loop. |
| 63 | "Closing one undertaking or merging a PR does not pass that gate." (153) | a | AUM §5: "A strict audit, a closed graph-closure undertaking, a merged PR, or agent review does not pass the gate." |
| 64 | Present the result, unresolved matters, reliance limits and the continuation (154–155) | a | FB §1: "At a stage gate, present what has been established, what remains unresolved, what the next work would rely on, and the proposed continuation." |
| 65 | "Stage, lifecycle, task completion, acceptance and release remain separate." (155–156) | a | FB §2: "Keep project stage, deliverable lifecycle, task completion, and acceptance distinguishable." AUM §1 distinctions table, row "Source integration and release". |
| 66 | Agent 0/1/2 responsibilities (160–161) | a | AGENTS.md roles table; AUM §3. |
| 67 | What to supply each executor (161–162) | a | AUM §10: "It states the result and its use; accepted basis; relevant sources and scope; exact allowed writes; exclusions; required checks; expected return; parent; and return path." |
| 68 | Record the actual delegation; a brief is not proof; Type 2 does not delegate (163–164) | a | AGENTS.md: "Record the actual mechanism, parentage, supplied basis, scopes, enforcement limits, and returns. An executing child and a written launch brief are different facts." and "Type 2 does not delegate." |
| 69 | Integrate returns; size concurrency; one owner for shared writes (164–166) | a | FB §5, subsection 3: "Keep shared writes under one owner." and "Size concurrency to the team's capacity to examine and integrate returns." |
| 70 | Implement, verify, validate, review, repair and integrate via PRs (168–169) | a | AUM §11; FB §5, subsection 4. |
| 71 | Each PR carries its documentation, reconciliation and governance consequences, including a Task Management transfer (169–171) | a | Construct §3 (quoted in row 53). |
| 72 | Exercise connected behavior; record the candidate and evidence (171–172) | a | AUM §11: "Exercise the actual consumer route as soon as it becomes operable." and "Use one canonical copy with references from the graph or deliverable." |
| 73 | Prepare consequential decisions while unaffected work proceeds (172–173) | a | AUM §11: "Hold the affected acceptance or merge while independent work proceeds." Construct §3 (quoted in row 9). |
| 74 | Required production stays in the graph; an intermediate merge does not finish the undertaking (173–175) | a | AUM §9: "An intermediate merge or Task Management transfer cannot discharge it." |
| 75 | **One closeout after integration, using `bounded-reconciliation`, before the final PR** (179–182) | a | Confirmed. bounded-reconciliation: "The stage follows integration of the intended implementation and evidence work—normally the penultimate merge—and precedes the final PR." AUM §12 states the same. |
| 76 | Compare the result with the ScopeOfWork, dependency and governance records; apply warranted edits (183–185) | a | bounded-reconciliation §§2–3. |
| 77 | Preserve future requirements and the owning authority for scope, lifecycle, protected criteria and baselines (185–186) | a | bounded-reconciliation §3: "Future requirements remain requirements when implementation falls short" and "Changes to accepted scope, lifecycle, protected criteria or a pinned authority basis follow their owning decision path." |
| 78 | Closeout is bounded; a no-change result suffices; missing work returns; recheck (188–192) | a | bounded-reconciliation §3: "a supported no-change result is sufficient when the affected record already represents the result accurately". bounded-reconciliation §5 (quoted in row 10). |
| 79 | Resolve first through graph work, an amendment or a decision; successor work stays with its successor (196–200) | a | bounded-reconciliation §4: "First handle a consequence through the authorized graph, a warranted amendment, or the actual owning decision/scope-change route." AUM §13: "First seek an appropriate node in the current authorized undertaking or an identified owned successor." |
| 80 | Only a material, evidenced concern without a home qualifies for intake (202–203) | a + b | AUM §13, eligibility. The loop's permission is b (see row 38). |
| 81 | Hand it to WORKING_ITEMS selecting `task-management`; federation preflight (203–206) | a | AUM §13: "WORKING_ITEMS selects `chirality-root:bundled:workflow:task-management` directly with the invoking loop, purpose, authority and exact write boundary." |
| 82 | Promotion, disposition and external assignment are human acts (206–207) | a | AUM §13: "Promotion, disposition and external assignment remain actual human acts." |
| 83 | Retain the outcome in Task Management; link it; routing does not satisfy a requirement (207–210) | a | AUM §13: "Pending intake remains in its Task Management home, linked from the originating PR/node and closeout as applicable." task-management: "An open intake does not discharge an unmet requirement in the originating undertaking." |
| 84 | **"`loop/LOOP_RECEIPTS.md` is a reset compatibility pointer, not a receipt chain or recovery cursor."** (214–215) | b | Checked: only `LOOP_RECEIPTS.md` states it ("this empty compatibility file is not a recovery cursor"); no manual or workflow does. AUM §18's material on receipt cursors and validators could mislead an agent who meets the file. Draft, "Conventions". |
| 85 | "The selected work graph carries ongoing execution." (215) | a | Construct introduction: "One graph carries the undertaking across sessions." |
| 86 | **One receipt at `AgentRuns/<RunID>/RECEIPT.md`, using the graph's run identity** (217–219) | a + b | Confirmed. Construct §3: "For a loop that adopts this method (currently App, Piping and PEC), use the graph's stable run ID for one receipt at `execution/_Coordination/AgentRuns/<RunID>/RECEIPT.md`". The workflow's "App" does not clearly cover App v4, so App v4's adoption is b (draft, "Methods" and "Conventions"). |
| 87 | **The receipt's content and limits:** "a concise, derivative account of what landed, affected deliverables, actual PRs, checks and evidence, decisions or Task Management transfers, and material limits"; it supplies the PR description; it is not a second graph, a future-work list or a decision authority (219–224) | **c** | Only the location (construct §3) and the PR-description use (bounded-reconciliation §5: "The invoking loop's concise receipt may supply its final PR-sized result/checks/limits account") are stated elsewhere. Nothing else defines what a receipt holds or must not become. Proposed addition A1 below. |
| 88 | Keep detailed logs at their sources and link the graph (224–225) | a | Construct §4: "Keep detailed launch histories, child attribution, source hashes and old pauses in their owning run records rather than repeatedly appending them to the current graph." |
| 89 | "A graph node or Task Management invocation does not create another loop receipt." (225–226) | a | task-management, step 5: "Do not create a separate Task Management receipt or a MEMORY work list." AUM §13: "Graph-led App/Piping closeout needs no new loop receipt or duplicate narrative." |
| 90 | **A MEMORY entry in each affected deliverable, created when first needed; its contents** (227–230) | a + b | Confirmed. AUM §13, "Index the run without duplicating its decisions": "add a terse entry near final PR preparation in each affected deliverable's `MEMORY.md` Runs table. Use a stable run ID and date, state the work performed in that deliverable, and link the PR, central evidence, applicable rulings, scope changes, and Task Management transfers." The creation grant is b, because AUM §6 says "optional `MEMORY.md` requires a selected, authorized path" and construct §3 says "MEMORY and closeout writes remain subject to the project's write fences". Draft, "Conventions". |
| 91 | MEMORY is an index, not a decision record or future assignment; preserve history (230–231) | a | AUM §4 record table: `MEMORY.md` must not be read as if "A memory entry supplies a ruling or becomes a second execution queue." AUM §13: "The table has no future-work queue." and "Preserve existing headings and entries." |
| 92 | The setup undertaking gets no retroactive MEMORY work (232–233) | d | Historical. Setup closed on 2026-09-27, and 23 deliverables now carry `MEMORY.md` from later runs. |
| 93 | Include the receipt and MEMORY in the final PR; use a stable link until the PR URL exists; do not claim a pending merge (234–236) | a | AUM §13: "While a PR URL is unavailable, use a stable run/branch link and bind the actual URL before final candidate checks. Do not assert a future merge SHA or require a later commit solely to record that merge." Construct §3: the closeout stage includes the receipt, the MEMORY entries and the final PR. |
| 94 | "Root SPEC §9.8 still governs required multi-agent execution provenance." (236–237) | a | AGENTS.md (quoted in row 68). Construct §4: "Required execution provenance remains recoverable through those links." |
| 95 | Complete the graph; prepare the final PR; review and checks cover the final candidate; reserved decisions (241–245) | a | AUM §18: "complete its promised work, the single planned documentation/governance closeout, and affected deliverable Runs entries; then complete final PR review, required checks and decisions, and merge." AGENTS.md: "with review and validation covering the actual candidate revision". |
| 96 | Record readiness and the PR URL in the graph; verify the merge afterward; no future SHA or completion commit (245–247) | a | Construct §3: "Its candidate records readiness and the PR URL; later Git/PR evidence establishes the actual merge." Construct §4: "Do not require a later commit solely to write the final merge result back into its own candidate." |
| 97 | The loop ends when the final PR merges; a hold, an open node or an unmerged PR keeps it open (249–251) | a | AUM §18 (quoted in row 12). |
| 98 | On interruption, keep the candidate, open checks, operations and next action in the graph (251–252) | a | Construct §4: "Keep one current account of the ready work, holds and next safe action, bound to the checked candidate." |
| 99 | Final integration does not issue, accept or release (252–253) | a | AUM §9: "A completed graph remains selected and visible; it does not start another phase, release a product, or issue a deliverable." |

**Class counts** (99 rows, by first-listed class):
- (a) 75;
- (b) 11;
- (c) 1;
- (d) 12.

Thirteen rows are mixed:
- nine are a + b: rows 6, 18, 36, 38, 46, 52, 80, 86 and 90;
- two are d + b: rows 31 and 62;
- two are b + a: rows 35 and 37.

Counting every row with a project-specific part, 22 rows feed a line in the draft.

The rules the brief flagged were each checked:
- intermediate PR (row 12): a;
- closeout before the final PR (row 75): a;
- the receipt's location (row 86): a + b;
- the receipt's content (row 87): c;
- MEMORY (row 90): a + b;
- LOOP_RECEIPTS (row 84): b.

## New lines in the draft (not in the current file)

| # | Draft line | Source |
|---|---|---|
| N1 | Entry reading: the AUM headings to three levels (33 heading lines today) and the Field Book in full, from the README's current editions; then the work graph | The owner: "presenting just the Agent User Manual's headings and the Field Book is excellent and accepted"; "No don't pin to editions." |
| N2 | The principles paragraph on when to read further | The owner: "the agent decides when to visit it (and here guidance can be given around this level of decision making if done right)". The wording is from the brief. |
| N3 | `coordinated-knowledge-work`, applied in proportion to the work | The owner: "We should incorporate the `coordinated-knowledge-work` workflow into the LOOP_INIT instructions too." |
| N4 | GROUPS.md, with GC-7 and GC-8 | Owner acceptance of the 60% gate and both regrouping moves; GC_RULINGS GC-7 and GC-8. |
| N5 | The contract core (group A) frozen under change control; issues logged in `app/CONTRACT_ISSUES.md` | The owner: "Yes you can take this approach…", in reply to "treat the co-designed contract core as one merged unit under change control". The issue log is named in the graph-closure work graph. **The core's membership is an inference.** GROUPS.md names group A "Runtime and contract core", and the B0 member list was dropped. Confirm it before adoption. |
| N6 | Standing constraints: Codex scratch home, sign-in, downloads, offline builds | The SK dispatch (DISPATCH.md) and `app/README.md`. The owner's download answers are recorded case by case in `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` and in this run. No standing project record states them; the draft makes them standing. |
| N7 | Decision recording, and no implied owner review | AGENTS.md: "never imply personal owner review" (in its Git context). AUM §5 gives exact words, source and custody, but only for the gate. The draft adds the project location, the run's `OWNER_DECISIONS.md`. See optional addition A5. |
| N8 | Task Management intake permitted | Required by the workflow's "A loop may authorize bounded intake under its own stated conditions" (see row 38). |
| N9 | "The owner assesses each stage gate." | Required by AUM §5, "The project loop states who assesses the position" (see row 62). |

## GROUPS.md location

**Recommendation:** move it with `git mv` to
`execution/_Coordination/GROUPS.md`.

Why move it:
- Every development loop reads it for the whole 90% phase. Regrouping is an
  owner decision that edits it, and that should not mean editing the folder
  of a closed run.
- `_Coordination/` already holds the project's standing coordination
  records, such as `_COORDINATION.md` and `HANDOFF_SWBPIPE_DOMAINS.md`.
- The file and its type are unchanged, so no new record type is created.

Why not `execution/_DAG/`:
- `project-dag` owns that folder's structure: immutable versions,
  `_LATEST.md`, `_Candidates/` and `cases/`.
- AUM §5 says grouping for development "is not a merge ruling under the
  doctrine's §2 rule 3 or `project-dag` selection".

After the move:
- Update the AUM link `[app-v4-groups]` (AUM line 836).
- Leave the historical mentions in `DISPATCH.md`, `reviews/MR-MANUAL.md`,
  `MANUAL_CHANGES.md` and `SURVEY/GROUP_SORT.md` as they are. They cite the
  file by name and commit.

If HELP_HUMAN keeps it in the run folder, change the one path in the draft.

## Additions needed elsewhere

**A1 (class c, row 87): the receipt's content.**

Placement: AUM §13, subsection "Index the run without duplicating its
decisions". Add it as a new paragraph before the MEMORY table, after the
paragraph that begins "Under the revised arrangement, add a terse entry…".

> Where the loop's method calls for one, write the undertaking's single
> central receipt near final PR preparation, at the location the method
> names (for `construct-local-work-graph`,
> `execution/_Coordination/AgentRuns/<RunID>/RECEIPT.md`, under the graph's
> stable run ID). It is a concise, derivative account of what landed: the
> affected deliverables, the actual PRs, the checks and evidence, any
> decisions or Task Management transfers, and material limits. Its result,
> checks and limits supply the final PR description. It is not a second
> execution graph, a future-work list or a decision record. Link the graph
> and the detailed sources rather than copying them. A graph node or a Task
> Management invocation creates no further receipt.

Alternative home: construct §3, beside the existing receipt sentence. That
is a workflow revision, so it goes through `create-workflow`, as AGENTS.md
requires.

**A2 (recommended): an App v4 entry in the AUM.**

Placement: a new subsection at the end of §14, after the paragraph on
`npm test`, `npm run typecheck` and `npm run build`. Use the anchor
`app-v4`. A subsection avoids renumbering the chapters that other documents
cite.

> ### Enter App v4 development
>
> App v4 (`projects/chirality-app-v4`) is a separate project from the App
> development described above. Enter through its
> `init/dev-loop-init-prompt.md`, which leads to `loop/LOOP_INIT.md`. App v4
> has no project `AGENTS.md`. Its `LOOP_INIT.md` binds it to this manual, the
> Field Book and the bundled workflows, and holds its project pointers,
> conventions and standing constraints. Nothing earlier in this section
> applies to App v4: the APP-HOLD-1 preflight, the `frontend/` layout, the
> App software profile and its registered checks belong to App development.
> [App v4 loop][app-v4-loop]

This text holds no time-sensitive state, since phase, groups and the
current DAG stay behind LOOP_INIT's pointers. It does not repeat LOOP_INIT.
Optionally, also change the alignment-manual README's description of the
AUM, "across App, Piping, Runtime, and PEC", to "across App, App v4,
Piping, Runtime, and PEC".

**A3 (optional): the gate sentence in AUM §5.** The sentence "the App v4
loop, for example, reserves the 60% assessment to the human" stays true
under the draft's "The owner assesses each stage gate." To match the
draft, it could become:

> the App v4 loop, for example, reserves each stage-gate assessment to the
> human

**A4 (needs `create-workflow`, not blocking): construct-local-work-graph.**
- Introduction. It says "`LOOP_INIT.md` supplies the evergreen procedure
  for recovering, constructing and following its graph." App v4's reduced
  LOOP_INIT points to the procedure instead. Proposed: "`LOOP_INIT.md`
  supplies, or points to, the evergreen procedure…".
- §3. "(currently App, Piping and PEC)" does not clearly cover App v4.
  Proposed: "(currently App, App v4, Piping and PEC)".

**A5 (optional): recording human decisions, in AUM §13.** Place it after
"Preserve the human's words and distinguish them from the agent's
interpretation; silence is no ruling."

> Record each decision with the human's exact words, their source and their
> custody (for example, the session transcript), apart from your
> interpretation, and imply no review the human did not perform.

With A5 in place, the draft's decision line shrinks to its location, the
run's `OWNER_DECISIONS.md`.

**A6 (optional): the principles paragraph in AUM §1.** If other loops
should read the manuals the same way, move the principles paragraph into
AUM §1, "Use the guide at the right scale". LOOP_INIT would then only point
to it. For now it stays in LOOP_INIT, which the owner named as the place
for this guidance.

**A7 (stale wording, from GC-8).** The last sentence of GROUPS.md reads "…
does not cover relationships recorded only in work graphs or the shared
list." GC-8 retired the shared list. It should end "…recorded only in work
graphs."

## Other gaps met in passing

These were seen from LOOP_INIT's perspective only; no document was reviewed
as a whole.

1. **Project README.md.** It carries stale, time-sensitive state:
   - "qualified initial graph and 30% package under final review";
   - "No separate standing project AGENTS or production loop is created at
     this stage";
   - it names the PROJECT-DEFINITION work graph as current.

   An agent reading it gets the wrong position. Recommendation: replace the
   Position paragraph and the "Current execution-definition review" section
   with an entry pointer, `init/dev-loop-init-prompt.md` →
   `loop/LOOP_INIT.md`. State then stays in the DAG pointer and the work
   graphs.
2. **HANDOFF_SWBPIPE_DOMAINS.md.** The draft points to this file. Its line
   "Current App v4 standing (updated 2026-09-30)" still names DAG-003 as
   the accepted graph. Recommendation: drop that line or mark it as dated.
   The DAG pointer carries the current graph.
3. **CURRENT_EXECUTION_BASIS.md and HANDOFF_30_PERCENT.md.** Both pin
   manual editions by hash for the definition run. HANDOFF_30_PERCENT says
   "Current manual editions are pinned in `CURRENT_EXECUTION_BASIS.md`". Both
   are scoped historical records, and the draft no longer points to either,
   so no edit is needed.
4. **docs/alignment-manual/README.md.** It becomes the edition pointer for
   LOOP_INIT's entry reading, so it must be kept accurate at each edition
   change. DISPATCH's last row records the manual writer making v8 current
   there, "Local commit only (merge hold)". Until that merges, the README
   names Consolidated v7. This does not affect the entry reading, which uses
   only the AUM and the Field Book.
5. **Entry cost.** The AUM headings are 33 lines. The Field Book is 23,342
   bytes, about 6,000 tokens. Together with the draft (about 1,250 tokens),
   entry is about 7,500 tokens before the work graph. The current file
   alone is about 4,100 tokens, but it points into some 15 manual sections.
6. **taskmgmt-init-prompt.md.** No change is needed (see
   `DEV_LOOP_INIT_PROMPT_PROPOSED.md`).
