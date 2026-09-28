# Wave-1 TASK briefs — APP-V4-FIRST-INCREMENT-20260928

Parent: HELP_HUMAN (Claude Code session, worktree
`.claude/worktrees/test-ci-optimization-f6cacd`, branch
`claude/chirality-app-v4-60-percent-a41fd5`, base `6e18505e3`). Graph:
[WORK_GRAPH.md](../../WorkGraphs/APP-V4-FIRST-INCREMENT-20260928/WORK_GRAPH.md).
Mechanism: Claude Code `Agent` subagents (Type 2; they do not delegate).
Dispatch record: [DISPATCH.md](DISPATCH.md).

## Common brief (applies to W1–W6)

**Purpose.** Produce the earliest separately usable *definition* version
(v0.1) of your deliverable's contribution to the first App/host increment, at
60% design level: interfaces, states, data meanings, operating sequences,
failure behavior and verification cases. It will be compared by named
receivers (CASE-002 M1–M3) and then repaired to v0.2.

**Basis (read these; `P` = `projects/chirality-app-v4`).**
- Your deliverable's `ScopeOfWork.md` (fully), `Dependencies.csv` ACTIVE
  EXECUTION rows, `_REFERENCES.md`.
- `P/docs/PRD.md`, `P/docs/HOST_INTEGRATION.md`, `P/docs/ARCHITECTURE.md`,
  `P/docs/EXAMINATION.md` — sections your SoW cites.
- `P/execution/_DAG/cases/SCC-CASE-002/Case_Datasheet.md` — the M1–M4 rows
  naming your deliverable (producer and receiver).
- Accepted decision brief `P/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/DECISION_BRIEF.html`
  where cited (d3 human acts, d4 parity, d5 first activity).
- Read other deliverables' SoWs only for the interfaces you exchange with them.

**Write scope (exact).** Create files only under
`<your deliverable folder>/Design/`. Do not edit ScopeOfWork.md, `_STATUS.md`,
`Dependencies.csv`, `_DEPENDENCIES.md`, `_REFERENCES.md`, any other
deliverable, docs, cases or coordination files. No git operations (no add,
commit, stash, checkout, push). No network access, no package installs.

**Required form.** Each Design file opens with:

```
# <Title>
- Contribution: <DEL-xx-yy>/<short-id>-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: <OUT-/REQ-/VER- ids of this deliverable>
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 <full hash>; <doc §§>
- Consumed inputs: <DEL/contribution version, or "accepted basis only; <DEL> referenced by accepted meaning, to be reconciled at V1">
- Receivers: <DEL-xx/OUT/REQ/VER that will compare this, from CASE-002 or Dependencies.csv>
```

followed by the content and a closing `## UNRESOLVED` table
(item | owner | point of need | effect on this definition) and a
`## Verification cases` section (designed, not run; each with expected result
and which VER-nnn it serves). Keep one main file per deliverable
(`Design/<NAME>.md`); add an `EXAMPLES.md` only if examples are long.

**Constraints (hard).**
- Representation-neutral: do not select wire field names, JSON/TS types, a
  transport (MCP vs CLI), a hash/canonicalization algorithm, persistence,
  thread/process placement, or shared-component placement (OI-013, OI-014,
  DEL-03-01 TBD-003, DEL-03-02 TBD-002, DEL-03-03 TBD-007). Use descriptive
  element names and say they are semantic, not wire names.
- Unruled policy (OI-001 reserved acts, OI-002 classifier permissions, OI-003
  extension promise, OI-021 first operation) appears as
  `UNRESOLVED{OI-nnn}` — never as a permission, a default choice or a pass.
- Do not invent human acts, host behavior, SWBPIPE commitments, receipts or
  evidence. Examples use invented engineering material and are labeled
  fixture subjects.
- Preserve every SoW obligation; if the SoW appears wrong or a needed input is
  missing, report it as a finding — do not change scope.
- Settled distinctions from the accepted basis may be stated as settled with
  citation (e.g. V4-HI-23 lifecycle, V4-HI-25 queued ≠ applied, V4-HI-32
  lapse, V4-HI-33 "accept" wording).

**Return (to parent, final message).** (1) files written with line counts;
(2) contribution summary (≤ 12 bullets); (3) interface elements you *expect
from* named suppliers and *provide to* named receivers; (4) UNRESOLVED list;
(5) findings about SoW/basis gaps or contradictions; (6) confirmation that you
wrote only inside your `Design/` folder and ran no git/network operations.

## W1 — DEL-04-01 Operation-policy and human-act distinctions

Folder: `PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-01_Operation-policy and human-act distinctions`.
Main file `Design/ACT_AND_POLICY_CONTRACT.md`. Content: act taxonomy with
actor / subject / evidence per act (propose, apply, examine, check/mark
checked, accept an edit, approve, rely; plus faithful recording where
actor ≠ recorder); the settled distinctions S1–S12 with citations (PRD §4.5,
HI §§4–7, d3); autonomy-grant model (operation class × consequence →
direct | propose | reserved | `UNRESOLVED{OI-001/002}`), person-set scope,
widening rule bounded by reserved acts and checkpoints (V4-HI-42); SWB default
example (model change = propose; row / multi-row / batch accept) labeled as
the accepted default; policy-class record meaning with a decision-basis
element; value → decision → consumer map for DEL-02-01, 02-03, 03-01, 03-02,
03-03, 04-02, 04-03, 05-01, 05-02, 01-04, 09-09; fixture catalogue (fabrication,
success-only, independent act, faithful recording, "accept" wording, unresolved
value not treated as permission). Do not decide OI-001/OI-002; list the owner
questions precisely.

## W2 — DEL-04-03 records and DEL-04-02 autonomy/standing exchange

Folders: `PKG-04_…/1_Working/DEL-04-03_Content-bound decisions and compact run records`
and `PKG-04_…/1_Working/DEL-04-02_Visible autonomy and result standing`.
Files: `DEL-04-03/Design/RECORD_SEMANTICS.md`; `DEL-04-02/Design/AUTONOMY_AND_STANDING_EXCHANGE.md`.
DEL-04-03: ordinary-file authority rules; run-record inventory (workflow +
version/source identity, conversation, autonomy settings, operations and
outcomes incl. `unknown`, receipt references linked not copied, human acts,
model); human-act record (actor, recorder, act kind by DEL-04-01 accepted
name, content identity, scope, purpose, evidence refs, lapse state); lapse
comparison rule (representation-neutral); consumer table (PKG-02, PKG-03,
PKG-06, DEL-04-02, DEL-09-11); examples. DEL-04-02: grant display states
(effective, requested-unestablished, unconfirmed), during-work change, the
settings-in / record-out exchange with DEL-04-03 (CASE-002 M3), abstract host
contribution (origin ref, undo route, check route, receipt ref), standing
model (current, historical, checked, limited, lapsed, unknown/missing),
fixture scenarios. Act class values remain `UNRESOLVED{OI-001}`.

## W3 — DEL-03-01 catalog C and DEL-03-02 proposal P

Folders: `PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract`
and `…/DEL-03-02_Proposal, validation and outcome contract`.
Files: `DEL-03-01/Design/CATALOG_AND_READ_BASIS.md`; `DEL-03-02/Design/PROPOSAL_LIFECYCLE_AND_OUTCOMES.md`.
C: entry meaning with every REQ-002/V4-HI-02 element; availability and
unavailable-reason parity (HI-04) distinct from empty success; read-basis
descriptor (workspace identity, generation, model revision, canonical content
identity — algorithm unselected) kept distinct from operation identity; how a
later action cites the relied-on basis; standing (current/historical, checks,
limits); three-surface responsibility map skeleton (generated / checked /
hand-built / unagreed) preserving OI-003; representative examples on an
invented piping model. P: one route; origin and basis; lifecycle
drafted → validated → queued → accepted → applied(receipt) with rejected /
withdrawn / stale / outcome-unknown overlay and the direct-autonomy branch
(HI-22/23); stale refusal with reason and separately based re-draft; no
retargeting; repeated submission → one effect (mechanism unselected); host view
old/new/objects/reason; success ≠ acceptance; outcome taxonomy; execution vs
human-act table; the M3-CP read-then-action comparison design with an
intervening edit. Note SWBPIPE limits in HI §11 (queue-time basis differs from
inspection basis; no exactly-once) as receiving risks, not host assignments.

## W4 — DEL-02-01 portable workflow contract

Folder: `PKG-02_Workflow and role portability/1_Working/DEL-02-01_Portable workflow contract and shared allocation`.
File `Design/WORKFLOW_DECLARATION.md`. Content: declared-part meaning
(inputs, required tools as opaque capability references into catalog C,
checkpoints naming the required act kind by DEL-04-01 accepted name, outputs,
evidence); four roles and single agent seat in hosts; source identity
(origin project|user|bundled|host, source root, name, revision) and promised vs
observed distinction; readable examples (App-authored workflow for the
invented supports/run-adjustment fixture; a same-name collision); responsibility
map rows labeling each consumer need (DEL-02-02, 02-03, 02-04, 05-01, 05-02)
and each still-open allocation (OI-013/OI-014). Reuse sources to study, not
adopt blindly: Root `workflows/WORKFLOW_TEMPLATE.md`, `workflows/*/execution.json`,
`workflows/catalog.schema.json`, `docs/SPEC.md` §9.3, `docs/AGENT_WORKFLOW_RUNTIME.md`.
Say explicitly which Root conventions the v4 declaration keeps, changes or
leaves open, and why.

## W5 — DEL-05-01 loop and DEL-05-02 panel receiving

Folders: `PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract`
and `…/DEL-05-02_Host panel and shared interaction receiving`.
Files: `DEL-05-01/Design/LOOP_RECEIVING_CONTRACT.md`; `DEL-05-02/Design/PANEL_RECEIVING_CONTRACT.md`.
DEL-05-01: four-subject boundary (messages, tools, events, checkpoints) with
needed catalog/proposal/record/workflow meanings named by contribution; Chat
Completions with tool calls, distinct from the App's Codex/Responses path;
local-default / cloud-by-choice / native endpoint enforcement / key outside
script case matrix; validation order (catalog schema before host domain
validation); malformed / truncated tool-call cases never executed with empty
arguments; responsiveness observation protocol without numeric thresholds;
OUT-004 allocation and open-choice account (OI-013, DEP-05-01-024 UNKNOWN).
DEL-05-02: the four interactions (conversation, workflow selection, proposal
queue, checks) each traced to consumed definitions; host tables/views, no
agent-private surface; old/new/reason; "accept" wording and lapse; receiving
case inventory labeled designed/unexecuted; OUT-002 open allocation account.

## W6 — DEL-01-01 Codex hosting boundary (version-independent)

Folder: `PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract`.
File `Design/HOSTING_BOUNDARY.md`. Content: main-process ownership of the
stock Codex App Server child over JSON-RPC stdio; lifecycle (spawn, handshake,
version identity capture, crash/exit, restart) invariants; outstanding
server-request register interface (every request answered or explicitly
declined; unknown requests get an explicit error; silence never grants);
seam for version identity and plan/revision handoff to DEL-01-03; the
local-provider requirement account (published claim vs to-be-observed);
recorded-exchange fixture method and upgrade-comparison procedure (REQ-006);
owner/act boundary table (REQ-007/008); a *proposal* for OI-008 Rust/TS
division presented as options with a recommendation (the App implementation
owner decides; label it a proposal). No pin: 0.154.0 / 0.157.1 are dated
evidence only; do not name a selected version. Also list precisely what a pin
spike would need to observe (generation commands, fields, experimental
supplement) so W11 can be briefed.

## Owner rulings now in force

[OWNER_DECISIONS.md](OWNER_DECISIONS.md) (`APP-V4-FIRST-INCREMENT-20260928-DECISION-1`):
scope Option A; the OI-001 five reserved acts; the OI-002 App user setting with
no classifier mode in hosts; the OI-012 pin `0.158.0` with spike W11. The v0.1
drafts predate these rulings; V1 notes where they apply and R1 applies them.

## V1 — receiver comparisons for the Wave-1 joins (independent reviewers)

**Purpose.** Answer CASE-002 Open_Questions Q-03 for each join below: *which
identified version does the named receiver have, what check did it perform,
and what remains absent or disagrees?* The reviewers were not the authors.
They read the v0.1 Design files and the ScopeOfWork/Dependencies of both sides.

**Write scope.** Only `comparisons/V1-<letter>.md` in this run folder. Design
files, SoWs, registers and every other file are read-only. No git or network
operations.

**Per join, record:** supplier contribution ID/version and receiver
contribution ID/version as read; the receiver's OUT/REQ/VER that consumes it;
the check performed (element-by-element meaning comparison); a table of
**agreements**, **disagreements** (each with the exact quotes/sections from
both files, severity BLOCKING/MAJOR/MINOR, and a proposed resolution naming
which side should change) and **absent** inputs (with owner and point of
need). Also record where the owner rulings D2/D3 change a v0.1 statement, and
list register findings (missing or mirror dependency rows) with row IDs checked
in `Dependencies.csv`. Do not rewrite the designs. End with a prioritized
repair list for R1.

- **V1-A (policy consumers):** DEL-04-01/ACT-POLICY-v0.1 → W2 (DEL-04-03,
  DEL-04-02), W3 (DEL-03-01, DEL-03-02), W4 (DEL-02-01), W5 (DEL-05-01,
  DEL-05-02), W6 (DEL-01-01 routine tool-permission answers vs D3). Focus:
  act names/kinds (including reject, withdraw, grant change, registration),
  class values, grant model, widening bounds, "checked" ambiguity, "approval"
  overloading.
- **V1-B (catalog, proposal, record, autonomy):** DEL-03-01/C ↔ DEL-03-02/P
  (including the M3-CP return); P → DEL-04-03 (outcomes, receipt links,
  origin); P → DEL-04-02 (direct branch, grant in force); DEL-04-03 ↔ DEL-04-02
  (M3 settings-in/record-out); C → DEL-04-03 (content identity per
  subject/scope for lapse); item-level acceptance and lapse granularity.
- **V1-C (workflow, loop, panel, hosting):** DEL-02-01/WD ↔ DEL-05-01/LOOP and
  DEL-05-02/PANEL (checkpoints, tool references, selection identity, seat/role);
  DEL-05-01 ↔ DEL-05-02 reciprocal join (both drafted by one author, so needs
  independent comparison); C → DEL-02-01 tool descriptors; C/P → DEL-05-01/02
  proposal elements; DEL-01-01/HOSTING-BOUNDARY seams where they touch these
  (additive guidance, answer origin).

## W11 — Codex 0.158.0 pin spike (DEL-01-01)

**Purpose.** Observe the pinned supplier's actual protocol facts that DEL-01-01
§10 (P-01…P-15) lists, and generate the protocol types, so the boundary
definition rests on observation rather than dated evidence.

**Authority.** Owner decision D4. Permitted: `npm install @openai/codex@0.158.0`
into a scratch prefix under the session scratchpad; running that binary's
`--version`, `--help`, `app-server --help` and generator subcommands; starting
`app-server` over stdio with `CODEX_HOME` pointed at an empty scratch directory
to observe the `initialize` handshake and unknown-method behavior only. Not
permitted: signing in, touching `~/.codex`, sending model turns, the global
npm prefix, or git operations.

**Write scope.** DEL-01-01 `Design/PIN_SPIKE_0.158.0.md` and
`Design/generated/0.158.0/` (generated TS and/or JSON Schema, with a
`MANIFEST.sha256`; if the total exceeds about 3 MB, commit JSON Schema plus a
manifest of the TS output and state the omission).

**Return.** Exact commands and their exit codes; observed version label and
binary content hash; generator availability and flags; determinism (run
twice and compare); method/request inventory counts; handshake observations;
unknown-method response; per-P-item observed / not observed / contradicts
HOSTING_BOUNDARY v0.1; findings that require a v0.2 change.

## IR1 — independent review of the v0.2 set (fresh reviewers)

**Purpose.** Independently review the nine v0.2 Design files (commit
`c387730fb`) before PR-2. The R1 repairers built sibling elements from
[R1_RESOLUTIONS.md](R1_RESOLUTIONS.md), not from sibling text, so the core
check is **actual v0.2 ↔ v0.2 alignment** at each join. Secondary checks:
fidelity to each ScopeOfWork (no obligation dropped, no scope added, no
selected wire/transport/placement), correct use of owner decisions D2–D4
(no over-claiming), and truthful standing (nothing claims implementation,
qualification, host delivery or a human act).

**Write scope.** Only `reviews/IR1-<letter>.md` in this run folder.
Everything else is read-only. No git or network operations.

**Record.** Files reviewed, with sha256. For each join: which of its R1
resolutions actually hold in both texts, and any residual disagreement (with
quotes, severity BLOCKING/MAJOR/MINOR, and the side that should change). For
each assigned [R2_CANDIDATES.md](R2_CANDIDATES.md) item: *agree with the
proposed treatment*, *amend it* (give the wording) or *reject it* (give
reasons). Also give SoW-fidelity findings, over-claiming findings and a
prioritized R2 list. Say plainly if the set is fit to merge as v0.2 drafts
once the listed BLOCKING items are fixed.

- **IR1-A (policy & records):** DEL-04-01, DEL-04-02, DEL-04-03 against
  each other and against the policy/record consumers in the other six files.
  R2 items X-1, X-2, X-3, X-4, X-13, X-15.
- **IR1-B (catalog & proposal):** DEL-03-01, DEL-03-02 against DEL-04-01/02/03,
  DEL-05-01/02 and DEL-02-01. Also the shared fixture FX-PIPE-01 (C §10),
  checked against every file that cites it. R2 items X-5, X-6, X-7, X-8, X-9.
- **IR1-C (workflow, loop, panel, hosting):** DEL-02-01, DEL-05-01,
  DEL-05-02 and DEL-01-01. Include an independent LOOP↔PANEL check (single
  author) and the HOSTING boundary against PIN_SPIKE_0.158.0.md. R2 items
  X-9, X-10, X-11, X-12, X-14, X-17, X-18.
