# Work graph — App v4 first App/host increment: technical details and interfaces

Method: `chirality-root:bundled:workflow:construct-local-work-graph`, applied
under [`loop/LOOP_INIT.md`](../../../../loop/LOOP_INIT.md). Maintainer: HELP_HUMAN
(this Claude Code session), dispatching bounded Type 2 TASK executors directly
(Root `AGENTS.md`: HELP_HUMAN may dispatch bounded Type 2 work). No WORKING_ITEMS
manager session is running; any lifecycle record this graph needs is made under
a recorded WORKING_ITEMS consultation or by the human.

## Intent and selected route

- **Stable run identity:** `APP-V4-FIRST-INCREMENT-20260928`. Run records:
  [`AgentRuns/APP-V4-FIRST-INCREMENT-20260928/`](../../AgentRuns/APP-V4-FIRST-INCREMENT-20260928/).
- **Steering (exact, owner, 2026-09-28, init prompt):** "Begin Chirality App
  v4's detailed development toward the 60% gate. Recover the accepted 30% basis
  … then establish and execute the first bounded undertaking to develop the
  technical details and interfaces for the first App/host increment. Use the
  accepted DAG, local scopes of work and characterized SCCs to organize
  coordinated and parallel work. … Bring consequential choices to me with
  concrete recommendations, and preserve the separately owned SWBPIPE, PEC and
  Domains responsibilities."
- **Interpretation (HELP_HUMAN):** the "first App/host increment" is the
  connected model-adjustment/checking activity accepted in B-HTML 05 (PRD §3,
  V4-EXT-01, OQ-11): a reusable workflow carried between App and host; inspect a
  model, propose an adjustment, request a non-mutating check, meet an
  intervening edit, recover the actual outcome/receipt. This undertaking
  develops the App/shared side of that increment's **interfaces and technical
  details** to design (60%) level — the CASE-002 M1 semantic contributions,
  their M2/M4 receiving descriptions and case inventories, and the two root
  suppliers every consumer names (DEL-04-01, DEL-01-01). It is the continuation
  proposed in [THIRTY_PERCENT_REVIEW.md](../../THIRTY_PERCENT_REVIEW.md#proposed-post-30-continuation-and-handoff),
  now selected by the owner's steering.
- **Completion conditions:**
  1. Each node below has produced its identified, versioned contribution in
     the owning deliverable's `Design/` folder, stating what it serves
     (OUT/REQ), what it consumed (by version), and what remains `UNRESOLVED`
     with owner and point of need.
  2. Each CASE-002 join in scope has an actual receiver comparison recorded
     (which version the receiver has, what check it performed, what remains
     absent) — Open_Questions Q-03.
  3. Owner decisions requested in [DECISIONS_PENDING.md](../../AgentRuns/APP-V4-FIRST-INCREMENT-20260928/DECISIONS_PENDING.md)
     are either applied or explicitly left open at their points of need.
  4. The SWBPIPE relay packet is updated with concrete interface questions;
     delivery/adoption is recorded only if actually observed.
  5. DAG-001 currency re-checked; any changed relationship routed through
     `project-dag` departure (none expected).
  6. Independent review, bounded closeout, central receipt, MEMORY rows and
     the final PR merged.
- **Excluded:** SWBPIPE construction and host evidence (external session, human
  relay); PEC and Domains work; product implementation beyond bounded spikes
  that resolve a design question; live witnesses, qualification, lifecycle
  CHECKING/ISSUED, SCC closure, DAG successor, fallback replacement.
- **Route through DAG-001:** roots DEL-04-01 and DEL-01-01 (level 0, admitted
  suppliers of ~20 consumers) → CASE-002 members at level 1 (DEL-03-01/02/03,
  DEL-02-01/03, DEL-04-02, DEL-05-01/02) → level 2 (DEL-04-03, DEL-09-09) →
  DEL-09-06 and DEL-03-04 (integrating consumers). CASE-002 candidate arcs are
  non-gating; they organize co-development and receiver comparisons, not
  readiness verdicts.
- **Owner decisions:** [OWNER_DECISIONS.md](../../AgentRuns/APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md)
  — Option A; OI-001 five reserved acts; OI-002 App user setting / none in
  hosts; OI-012 pin `0.158.0` with spike W11. Remaining open: OI-003, OI-008,
  OI-009, OI-013, OI-014, OI-018, OI-021.

## Deliverable scope (Option A — selected by owner decision D1)

| Deliverable (SoW sha256 prefix) | What exists | What this undertaking produces | Nodes |
|---|---|---|---|
| DEL-04-01 (`fc1a0503`) | INITIALIZED SoW | Act taxonomy; autonomy-grant model with `UNRESOLVED` classes; consumer map; fixture catalogue | W1 |
| DEL-04-03 (`74d42c38`) / DEL-04-02 (`23a28caa`) | INITIALIZED SoWs | Run/act record semantics, receipt links, lapse; settings-in/record-out exchange; standing model | W2 |
| DEL-03-01 (`179a6d35`) / DEL-03-02 (`42328987`) | INITIALIZED SoWs | Catalog C and read-basis semantics; proposal P lifecycle, outcomes, stale/no-retarget/one-effect | W3 |
| DEL-02-01 (`080d7f5a`) | INITIALIZED SoW | Portable declaration draft (inputs, tools, checkpoints, outputs, evidence, source identity); responsibility map | W4 |
| DEL-05-01 (`6fbbb580`) / DEL-05-02 (`5c554956`) | INITIALIZED SoWs | Loop boundary (messages/tools/events/checkpoints), validation order, endpoint/key cases; panel interaction trace and receiving cases | W5 |
| DEL-01-01 (`eddd122c`) | INITIALIZED SoW | Version-independent stdio/process boundary, request-register interface, OI-008 allocation proposal, recorded-exchange method; then pin spike | W6, W11 |
| DEL-02-03 (`9a921ba5`) | INITIALIZED SoW | Required-tool compatibility report, checkpoint hold state machine, transfer trace | W7 |
| DEL-03-03 (`5ac5db97`) | INITIALIZED SoW | Transport-neutral enablement account and consumer fixture inventory | W8 |
| DEL-09-06 (`511f2c00`) / DEL-09-09 (`082db8fa`) | INITIALIZED SoWs | Draft increment contract with operation placeholder (OI-021); relay question file; EXM-24/25 case inventories | W9 |
| DEL-03-04 (`203c0928`) | INITIALIZED SoW | Receiving matrix and new-host checklist integrating the above | W10 |

Option B would add the standalone-App definitions (DEL-01-02…05, DEL-02-02,
DEL-02-04) as a Wave 3; otherwise they are the natural next undertaking.

## Work

States: PLANNED, READY, ACTIVE, BLOCKED, UNCERTAIN, COMPLETE.

| ID / outcome | Deliverables and write scope | Needs / why | Completion check | State / result |
|---|---|---|---|---|
| W0 Graph, briefs, decision package | This folder; `AgentRuns/<RunID>/` | Steering; DAG-001 current (manifests pass at `6e18505e3`) | Graph committed on branch | COMPLETE `8d3c66542` |
| W1 Human-act and operation-policy distinction contract v0.1 | DEL-04-01 `Design/` only | Accepted basis only (PRD §4.5, HI §§4–7, d3) | Header complete; S1–S12 traced; `UNRESOLVED` shape; fixture catalogue | COMPLETE (v0.1) — `DEL-04-01/ACT-POLICY-v0.1` |
| W2 Record semantics and autonomy/standing exchange v0.1 | DEL-04-03, DEL-04-02 `Design/` only | Accepted basis; act kinds by accepted names (reconciled with W1 in V1) | Header complete; lapse rule; outcome `unknown`; M3 exchange examples | COMPLETE (v0.1) — `DEL-04-03/RS-v0.1`, `DEL-04-02/AS-v0.1` |
| W3 Catalog C and proposal P semantics v0.1 | DEL-03-01, DEL-03-02 `Design/` only | Accepted basis; coupled pair co-developed (CASE-004 lineage) | REQ-002 fields; four basis elements; HI-23 lifecycle; M3-CP comparison design | COMPLETE (v0.1) — `DEL-03-01/C-v0.1`, `DEL-03-02/P-v0.1` |
| W4 Portable workflow declaration v0.1 | DEL-02-01 `Design/` only | Accepted basis; Root workflow format as reuse source; C/act refs by name | Declared-part draft + examples; responsibility map rows | COMPLETE (v0.1) — `DEL-02-01/WD-v0.1` + examples |
| W5 Loop and panel receiving needs v0.1 | DEL-05-01, DEL-05-02 `Design/` only | Accepted basis; C/P/record refs by name | Four-subject boundary; case matrices; interaction trace | COMPLETE (v0.1) — `DEL-05-01/LOOP-v0.1`, `DEL-05-02/PANEL-v0.1` |
| W6 Codex hosting boundary (version-independent) v0.1 | DEL-01-01 `Design/` only | Accepted basis; no pin | Boundary invariants; request register; OI-008 proposal; fixture/upgrade method | COMPLETE (v0.1) — `DEL-01-01/HOSTING-BOUNDARY-v0.1`; OI-008 proposal O-1 |
| V1 Receiver comparisons, M1 joins (V1-A policy, V1-B C/P/record, V1-C workflow/loop/panel) | Run folder `comparisons/`; read-only on Design | W1–W6 returned | Each join: version received, check performed, disagreements, absent | COMPLETE — [V1-A](../../AgentRuns/APP-V4-FIRST-INCREMENT-20260928/comparisons/V1-A.md), [V1-B](../../AgentRuns/APP-V4-FIRST-INCREMENT-20260928/comparisons/V1-B.md), [V1-C](../../AgentRuns/APP-V4-FIRST-INCREMENT-20260928/comparisons/V1-C.md): 4 BLOCKING, 37 MAJOR, 35 MINOR; 24 register findings → C1/D0 |
| R1 Repair to v0.2 against V1 findings | Same Design folders | V1; [R1_RESOLUTIONS](../../AgentRuns/APP-V4-FIRST-INCREMENT-20260928/R1_RESOLUTIONS.md) | Findings dispositioned; affected comparisons rechecked at IR1 | COMPLETE (v0.2 × 9 files); cross-file items → [R2_CANDIDATES](../../AgentRuns/APP-V4-FIRST-INCREMENT-20260928/R2_CANDIDATES.md) |
| P1 PR-1: graph + decision package | Graph, run folder | W0 | Folded into PR-2 (graph pushed on branch early) | COMPLETE (folded) |
| P2 PR-2: Wave-1 definitions + comparisons + reviews | W1–W6, V1, R1, IR1, R2, R3, V2 outputs | V2 verdict MERGE (0 BLOCKING); CI green | PR merged under standing Git authority | COMPLETE — [#1039](https://github.com/sgttomas/chirality/pull/1039) merged; CI 9/9 passing; review V2 at `ba0b37123` (later commits were records only) |
| W7 Workflow execution compatibility v0.1 | DEL-02-03 `Design/` | Wave-1 v0.3 at `ba0b37123` | Compatibility report, checkpoint hold, transfer trace; resolves the W7-held items | ACTIVE |
| W8 External-agent adapter enablement account v0.1 | DEL-03-03 `Design/` | Wave-1 v0.3 at `ba0b37123` | Enablement states; policy cases; transport-neutral fixtures; MCP/CLI open-choice register | COMPLETE (v0.1) — `DEL-03-03/ADAPTER-v0.1`; 12 relay questions (XQ); findings F-1…F-12 → A1 / C1; U-X2 data boundary → owner |
| W9 Connected activity draft contract + relay questions; EXM-24/25 inventories | DEL-09-06, DEL-09-09 `Design/`; `_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` (question section only) | W3, W4, W5, W7, W8 | Operation placeholder per OI-021; relay file ready for human | PLANNED |
| W10 Host receiving matrix and checklist | DEL-03-04 `Design/` | W1–W9 | Every receiving-map row cites a contribution version or `UNRESOLVED` | PLANNED |
| W11 Codex pin spike | DEL-01-01 `Design/` + generated types location | Owner decision D4 (OI-012) — given | Types generated at pin; observed protocol facts vs published claims | COMPLETE — `DEL-01-01/PIN-SPIKE-v0.1`; 18 findings into DEL-01-01 v0.2 |
| A1 Wave-1 residual sweep (V2 MAJOR-1, m-1…m-13) | Wave-1 `Design/` files | V2 | Residuals fixed or carried with reason | PLANNED |
| V2 Wave-1 consistency check | `reviews/V2.md` | R3 at `ba0b37123` | Verdict | COMPLETE — MERGE AS v0.3 DRAFTS |
| V3 Receiver comparisons, Wave 2 | Run folder | W7–W10, A1 | As V1 | PLANNED |
| IR1/IR2 Independent review | Read-only; `reviews/IR1-*.md` | P2 / P3 candidates | Findings resolved or dispositioned; R2 alignment pass | IR1 ACTIVE |
| P3 PR-3: Wave-2 definitions | W7–W11, V2 | IR2 | PR merged | PLANNED |
| D0 DAG currency recheck | Read-only | P3 | Manifests; any relationship change routed to project-dag | PLANNED |
| C1 Bounded closeout (`chirality-root:bundled:workflow:bounded-reconciliation`) | Affected DEL `_REFERENCES.md`/`_STATUS.md` as authorized; CASE-002 pointer | P3 | Commitment↔result both directions | PLANNED |
| M1 MEMORY rows | Affected `MEMORY.md` | C1 | Terse rows → receipt | PLANNED |
| RC Central receipt | `AgentRuns/<RunID>/RECEIPT.md` | C1 | Result/checks/limits | PLANNED |
| F1 Final PR | All | C1, M1, RC, review | Final PR merged | PLANNED |

**Conventions for all Design artifacts.** Each file opens with a contribution
header: contribution ID and version (e.g. `DEL-03-01/C-v0.1`), status
`DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted`,
served OUT/REQ IDs, basis (repo commit, SoW hash, accepted-doc sections),
consumed inputs by version (or "accepted basis only"), and an `UNRESOLVED`
table (item, owner, point of need). Definitions are representation-neutral:
no wire field names, transport, hash algorithm, persistence or shared-component
placement are selected (SoW TBDs; OI-013/OI-014; DEL-03-01 TBD-003). Unruled
policy values appear as `UNRESOLVED{OI-nnn}`, never as a permission.

## Current state and recovery

- Checked basis: `main` at `6e18505e3`; DAG-001 `MANIFEST.sha256` and
  `SOURCE_MANIFEST.sha256` both pass; no `PKG-*` change since acceptance merge
  `7535bd7e`.
- Next work: W7 running. When it returns: W9 (connected activity + relay
  consolidation) ∥ A1 (Wave-1 residual sweep incl. W7/W8 findings); then W10
  (guide); V3; PR-3; then owner question on the App-conversation data boundary
  (U-X2 / DEL-03-03 F-12); D0; C1; M1; RC; F1.
- Local/unmerged work: branch `claude/chirality-app-v4-60-percent-a41fd5`
  (worktree `.claude/worktrees/test-ci-optimization-f6cacd`).
- Active operations: see run folder `DISPATCH.md`.
- Graph maintainer: HELP_HUMAN, this session.
- Open deferrals: V2 residuals ([reviews/V2.md](../../AgentRuns/APP-V4-FIRST-INCREMENT-20260928/reviews/V2.md)):
  MAJOR-1 (T15 grant re-point in DEL-04-01/02/03, DEL-05-02, WD EXAMPLES) and
  MINOR m-1…m-13 (fixture naming, R3-1 class in DEL-04-02/03, OP-C10 class in
  EXAMPLES, R3 citations in headers, closing "to be confirmed at V2" markers).
  Owner: node **A1**, a Wave-1 alignment sweep in PR-3 before V3.
- SWBPIPE relay (DEP-001, OI-021) not delivered; local
  `codex` CLI install (0.130.0) is broken (missing vendor binary; the user's own
  tool, not changed by this run). W11 observation for owner/DEL-01-05: a fresh
  Codex 0.158.0 home fetches `openai/plugins.git` at app-server start with no
  sign-in (S-F-10). Scratch install `<scratchpad>/codex-0.158.0` holds the TS
  output; retain until IR1, then delete.
- Current graph ref: branch above until PR-1 merges.

| Completed work / node | What changed and was checked | Unresolved consequence |
|---|---|---|
| W0 | Graph, briefs, decision package committed `8d3c66542` | PR not yet opened (graph travels with PR-2) |
| W1–W6 | v0.1 Design files, fences verified | V1 comparisons; R1 applies D2/D3 |
