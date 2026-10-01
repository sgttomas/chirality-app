# R17 rulings — for the design nodes (D) of design pass 3

Integrator: HELP_HUMAN. Inputs: the surveys S1-A, S1-B and S1-C;
DECISION-K3 as revised (OWNER_DECISIONS.md); DECISIONS_PENDING.md Part 2,
which the owner did not object to. R1–R16 stand. Labels as in R9:
SETTLED (an accepted text or owner decision says it), DERIVED (follows from
those), INTEGRATION (the integrator's choice, open to the owner),
PROPOSED (a design structure not yet decided by anyone).

## R17-1 What the pass produces — INTEGRATION

Each of the six deliverables gains its first Design file(s), v0.1, at the
60% description of `loop/LOOP_INIT.md`: interfaces (supplier, receiver,
condition of use, behaviour when the exchange fails), states (one
transition table per stateful thing the file owns), data (PROPOSED JSON
Schema 2020-12 beside the file, with a valid and an invalid instance, for
each format handed to a receiver), operating sequences with failure
behaviour at each step, and verification (each designed case says what it
needs: test double, fixture, the person, a candidate). R12-1, R12-2 and
R12-3 apply unchanged: prototypes are Python 3 standard library or `node`,
no installs, under `Design/prototype/`. The survey's design-scope section for
the deliverable is the starting list; this ruling overrides it where they
differ.

## R17-2 The owner's answers, by file — SETTLED (DECISION-K3 revised)

| K | Answer | Designed in | Consequences elsewhere (node F, R17-14) |
|---|---|---|---|
| K-1 | Shared Codex settings, providers and MCP servers; separate sign-in custodied by Codex; mechanism PROPOSED, confirmed by OBS-2; if Codex 0.158.0 cannot do it, fall back to a Chirality home of its own (option A) and say so | DEL-01-05 (account home record) | HOSTING §4.2 step 3, §7.2, H9, F-14, U-03 |
| K-2 | ChatGPT sign-in is the Codex account; an API key is a separate provider entry; local models are provider entries; all stay configured; each conversation picks one | DEL-01-05 | If OBS-2 or the types show this needs more than one Codex home, HOSTING U-12 gains a per-home dimension: report it, do not restructure HOSTING in D |
| K-3 | No model chosen in a new App conversation until the person chooses; the App may offer the last explicit choice for that project, shown as such, never applied silently | DEL-01-05 (selection states); DEL-01-04 (conversation start display) | R15-1 wording "run not started — no model selected" reused |
| K-4 | Quit with live work asks first, listing live turns and pending requests; if the person quits, turns are interrupted and recorded "interrupted by quit"; on relaunch they are shown with an offer to resume | DEL-01-02 | HOSTING §4.5 |
| K-5 | Use Codex's experimental plan mode and delegation surfaces, labelled "experimental" where they appear; the App is fully usable without them (the views are absent) | DEL-01-03 | HOSTING U-21, F-13 |
| K-6 | A draft made from a registered workflow registers as a new revision of it; earlier revisions are kept; every run cites the revision it used; a same-name draft with no such origin is refused with a request for a new name; nothing is overwritten | DEL-02-02 | Agrees with CA §4, EXEC RT-6/RT-7, WD-EX E4 (no rework); WD C-4 stands |
| K-7 | **Owner's alternative:** only registered revisions run; a draft is tried in an ordinary conversation, which is not a run of any workflow identity | DEL-02-02 (journey) | EXEC HR-3, TR-1/T-1 and WD OS-2/OS-3 stand unchanged; RS R2 needs no draft form |
| K-8 | Registration (A15) is performed through the person-only act control of DEL-01-04, bound to the exact reviewed bytes; a draft changed after review needs a new review | DEL-01-04 (act control); DEL-02-02 (review binding, registration sequence) | ACT §2.6 and RS HA-10 re-point from "the App's registration control" to the act control; SC2-01-04-1's consumers include DEL-02-02 |
| K-9 | The App ships default role guidance and seeds an editable copy in its own data folder; a change takes effect at the conversation's next idle point, never mid-turn; the record names the guidance by content | DEL-02-04 | — |
| K-10 | The task role's guidance states that a task agent does not delegate, labelled "stated, not enforced"; any delegation a task agent makes is recorded and shown; no override of the user's Codex configuration | DEL-02-04 (limit account); DEL-01-03 (delegation view shows it) | — |
| K-11 | Local-model observations allowed (OBS-2, R17-16); sign-in and API-key flows are not observed without a separate owner answer | OBS-2 | — |
| K-12 | The App turns off whatever Codex's settings allow of its start-up traffic, shows the rest in a network view and records it; the design names which is which | DEL-01-05 | HOSTING L-4, U-18. Codex does not report its own connections in its event stream: DEL-01-05 states how the App learns them (its own observation of its Codex process, a per-version list from an observation, or both), PROPOSED |

## R17-3 "Stop" is three operations — INTEGRATION (Part 2)

1. **Interrupt a turn**: the person's act in a conversation; Codex
   `turn/interrupt`; the turn ends interrupted; the conversation and any
   workflow run continue. Not a run end.
2. **End a run**: the person ends a workflow run explicitly (EXEC's run
   end). Quitting, a supplier exit or an interrupt never ends a run by
   itself.
3. **Stop the Codex process**: the App stops its supplier (quit, HOSTING
   §4.5). Live turns become "interrupted by quit" (K-4); an unexpected exit
   leaves turns "interrupted" or "unknown" as observed (HOSTING §4.3).

Observer loss (window close, reload) and connection loss are not stops.
DEL-01-02 owns these definitions; HOSTING §4.5/§4.6, EXEC AE-7/RE-6 and RS's
run-ended event are reworded in node F to cite them.

## R17-4 App-kept records versus Codex history — DERIVED (ARCHITECTURE §3)

Conversation content is read back from Codex ("rather than a Chirality
copy"). The App keeps only its own run records (RS) and the pointers it needs
(for example the run ↔ thread association), labelled App-observed, never
authority for what Codex holds. Plan checklist revisions that Codex does not
keep in history are not copied: after a relaunch they are shown as
"not recoverable after relaunch" (S1-A B-2; HOSTING S-2 stays "Not
supplied"). PROPOSED where the survey marks the supplier fact as inference.

## R17-5 Process division — INTEGRATION (OI-008 option O-1, PROPOSED)

The Rust host owns the Codex process, the request register and record
writing; the interface composes and presents; act capture is produced in the
host from a native interface event, so no agent tool can operate it. Stated
as PROPOSED; the phase review owns OI-008. Files state requirements (for
example CAP-4) separately from this placement.

## R17-6 The act control — INTEGRATION (Part 2; K-8)

DEL-01-04 designs the App act control now (CAP-1…CAP-9 accepted or amended),
labelled PROPOSED until SCA-V4-003 carries SC2-01-04-1. It serves every
reserved act kind, including A15 registration. It is a standing facility,
never raised by an arrival (K1-1). Identity per K1-4 ("identity not
verified").

## R17-7 Checkpoint and standing display — INTEGRATION (Part 2)

DEL-04-02 defines the display components and their meaning (AS §13 K-5,
K-6); DEL-01-04 places them in the App and owns their behaviour there. EXEC
§2.4.4 re-points in node F.

## R17-8 Workflow supply — INTEGRATION (Part 2; SCA-V4-003 item)

DEL-02-04 composes the selected workflow with the product guidance and the
role into the additive instruction input (`developerInstructions`);
`baseInstructions` is never set. The agent may also read the workflow file;
that read is a tool item, not evidence of supply. A new register row
DEL-02-04 consumes DEL-02-01/DEL-02-02 is proposed for SCA-V4-003 (S1-C
reports it inside SCC-002, held and SCC-neutral; the comparison node checks).

## R17-9 Small matters — INTEGRATION (Part 2)

- **No automatic decline.** A pending request waits; a supplier's own
  auto-resolution is recorded `resolved-by-supplier` (HOSTING RT-10), never
  as an answer.
- **Plan acceptance** ("carry out this plan") is ordinary conversation
  input, not a reserved act, unless a workflow checkpoint names an act.
- **Untyped sessions** are allowed: a conversation may run with no role.
  Whether a new conversation preselects a role follows the Root registry's
  `default_for_new_chat` as data, shown as a preselection the person can
  clear (PROPOSED).
- **Native child roles**: the four roles are supplied to delegated children
  through Codex's native agent-role configuration where 0.158.0 supports it;
  otherwise children inherit the parent's guidance, and the file says so
  (DEL-02-04 with DEL-01-03).

## R17-10 Cycle guard — DERIVED (DAG-003; S1-A §3.2 S-1)

DEL-01-02 and DEL-01-03 must not consume DEL-01-04, DEL-02-02, DEL-02-03,
DEL-04-02, DEL-04-03 or DEL-06-01. What those need from DEL-01-02/01-03 is
written as offered interfaces; what DEL-01-02/01-03 show of them is a
runtime value they are handed, not a production input. Any new row a D node
proposes states its direction and whether it forms an SCC.

## R17-11 "Derived from" — INTEGRATION (S1-C S-3)

WD §6.1 and EXEC HR-4 keep *derived-from* for the parent **workflow
identity**. The A15 registration record names its subject by two elements:
the **reviewed draft content** and, for a new revision (K-6), the **prior
revision**. ACT §2.5, RS HA-10, RS's schema `relations.derivedFrom` and their
fixtures are aligned in node F. DEL-02-02 uses these names.

## R17-12 Act presentation and identity — SETTLED (DECISION-K1)

K1-1…K1-4 apply as written: the agent asks; the product records what it
observes; an earlier act on still-current content counts in the current
phase and is cited; the person is recorded "identity not verified".

## R17-13 Supplier facts and standing — INTEGRATION

Supplier facts cite HOSTING v0.8, PIN_SPIKE, OBS_1 (with OBS-1b) or the
generated types at 0.158.0 (`…/scratchpad/codex-0.158.0/gen`, read only),
labelled `observed`, `observed-in-generated-types` or `inference`. Cells
OBS-2 will settle are marked "OBS-2 pending" and filled in round 2.

## R17-14 First-increment files — INTEGRATION

D nodes do not edit first-increment Design files. Each returns a join list
(file, section, what the other side now needs). Node F, after round 1, makes
the edits in one pass, including at least: HOSTING §4.5/§4.6 and §6.5
(R17-3; DEL-01-02's re-attachment), §4.2/§7.2/H9 (K-1), U-12 if K-2 needs it,
L-4/U-18 (K-12); EXEC AE-7, RE-6, §2.4.4, U-E19; RS run-ended event, HA-10,
`relations`; ACT §2.5, §2.6, §10.3 (R17-6, R17-11). One version step per file.

## R17-15 ScopeOfWork lags — INTEGRATION

Where a ScopeOfWork lags the basis or these answers, the Design file states
its reading in the header and the return file lists a precise proposal for
SCA-V4-003 (file, location, old → new, reason, source). No executor edits a
ScopeOfWork, register or `_STATUS.md`.

## R17-16 OBS-2, the local observations — SETTLED scope (K-11), INTEGRATION method

At Codex 0.158.0 (the scratch binary from the pin spike), against the
installed LM Studio model `qwen/qwen3.5-9b`, with invented material, scratch
`CODEX_HOME`s only (never `~/.codex`), no sign-in, no API key, no download,
no install. Items:

- O-1 interrupt a running turn (`turn/interrupt`): turn status, items,
  notifications;
- O-2 stop the app-server while a turn is live and a request is pending,
  restart, resume the thread: what history shows, whether the pending request
  is re-raised, turn status after;
- O-3 a request resolved by the supplier before the App answers, if it can be
  provoked locally; otherwise record "not provoked";
- O-4 delegation with the experimental opt-in (`experimentalApi`): what items
  and notifications a child produces; whether a child thread is readable;
- O-5 resume with changed `developerInstructions` (P-15): what the thread
  reports;
- O-6 the K-1 mechanism: whether one home's configuration can be shared with
  a second home that has its own (empty) authentication, by the means 0.158.0
  offers (for example configuration file location, profiles or `-c`
  overrides), observed by `config/read` and `account/read` only;
- O-7 start-up traffic (K-12): which Codex settings stop which start-up
  connections (remote control, plugins, plugin sync), by comparing connection
  lists with each setting on and off. Connections are observed with local
  tools (for example `lsof`); nothing is intercepted.

Codex's start-up connections to chatgpt.com and github.com occur as in OBS-1
and are recorded, not prevented, unless O-7 finds a setting that prevents
them. No credential exists in any scratch home.
