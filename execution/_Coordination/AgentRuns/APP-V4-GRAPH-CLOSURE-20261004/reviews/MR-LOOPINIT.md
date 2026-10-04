# MR-LOOPINIT: independent review of the LOOP_INIT revision drafts

**Reviewer:** MR, a Chirality Type 2 TASK dispatched by HELP_HUMAN. Model: Claude Opus 5.5 (`claude-opus-5-5`). I wrote none of the reviewed text. I used read-only git and no network. I wrote only this file and Addendum C of `MR-MANUAL.md`.

**Candidate:** local commit `1e930cb16e` on `claude/app-v4-graph-closure`. The owner's merge hold is in force. The live `loop/LOOP_INIT.md` is unchanged from `3a7fd0ef76`.

| File | sha256 (prefix) |
|---|---|
| `LOOP_INIT_PROPOSED.md` | `79d96feb7ca1…` |
| `DEV_LOOP_INIT_PROMPT_PROPOSED.md` | `135f731d8168…` |
| `LOOP_INIT_MAPPING.md` | `506b0a236cf7…` |

**Basis.**
- `OWNER_DECISIONS.md`, the sections from "How LOOP_INIT steers agents…" onward:
  - "No routers";
  - the headings of the Agent User Manual (AUM) and the Field Book as the entry reading;
  - "I don't want to create a new type of record…";
  - "No don't pin to editions";
  - LOOP_INIT as the one place that binds the project, under a three-part test: a sentence is specific to App v4, instructs, and is stated nowhere else;
  - the merge hold.
- Rulings GC-7, GC-8 and GC-9.

**Method.**
- **Mapping quotes.** I re-ran 84 of the mapping's destination quotes, taken from 70 rows (most of them class a), with a script that normalises whitespace against the files at HEAD. The files were the AUM, the Field Book, `construct-local-work-graph`, `coordinated-knowledge-work`, `bounded-reconciliation`, `task-management`, Root `AGENTS.md`, `_COORDINATION.md`, `HANDOFF_SWBPIPE_DOMAINS.md`, `LOOP_RECEIPTS.md` and the alignment-manual README.
- **Rules lost.** I read the live LOOP_INIT in full and compared it with the draft to see whether any rule is lost.
- **Draft checks.** For every path and workflow in the draft:
  - I checked each path with `test -e`;
  - I checked each workflow name against `workflows/index.json` (source `bundled`, `sourceRootId` `chirality-root`) and the repository's existing usage of `chirality-root:bundled:workflow:<name>`.
- **Standing constraints.** I checked them against the earlier owner records: DESIGN-PASS-2, -3 and -4 `OWNER_DECISIONS.md`, DISPATCH row SK, and `app/README.md`.

## 1. The mapping

**The quotes are verbatim.** All 84 quotes were found exactly in the destinations cited. That covers every class (a) row I sampled: rows 2, 4–13, 17–22, 24, 28, 30, 36–38, 41–47, 49–53, 55–61, 63–69, 72–83, 85, 86, 88–91 and 93–99.

**The rules are carried.** Each cited destination carries the substance of the current rule, not just similar words. The loop contract rows (8–11), the closeout rows (75–78), Task Management (79–83), receipt and MEMORY (84–93), and merge and end (95–97) are all genuinely stated in the workflows, the AUM or the Field Book.

**Class (b) and (d).** Rows 26 and 31 are classified correctly:
- `execution/_ScopeChange/_LATEST.md` exists;
- `CURRENT_EXECUTION_BASIS.md` pins manual hashes for the definition run, and its own text limits it to that run.

**One weak destination (NOTE-L1).** Row 58 ("definitions, prototypes and observed behavior have different standing") cites ckw §1 and an AUM §5 sentence about evidence at 60%. A closer general home is the Field Book §3: "Keep prototypes and proposed solutions identifiable". The rule is not lost; the citation should be improved.

**No load-bearing rule is lost.** Three items not carried into the draft belong elsewhere, correctly:
- merge authority is in Root AGENTS.md;
- the SPEC §9.8 provenance rule is in Root AGENTS.md and construct §4;
- the 60%-phase text is superseded by the gate.

One gap remains, but it arises from GC-8, not from the current file. See MAJOR-L1.

## 2. The draft LOOP_INIT

### What is right

- **Paths.** All 16 paths exist: `docs/PRD.md`, the basis ACCEPTANCE, `_LATEST_ACCEPTED.md`, `_ScopeChange/_LATEST.md`, `_DAG/_LATEST.md`, `DAGCurrency/_LATEST.md`, `_COORDINATION.md`, the SWBPIPE handoff, `app/README.md`, `app/CONTRACT_ISSUES.md`, `foundation/thesis/`, `loop/LOOP_RECEIPTS.md`, `WorkGraphs/`, the init prompt, the role file and the alignment-manual README. `app/` has no `software-workflow.json`, as stated.
- **Methods.** All eight workflow names are correct and exist as bundled `chirality-root` workflows: `construct-local-work-graph`, `coordinated-knowledge-work`, `bounded-reconciliation`, `task-management`, `scope-change`, `dependency-extract`, `audit-dep-closure` and `project-dag`. The ID form matches established usage. ckw is included, as the owner asked.
- **Owner's directions.**
  - There is no router.
  - There is no edition pin: editions come from the README's current editions.
  - No new record type is created.
  - The entry reading is the AUM headings to three levels (34 lines at HEAD) and the Field Book in full.
  - The "when to read further" paragraph is principle-level guidance, which the owner allowed ("guidance can be given around this level of decision making").
- **Size.** About 1,260 tokens, down from about 4,100.
- **Accuracy of the standing constraints.**
  - *Downloads and sign-in.* The rule matches the owner's consistent answers. Each download or sign-in needed its own yes: DESIGN-PASS-2 ("Any other model, or the Codex sign-in, needs a new owner answer"), DESIGN-PASS-4 ("Any other download, or a sign-in, needs a new owner answer"), and L-6.
  - *"The owner assesses each stage gate."* This matches the 30% and 60% records. It also answers AUM §5's "The project loop states who assesses the position".
  - *Change control.* This follows GC-9 item 1, which is HELP_HUMAN's ruling, and the draft does not attribute it to the owner.

### MAJOR-L1: No loop is told to read the other groups' work graphs, so GC-8's carry-over has no actor

**Evidence.**
- GC-8: "Where the other group has no active work graph yet, the relationship is recorded in the finding loop's graph. It is carried into the other group's graph when that loop constructs it."
- The draft's entry reading is: "Read the work graph of the undertaking the steering names. If it has none, construct one."
- Neither the draft nor `construct-local-work-graph` tells a loop that is constructing or resuming a group's graph to read the other groups' graphs for relationships recorded against its group. The construct §2 sources table covers the accepted DAG and the current graph, but not the graphs of sibling loops.

**Consequence.** A cross-group relationship found before the other group's loop exists can stay invisible to that loop. This is the problem the owner warned against: "a problem that builds and isn't recognized". It is also what the earlier visibility criterion was meant to prevent, and GC-8 removed the shared list that used to provide it. The rule is project-specific, because GC-8 is App v4's own ruling, so LOOP_INIT is the only place that can state it.

**Fix.** Add one sentence to the draft's entry reading, step 2: "When you construct or resume a group's graph, read the other groups' graphs under `execution/_Coordination/WorkGraphs/` for relationships recorded against your group (GC-8)."

Optionally, HELP_HUMAN can append a clarification to GC-8 in active voice ("the loop that constructs the graph carries it in").

### MINOR-L2: The App v3 line contradicts the new AUM App v4 subsection

**Evidence.**
- The draft says: "`projects/chirality-app-dev` belongs to App v3, as do the Agent User Manual's §14 and that section's tools, checks and decision register. Do not apply them here."
- Under GC-9, A2 added "Enter App v4 development" (`#app-v4`) inside AUM §14, and that subsection applies to App v4.
- The two texts also say the same thing twice, which fails the owner's "stated nowhere else" test.

**Fix.** Shorten the line to: "`projects/chirality-app-v4` is not App v3. The App v3 material in AUM §14 does not apply (see its 'Enter App v4 development')." Alternatively, drop the §14 clause and rely on A2.

### MINOR-L3: The owner-decision location is stated twice, and "that folder" is ambiguous

**Evidence.**
- The Basis bullet says "Owner decisions are kept in that folder and in each run's `…/OWNER_DECISIONS.md`". "That folder" reads as `Acceptances/APP-V4-BASIS-20260926/` itself.
- The last standing constraint repeats: "Owner decisions are recorded in the run's `OWNER_DECISIONS.md`."

**Fix.** Keep one sentence: "Owner decisions are in `execution/_Coordination/Acceptances/` and each run's `OWNER_DECISIONS.md`; record new ones in the run's file. There is no central register."

### MINOR-L4: The Conventions section repeats what the Methods adoption line already binds

**Evidence.**
- Methods already says "App v4 adopts [construct-local-work-graph's] graph, closeout, receipt and MEMORY conventions".
- The Conventions section then repeats the WorkGraphs path and the receipt path. Both are stated in construct §3 and §4, and the receipt content is now also in AUM §13 (A1).

**Fix.** In Conventions, keep only what is App v4-specific:
- the MEMORY creation grant (mapping row 90, class b);
- the LOOP_RECEIPTS statement (row 84, class b);
- optionally, "the run's other records go in the same folder".

Drop the two path restatements.

### MINOR-L5: The Codex constraint needs its scope, and the README it points to needs the configuration

**Evidence.**
- The draft says: "Run Codex only with a scratch home made by `mktemp -d`, never with `~/.codex`. Configure the scratch home as `app/README.md` describes."
- `app/README.md` gives the configuration only inside the handshake test: plugins off, analytics off, and a provider at 127.0.0.1:9. Its "Run the App" section says only that a `config.toml` "stands in for the person's configuration".
- DISPATCH row SK records the risk: an early probe without a provider made Codex open `wss://api.openai.com` at `thread/start`.
- Without a scope, the sentence could also be read as a statement about the product. The product's own hosting design follows the person's Codex configuration.

**Fix.**
- In LOOP_INIT: "When you run Codex for development or tests, use a scratch home made by `mktemp -d`, never `~/.codex`, configured as `app/README.md` describes."
- In `app/README.md` "Run the App", state the same `config.toml` contents as the test uses. That is a code-document fix, outside LOOP_INIT.

### NOTEs

- **NOTE-L2.** "App v4 has no `software-workflow.json`" is a current-state fact. It is acceptable as a guard against borrowing App v3 commands. Phrasing it conditionally ("Until App v4 has a `software-workflow.json`, the checks are those in `app/README.md`") would keep it true later.
- **NOTE-L3.** "Record what you read in the run evidence" is a weaker restatement of Root AGENTS.md, which says to record "actual origins and hashes". Either drop it or say "as Root AGENTS.md requires".
- **NOTE-L4.** The merge hold is correctly absent from LOOP_INIT, because it is ephemeral owner direction. It must reach the next session through its steer or handoff. Root AGENTS.md already makes explicit holds take precedence.
- **NOTE-L5.** Only GC-7, GC-8 and GC-9 (change control) are bound. GC-5 items 1 and 2 are bound through GC-7 item 1, and GC-6's no-narrowing rule is general practice in ckw §2. Nothing more is needed.

## 3. The init prompt draft

**It is right.**
- It keeps the order: AGENTS.md, then the role, then LOOP_INIT, then the steer.
- It drops the sentence that conflicted with the accepted entry reading ("the Field Book is a summary").
- It drops a redundant authority clause that AGENTS.md and the role already cover.
- The role option is consistent with AGENTS.md ("directly select HELP_HUMAN, HELPS_HUMANS, or WORKING_ITEMS"), and the `agents/AGENT_*.md` files exist.
- The note on the Task Management prompt is accurate.

No change is needed. The steer line is where the merge hold (NOTE-L4) and the undertaking belong.

## 4. Where the Codex binary location belongs

**View: LOOP_INIT should not name the cache location.** Keep the location out of tracked instructions; `app/README.md` should carry the identity instead. The reasons:
- **It is machine state, not project direction.** The cache is outside the repository and specific to one machine. A path in LOOP_INIT would be wrong on any other checkout, and would need to be maintained as current state, which the owner ruled out ("I don't want to create a new type of record…").
- **It would duplicate.** `app/README.md` already defines `CHIRALITY_CODEX_BIN`. Naming the path in LOOP_INIT as well fails "stated nowhere else".
- **The durable fact is the identity, not the location.** Put that in `app/README.md`, beside the variable: the required version (0.158.0) and the expected sha256 (`788a818f…`, given in full), as the value for `CHIRALITY_CODEX_EXPECTED_SHA256`. The README currently says only `<hex>`. The start check then verifies whichever binary a session finds.
- **The machine path goes in ephemeral places:** the closing session's handoff or the next steer, or the person's own shell environment. A later session that cannot find the binary asks the owner. A new download would need the owner's yes anyway.

## Verdict

**REPAIR.** The repair is small.

| Severity | Count |
|---|---|
| BLOCKING | 0 |
| MAJOR | 1 (MAJOR-L1, a one-sentence addition) |
| MINOR | 4 (L2–L5) |
| NOTE | 5 (L1–L5) |

The mapping is accurate and loses no load-bearing rule. The draft meets the owner's test apart from the duplications noted. Its paths and method identifiers are correct, and its constraints match the owner's directions. The init prompt is READY as drafted.

The LOOP_INIT draft becomes READY once MAJOR-L1 is added. I recommend fixing L2–L4 in the same pass. L5's README change can travel with the close-out.

---

## Addendum A: confirmation of repairs

**Candidate:** `b30cef06a0`, a local commit under the merge hold.

| File | sha256 (prefix) |
|---|---|
| `LOOP_INIT_PROPOSED.md` | `0aaabcdbefea…` |
| `app/README.md` | `a9357153a464…` |

The reviewer is the same MR instance (Claude Opus 5.5). I used read-only git and no network.

### Repairs

| Item | Status | Evidence |
|---|---|---|
| MAJOR-L1 | Repaired | Entry step 2: "When you construct or resume a group's graph, read the other groups' graphs under `execution/_Coordination/WorkGraphs/` for relationships recorded against your group (GC-8)." |
| L2 | Repaired | The App v3 line now covers `projects/chirality-app-dev` "and its tools, checks and decision register" and no longer names AUM §14. |
| L3 | Repaired | One "Owner decisions" bullet names `Acceptances/` and each run's `OWNER_DECISIONS.md`, says to record new decisions in the run's file, and says there is no central register. The duplicate standing constraint is removed. |
| L4 | Repaired | Conventions keeps only the MEMORY creation grant and LOOP_RECEIPTS. The Methods line still binds App v4's adoption of the construct conventions for graph, closeout, receipt and MEMORY. |
| L5 | Repaired | Draft: "When you run Codex for development or tests, use a scratch home…". |
| L5 (README) | Repaired | `app/README.md` "Run the App" now gives the `config.toml`. I checked it line by line against `src-tauri/tests/handshake.rs` and it is identical: provider `skeleton_local` at `http://127.0.0.1:9/v1`, `wire_api = "responses"`, plugins off, analytics off. Its cross-references EVIDENCE.md N-1 and CONTRACT_ISSUES.md CI-8 both exist. |
| NOTE-L1 | Done | Mapping row 58 now cites Field Book §3. |

**Codex identity.** `app/README.md` now states version 0.158.0 (darwin-arm64) and the full sha256 as `CHIRALITY_CODEX_EXPECTED_SHA256`. It says the binary's location "is not recorded here". This matches my §4 view. I did not re-hash the binary myself; the coordinator reports that check, and the `npm test` rerun of 3/3.

### NOTE-L2 and NOTE-L3: no change needed

- **NOTE-L2, "App v4 has no `software-workflow.json`".** No change. The line is project-specific and stops agents borrowing App v3 commands. If App v4 later adds a profile, that change will need its own LOOP_INIT edit anyway, so the line will not stay wrong unnoticed.
- **NOTE-L3, "Record what you read in the run evidence".** No change required. It is consistent with Root AGENTS.md, and it reinforces the read-further guidance the owner invited. Appending "as Root AGENTS.md requires" would be a harmless improvement but is optional.

### Verdict

**READY.** The LOOP_INIT draft, the mapping and the init prompt are ready for the close-out replacement of `loop/LOOP_INIT.md`.

Carried forward from MR-MANUAL Addendum C, MINOR-C3: land the replacement in the same PR as the AUM sentence "reserves each stage-gate assessment", and convey the merge hold through the next steer (NOTE-L4).
