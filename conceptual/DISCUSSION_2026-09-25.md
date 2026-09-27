# Discussion — open items after the owner's answers (2026-09-25)

Standing: **proposals (agent) for discussion.** Responses to the items the
owner opened for discussion (D-01, D-04, D-09, D-12). Nothing here is
decided until the owner says so in `DECISIONS.md`.

## 1. The working statement (Q-01, D-01)

What the correction changes:

- The standalone app is **the App for Creating Workflows**. It is the
  exemplar of what then lives "in various guises" in each application.
- Each application has **its own** workflows, skills and tools, made for its
  needs and uses — they are not all authored in one place.
- **The same four agents** apply across all applications; no additional
  roles are planned, though they may come.

With the owner's Q-05 words — "the harness for the model needs to be the
least of my concerns. I'm building agentic engineering applications. There's
plenty to do for getting a generic harness to know the specifics of how
agents should act within and for a particular application" — the product's
distinctive work comes into focus: **making a general agent harness act well
within and for a particular application.**

Three candidate statements, each emphasising something different:

**A. What Chirality does for an application**

> Chirality makes a capable general agent work within and for a particular
> application. Each application carries its own workflows, skills and tools;
> the same four agents use them to act on the application's objects with the
> means the professional has, and the professional directs the work and
> validates it to the degree the situation warrants. The Chirality App, for
> creating workflows, is the exemplar each application follows.

**B. What the professional experiences**

> In a Chirality application, a professional works with four agents that can
> do what the professional can do in that application — guided by workflows,
> skills and tools made for its work. The professional directs, checks and
> decides; what proves useful becomes a workflow to reuse and improve. The
> Chirality App is where workflows are created, and the pattern the other
> applications share.

**C. Short form**

> Chirality turns capable agent harnesses into agentic applications: four
> agents, application-specific workflows, skills and tools, and a
> professional who directs and validates the work.

The agent's preference is **A** as the PRD's opening statement, with C as the
one-line summary. A keeps the three things the owner has insisted on — the
harness is not the product, the application is where the work is, and the
human validates — and names the standalone app's role exactly.

## 2. Autonomy follow-ups (Q-04, D-04)

Option B is settled: the user and the agent work out how to work together;
outputs are validated "to the degree warranted by the situation". Two points
the words leave open, stated as proposals to confirm:

1. **Classifier approval modes are a user choice.** A harness's mode in which
   a model classifier approves routine requests (T7 §4) is one of the ways
   the user and agent may choose to work, like any other permission setting.
2. **One invariant holds everywhere.** An agent never originates or
   represents a human act — acceptance, a checked mark, an approval, an act
   of reliance — in the human's name. Agents may prepare, propose, perform
   within what the user allows, and record; the human's own acts stay the
   human's. (This is Root governance already, K-AUTH-1; stating it in the
   PRD keeps option B from being read as permission to blur it.)

SWBPIPE's row-by-row acceptance then becomes one mode the host offers, not
the only one.

## 3. The build method (Q-11, D-12)

The owner's proposal: keep the decomposition and execution folder structure
and the graph-traversal development loop (teams, subagents or solitary work);
guide the work graphs by having agents **follow the Project Management manual
according to the Agents User Manual**.

### What the proposal gains

- **The manuals get the use they were written for.** OD-08 asks for practices
  to be tried again, examined through use and improved through feedback. T2
  found no project record citing the manuals as a working basis since
  publication. The v4 build would be their first real field test.
- **One coherent method instead of accreted loop instruments.** The lessons
  (L-02, L-06, L-07) came largely from machinery added layer on layer. A
  published method with a stated route (the Field Book) replaces that with
  one source.
- **Symmetry with the product.** Option B for project management (D-09) puts
  coordination of an agent fleet into the product. If the v4 build is run
  by the same practices, the product's project-management capability is
  exercised in its own development — possibly part of the "more to it" the
  owner mentioned.

### Conditions it needs to work

1. **Standing.** The manuals say of themselves that reading them "does not
   amend those instructions or adopt a new execution basis." To make them the
   v4 method, the v4 project's own instructions must adopt them explicitly,
   with a precedence rule: Root governance, then v4 project instructions, then
   the accepted v4 basis (PRD) for *what* to build, then the manuals for
   *how* to organise the work. Creating those project instructions is an
   instruction change with its own scope — naturally part of the
   implementation session's setup, with the owner's approval.
2. **Selective loading.** The Consolidated manual is about 69,000 words. The
   Field Book (about 2,600 words) can be the always-present route; its
   section references into the full manual are loaded when a step needs the
   reasoning; the User Manual supplies the repository application.
3. **Pinned editions.** The User Manual moves with the Root workflow library —
   it changed today alongside workflow repairs on `main`. The v4 project
   should name the manual editions it follows and adopt new ones
   deliberately, not drift with every edit.
4. **Purposes over mechanisms.** The full manual still names some
   repository-specific mechanisms. Where it names one the v4 project does not
   use, the purpose governs and the project records what it does instead.
5. **A feedback loop someone reads.** Agents note, briefly and at the work
   graph node where it happened, where a practice helped, did not fit, or was
   ambiguous. Those notes are reviewed with the owner at each stage gate and
   become manual revisions or deliberate departures. Without a scheduled
   reader, this repeats L-06.
6. **Enforcement from the host, not prose.** Write boundaries and delegation
   limits come from the harness's actual permissions and worktrees; the
   manual describes intent, independent review checks it.

### Questions for the owner

- Does "follow the manual" replace the current loop instruction files for v4
  entirely, or sit beside a thin project loop file that points to it?
- Where the manuals are silent (estimation, schedule, risk — T2 found none),
  should agents improvise and record, or bring the gap to you?
- Who revises the manuals from the feedback: you directly, or agents proposing
  changes for your approval?

## 4. Project management — "more to it" (Q-08, D-09)

Option B is agreed for v4.0. The owner said there is more to it. Candidate
areas the agent would ask about: coordination across projects (PEC's
cross-loop "Waiting on you" slate), estimation and risk (absent from the
manuals), resource and cost tracking for agent work (model usage, time), and
project management inside host applications for engineering projects
themselves (option C). Which of these, or what else, does the owner have in
mind?

## 5. PEC and Domains as connectors (Q-07, D-08)

From T9 (read-only; `2b0572fe0`, `origin/main`, the SCA-006 branch, and the
Git-ignored `domains/` residue), with one check of the private repository's
activity by HELPS_HUMANS:

- **"Domains" is ambiguous in the record.** It most probably means the
  **domain packs**: knowledge corpora, each with an accepted decomposition
  ledger (atoms → category, knowledge type, subject) and a derived BM25 plus
  vector search index queried through the `researcher` and
  `research-orchestration` workflows (`tools/retrieval/query_source_index.py
  --json`). Three of the four packs index project repositories (Chirality,
  the App, Piping); the fourth indexes piping-design handbooks. The corpora
  moved on 2026-08-20 to the private repository `sgttomas/chirality-domains`,
  whose last push was 2026-08-21. The word also names **domain engines**
  (`_DomainEngines/`), and PEC is itself registered as one — which would make
  PEC one of the Domains unless the two senses are kept apart.
- **Domain packs already realise two of the thesis's three "intended"
  pieces** (a decomposition over files; BM25 plus vector search through a
  workflow), contrary to thesis §4.3.5's "None of the three is built". The
  local indexes date from June 2026 and are stale against today's files.
- **PEC** prepares a read-only, rebuildable projection of loop files in two
  tiers — record (orientation, deltas, gate verdicts, the "Waiting on you"
  slate, work graphs, run records, drift) and presence (sessions, worktrees,
  scope claims) — designed for a local token-scoped socket. On `origin/main`
  only foundations exist (API envelope, registry, store); reliance begins
  only at a PEC release that passes its reliance gate (D-PEC-90). An
  `agent` access class for tool-call queries is a checkpoint-2 candidate.
- **Independence holds** in code and data. The coupling risks are the shared
  word "domain", the shared substrate (both project the same files), and
  that v4's own project-management files (work graphs, decision records)
  would become things PEC parses — a de facto contract.

**Proposed reading for the PRD:** the App has two optional, independent
connectors. **Domains** supplies knowledge — accepted decompositions and a
search index over corpora (including, potentially, each application's own
files); results locate evidence and never prove membership or authority.
**PEC** supplies coordination state — a pinned, freshness-stamped view of
work across loops; the App acts, PEC observes. The App works without either
(files are the fallback) and always shows the standing and freshness of what
it shows.

**Questions for the owner:**

1. Does "Domains" mean the domain packs (knowledge corpora), the domain
   engines (such as SWBPIPE's solver lineage), or both?
2. Is the June 2026 pack format what you are preparing now, or a successor —
   and where does that work live?
3. Should v4's project-management files use formats PEC already reads, and
   should the v4 project register as a PEC loop?

## 6. T3 Code and the local-model requirement (Q-05, D-05, D-06)

From T8 (GitHub and web, read-only; `pingdotgg/t3code@a21b42c`,
`openai/codex@e72da2b`, `jundot/omlx@3f2d07e`), with three claims checked
directly by HELPS_HUMANS against those commits (T3's Codex launch-argument
layer; Codex's per-thread `modelProvider` on `thread/start`; oMLX's
`/v1/responses`, `/v1/messages` and `/v1/chat/completions` routes).

**Your question — has T3 Code ported Codex's local-model support?** Not as
a feature. T3 Code has no local-model provider or "OSS" switch; feature
requests for one were closed. Local models **do work by pass-through**,
because T3 runs your own harness binaries with your own configuration:

- **Codex:** a T3 "Codex" instance whose launch arguments point Codex at a
  custom provider (`-c model_provider=…`). Works; lightly documented; open
  bugs (truncated replies from custom providers — fix pending; misleading
  auth and usage warnings).
- **Claude Code:** a T3 "Claude" instance with `ANTHROPIC_BASE_URL` set to a
  local Anthropic-compatible server. Documented by T3.
- **OpenCode:** the route T3's maintainer recommends for local models.

oMLX ships its own integrations for both Codex and Claude Code, so both
routes are plausible on this Mac; whether oMLX handles everything Codex
sends in long agentic turns is unknown until tried. A reported March 2026
post by T3's founder says local models "are not capable of meaningful
engineering work" (unverified: the post itself could not be retrieved).

**What T3 Code does well for your requirements:**

- Multi-provider on `main`: Codex, Claude Code, Cursor, Grok, OpenCode,
  Antigravity; Pi and a generic agent-protocol provider are in its pending
  rewrite.
- **OAuth, API key and local at once**: separate provider instances
  (for example "Claude subscription", "Claude API", "Claude oMLX", "Codex
  ChatGPT", "Codex oMLX") shown together; each conversation picks one.
- It uses the user's own sign-ins to the official CLIs, which keeps it out
  of "offering claude.ai login" — though whether a *distributed* Chirality
  application may rely on users' subscriptions still needs written vendor
  confirmation.
- Mac first: yes. MIT licence. Momentum: ~23.6k stars, very active.

**Where it is a weak fit:**

- **Alpha and moving fast**: versions 0.0.x; 1,522 commits in September; an
  open rewrite of its orchestrator of roughly +341k/−171k lines;
  contributions "not actively accepted"; roughly half the commits from one
  maintainer.
- **No host-tool interface**: it passes no application tools to Codex and
  no in-process tools to Claude; host tools would come in as an MCP server
  registered in the harness's own configuration.
- **No role or workflow concept**, its own injected instructions and tools,
  default permission "Full access", usage telemetry on by default.
- **Embedding**: `t3 serve` runs headless with an HTTP and WebSocket API that
  third parties already drive, but it is not declared stable. A native
  SWBPIPE panel means writing a client for that API, or forking.

**A useful separation this reveals.** If each host exposes its typed
operations (inspect, preview, submit proposal, status) as an **MCP server**,
any harness — Codex, Claude Code, OpenCode, directly or through T3 — can use
them. The host-integration contract (D-02) then does not depend on the
harness choice at all. Condition: the harness must speak the current MCP
protocol (SWBPIPE's earlier attempt failed against an older bundled Codex
client; current Codex supports the 2026-07-28 protocol behind a flag).

**Three harness arrangements to test, not yet to choose:**

| Arrangement | Local model | OAuth + API + local | Host tools | Maintenance |
|---|---|---|---|---|
| T3 Code unmodified, run as a gateway (`t3 serve`), driven by Chirality's own interface | Pass-through (Codex, Claude Code, OpenCode) | Yes, per conversation | MCP server registered in harness config | Low code, but tracks an unstable alpha API |
| Stock Codex App Server directly (the v3 path) | Codex custom provider, chosen **per conversation** (`modelProvider`) | Yes within Codex; Claude models not available | Codex application tools or MCP | Known; single loop vendor |
| T3's MIT provider adapters as a pattern source for a thin Chirality provider layer | As above, both harnesses | Yes | Either | Most code owned by Chirality |

**Experiments that would settle it** (each disposable, in scratch
directories, and each needing your go-ahead because it installs T3 Code
and uses your oMLX server, which the Piping records say is not to be used
without an agreed slot):

1. T3 Code + Codex + oMLX: a multi-file edit, a plan, a restart and resume,
   and a switch to a ChatGPT instance mid-conversation.
2. T3 Code + Claude Code with three instances (subscription, API key, oMLX).
3. Stock Codex App Server with a per-conversation oMLX provider (baseline
   without T3).
4. `t3 serve` driven by a toy Tauri host that exposes one typed tool as an MCP
   server.

LM Studio and OpenCode are also installed on this Mac; LM Studio is a second
local server Codex supports natively.
