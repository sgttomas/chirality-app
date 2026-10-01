# Decisions pending — APP-V4-DESIGN-PASS-3-20261001 (checkpoint K)

Prepared by HELP_HUMAN from the three surveys in [SURVEY/](SURVEY/). The
recommendations are the integrator's. Nothing here is decided until the
owner's answer is recorded in [OWNER_DECISIONS.md](OWNER_DECISIONS.md).

Twelve choices change what the six standalone-App Design files say. Part 2
lists what the integrator takes in the pass (open to being overruled).

## Part 1 — asked now

### Account and model access (DEL-01-05)

**K-1 Where the App's Codex keeps its settings and sign-in (OI-009).**
- A. A Chirality home of its own: separate sign-in and separate settings.
- B. Your existing Codex home: same sign-in, settings and MCP servers as your
  Codex CLI.
- **C. Shared settings, separate sign-in (recommended).** The App sees your
  Codex settings, providers and MCP servers, and signs in on its own. This is
  the arrangement the repository doctrine already describes for the App
  ("the user's shared Codex configuration and resources, with authentication
  separated for Chirality and custodied by Codex"). The mechanism is designed
  as PROPOSED and confirmed by a local observation; if Codex 0.158.0 cannot do
  it, the design falls back to A and says so.

**K-2 ChatGPT sign-in and API key side by side.** At the pinned Codex one
home has one signed-in account.
- **Recommended:** the ChatGPT sign-in is the Codex account; an API key is a
  separate provider entry; local models are provider entries too. All three
  stay configured, and each conversation picks one (the scope of work asks
  for exactly this). To be confirmed by observation.
- Alternative: one cloud mode at a time, switched in settings for new
  conversations.

**K-3 "No default" in the App as well as in a host.** The accepted text
says it for a host's agent only.
- **Recommended: yes.** A new conversation starts with no model chosen until
  you choose. The App may offer your last explicit choice for that project,
  shown as such, never applied silently.
- Alternative: the App follows Codex's own configured default.

### Running and stopping (DEL-01-02, DEL-01-03)

**K-4 Quitting the App while work is live.**
- **Recommended:** the App asks first and lists the live turns and pending
  requests. If you quit, the turns are interrupted and recorded "interrupted
  by quit"; on relaunch they are shown, with an offer to resume.
- Alternatives: quit without asking (turns end as interrupted or unknown);
  refuse to quit until work is done.

**K-5 Codex features marked experimental.** Plan mode and delegation views
need an experimental Codex setting at 0.158.0.
- **Recommended:** use them, marked "experimental" where they appear, with
  the App fully usable without them (the views are simply absent).
- Alternative: leave them out until Codex marks them stable.

### Workflows (DEL-02-02)

**K-6 Registering a workflow whose name already exists.**
- **Recommended:** when the draft was made from that workflow, registering
  it adds a new revision; earlier revisions are kept and every run cites the
  revision it used. A draft with the same name but no such origin is refused,
  with a request for a new name. Nothing is overwritten.
- Alternatives: always refuse an existing name; or replace the old one.

**K-7 Trying a draft before registering it.**
- **Recommended: yes**, as a run labelled "draft trial". It is recorded with
  the draft's content identity and never counts as a run of a registered
  workflow. (Three first-increment files currently say a draft cannot run;
  they would be updated.)
- Alternative: only registered revisions run; drafts are tried out in
  conversation.

**K-8 How registration is performed.**
- **Recommended:** through the same person-only act control as the other
  reserved acts (DEL-01-04). It binds the exact bytes you reviewed, so a
  draft changed after review cannot be registered without a new review.
- Alternative: a separate registration button owned by the workspace.

### Roles (DEL-02-04)

**K-9 Where role guidance comes from, and how changes reach a conversation
(OI-018).**
- **Recommended:** the App ships default role guidance and seeds an editable
  copy in its own data folder, as the repository doctrine describes. A change
  takes effect at the next idle point of a conversation, never mid-turn, and
  the record names the guidance by content.
- Alternatives: guidance bundled read-only with the App; or guidance kept in
  each project.

**K-10 "A task agent does not delegate."**
- **Recommended:** state it in the task role's guidance, label it "stated,
  not enforced", and record and show any delegation a task agent makes. The
  App does not override your Codex settings to enforce it. Enforcing it
  would mean overriding a setting the doctrine leaves to you, and the
  matching setting at 0.158.0 is deprecated.
- Alternative: enforce it with a per-conversation override.

### Observation and supplier behaviour

**K-11 Live observations for this pass.**
- **Recommended:** allow local-model observations (your installed Qwen 3.5
  9B, invented material, no sign-in, no download) of interrupting a turn,
  resuming after a restart, whether pending requests come back, and
  delegation. The sign-in and API-key flows would need you to sign in
  yourself; I would ask for that separately, only if the design cannot settle
  without it.
- Alternative: no live observation; those parts rest on the protocol types.

**K-12 Codex's start-up traffic** (chatgpt.com remote control, a refused
plugins request and a github.com plugin check, seen with analytics off and
no sign-in).
- **Recommended:** the App turns off whatever Codex's settings allow, shows
  the rest in its network view, and records it. The design names which is
  which.
- Alternative: accept it as the supplier's behaviour and only record it.

## Part 2 — taken by the integrator (open to being overruled)

| Matter | What the integrator does |
|---|---|
| What "stop" means | Three distinct operations with their own records: interrupt a turn, end a run, stop the Codex process |
| App-kept records versus Codex history | Conversation content is read back from Codex (ARCHITECTURE §3, "rather than a Chirality copy"); the App keeps only its own run records and the pointers it needs |
| The App's process division (OI-008) | HOSTING's recommended O-1: the Rust host owns the Codex process, the request register and record writing; the interface composes and presents; act capture is produced in the host from a native interface event, so no agent tool can operate it |
| Designing the act control before its contract changes | Designed now in DEL-01-04, labelled PROPOSED until SCA-V4-003 carries the obligation |
| Who builds the App's checkpoint and standing display | DEL-04-02 defines the components and their meaning; DEL-01-04 places them in the App |
| Who supplies the selected workflow to a conversation | DEL-02-04 composes it with the role guidance (as four first-increment files assume); the agent may also read the file. Recorded as an SCA-V4-003 item |
| No automatic decline after a timeout | A pending request waits; a supplier's own auto-resolution is recorded as such, never as an answer |
| Plan acceptance | "Carry out this plan" is an ordinary instruction, not a reserved act, unless a workflow checkpoint names an act |
| Untyped sessions | A conversation may run with no role, as the doctrine allows |
