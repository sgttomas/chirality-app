# Working record — V4-CONCEPT-20260925

Standing: **working record (agent).** Position, basis, delegation and open
work of the conceptual undertaking. Revised in place as the work proceeds;
Git history keeps earlier states.

## Assignment

| Field | Value |
|---|---|
| Undertaking | Chirality App v4 conceptual undertaking (OD-01) |
| Owner | Ryan Tufts (the human accountable for acceptance) |
| Active role | HELPS_HUMANS (Type 1), engaged directly by the owner |
| Selected workflow | `chirality-root:bundled:workflow:reverse-engineer-software` (bundled; no project or user workflow of that name exists, so no collision) |
| Brief | [Opening brief](../execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/OPENING_BRIEF.md), 2026-09-25; directions in [`DECISIONS.md`](DECISIONS.md) |
| Host | Claude Code desktop, model Claude Opus 5.5; worktree `chirality-app-v4-architecture-9f35c4`, branch `claude/chirality-app-v4-architecture-9f35c4` |
| Working root | `projects/chirality-app-v4/` (did not exist before 2026-09-25) |
| First completion boundary | An independently reviewed seed set presented for acceptance (OD-12) |

## Instructions and methods actually supplied

SHA-256 of the bytes at the investigation revision `2b0572fe0`.

| Item | Origin | SHA-256 | How it entered |
|---|---|---|---|
| Root `AGENTS.md` (imported by `CLAUDE.md`) | Root | `c8ce87ef342902cb081bc659b26fc9a4edda1b6dba513814e5cb1e14e0b1dffd` | Host project instructions |
| `CLAUDE.md` | Root | `336cc4fbf19beaada7ccf9986414fa91851a8d7a07dfb3ccbe800a69eed0ab49` | Host project instructions |
| `agents/AGENT_HELPS_HUMANS.md` | Root | `a0c9fb9443d8671d694c1f7b24ff3c402ffd626c781a2739342c938f2f3c3d1e` | Read on selection |
| `workflows/reverse-engineer-software/WORKFLOW.md` | Root, bundled | `51b99054ac6d93989ab6a427ef3867d602a03832583104789bfbe5dfc601c9f7` | Read on selection |
| `…/resources/successor-basis.md` | Root, bundled | `7fc969aa7ee61886576b1eb4dddcd1d45b9c6e47bf7625b89c472dff611e37a7` | Read for the output guidance |
| `…/resources/worked-example.md` | Root, bundled | `e337148a5c29918d2daa1b56f9a4ad4bcbea3bd63f4202b37654061bd6441d90` | Hashed, not loaded (optional) |
| `.agents/skills/chirality-change/SKILL.md` | Root, project skill | `2b490e172436417896c1cd25dbcd543c676e3473aa58b7663985d75785ff7dba` | Read for Git and PR conventions |

No other role's instructions were consulted.

## Delegation

Seven read-only TASK investigations were dispatched in parallel through the
host's native subagent mechanism (Claude Code background agents; parent:
this HELPS_HUMANS session). Each brief stated a read-only boundary; the
boundary was instruction-asserted, not host-enforced (the children had the
host's general tools). Briefs and returns are preserved verbatim in
[`tasks/`](../execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/tasks/),
extracted programmatically from the host's transcripts.

| Task | Subject | Model | Dispatched → returned (UTC) |
|---|---|---|---|
| T1 | Thesis and owner notes | claude-opus-5-5 | 19:58:39 → 20:03:57 |
| T2 | Manuals and practice | claude-opus-5-5 | 19:58:39 → 20:06:40 |
| T3 | App v3 (fallback line) | claude-opus-5-5 | 19:58:39 → 20:12:07 |
| T4 | App history and archives | claude-opus-5-5 | 19:58:39 → 20:11:19 |
| T5 | Runtime, PEC, Root program | claude-opus-5-5 | 19:58:39 → 20:09:25 |
| T6 | SWBPIPE as host | claude-opus-5-5 | 19:58:39 → 20:10:23 |
| T7 | Supplier landscape (web) | claude-opus-5-5 | 20:03:40 → 20:23:26 |
| T8 | T3 Code suitability, including local models (web, GitHub read-only) | claude-opus-5-5 | 2026-09-26 05:07:31 → 05:22:57 |
| T9 | PEC and Domains as connectors | claude-opus-5-5 | 2026-09-26 05:07:31 → 05:16:51 |
| T10 | Pi libraries: browser use, data behaviour, stability (read-only) | claude-opus-5-5 | 2026-09-26 06:22:04 → 06:35:54 |
| T11 | v3 Runtime responsibilities and frontend reuse (read-only) | claude-opus-5-5 | 2026-09-26 06:22:05 → 06:35:07 |

Notes on the returns:

- The host flagged T4's and T7's returns for an instruction-shaped pattern
  ("bypass-permissions"). On inspection both describe permission modes (v1's
  historical default mapped to `bypassPermissions`; the Claude Agent SDK's
  documented modes); findings, not instructions.
- T7's web claims are vendor documentation, release notes or third-party
  reports retrieved 2026-09-25; some reached it only as tool summaries and are
  marked so. None has been tested locally.
- HELPS_HUMANS checked the load-bearing claims used in the questions against
  their primary files (application-tool design; the A2 Tauri rationale; the
  owner's 2026-09-11/12 words; D-APP-87; D-PEC-57; the peer-reported
  local-model intent; the 1,044 / 3,217 census). One refinement: the D-PEC-57
  line about a "human-used project-management tool" is an agent's summary of
  the owner's direction, and is cited as such.
- T8 reported one boundary deviation: it wrote a temporary path-and-size
  listing of the T3 Code repository tree (about 1.7 MB) into this session's
  scratchpad, outside the repository, despite a no-local-files brief. No
  other file was created or changed. The listing is scratch material and is
  not part of the record.
- All returns and the synthesis are same-family model work; none of it is
  independent review.

## Work performed (2026-09-25)

1. Inspected existing state: no `projects/chirality-app-v4/`; clean worktree
   at `2b0572fe0` = `origin/main`.
2. Pinned the investigation revision and the v3.0.1 fallback
   ([`REFERENCES.md`](../reference/REFERENCES.md)).
3. Inventoried the Git-ignored archives, wrote a read-only digest tool, and
   recorded and verified digests for 19 locations and 57,073 files
   ([`ARCHIVES.md`](../reference/archives/ARCHIVES.md)). `sgttomas/chirality`
   is public, so the committed digests name nothing below the 19 locations
   (subtree keys are hashes of their paths); the tool was tested against a
   disposable fake root for added, changed and removed subtrees. The
   inventory and the TASK returns do name and briefly describe some archived
   documents, at the level the thesis and repository records already do.
4. Carried `docs/thesis/` forward byte-for-byte (19 files; blob identity and
   byte comparison matched) with a transfer companion
   ([`foundation/README.md`](../foundation/README.md)).
5. Read the thesis README, the Field Book, and the owner-words records
   directly; dispatched T1–T7.
6. Wrote the source inventory, exemplars and lessons, questions, and this plan.
7. Committed `3c37fe292`; the committed thesis tree equals the source tree
   object `47fc49e96c2931ba18090f1a82d56a49f230b3ee`. Pushed the branch.
8. Folded T7 (supplier landscape) into Q-02, Q-04, Q-05 and a new Q-15.
9. Received the owner's answers; preserved them exactly
   ([`OWNER_ANSWERS_2026-09-25.md`](../execution/_Coordination/AgentRuns/V4-CONCEPT-20260925/OWNER_ANSWERS_2026-09-25.md))
   and recorded D-01…D-15 in [`DECISIONS.md`](DECISIONS.md); added
   dispositions to [`QUESTIONS.md`](QUESTIONS.md).
10. Q-13: made the protective APFS clone of the archives, verified it against
    the recorded digests, and made it read-only
    ([`ARCHIVES.md`](../reference/archives/ARCHIVES.md)).
11. Q-14: requested computer-use access to Chirality v3.0.1 for an
    observation-only tour; the owner declined the access request. No
    interaction with the app occurred. Stage E1 awaits the owner's preferred
    arrangement.
12. Noted concurrent activity: `origin/main` moved 141 commits past the
    investigation revision (workflow repairs, PEC work). Of the sources this
    undertaking relies on, only `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md`
    and its README changed (link and wording updates after the retirement of
    `software-bounded-implementation` and the `preparation` workflow). The
    investigation revision stays `2b0572fe0`; the change matters to Q-11,
    since the User Manual moves with the Root workflow library.
13. The owner asked whether an agent on another machine (where oMLX runs)
    could run experiments from a brief; HELPS_HUMANS prepared the HX-01 brief.
    The owner then declined the tests (D-16) and made code maintainability the
    governing concern; the brief was marked withdrawn, never launched.
14. Verified the Agent Client Protocol's session, permission and MCP
    provisions from its documentation, and the adapters' and SDKs' licences,
    features and activity from their repositories (read-only), then wrote
    [`MAINTAINABILITY_ANALYSIS.md`](MAINTAINABILITY_ANALYSIS.md).
15. The owner rejected the ACP direction (D-17: maintainability first,
    functionality second; native harness functionality and native OAuth are
    essential). HELPS_HUMANS agreed the recommendation was wrong — it
    repeated the generic-vocabulary failure of D-GOV-43 finding 4 and traded
    certain functionality for hypothetical replaceability — and added §9 to
    the analysis with the revised direction.
16. The owner separated the two expressions (D-18): the full Codex experience
    in the Chirality App; a simpler, local-first, private agent with semantic
    parity in hosts. HELPS_HUMANS verified Pi's model and agent libraries
    (licence, local-provider and browser support, telemetry defaults) from
    its repository and added §10 to the analysis.
17. The owner accepted the two-tier direction as the v4.0 basis (D-19).
    HELPS_HUMANS dispatched T10 and T11 (reading only) for the architecture
    basis and wrote [`SEED_SET_PLAN.md`](SEED_SET_PLAN.md).
18. T10 and T11 returned. HELPS_HUMANS verified Pi's versioning and
    compatibility statements at source and the v3 topology record's A2
    premise, added §11 to the analysis (two choices for the owner), and
    wrote PRD draft 1 (`docs/PRD.md`).
19. The owner raised Windows and native-webview risk (M-06); HELPS_HUMANS
    answered in §11.3 and flagged SWBPIPE's Chromium-only end-to-end tests as a
    separate task, which the owner started in its own session. The owner then
    chose Tauri and the minimal loop (D-20).
20. Drafted the four companion documents (`docs/ARCHITECTURE.md`,
    `docs/HOST_INTEGRATION.md`, `docs/EXAMINATION.md`,
    `docs/OPERATING_METHOD.md`), completing draft 1 of the seed set, and
    corrected one gendered pronoun for the owner in the examination draft.
21. The owner handed the remaining work (revision, review, merge) to another
    session on 2026-09-26. This session's work ends at commit `54eb7d1bc`
    plus this entry: everything is pushed on branch
    `claude/chirality-app-v4-architecture-9f35c4`, not merged, with no pull
    request; the branch merges cleanly with `origin/main` as of this entry.

## Handoff to the next session

- **Take the whole folder, not only `docs/`.** The five drafts cite
  `conceptual/DECISIONS.md` (the owner's directions and decisions, D-01…D-20,
  quoted exactly), the analyses, `foundation/thesis/` and the run record.
  Build on this branch or merge it.
- **Read in this order:** `README.md`; `conceptual/DECISIONS.md`;
  `conceptual/SEED_SET_PLAN.md` (§3: the drafting defaults still pending);
  `docs/`; then this record's open work.
- **Before presenting for acceptance:** obtain the owner's answers to the
  pending items (Q-01, Q-04 two points, Q-07, Q-08 scope, Q-11 three
  questions); walk `docs/EXAMINATION.md` through the set; obtain independent
  review of the assembled candidate by a Codex reviewer, or Claude on a
  different model (D-13). The drafts here and any revisions by another Claude
  session are the same model family; neither is independent review.
- **Protected:** `foundation/thesis/` must stay byte-identical —
  `git rev-parse HEAD:projects/chirality-app-v4/foundation/thesis` must equal
  `47fc49e96c2931ba18090f1a82d56a49f230b3ee`. The Git-ignored archives and the
  read-only clone at `/Users/ryan/ai-env/archives/chirality-2026-09-25/` are
  read only (`reference/archives/ARCHIVES.md`).
- **Do not run** the withdrawn HX-01 brief (D-16).
- **Practicalities:** the repository is public; a pull request touching
  `projects/chirality-app-v4/` selects the full App and PEC CI suites because
  no routing rule covers the path; the Agent User Manual changed on `main`
  after the investigation revision (see `docs/OPERATING_METHOD.md` V4-OPS-11).

## Current position

Stage F: draft 1 of the seed set (`docs/`, five documents) is complete and
awaits the owner's review. Architecture direction is settled (D-16…D-20).
Still pending with the owner: the working statement (Q-01), two autonomy
points (Q-04), the meaning of "Domains" and the essential hosts (Q-07), the
further project-management scope (Q-08), and three operating-method
questions (Q-11). No PRD requirement is accepted yet.

## Open work

| Item | Owner | Condition |
|---|---|---|
| Discussion of Q-01, Q-04 follow-ups, Q-08 scope, Q-11 method | Owner with HELPS_HUMANS | Stage D |
| Confirm or correct the drafting defaults for the open items | Owner | [`SEED_SET_PLAN.md`](SEED_SET_PLAN.md) §3 |
| Owner's review of PRD draft 1 (`docs/PRD.md`) | Owner | Plan checkpoint 4 |
| Owner's review of draft 1 of the five seed documents, and the remaining pending items (Q-01, Q-04, Q-07, Q-08 scope, Q-11 questions) | Owner | Plan checkpoint 4 |
| Self-check walk of the examination scenarios through the set; repair | HELPS_HUMANS | After the owner's review |
| Independent review by a Codex reviewer (D-13) | HELPS_HUMANS, with the owner's Codex session | Stage G |
| Stage E1 arrangement (the owner drives, or grants access later, or skip) | Owner | When convenient |
| Stage E investigations selected by the answers | HELPS_HUMANS with TASKs | After D |
| Hosted CI routing has no rule for `projects/chirality-app-v4/**`, so a PR touching it selects full product coverage | Owner's choice whether to add a `records` route (a Root tooling change) | When CI cost matters |

## Next

Present the inventory, plan, questions and first exemplars to the owner;
record the answers; select Stage E work.


## Current continuation — 2026-09-26, after author handoff

The owner's later acts accept the identified composite seed basis and authorize App v4 decomposition/project definition. See [acceptance](../execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md) and exact later messages J–O. Earlier Draft1/pending/checklist and Next statements above preserve their historical position;they do not undo later acceptance. The new session preserves all76 handoff files before changing current working surfaces. The five seed documents were consolidated after the act and passed [independent substantive source-fidelity review](../execution/_Coordination/AgentRuns/APP-V4-DEFINITION-20260926/SEED_FIDELITY_REVIEW.md). Their administrative completion headers received a separate bounded backcheck; edit ownership has transferred to WORKING_ITEMS for integration. Group1 normalization remains a separate upcoming checkpoint;no structural/decomposition acceptance is inferred. Current work is owned in the [project-definition graph](../execution/_Coordination/WorkGraphs/APP-V4-PROJECT-DEFINITION-20260926/WORK_GRAPH.md). The withdrawn HX01 and unrun E1 remain unrun. SWB implementation stays outside this undertaking and coordination is relayed by the human.
