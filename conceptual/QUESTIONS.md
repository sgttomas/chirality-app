# Consequential product questions

Standing: **proposed choices (agent) awaiting the owner.** Each question
states why it matters, the alternatives with their consequences, the agent's
recommendation where it has one, the evidence that would settle it, and the
point by which an answer is needed. Answers are recorded in the owner's words
in [`DECISIONS.md`](DECISIONS.md); this file then records the disposition.
Exemplar (`X-`), lesson (`L-`) and tension (`N-`) references point to
[`EXEMPLARS_AND_LESSONS.md`](EXEMPLARS_AND_LESSONS.md).

## Dispositions after the owner's answers (2026-09-25)

The owner's words are recorded in [`DECISIONS.md`](DECISIONS.md) (D-01…D-15).

| Question | Status | Follow-up |
|---|---|---|
| Q-01 nucleus | Open — corrected (D-01) | Revise the working statement with the owner: the standalone app is the App for Creating Workflows and the exemplar; workflows, skills and tools are made in each application for its needs; the same four agents apply everywhere |
| Q-02 host integration | Settled — option D (D-02) | Topology and panel surface follow the supplier experiments |
| Q-03 workflow | Settled — option C (D-03) | Define the declared part in the PRD |
| Q-04 autonomy | Settled — option B (D-04) | Confirm two points the words leave open: whether harness classifier approval modes are an acceptable user choice, and whether one invariant holds everywhere — an agent never originates or represents a human act (acceptance, checked mark, approval) in the human's name |
| Q-05 supplier | **Settled (D-19, amended by D-20)** | Chirality App: stock Codex App Server, pinned, run from the App's own process, Tauri + React/Vite. Hosts: minimal Chirality loop over Chat Completions, local model server by default, Pi as the upgrade path. Revisit for v5.0 |
| Q-15 distribution | Settled (D-06) | Mac first; OAuth, API key and local model, possibly all at once — check against vendor terms (T7, T8) |
| Q-06 records | Settled — proposal (D-07) | — |
| Q-07 users and hosts | Partly settled (D-08) | PEC and Domains are independent connectors the App consumes; T9 returned — see `DISCUSSION_2026-09-25.md` §5 for the proposed reading and three questions (what "Domains" means). Confirm SWBPIPE and the standalone app as the essential hosts |
| Q-08 project management | Settled — option B (D-09) | The owner signals more scope: to discuss |
| Q-09 roles | Settled (D-10) | — |
| Q-10 replacement | Settled — (b) building on (a) (D-11) | — |
| Q-11 build method | Open — owner's proposal (D-12) | Discuss: agents follow the Project Management manual according to the Agents User Manual, within the retained decomposition, execution structure and graph-traversal loop |
| Q-12 review | Settled (D-13) | Codex reviewer when the seed is ready; Claude on a different model as fallback |
| Q-13 archives | Settled; done (D-14) | Clone made, verified, read-only |
| Q-14 v3 examination | v3.0.1 installed and open (D-15) | Stage E1 |

Questions Q-01 to Q-08 and Q-15 (placed after Q-05, which it informs) shape
the PRD. Q-09 to Q-14 are narrower and can be answered briefly or deferred.

---

## Q-01 The product's nucleus

**Why it matters.** Every other section of the PRD follows from it.

**Proposed working statement** (agent synthesis of the owner's words, §1 of
the exemplars file):

> Chirality lets professionals direct agents through reusable workflows inside
> the applications where their work lives. Agents act on the same objects
> through the same operations as the professional; the professional checks,
> decides and remains accountable; what works is kept as workflows to reuse
> and improve.

The v3 core loop (plan → execute → save → reuse → iterate; "direct and
validate knowledge work") is kept in purpose; what moves is its location — into
host applications, with the standalone app as the place methods are made.

**Alternatives.** Accept as the working nucleus; amend it; or state a
different centre (for example, "a coordination layer for agent fleets" with
host integration secondary).

**Recommendation.** Accept or amend. **Needed by:** the start of PRD drafting.

---

## Q-02 What a host application integrates

**Why it matters.** It fixes the product boundary: what Chirality supplies,
what each host supplies, and what the supplier harness supplies (OD-03,
OD-04).

| Option | What it means | Consequences |
|---|---|---|
| A. Controller outside the host | An agent session (the standalone app or another harness client) drives the host through the host's typed tools or CLI; no agent interface inside the host | Cheapest; matches SWBPIPE's current path ("Codex controller first; embedded agent follows"). The engineer works in two windows; no in-host conversation, queue or checks |
| B. Embedded service | The host starts and owns a local Chirality service that runs the harness and workflows; the host shows a Chirality panel (conversation, workflow, proposal queue, checks) beside its own object overlays (proposed rows, origins, checked tags) | Matches the owner's 2026-09-12 intent and the SWBPIPE collaborative surface (X-07, X-11). Needs packaging per host (no Tauri packaging exists) and a live proof (L-09) |
| C. Embedded library | Chirality as an in-process library in each host's language | Blocked for a Tauri/Rust host with a Node harness (X-11); would need a Rust-native harness or re-implementation |
| D. One contract, two routes | Define a single host-integration contract — typed objects, reads, previews, proposals, receipts, basis binding (X-08) — used first by an outside controller (A) and then by the embedded panel (B) | The contract becomes the core of the product; topology stays an architecture choice tested in Stage E3 |

**Recommendation.** D, with B as the leading embedded topology pending the
supplier investigation. The panel itself could be host-native components,
or a standard surface such as an MCP Apps panel or an AG-UI event stream
(T7 §2); that choice follows the experiments. **Evidence that would settle the topology:** a
disposable spike hosting a candidate harness beside a Tauri shell with two
application tools (Stage E3). **Needed by:** the PRD's boundary section (the
contract); the architecture basis (the topology).

---

## Q-03 What a "workflow" is in v4

**Why it matters.** Workflows are the primary expression (OD-04). In an
engineering host, the owner's "prescribed workflow gates" need to be real
(N-4, L-04).

| Option | What it means | Consequences |
|---|---|---|
| A. Method guidance (v3) | A prose package the agent reads and follows; gates exist as instructions | Flexible and conversational to author (X-02); gates depend on agent compliance |
| B. Structured, executed definition | Steps, tools, typed inputs and outputs, and gates run by a Chirality workflow engine; agents fill judgement steps | Enforceable and repeatable; heavier to author; v3 deliberately excluded an execution engine |
| C. Method guidance with declared checkpoints | Prose method plus a small declared part: the inputs it expects, the host tools it needs, the points where a human act is required, and the outputs and evidence it returns — which the host and Chirality can observe and enforce | Keeps conversational authoring; makes gates and required tools checkable by the host; no general workflow engine |

**Recommendation.** C. **Needed by:** the PRD's capability section.

---

## Q-04 Agent autonomy and human acts inside hosts

**Why it matters.** It is the practical meaning of "shared access does not
transfer human decision rights" (OD-05), and two owner statements pull in
different directions (N-3): near-parity autonomy with prescribed gates
(2026-08-01) and row-by-row acceptance of agent edits in SWBPIPE (2026-09-17).

| Option | What it means |
|---|---|
| A. Proposal always | Every agent change to host objects is a proposal the human accepts (row, several rows, or batch) |
| B. Graduated | The workflow or the human sets what the agent may apply directly, per operation class and consequence, with origin marks, undo and later checking; human acts are required at declared gates |
| C. Proposal always at first, graduated by design | Ship A in the first host; shape the contract so B can be enabled per project and per workflow later |

**Recommendation.** C. **Also asked:** may a harness's model-classifier
approval mode (T7 §4) ever resolve a request on the human's behalf, and if
so for which classes of operation? And which acts are always reserved to the
human in every host — for example accepting a change to the engineering
model, marking work checked, issuing a report, and any act of reliance or
approval? **Needed by:** the PRD's interaction and decision-rights sections.

---

## Q-05 Supplier stance for the seed

**Why it matters.** OD-03 asks for actual suitability before selection. The
incumbent (a stock Codex App Server) worked for v3 (X-13) but carries
observed constraints (tool catalogs fixed when a conversation starts;
instruction changes need a cold resume; commercial terms for embedding with
a consumer sign-in recorded as unconfirmed). Root `AGENTS.md` still states
"For the App MVP, Codex is the sole engine qualification and release target"
(N-5).

| Option | What it means | Consequences |
|---|---|---|
| A. Select now | For example, continue with the incumbent | Least change; its constraints become v4 constraints |
| B. Require, shortlist, then select | The seed states the behaviour v4 needs from a harness and a shortlist; selection follows disposable experiments before FEED; the incumbent is the reference | The seed can be accepted without a supplier; architecture work waits on the experiments |
| C. Harness-neutral layer | Build an adapter layer so several harnesses can be used | The pattern v1/v2 paid for (L-05) |

**What the landscape scan found** (T7, vendor documentation and releases
retrieved 2026-09-25; to be confirmed by experiment before any fitness claim):

- Every major vendor now ships an embedding surface: the Codex App Server (a
  native binary speaking JSON-RPC over stdio — plausibly a Tauri sidecar), the
  Claude Agent SDK (a TypeScript or Python library around a bundled binary; no
  Rust SDK), and the GitHub Copilot SDK (includes Rust; bring-your-own-key).
  Open harnesses (Pi, goose, OpenHands, OpenCode) are permissively licensed
  and differ widely in how much approval and delegation they provide.
- Credentials and billing are the least stable facts. Anthropic's documentation
  says third-party products may not offer claude.ai login without approval
  (API keys instead). Using a ChatGPT plan inside third-party harnesses is
  reported as tolerated practice, not a contractual permission.
- Both leading harnesses offer approval modes in which a model classifier
  decides (`auto`; `auto_review` / `guardian`). This bears directly on Q-04.
- Vendor desktop computer-use features are tied to the vendors' own apps and
  are not available through their embedding surfaces; API-level computer use
  and accessibility-tree tools are.
- The protocol layer is consolidating: MCP (stateless core, Tasks, MCP Apps
  for interface panels rendered by the host), ACP (editor-to-agent), AG-UI
  (application interface events). Seven disposable experiments are proposed
  in T7 §5.

**Recommendation.** B. The agent reads the Root Codex clause as scoped to the
v3 App MVP; if v4 selects differently, the clause needs a Root instruction
change with its own scope. **Also asked:** is local-model operation (on the
user's machine or an organisation server) a v4.0 requirement or later? A peer
agent reported it as "central to the premium feature after MVP" for SWBPIPE
(`…/OWNER_CLI_PROTOCOL_DISPOSITION_PEER_2026-09-20.md`, reported, not
verbatim). **Needed by:** the architecture basis; selection before FEED.

---

## Q-15 Distribution and whose credentials pay

**Why it matters.** Vendor terms turn on it (Q-05), and so does the
professional record: engineering data may leave the machine through the
model provider.

Will v4 and SWBPIPE-class hosts go to other engineers (the owner's release
stance is open source once the paradigm is established, AT §1 item 6)? If so,
whose model access do they use: each user's API key, an organisation
account, each user's consumer subscription, a local model, or a mix? Is
macOS-only acceptable for v4.0? **Recommendation:** decide the intended
distribution for v4.0 now (even "owner's own use first" is a useful answer);
the credential model then follows. **Needed by:** the supplier requirement
statement (Stage E3).

---

## Q-06 Where authoritative records live

**Why it matters.** Root doctrine keeps authority in files and Git; hosts keep
domain truth in their own stores; harnesses keep conversations in theirs
(N-2). Reliance later depends on being able to reconstruct what was supplied,
done and decided.

**Proposal.** Host domain truth stays in the host (SWBPIPE's project store).
Workflow definitions, owner decisions and accepted records are ordinary files
in the user's project or workspace. Harness session stores are operational,
not authority. Each workflow run leaves a compact record, kept with the host
project, that links the host's own receipts and hashes rather than copying
them.

**Alternatives.** Files-only authority with host exports; or the host store
as authority for everything done in the host.

**Recommendation.** The proposal. **Needed by:** the product vocabulary and
state document.

---

## Q-07 Users and hosts the seed must describe

**Why it matters.** The PRD must walk connected activities in the hosts
essential to its claim (successor-basis guide).

Candidate personas: (1) the practitioner in a host (the stress engineer in
SWBPIPE); (2) the workflow maker (standalone); (3) the application builder
who integrates Chirality into a new app; (4) the coordinator of an agent
fleet.

**Recommendation.** SWBPIPE and the standalone app are the essential hosts;
personas 1 and 2 are primary; persona 3 is served through the integration
contract (Q-02) and described; persona 4 through Q-08. **Also asked:** is any
other host essential to v4.0 (PEC dashboards, office documents such as
spreadsheets, another engineering application)? **Needed by:** the PRD's
users and activities.

---

## Q-08 Project-management capability

**Why it matters.** OD-06 says these needs arise from coordinating agents at
scale. The manuals describe the practices; PEC was redirected on 2026-07-24
from a human-team project tool to a coordination plane for "the owner plus an
agent fleet" (agent summary of owner direction, D-PEC-57); the manuals have
no estimation or risk practice (T2 §2).

| Option | What it means |
|---|---|
| A. Method only | Coordination stays a development method (manuals), not a product feature |
| B. Product capability for the owner and an agent fleet | In the standalone app: delegation with briefs, one current work graph per undertaking, a queue of returns awaiting examination, decision packages that name the act, status across sessions — all derived views of file truth (X-15–X-18) |
| C. B plus team coordination inside hosts | For example, review workflows across an engineering project with several people |

**Recommendation.** B for v4.0; C later. PEC stays a separate project that v4
may consume. **Needed by:** the PRD's capability section.

---

## Q-09 Roles in the product

The four roles are v3 product relationships and Root development roles.
**Options:** keep all four visible everywhere; show roles in the standalone
app (method making, coordination) and let them recede in hosts behind a
single agent seat and workflows; or drop roles from product vocabulary.
**Recommendation:** the middle option. **Needed by:** the interaction section.

## Q-10 Conditions for v4 to replace the v3.0.1 fallback

**Proposal:** (a) the standalone core loop at least at v3.0.1's level —
plan, execute, save and reuse a workflow, approvals, interruption, restart;
(b) one live embedded journey in SWBPIPE from request to human acceptance;
(c) a stated position on existing users' workflows and chats (migrate,
import, or leave). **Needed by:** the seed's conditions for further work.

## Q-11 Weight of the v4 build method

The implementation session sets its own method (OD-13); the lessons show the
cost of heavy machinery (L-02–L-07). **Proposal:** the seed includes a short
operating-methods note naming the purposes of selected practices, the
feedback that would show they help, and a proportion rule (keep Git and
reviewed PRs, independent review of identified candidates, one current work
graph, decision records for owner acts; avoid duplicate evidence systems and
registers nobody reads). **Alternative:** leave method wholly to the
implementation session.

## Q-12 Independent review of the seed set

A same-model reviewer adds no model diversity (manuals). **Options:** a
separately prepared Claude reviewer in this environment; a Codex reviewer
(the Codex CLI is installed here; it would run on the owner's account and
needs the owner's consent); or a reviewer the owner arranges.
**Recommendation:** a Codex reviewer with consent, otherwise a separately
prepared Claude reviewer on a different model.

## Q-13 Archive protection

The Git-ignored archives exist in one place and `git clean -X` in the
original checkout would delete them. **Option:** make a copy-on-write APFS
clone (near-zero extra space) outside the repository, for example
`/Users/ryan/ai-env/archives/chirality-2026-09-25/`, and add it to the digest
check. **Yes or no.**

## Q-14 Hands-on examination of v3

The installed copy is **v3.0.0**; the fallback is **v3.0.1**. If Stage E1 is
wanted, should the agent update the installed copy to v3.0.1 (a 340 MB
download from the release page), and may it operate the app through computer
use, or should the owner drive while the agent observes?
