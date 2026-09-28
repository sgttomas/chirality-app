# Adapter enablement and receiving
- Contribution: DEL-03-03/ADAPTER-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (meaning of the App-side native MCP/CLI configuration and of the receiving adapter "as needed" — definition only, no code), OUT-002 (machine-local enablement and operation-policy interface account; owner/act map; open-choice register), OUT-003 (designed, transport-neutral external consumer fixture inventory, labeled simulated); REQ-001…REQ-006; AC-001…AC-007; VER-001…VER-007
- Basis: branch base 6e18505e3; Wave-1 inputs at commit `ba0b37123`; ScopeOfWork.md sha256 5ac5db97eba3851eb5324054e5a2b38429a53e8e9c85428903432cd8d9efb1b6; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da) §1, §2 (V4-HI-01…04), §3 (V4-HI-10…12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §7 (V4-HI-50…52), §11; `P/docs/PRD.md` (sha256 657593ce12a9a6da9f8b6c66579945499d909a8b6272d919d2d14a3db4538573) V4-HOST-02/03, V4-PAR-01…05, V4-AUT-03…05; `P/docs/ARCHITECTURE.md` (sha256 c3ae766ee2d660fb391b7db0aa99526f84d21421cf3a6b692ddd17e42687e533) V4-ARC-20/21; `P/docs/EXAMINATION.md` (sha256 1b156553dec7eb103dbb1166f5c0dbe9c719d26630d2fcace26c28b3ef54ee19) V4-EXM-23/24/25; SCC-CASE-002 `Case_Datasheet.md` (sha256 6acdc6c4e484ab7b46ba7d45a347961bc69b3e624bd29ef58a613ec6c66a71a6) rows M1-C, M1-P, M2-A; run `APP-V4-FIRST-INCREMENT-20260928`: `OWNER_DECISIONS.md` (Decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D1–D4, `R1_RESOLUTIONS.md` (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4), `R2_RESOLUTIONS.md` (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088), `R3_RESOLUTIONS.md` (sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf), `BRIEFS.md` (sha256 58de4a2c48f651391383aecf85fa5e9073d2cc34240c37cdab216a16481c698f) "Common brief", "Owner rulings now in force", "Wave 2 — common additions", "W8"
- Consumed inputs (all read with `git show ba0b37123:<path>`):
  - DEL-03-01/C-v0.3 `CATALOG_AND_READ_BASIS.md` (sha256 ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26): §2–§8, §10 FX-PIPE-01;
  - DEL-03-02/P-v0.3 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` (sha256 ec0db87f239bc42e2e3e953d660ce3c4ceddf605d7b98cf1393f97a099b699cf): §2–§11, §13;
  - DEL-04-01/ACT-POLICY-v0.3 `ACT_AND_POLICY_CONTRACT.md` (sha256 b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128): §2.1, §4, §5.3–§5.6, §6, §8.3, §10 V-10, §13 FX-24/25/42;
  - DEL-04-02/AS-v0.3 `AUTONOMY_AND_STANDING_EXCHANGE.md` (sha256 7b634137bb8402f3eaedc943dab0c5f1114b9d4433d2b94e13540ac0bf8e0514): §2, §3, §7;
  - DEL-01-01/HOSTING-BOUNDARY-v0.3 `HOSTING_BOUNDARY.md` (sha256 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e): §1–§3, §6, §8.2; DEL-01-01/PIN-SPIKE-v0.1 `PIN_SPIKE_0.158.0.md` (sha256 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115) §4–§6;
  - DEL-01-01 generated bundles at pin 0.158.0, read-only: `Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.schemas.json` (sha256 aa5cb3fbcdebf833515fb42cd085a0670eb755d461037a0ad67bb72a709dcd0f), `…/codex_app_server_protocol.v2.schemas.json` (sha256 34f28a486d00fbd20e5da0b0da3422d1d6e20ec897d12b31408f87499198f458) and `_spike/inventory.txt`;
  - for joins only: DEL-02-01/WD-v0.3 `WORKFLOW_DECLARATION.md` (sha256 84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb) §4.2, §4.3.4–§4.3.6; DEL-05-01/LOOP-v0.3 `LOOP_RECEIVING_CONTRACT.md` (sha256 6b771c8027787193d536fa3507214a8cc579d6ec2f476ee880609c920b6f25c7) §1, §6, §13; DEL-04-03/RS-v0.3 `RECORD_SEMANTICS.md` (sha256 925f35ca27bd7d1e71a375883ada9903267408af57312eed1ae02b47776a3528) R5, R7, R11, R13;
  - evidence only, **not a commitment**: the description of draft PR #885 "Connect a private live-control CLI to reviewed Piping operations" (head `12907f393f5ead1badfac894502895684448c6e2`, state OPEN, draft), read with `gh pr view 885` on 2026-09-28;
  - SWBPIPE endpoint contract and host contributions: **not supplied** (DEP-03-03-010, DEP-03-03-011; DEP-001).
- Receivers: DEL-09-09 (CASE-002 M2-A: OUT-001; REQ-001, REQ-002, REQ-004, REQ-008; VER-001, VER-002, VER-004, VER-008) via DEP-03-03-012 / DEP-09-09-009; DEL-03-04 (guide row "Optional external catalog access"; CLM-002; REQ-008) via DEP-03-04-007 (no DOWNSTREAM mirror in this register — F-11). By join, not registered here: DEL-03-01 and DEL-03-02 (receiving comparison of C/P meanings), DEL-04-01 (V-10), DEL-02-03 (external-path hold and required-tool check), DEL-04-03 (record entries R7/R9/R11/R13), DEL-01-01 (supplier surfaces).

**Reading note.** Every element name this file defines (for example
*channel state*, *native-tool mapping*, *carriage assurance*) is a
**semantic label, not a wire name**. Supplier method and field names appear
only as **observed supplier facts at pin 0.158.0**, with the DEL-01-01
standing labels `observed`, `observed-in-generated-types`,
`published-only` and `not-observed`. They are not Chirality wire choices.
Names from PR #885 are quoted as evidence from its description only.

This definition selects **no** transport (MCP versus CLI), wire field,
JSON/TS type, authentication scheme, hash or canonicalization algorithm,
persistence, process placement or shared-component placement (TBD-007;
OI-013; OI-014). §9 registers those choices and does not make them.

---

## 0. How to read this definition

Markings follow R1/R2: **SETTLED** (accepted basis or owner ruling, cited),
**DERIVED** (follows from cited rules), **INTEGRATION** (an R1/R2/R3
integrator choice, cited), **PROPOSED** (this contribution's proposal, open to
review). Owner rulings are credited only with what they say (R2-11).
Unruled policy appears as `UNRESOLVED{OI-nnn}` and is never a permission, a
default or a pass. Fixture subjects come from FX-PIPE-01 (C-v0.3 §10); local
subjects are named `L-ADAPTER-n` with their reason (§10.1).

Settled distinctions relied on (cited, not re-decided):

| Id | Settled distinction | Source |
|---|---|---|
| S-X1 | A host may expose its catalog to an external agent, such as the App's Codex, as an MCP server or as a CLI over its live controller. Both are built from the catalog and apply the same validation, autonomy settings and reserved acts | V4-HI-50; V4-ARC-21 |
| S-X2 | External access is **off** unless the person enables it, and it is **local to the machine** | V4-HI-52 |
| S-X3 | An external agent cannot perform an act reserved to the person. The earlier SWBPIPE no-external-apply design is historical context, not a universal v4 ruling, and v4 does not amend the host's operative policy without its receiving adoption | V4-HI-51; SoW AX-001 |
| S-X4 | One route for every change; treatment resolved on the host route at validation and again at application; loop and adapter relay intent and do not decide treatment | V4-HI-20; R-3.1 (INTEGRATION); P §2 |
| S-X5 | Runtime non-success results are C §4.1's; proposal/operation outcomes are P §9's; both adopted unchanged | R-7; C §4.1; P §9 |
| S-X6 | Reserved to the person (D2, adopted): A4, A5 where autonomy requires a proposal, A6, A7, A12, **A13 enabling external access**. DERIVED: A10 wherever A5 is. INTEGRATION (R2-3): **disabling** external access is also A13 | D2; R-1; R2-3; ACT §2.1 |
| S-X7 | App routine tool-permission and sandbox modes are the user's own Codex setting (A14); they govern tool execution only and never stand in for a reserved or professional act. INTEGRATION (R-2): no App rule answers A14 affirmatively; A14 is recorded only in R13 (R2-8) | D3; R-2; R2-8; HOSTING H9, R7–R9 |
| S-X8 | Stock, unmodified Codex App Server, owned by the App process, full published protocol, native delivery, no veto of the user's Codex configuration, no pinning of approval or sandbox policy. Definition/generation pin 0.158.0, not a qualification | V4-ARC-01; HOSTING H1, H6, H9; D4; DEP-005 |
| S-X9 | Success means it ran; queued ≠ applied; a receipt is not acceptance; one act never implies another | V4-HI-25; #d3; P S-P7/S-P8 |
| S-X10 | Checkpoints override autonomy; an A5 checkpoint forces *propose* for the operation in that run and is carried as a governing checkpoint constraint {workflow run, checkpoint name, required act A5, operation} | V4-HI-42; R-5; R2-12; ACT §4.4 |

---

## 1. Parties and the owner/act map (REQ-005; AC-006; VER-006)

This contract performs no act owned by another party. The table lists every
act or production the SoW excludes, one for one, with its actual owner.

| Act or production | Owner | This contract's part |
|---|---|---|
| Catalog and read-basis contract meaning; shared fixture | App DEL-03-01 (CLM-002) | Consumed (C-v0.3) |
| Proposal, validation and outcome contract meaning | App DEL-03-02 (CLM-002) | Consumed (P-v0.3), including constraint carriage |
| Canonical act names, class records, treatment → outcome map | App DEL-04-01 | Consumed (V-10, V-02, V-03, V-05, V-09, V-14) |
| Grant display states and standing display | App DEL-04-02 | Consumed; supplies the external-channel facts it displays |
| Human-act and run-record format | App DEL-04-03 | Supplies external-dispatch entries (R7), act references (R9), evidence limits (R11), A14 facts (R13) |
| Workflow checkpoint declaration; hold machine; required-tool check | DEL-02-01 declares; DEL-02-03 (W7) holds and checks | Supplies external-channel observations and a held question (§5.3, U-X3) |
| Hosting boundary; server-request register; A14 answer origins | App DEL-01-01 (with DEL-01-04/01-05 in a later undertaking, D1) | Consumes supplier facts at the pin; answers nothing |
| Joined external-control witness; extension trace | App DEL-09-09 (CLM-003) | Receives this contribution and its fixture results; never claims the joined witness |
| Integrated host guide | App DEL-03-04 | Receives §§1–9 for its external-access row |
| Endpoint/server or CLI construction; catalog implementation; domain objects and truth; validation; application; receipts; host views; offering, capturing and presenting human acts; host enablement facility | External host owner — SWBPIPE outside session (CLM-001, CLM-003) | Requirements and relay questions only (§12); no host behavior assumed |
| A13 enabling or disabling external access | The person (D2e; R2-3) | Consumes its evidence; the agent may only request it (A8) |
| A4, A5, A6, A7, A10, A12 | The person; A7 the accountable professional | Consumes captured evidence; never records one without it |
| A14 answer tool permission | The person, or the user's own Codex mode | Observes the settlement; never answers |
| OI-001 / OI-002 rulings | The owner (DECISION-1 D2/D3) | Carried as adopted through DEL-04-01 P-01/P-04 |
| `OI-021` operation-specific additions; first connected operation | Owner via the outside SWB session and App/shared owner | `UNRESOLVED{OI-021}` |
| `OI-003` extension promise | Owner with host contract owner | `UNRESOLVED{OI-003}`; this file supplies evidence of adapter work only |
| `OI-013` / `OI-014` placement | Shared contract owner with SWB implementation owner / App-shared contract owners | `UNRESOLVED{OI-013}` / `UNRESOLVED{OI-014}` |
| MCP-versus-CLI selection, transport, authentication, wire schemas (TBD-007) | App external-host integration owner **with** external host owner | Registered in §9; not selected |
| Professional reliance, certification, sealing, code compliance | The accountable professional | Never inferred |

---

## 2. The receiving path in outline

```text
 the person ──A13──► host external-interface enablement (host-captured; §3)
     │                              │ off ⇒ "channel not enabled" (host-reported)
     │ App-side access configuration│ on
     ▼  (person-directed; §3.2)      ▼
 App's Codex (stock App Server, pin 0.158.0; App process owns it; HOSTING)
     │ native tool use by the model: an MCP tool call, or a CLI command run
     │ through Codex command execution — one of the §9 realization families
     │    ├─ A14 tool permission (user's own Codex setting) — App-side, R13 only
     ▼
 host catalog-derived endpoint (MCP server or CLI over the live controller)
     ▼
 host's one validation/application route  ──► C §4.1 / P §9 outcome, receipt
     ▼
 App observes the native item (arguments, result, status) and records R7/R9/R11
```

Two **realization families** exist; neither is selected (§9 OC-2):

- **Native (N).** The App's Codex reaches the host endpoint through its own
  native capability: a configured MCP server whose tools the model calls
  (N-MCP), or the host CLI run through Codex command execution (N-CLI). No
  App code sits on the dispatch path; the App configures (with the person),
  observes and records.
- **Interposed (I).** App code sits on the dispatch path and forwards to the
  host endpoint: App-registered dynamic tools (I-DT; `thread/start` field
  `dynamicTools` and server request `item/tool/call`, both
  `observed-in-generated-types`, `dynamicTools` **experimental-only** at the
  pin), or an App-side local MCP proxy the App's Codex is configured to use
  (I-PX).

**When an adapter is "needed" (PROPOSED).** The SoW asks for a receiving
adapter "as needed". This file defines the need precisely: an App-interposed
adapter is needed for exactly those carried elements (§5) and holds (§5.3)
that must be **App-assured** and that the host cannot hold itself. If the host
holds the run context and the checkpoint declaration (XQ-3, XQ-5), native
realization can meet every obligation below; otherwise some obligations can
be met only by interposition or not at all. The choice stays with TBD-007's
owners.

---

## 3. Enablement account (REQ-002; AC-002; SOW-184)

### 3.1 Elements (semantic)

| Element | Meaning | Supplier / evidence |
|---|---|---|
| Host enablement record | The person's A13 (enable or disable) on the host's external interface on this machine, as captured by the host's facility, with a capture-evidence reference | Host (DEP-001; XQ-2). ACT §2.1 A13 subject |
| App-side access configuration | Whether the App's Codex is configured to reach this host's endpoint (N-MCP server entry, N-CLI availability, or I-DT/I-PX registration), with its locus (§9 OC-3) and who directed it | App, at the person's direction (PROPOSED §3.3 E-4) |
| Endpoint observation | Whether the endpoint is reachable and what it reports about itself, with the observer and time | Supplier facts (§3.5) and host responses |
| Operation-level outcome | Per entry: the C §4.1 / WD §4.2.4 outcome on the external surface X | Host (catalog, exposure element 9, availability) |
| Data-boundary statement | Where data read over the channel goes: the App conversation's model destination class (RS R5), and that no other destination is added | App (observed); rule owner open (§3.4, U-X2) |
| Locality statement | The endpoint is on this machine (local process, local socket or loopback origin) | Host endpoint contract; App observation (§3.5) |

### 3.2 Channel states

The four brief states are **channel-level summary labels**. They never replace
the distinct outcome values of C §4.1, which every request still reports.

| Channel state | Condition | What a request gets | Reporter |
|---|---|---|---|
| **disabled** | No A13 enablement is in force: never enabled, disabled by A13, or host enablement not evidenced. Sub-cases: *App-side not configured*; *host reports off* | **channel not enabled**, naming "A13 not performed" (ACT §6 row 1). An App-originated or App-interposed request is **not sent** to the host | App, when its own configuration is off (**no host request**); host, when a request reached it |
| **enabled** | Host enablement record in force (A13 evidenced) **and** App-side access configuration present **and** endpoint reachable | Each operation's own outcome (C §4.1; P §9) | Host |
| **endpoint-unavailable** | Enabled, but the endpoint is not reachable, not started, failed, needs authentication, or its tool discovery failed | No operation outcome is inferred. A submission whose transport failed after sending is **outcome unknown** (§7.4); before sending, nothing was sent | App (from supplier or transport observation), naming the observed reason |
| **operation-unavailable** (situation label) | Enabled and reachable; a particular entry is not usable now | Exactly one of: **unavailable** (precondition; reason; evaluated basis) · **not exposed on this surface** (host-reported from element 9) · **missing** (no entry in the edition; discovery finding) · **version mismatch** · **not established** (mapping unresolvable, element 9 *unagreed*, catalog unreadable) · App-side **not offered** (interposed families only, §4.5) | Host for the first two; App for the rest, each naming itself |

A further qualifier, **enablement unconfirmed**, applies when the App cannot
observe the host enablement record (for example the host exposes no read of
it). It is treated as *disabled* for App-originated requests and shown as
"unconfirmed", never as *enabled* (DERIVED from S-X2 and HOSTING H8
"silence never grants").

### 3.3 Enablement rules

- **E-1 A13 is the person's act (SETTLED D2e; disable INTEGRATION R2-3).**
  Enabling and disabling are performed only by the person, through a
  capturing surface. An agent may **request** either (A8); a request changes
  nothing (ACT FX-42). An agent attempt to perform A13 is *not permitted*.
- **E-2 Host enablement is authoritative (PROPOSED; DERIVED from S-X8).** The
  App must not patch Codex, filter its notifications, veto the user's Codex
  configuration or pin sandbox policy. The App therefore **cannot** stop the
  user's own Codex from reaching a host CLI through command execution, or from
  using an MCP server the user configured independently, or the agent from
  editing the user's Codex configuration with its file tools. Only the host's
  own refusal (*channel not enabled*) guarantees "off". The App's own
  guarantee is narrower: while the App knows the channel is disabled, **the
  App makes no host request and supplies no access configuration**, and it
  displays the state truthfully (SoW AC-002 "no host request", read as the
  App's requests; F-2).
- **E-3 App-side configuration alone never enables (PROPOSED).** An App-side
  access configuration without a host enablement record leaves the channel
  *disabled*. A configuration written by an agent (for example into the
  user's Codex configuration file) is **not A13**, does not enable, and is
  recorded as an evidence limit (R11) when observed (L-ADAPTER-2).
- **E-4 App-side configuration is person-directed (PROPOSED).** The App adds,
  changes or removes its access configuration only at the person's direction
  in the App interface, shows what it changed and where (§9 OC-3), and never
  on an agent's instruction. Whether that App-side direction is itself part
  of A13, a second A13 captured by the App, or an ordinary user
  configuration change is **U-X1** (DEL-04-01 with the owner and host owner).
- **E-5 Enablement grants no autonomy (SETTLED V4-HI-52 with W-f; DERIVED).**
  Enabling changes no grant state, no class and no checkpoint. After
  enablement the external agent is governed by the **same** host grant for
  each class (for the SWB model-change class, ⟨set-1⟩ *effective (policy
  default): propose* until the person performs A12). An enablement is never
  displayed as, recorded as, or used as A12.
- **E-6 Enablement grants no data destination (SoW REQ-002).** See §3.4.
- **E-7 Machine-local (SETTLED V4-HI-52).** Only a local endpoint is a valid
  target: a local process, a local socket, or a loopback origin. A
  non-loopback origin observed for the host's server entry (§3.5) makes the
  channel **not established** for this contract, whatever the supplier
  reports.
- **E-8 Disabling during work (PROPOSED; host behavior XQ-2).** Disabling
  stops new external requests (*channel not enabled*). It withdraws nothing:
  a proposal already queued stays queued and the person can still decide it
  in the host. The App shows the last observed state with "channel since
  disabled", never *withdrawn*, *rejected* or *outcome unknown* merely
  because observation stopped (L-ADAPTER-6).
- **E-9 No silent re-enable.** Reconnect, endpoint restart, App relaunch or
  supplier restart never restores *enabled* without a host enablement record
  in force at that time (HOSTING H8).

### 3.4 Data boundary (REQ-002; V4-HOST-02; V4-EXM-23)

- Content read over the channel enters the App's Codex conversation and
  therefore reaches **that conversation's model destination**: the user's
  Codex model provider, local or user-chosen cloud (RS R5 records the
  observed class).
- The person's A13 enables the channel. It does **not** by itself establish
  that host content may reach that destination, and it adds no other
  destination (no App relay, no App telemetry, no remote endpoint).
- V4-HOST-02 governs the **host's own agent** in local operation. This file
  does not silently extend it to every App conversation (SoW REQ-002), nor
  does it waive it. Whether the host imposes a rule on the destinations that
  may receive content read over its external channel, and who selects the
  "local/privacy data boundary" the SoW asks the adapter to carry, is
  **U-X2** (owner with host owner; XQ-11).
- Until U-X2 is decided, the App **carries** the boundary by: showing the
  conversation's model destination class at enablement and with each
  external read in the record; never adding a destination; and attributing
  supplier-initiated traffic (for example the plugin fetch the W11 spike
  `observed`, S-F-10) to the supplier, not to the channel (VER-002).

### 3.5 Supplier facts at 0.158.0 that bear on channel state

All facts below are `observed-in-generated-types` unless marked. None was
exercised live.

| Supplier fact | Bearing on this contract |
|---|---|
| Stable client methods `config/mcpServer/reload`, `mcpServerStatus/list`, `mcpServer/resource/read`, `mcpServer/tool/call`, `mcpServer/oauth/login`; stable notification `mcpServer/startupStatus/updated` (startup state ∈ `starting`, `ready`, `failed`, `cancelled`; failure reason `reauthenticationRequired`) | N-MCP endpoint observation and reload after a person-directed configuration change |
| Per-server status: `name`, `tools` (map of tool descriptors: `name`, `description`, `inputSchema`, `outputSchema`, `annotations`, `_meta`), `toolsError` ("Tool discovery failed and no catalog was returned"), `authStatus`, `runtimeStatus` ∈ `notStarted`, `starting`, `connected`, `authenticationRequired`, `failed`, `cancelled`, `disabled`, `httpOrigin` (null for non-HTTP transports), `serverInfo` | `connected` + tools → reachable; `failed`/`authenticationRequired`/`notStarted`/`cancelled` → *endpoint-unavailable* with that reason; `toolsError` → every entry *not established*; `httpOrigin` is the locality evidence for an HTTP server (E-7). The supplier's **`disabled` is an App-side configuration fact, never the host's A13 state** |
| Typed `Config` has **no** MCP-server element; `Config` admits additional properties; `config/value/write` and `config/batchWrite` write a key path into the user's configuration file by default; `thread/start` carries a free-form `config` object | The App-side configuration locus is open (OC-3). Whether a per-thread `config` override accepts an MCP-server entry is `not-observed`. Writing the user's shared configuration is a change to the person's own Codex configuration (E-4) |
| Thread item `mcpToolCall` {`server`, `tool`, `arguments`, `status` ∈ `inProgress`/`completed`/`failed`, `result` {`content`, `structuredContent`, `_meta`}, `error` {`message`}, `readOnlyHint`, `durationMs`}; notification `item/mcpToolCall/progress` | What the App can observe of an N-MCP dispatch and its result (§4.4, §5) |
| `ToolExposureSurface` ∈ `direct`, `deferred`, `code_mode` | Codex's model-facing presentation of a tool. **Not** the catalog's exposure element 9 (§4.2) |
| Server request `mcpServer/elicitation/request` (modes include `form` and `url`); HOSTING R9 classes it person-input, answered only by the person | An elicitation answer is never host act capture (§7.6, L-ADAPTER-4) |
| Server requests `item/commandExecution/requestApproval` etc. (A14); `sandbox_workspace_write.network_access` default false; `NetworkUnixSocketPermission` ∈ `allow`, `deny` | N-CLI dispatch is subject to the user's own tool permission and sandbox (D3). Whether a local-socket CLI can reach the controller from the user's sandbox is `not-observed`; the App never changes those settings (S-X8) |
| `thread/start.dynamicTools` (DynamicToolSpec: function {name, description, inputSchema, deferLoading} or namespace) **experimental-only**; server request `item/tool/call` answered with {`contentItems`, `success`}; thread item `dynamicToolCall` | I-DT is possible only with the experimental opt-in, which changes the familiar set (HOSTING S-F-05). HOSTING classifies `item/tool/call` *known-app-unsupported* unless the App registers dynamic tools (none in this increment) |
| Legacy decision form `approved_mcp_policy_amendment` exists | Whether an MCP tool call raises an A14 request at 0.158.0, and by which request kind, is `not-observed` |

---

## 4. Receiving catalog entries through the App's Codex (REQ-001; AC-001)

### 4.1 Native-tool mapping (PROPOSED element)

| Element | Meaning |
|---|---|
| Native tool reference | What the App's Codex actually invokes: an MCP server and tool name, or a CLI command form. Supplier-facing; may be constrained by the supplier's naming rules |
| Catalog operation identity and version | The DEL-03-01 entry the native tool realizes (C §3 #1) |
| Catalog edition | The edition the native surface was generated from or checked against (C §2) |
| Mapping source | Host-supplied (generated with the catalog, or declared) or unagreed. The App never derives the mapping from tool names or descriptions |

Rules:

- **NM-1** Every external dispatch record and every received result names the
  **catalog operation identity and version**, not only the native tool name.
  A workflow requirement references the catalog identity, never an
  adapter-specific tool name (WD §4.2.1).
- **NM-2** A native tool with no resolvable mapping yields **not established**
  for any requirement that depends on it; it is never reported *present*.
- **NM-3** A catalog entry exposed on X but absent from the native surface is
  a parity gap for the host's X column (C §8), reported with the edition; the
  App does not synthesize a tool for it.
- **NM-4** Whether the native surface is generated from the catalog or hand-
  built is a §8 X-column value (*unagreed* now). This file's evidence of
  mapping work is **evidence for** `UNRESOLVED{OI-003}`, not its disposition
  (SoW TBD-003).

### 4.2 What each entry must carry to the App's Codex unchanged

All nine C §3 elements reach the external surface **with the same meaning**
(C §2 invariant 2): identity and version; purpose; input schema with explicit
target identification; availability with reasons; effects; result schema with
standing; errors with effect statements; class element with its sub-elements;
exposure element 9. Open description (C §2 inv. 4): a capable consumer reads
them without Chirality software. An MCP tool descriptor or CLI help text is a
**rendering** of the entry and may not add, drop or weaken any element.

Two supplier facts must not be confused with catalog elements (PROPOSED):

- A tool's `readOnlyHint` or other annotation is a **hint**. The catalog's
  effects element governs whether an operation is a read or a change. A
  mismatch is recorded as an evidence limit and the entry's effects are used
  (L-ADAPTER-3).
- Codex's tool exposure surface (`direct`/`deferred`/`code_mode`) is **not**
  element 9. A deferred tool is still *exposed*; *not exposed on this surface*
  comes only from the host (R2-4).

Reserved entries (OP-C6, OP-C7, OP-C8) are **always described and, where
exposed, offered** on X. The App never withholds, hides or filters an exposed
entry on its own reading of its class (C §2 inv. 5; R2-4).

### 4.3 Reads: content, standing and basis

- **RD-1** A successful read over X returns the same meaningful content and
  standing marks the person sees (V4-HI-10/12; C §6.1), including currency,
  "host checks passed: ‹named checks›" each with its evaluated basis, known
  limitations, human-act evidence with actor and recorder, and lapse state.
- **RD-2** Every read carries its **basis descriptor** (workspace identity,
  generation, model revision, canonical content identity, method designation)
  and per-row **subject content identities** (C §5). A read lacking any
  element is *basis incomplete* and cannot be cited for a change.
- **RD-3** The App delivers the native result unchanged (HOSTING H6). The App
  display of standing takes standing from the **host result**, never from the
  model's paraphrase of it; a model summary that strengthens standing is shown
  as the agent's text, not as the host's standing (DEL-04-02 §8 applies).
- **RD-4** Lost read response: no content is invented; a re-read obtains a new
  basis (C §7). Reads have no effects, so no model *outcome unknown* applies.
- **RD-5 Basis-citation check (PROPOSED).** The App compares each change
  request's relied-on basis with the reads the agent **actually received** in
  this conversation. A cited basis not observed in a prior read is recorded
  as an evidence limit ("cited basis not observed"); in interposed families
  the App may refuse to forward it (App-side failure, never a host outcome).
  This guards against a later basis being cited in place of the relied-on one
  (REQ-004; HI §11 queue-time basis risk).

### 4.4 Non-mutating checks (REQ-001)

A declared non-mutating operation is carried like any read: OP-C3 *Examine
support spacing* yields the requester's **findings (A3)**, never "host checks
passed" and never A4; OP-C12 *Run support-spacing host check* yields "host
checks passed: support spacing" or "host check failed: support spacing", each
with its evaluated basis. Neither is refused as *stale*; if the evaluated
basis differs from a cited one, both are stated (C §5.4).

### 4.5 Mapping native results to canonical outcomes (PROPOSED rules)

- **M-1 Transport success is not an outcome.** A completed MCP call or a
  zero exit status establishes only that the endpoint answered. The outcome
  is what the **host's result states** in C §4.1 / P §9 terms.
- **M-2 Host-stated outcomes are relayed unchanged**, with their reporter
  (host) and evaluated basis: *unavailable*, *not permitted* (naming the
  governing treatment or checkpoint constraint), *channel not enabled*, *not
  exposed on this surface*, *refused — invalid / stale*, *queued*, *applied
  (receipt)*, *application error*, *error*.
- **M-3 No outcome stated.** A read without a stated result is *error* as
  observed. A submission whose result states no outcome, or whose result
  cannot be interpreted, is **outcome unknown**, observer *App*, last observed
  state *submitted*; never *queued* or *applied*.
- **M-4 Supplier-reported call failure** (for example an `mcpToolCall` item
  with status `failed` and an error message) is a **supplier/transport
  observation**, not a host refusal. For a submission it is *outcome
  unknown* (observer App, via supplier) unless the host's own result is also
  observed.
- **M-5 App-side failures are named as App-side**: *channel not enabled*
  (App's own configuration off), *not offered* (interposed families: an
  operation absent from the edition the App offered; never dispatched,
  R2-4), *not established* (mapping). None is reported as a host outcome, and
  none is labeled *not exposed*. In native families, a supplier's or host's
  response to an unknown tool or command is relayed as observed with its
  reporter, and mapped to *missing* only on a host statement.
- **M-6 A14 settles App-side.** If the person (or the user's own Codex mode)
  declines the tool execution, no host request was made; it is recorded in
  R13 only and is not a host outcome. An affirmative A14 never stands for A5,
  A13 or any other act (S-X7; HOSTING R8).

---

## 5. Dispatch carriage (R2-12; R-7; P §3.3)

### 5.1 External dispatch record

Mirrors LOOP §6.2 for the external channel. Every dispatch carries, or the
record states it lacks, each element. **Carriage assurance** (PROPOSED
vocabulary) says how the element reached the host:

- **App-assured** — added or verified by App code on the dispatch path
  (interposed families only);
- **host-held** — the host holds its own copy (for example a run association
  or the selected workflow's declaration registered with it), so the dispatch
  need not carry it;
- **model-supplied** — composed by the model as a tool argument; observed
  and compared by the App, but not guaranteed;
- **absent** — not carried; recorded as an evidence limit (RS R11).

| Element | Meaning | Source | Assurance required (PROPOSED) |
|---|---|---|---|
| Origin | Author type *agent*; author identity (the App's Codex seat); channel *external agent*; conversation (the Codex thread); workflow run identity; workflow identity tuple {kind, origin, source root, name, revision} (+ derived-from); holding library | P §3.3; R-9; R2-20 | Any; a host origin mark is **linked, not copied**; mismatch → evidence limit (§5.4) |
| Seat role meaning | The role meaning in force for the App seat, or *unknown* | P §3.3 | Any |
| Grant in force | Settings reference, display state and scope for the operation's class, as last observed from the host | R-8; R2-6; AS §3 | Any; the host resolves treatment itself (§5.5) |
| Requested mode | Apply directly or propose | P §2 | Any |
| **Governing checkpoint constraint** | {workflow run, checkpoint name, required act A5, operation} when a declared A5 checkpoint governs this operation's result in this run | R2-12; P §3.3; ACT §4.4 | **App-assured or host-held only** (§5.3) |
| Relied-on basis | Basis descriptor(s) with method designation; per-target subject content identities | C §5.4; P §3.2 | Any, with the RD-5 check |
| Catalog edition and entry version | As offered or as mapped (§4.1) | C §2; LOOP O-3 | Any |
| Proposal identity | Minted **before** the first submission; unchanged on every retry | P §3.1; R-7; R2-13 | Model-supplied acceptable for *propose*; App-assured or host-issued for *apply directly* (§5.6) |
| Reason | The proposer's reason | P §3.3 | Any |
| Correlation identity | The native call identity and the Codex thread/turn identities | HOSTING H6 | Observed by the App in every family |

### 5.2 Carriage by realization family

| Element | N-MCP / N-CLI (native) | I-DT / I-PX (interposed) | With a host-held run association (any family) |
|---|---|---|---|
| Origin: conversation, workflow run, workflow identity | model-supplied (the model must be told and must copy them) | App-assured | host-held |
| Author identity | unverified (PR #885 description: controller metadata "does not claim a verified Codex/person identity") | App-assured to the endpoint; host verification still open (OC-6) | as host verifies |
| Grant in force | model-supplied or absent | App-assured (from last host read) | host-held (the host's own grant) |
| Governing checkpoint constraint | model-supplied — **insufficient** (§5.3) | App-assured | host-held |
| Relied-on basis | model-supplied; RD-5 after the fact | App-assured after RD-5 before dispatch | model-supplied or App-assured |
| Proposal identity on retry | model-supplied | App-assured | host-issued draft identity if offered (XQ-5) |

### 5.3 Governing checkpoint constraint (R2-12)

- **GC-1 (SETTLED/DERIVED, ACT §4.4).** Under the constraint the host route
  resolves *propose*. A direct request is **not permitted**, naming the
  constraint as the governing treatment, and is **never converted** into a
  proposal. The agent may submit a proposal separately; its queued items
  become the checkpoint's subject (reached-when kind (c), R2-17).
- **GC-2 An omitted constraint is indistinguishable from none (R2-12).** On
  the external channel the consequence is sharp: if the model omits it and
  requests direct application under an effective direct grant, the host would
  apply directly and the checkpoint would be bypassed (contrary to W-b).
- **GC-3 (PROPOSED; held for DEL-02-03, U-X3).** For a run whose selected
  workflow declares an A5 checkpoint on an operation, the external channel
  is usable for that operation only when the constraint is **App-assured or
  host-held**. With model-supplied carriage only, the required-tool
  compatibility outcome for that operation on X is **not established**, and
  the check does not pass (WD §4.2.4). This is a proposal to DEL-02-03, not a
  hold this file imposes.
- **GC-4** Whatever the family, the App records the constraint it expected
  (derived from the selected declaration, WD §4.2.2) beside the one observed
  in the dispatch. An omission in an App-carried run is an **App-side
  defect**, recorded as "omitted governing checkpoint constraint" (RS R11;
  P §3.3).
- **GC-5 Reached-when kind (a) on X (PROPOSED finding, U-X3).** Holding a
  call *before dispatch* requires App code on the dispatch path or a host
  that holds the declaration. In native families the App can neither hold
  the call nor rely on an A14 prompt (the user's Codex mode may not raise
  one, and an App rule may only decline, never hold-and-release). Kind (a)
  checkpoints over X are therefore *not established* in native families
  unless the host evaluates the declaration.
- Until host evidence of constraint receipt exists, V-CP1 over X is
  **AWAITING INPUT** (U-P10).

### 5.4 Origin

- The App records the request-side origin it observed (R7). The host's
  origin mark is **linked, not copied**; a mismatch is an evidence limit
  (P §3.3; V4-HI-71).
- Author identity over X is **unverified** until a caller-identity mechanism
  exists (OC-6). The record shows "external agent (unverified identity)"
  rather than asserting the App's Codex as the author.
- Channel is always *external agent*. The channel is attribution, never a
  route selector (P §2).

### 5.5 Grant in force

- The host holds the grant; the App holds none for host operations (R-2 D3
  bullet: the autonomy grant governs host operations only). The App reads it
  from the host for display and carriage.
- Standing at drafting and treatment at resolution are both recorded when
  they differ; the settings reference at application is **host-reported** or
  *unconfirmed* (R-3.6; R-8).
- Narrowing leaves a queued proposal unaffected; an unapplied direct request
  is re-resolved at application and becomes *not permitted* if no effective
  direct treatment remains. Widening never converts a queued proposal
  (R-3.6/3.7; ACT FX-37/38).

### 5.6 Proposal identity on retry

- **PI-1** A retry (resubmission after a lost acknowledgment or *outcome
  unknown*) carries the **same** proposal identity and unchanged content.
  The host de-duplicates by identity **before** any basis check and answers
  from the recorded state; a retry is never refused *stale* because of its
  own effects (R2-13).
- **PI-2** After *outcome unknown* the App (or, in native families, the
  agent following App-supplied guidance) **seeks observation first** — a
  host read of the proposal by identity — before any resubmission (LOOP R-d).
- **PI-3** A re-draft is a new proposal with lineage, a new read and new
  change-item content identities; no acceptance carries over (P §5).
- **PI-4 Durability limit (evidence, PR #885).** The PR description states
  that repeated submit keys recover the original result "within the same
  controller session" and that recovery "does not survive a controller
  restart". A retry after an endpoint restart may therefore be treated as a
  first receipt. Under *propose* this risks a second queued proposal, not a
  second effect without the person's A5; under *apply directly* it risks a
  second effect. PROPOSED: over X, *apply directly* requires an App-assured
  or host-issued identity whose de-duplication survives endpoint restart;
  otherwise a post-restart retry is reported *outcome unknown* and the
  one-effect obligation is recorded as unevidenced (XQ-5; L-ADAPTER-5).

---

## 6. Same route and same policy as the host UI (REQ-003; AC-003)

- **RP-1 One route (SETTLED S-X4).** Every external change goes to the host's
  one validation/application route. The App defines no alternate mutation
  path, never applies outside the host route, and never bypasses validation
  (P §2; AC-003). Interposed families forward only; they add carried
  elements and App-side failures and decide nothing.
- **RP-2 Equivalence.** For equivalent operation identity/version,
  arguments, relied-on basis and authority, X receives the same outcome and
  error meaning (identity and text) as H and E (P §2). The permitted
  difference is authority only, reported as *not permitted* naming the
  governing treatment, never as a different validation error.
- **RP-3 Treatment outcomes on X** (ACT §5.3, §6; consumed unchanged):

  | Situation on X | Outcome |
  |---|---|
  | A13 not performed | **channel not enabled** (§3.2) |
  | Declared catalog precondition fails | **unavailable**, same reason and evaluated basis as H and E (V4-HI-04; C §10.6) |
  | Entry not exposed on X (element 9) | **not exposed on this surface**, host-reported, relayed |
  | Direct requested without an *effective direct* treatment (policy default *propose*; unconfirmed; requested by agent; not set; refused) | **not permitted**, naming the policy record; **never converted** into a proposal |
  | Direct requested under a governing checkpoint constraint | **not permitted**, naming the constraint (§5.3) |
  | Operation performs A4, A5, A6, A7, A10, A12 or A13 (P-02) | **not permitted**; an A8 request is **offered**, recorded only if the agent issues it |
  | Class *no policy basis* (P-06) | direct **not permitted**; proposing available and confers no permission; A12 widening refused; dependent production **held** |
  | Class *proposal only* | *propose*; no grant widens it |
  | Effective direct grant in scope, no constraint | apply directly: receipt, origin mark, undo route, later-check route; **no acceptance recorded** |

- **RP-4 Channel-specific host restriction (evidence, PR #885).** The PR
  description states that "Apply stays in the app's human review route". If
  the host treats all external changes as proposals regardless of grant, that
  is a host policy about the channel. It must be **stated by the host** as a
  governing treatment (so a direct request is *not permitted* naming it) and
  never presented as a class value or as the grant (S-X3; XQ-8).
- **RP-5** App-side A14 precedes any host request and is not a host outcome
  (M-6). No classifier or permission layer is added on X by the App (D3).
- **RP-6** Undo over X (OP-C10) is a change through the same route with its
  own treatment, governed by the policy record of the operation whose receipt
  it reverses (R3-4); its outcome carries *reverses ⟨receipt⟩*.

---

## 7. Outcomes, acts and faithful recording (REQ-004; AC-004, AC-005)

### 7.1 Stale refusal and original basis

A submission cites the basis it relied on, unchanged from the read; the host
checks per item against the relied-on targets' subject content identities
(R2-13). A stale refusal is relayed with reason, failing targets, relied-on
basis and current basis (P §5). No App component rewrites the relied-on basis
and resubmits; a re-draft is a new proposal (PI-3).

### 7.2 No retargeting

Bound targets are fixed at drafting from explicit target identification. A
later selection in any surface — including the person selecting S-4 in the
host UI while an external proposal is pending — never changes them (P §6).

### 7.3 Repeated submission

Each submission is recorded separately with only the effects actually
observed (same receipt, two receipts, or unknown). One effect per item is a
**host obligation to be evidenced** (DEP-001), not a recorded fact; transport
or session de-duplication is not evidence of one domain effect (V4-EXM-25;
PI-4).

### 7.4 Outcome unknown

Reported whenever the result of a sent step cannot be observed, attributed to
the observer that lost it — here the **App** (directly, or via a supplier
report) — with the last observed state. Never inferred applied, failed,
accepted or rejected; a later observation is reported separately and does
not back-fill (P §4.1 rule 3).

### 7.5 Human acts are never fabricated

- Success, *queued*, a receipt, an A14 answer, an A8 request, a model
  statement or an MCP elicitation answer **never** establishes A4, A5, A6,
  A7, A10, A12 or A13.
- The App reports *queued* until the host records acceptance and
  application; "accepted" only with host-captured A5 and its actor; "applied"
  only with a receipt (P §4.1).
- Execution, edit acceptance, checking, approval and reliance keep separate
  standing. An independently evidenced act (for example T2's A4 on S-2 with
  no proposal) is carried without any acceptance predecessor (SoW REQ-004;
  ACT FX-07).

### 7.6 Positive faithful recording (A9)

When a host read over X reports an actually performed act (for example T11:
A5 on PR-2 item 1 and A10 on item 2 by Engineer A, captured by the host
facility), the App may record it **faithfully**: decision actor Engineer A;
recorder the App; recording mode *faithful recording*; bound content identity
(the change-item content identity for A5/A10, the subject content identity
for A4/A6/A7) with method designation; and the host's **capture-evidence
reference**. Without that reference the record is a record shape only and
satisfies no checkpoint (R-5; R2-20; XQ-10). An MCP elicitation or CLI
prompt answered in the App is **not** host act capture for acts on host
content (L-ADAPTER-4).

### 7.7 Checkpoint observation on X

For an A5 checkpoint with reached-when kind (c) *proposal queued*, the App
observes *queued* and later the host-captured item decisions through host
reads over X and passes them to the hold machine (DEL-02-03). The adapter
observes and reports; it does not hold, resume or evaluate dispositions.
Dispositions use the shared vocabulary: waiting · performed · resolved
negatively · lapsed · not reached · unknown.

---

## 8. Operating sequences

```text
S-1 Enable
  person performs A13 in the host facility ──► host enablement record (+capture ref)
  person directs App-side access configuration (E-4) ──► App configures (locus OC-3)
  App observes endpoint (reachable? locality?) ──► channel: enabled | endpoint-unavailable
  grant display unchanged (E-5); data destination shown (§3.4)

S-2 Inspect (read)
  model invokes native tool for OP-C1 ──[A14 per user's Codex mode]──► host read
  ◄── content + standing + basis B + subject identities (or a C §4.1 non-success)
  App records R7 (operation identity/version via §4.1 mapping, correlation, basis)

S-3 Submit a proposal
  model composes change citing B, targets, proposal identity, origin, [constraint]
  App: RD-5 basis-citation check; GC-4 expected-constraint comparison
  ──► host route: de-duplicate → treatment → per-item basis check
  ◄── queued | refused — stale/invalid | not permitted (named) | … (P §9)
  App reports queued (never accepted); observes item decisions by later reads

S-4 Lost acknowledgment
  submission sent; no result observed ──► outcome unknown (observer App)
  seek observation (read by proposal identity) ──► recorded state reported separately
  only if never received: retry with the same identity (PI-1…PI-4)

S-5 Disable
  person performs A13 (disable) ──► host refuses new requests: channel not enabled
  App removes its configuration at the person's direction; queued proposals unaffected (E-8)
```

---

## 9. Open-choice register — MCP versus CLI and related choices (TBD-007)

Nothing here is selected. Each row names its owner and point of need. Owner
for every row unless stated: **App external-host integration owner with the
external host owner** (SoW TBD-007). Point of need unless stated: **before
the App receiving implementation depends on it, and before DEL-09-09
qualification** (CASE-002 M2-A). V4-HI-50 lets the **host** choose which
seam it offers; the App receives the seam the host selects (DEL-09-09
REQ-002).

**Observed context — draft PR #885 (evidence only; not a commitment, not
merged, not a delivered SWBPIPE contribution).** From its description at head
`12907f39`: an **opt-in local JSON CLI** over a **private Unix-socket bridge**
to the running Piping desktop controller (the host this basis calls the
Piping controller, HI §11); operations "inspects Node data, previews single
or ordered atomic `position.x` edits, submits frozen proposals to the existing
review queue, and retrieves their outcomes"; "Apply stays in the app's human
review route"; acknowledgements follow published controller state; repeated
submit keys recover the original result within the same controller session,
and recovery does not survive a controller restart; controller metadata does
not claim a verified Codex/person identity; the optional CLI is excluded from
normal desktop packaging; the isolated self-test did not launch the live
controller, and no ordinary live endpoint or actual-human witness has been
recorded. Whether its operations are catalog-derived, whether its opt-in is a
person's captured A13, and how its outcomes map to P §9 are not stated.

| Id | Choice | Options | Evidence at pin 0.158.0 and observed context | What depends on it | Owner / point of need |
|---|---|---|---|---|---|
| OC-1 | Transport family the host offers | (a) MCP server; (b) CLI over the live controller; (c) both | MCP: stable client methods and `mcpToolCall` items (`observed-in-generated-types`). CLI: Codex command execution with A14 approval kinds (`observed-in-generated-types`). PR #885: a CLI instance (evidence only) | §3.5 observation; §4.5 mapping; §5.2 carriage; VER-001/002 | Host owner selects with App owner agreement |
| OC-2 | App realization family | N-MCP; N-CLI; I-DT; I-PX | I-DT needs the experimental opt-in (`dynamicTools` experimental-only; S-F-05). I-PX is an App-side server — tension with SoW OUT-001 "without prescribing … a new server" (F-6) | Carriage assurance (§5.2), GC-3/GC-5 holds, PI-4 | App owner, after XQ-3/XQ-5 answers |
| OC-3 | App-side configuration locus | (a) user's Codex configuration file (via `config/value/write` / `config/batchWrite`, or by the person by hand); (b) per-thread `config` on `thread/start`; (c) a Codex plugin; (d) none (N-CLI with the CLI on the person's path) | Typed `Config` has no MCP element; per-thread acceptance `not-observed`; plugin association appears in server status (`pluginId`). Writing the shared file changes the person's own Codex configuration (S-X8) | E-3, E-4, U-X1; reversibility; what "disable" removes | App owner with DEL-01-01 (and DEL-01-05 in the later undertaking) |
| OC-4 | Enablement loci | (a) host-side only; (b) App-side only; (c) both, host authoritative (PROPOSED E-2/E-3) | App cannot guarantee "off" App-side (S-X8). PR #885 "opt-in": nature not stated | §3.2 states; AC-002 reading (F-2); A13 capture (U-X1) | DEL-04-01 with owner and host owner |
| OC-5 | Local transport and endpoint locality | stdio subprocess launched by Codex; loopback HTTP (`httpOrigin`); local socket (PR #885) | `httpOrigin` null for non-HTTP (`observed-in-generated-types`); sandbox effect on a local-socket CLI `not-observed` | E-7 locality evidence; VER-002 | Host owner with App owner |
| OC-6 | Caller authentication and identity | none (PR #885: identity not verified); local-socket permissions; a token issued at enablement; supplier OAuth (`mcpServer/oauth/login` exists; its fit for a local endpoint `not-observed`) | See left | §5.4 author identity; multiple local callers; A13 scope | Host owner with App owner |
| OC-7 | Carriage mechanism for origin, constraint, grant and proposal identity | tool arguments (model-supplied); request metadata added by App code; host-held run association registered at run start; host-issued draft identity (preview step) | Whether the App can add metadata to a model-issued MCP call `not-observed`. PR #885 has a preview step and submit keys (evidence only) | §5.1–§5.6; GC-3; PI-4 | Host owner with App owner and DEL-03-02 |
| OC-8 | Native surface derivation | generated from the catalog; checked against it; hand-built | PR #885 operation set looks narrow and specific (Node data; `position.x`); derivation not stated | NM-3/NM-4; C §8 X column; `OI-003` evidence | Host owner; disposition `UNRESOLVED{OI-003}` |
| OC-9 | Result and outcome encoding | MCP structured content; MCP text content; CLI JSON on standard output with exit status | `McpToolCallResult` {`content`, `structuredContent`, `_meta`}; no error flag element observed in the generated result type | M-1…M-5 | Host owner with App owner and DEL-03-02 (TBD-002 mechanics) |
| OC-10 | Outcome read-back by proposal identity | host read operation; none | PR #885 "retrieves their outcomes" (evidence only) | S-4; PI-2; T13 | Host owner |
| OC-11 | Checkpoint hold on X | host evaluates the declaration; App interposition; App interrupts the turn | `turn/interrupt` exists (stable); hold semantics are DEL-02-03's | GC-3, GC-5, §7.7 | DEL-02-03 (W7) with host owner |
| OC-12 | Tool-permission interplay | whatever the user's Codex setting produces | Command approvals (A14) `observed-in-generated-types`; MCP-call approval path `not-observed`; `network_access` default false | M-6; RP-5; VER-002 destination inspection | Carried unchanged (D3); App implementation owner records observations |

---

## 10. Consumer fixture inventory (OUT-003) — transport-neutral, simulated

Every case below runs against a **simulated endpoint (test double)** unless a
row says otherwise; its evidence label is *illustrative* until executed and
*test-double* when executed (C-v0.3 evidence-label mapping; LOOP §12
FIXTURE-EXECUTED; PANEL EXECUTED on a test double). No case establishes host
behavior, host delivery, person enablement or the joined witness (DEL-09-09).
Each case is run once per realization family actually selected (§9 OC-2),
because carriage assurance differs; where a case depends on an unanswered
relay question it is **AWAITING INPUT**, and where it depends on an unruled
policy it is **HELD**.

### 10.1 Local subjects (named per R2-21, with reasons)

| Label | What it is | Why local |
|---|---|---|
| L-ADAPTER-1 | Channel states: never enabled; enabled; endpoint stopped; endpoint needs authentication; tool discovery failed | C §10 declares no enablement fixture; A13 is not a catalog entry (C §10.2 note) |
| L-ADAPTER-2 | The agent writes an App-side access configuration for the host into the user's Codex configuration | Adapter-specific risk from S-X8 |
| L-ADAPTER-3 | OP-C9's native descriptor carries a read-only hint although its effects are a change | Native hints are adapter-specific |
| L-ADAPTER-4 | The host endpoint asks, through an MCP elicitation or CLI prompt, "accept PR-2 item 1?" | Adapter-specific act-capture risk |
| L-ADAPTER-5 | Endpoint restart between T12 and the T13 retry | PR #885 session-scoped recovery |
| L-ADAPTER-6 | Person disables external access (A13) after T10, before T11 | C has no channel event |
| L-ADAPTER-7 | Person declines the tool execution (A14) of the T7 submission | App-side A14 is outside C |
| L-ADAPTER-8 | App conversation uses a user-chosen cloud model destination | Data-boundary case |
| L-ADAPTER-9 | In native carriage, the model omits the constraint in V-CP1 | Carriage-assurance case |
| L-ADAPTER-10 | The host origin mark names a different conversation than the App observed | Origin-mismatch case |

### 10.2 Cases

| Case | Steps / subject | Expected result | AC / VER |
|---|---|---|---|
| XF-01 Disabled, App-side off | L-ADAPTER-1 never enabled; a workflow requiring OP-C1 on X; agent attempts T3 | Channel *disabled* (reporter App); required-tool outcome *channel not enabled*; **no host request** from the App; never *unavailable* or *missing* (ACT FX-24) | AC-002 / VER-002 |
| XF-02 Disabled, host-side off | App-side configured; host enablement absent; agent attempts T3 | Host-reported **channel not enabled**, relayed with reporter host; channel *disabled* | AC-002 / VER-002 |
| XF-03 Agent-written configuration | L-ADAPTER-2, host enablement absent | Channel stays *disabled*; any request → host *channel not enabled*; evidence limit recorded; not A13 (E-3) | AC-002 / VER-002 |
| XF-04 A13 requested by agent | Agent asks the person to enable; separately attempts to enable | Request: A8 offered, recorded only if issued; attempt: *not permitted* (ACT FX-42); state unchanged | AC-002, AC-005 / VER-002, VER-005 |
| XF-05 Enablement grants no autonomy | Person performs A13 at T1 | Grant display for P-03 remains *effective (policy default): propose* (⟨set-1⟩); no A12 recorded; data destination shown (§3.4) | AC-002 / VER-002 |
| XF-06 Endpoint unavailable | L-ADAPTER-1 endpoint stopped; needs authentication; tool discovery failed | *endpoint-unavailable* with the observed reason; discovery failure → every entry *not established*; no operation outcome inferred; supplier `disabled` status never read as A13 | AC-002 / VER-002 |
| XF-07 Locality | Host entry resolves to a non-loopback origin (variant) | *not established* (E-7); no request sent by the App | AC-002 / VER-002 |
| XF-08 Unavailable parity | T8 over X (C §10.6) | *unavailable*, failed precondition "current solve exists", reason R-no-current-solve, same statement, evaluated basis B2 — identical to H and E | AC-001, AC-003 / VER-001, VER-003 |
| XF-09 Not exposed | V-X1 (OP-C9 not exposed on X) | Host-reported **not exposed on this surface**, relayed (reporter host); never *missing* or *channel not enabled* | AC-001 / VER-001 |
| XF-10 Not offered vs unknown tool | Interposed: call naming an operation absent from the offered edition. Native: model invokes an unknown tool name | Interposed: App-side *not offered*, never dispatched. Native: supplier/host response relayed with reporter; *missing* only on a host statement; never *not exposed* | AC-001 / VER-001 |
| XF-11 Read parity and basis | T3 over X | Content, subject identities ⟨S-1…S-4@r12⟩, standing and basis B1 = FX-W1/g1/r12/⟨v12⟩/⟨m-fx⟩ identical to H and E; operation identity OP-C1 v1 named via the mapping | AC-001 / VER-001 |
| XF-12 Non-mutating checks | T4 (OP-C3) and T4a (OP-C12) over X | T4: agent findings (A3), never "checked" or a host check; T4a: "host check failed: support spacing" with basis r12; neither refused stale | AC-001 / VER-001 |
| XF-13 Native hint mismatch | L-ADAPTER-3 | Catalog effects govern (change); evidence limit recorded; OP-C9 still routed as a change | AC-001 / VER-001 |
| XF-14 Stale, both bases | T5 → T6 → T7 over X | Both PR-1 items **refused — stale** per item: failing target S-3, relied B1, current B2; item-left events; no silent refresh | AC-004 / VER-004 |
| XF-15 Basis-citation check | Variant of T7 in which the submission cites B2 although the agent read only B1 | Evidence limit "cited basis not observed"; interposed families may refuse to forward (App-side failure) | AC-004 / VER-004 |
| XF-16 Re-draft and queued | T9 → T10 over X | PR-2 new identity, lineage PR-1, cites B2; **queued**, reported "queued; awaiting your decision", never accepted or applied | AC-004, AC-005 / VER-004, VER-005 |
| XF-17 No retargeting | During T10, Engineer A selects S-4 in the host UI | PR-2's bound targets remain R-100, S-2, S-3 | AC-004 / VER-004 |
| XF-18 Item decisions observed | T11 → T12, observed over X | Item 1 accepted by Engineer A (host-captured A5), then applied RC-1 with resulting objects S-5, R-100; item 2 rejected (A10); A5 not lapsed by application; acts faithfully recorded with capture-evidence reference — **AWAITING INPUT** (XQ-10) for the reference | AC-005 / VER-005 |
| XF-19 Retry precedence | T13 over X: acknowledgment lost; seek observation; if never received, retry with the same identity | Host answers from recorded state (item 1 applied RC-1; item 2 rejected); no stale refusal from its own effects; each submission recorded separately | AC-004 / VER-004 |
| XF-20 Lost outcome | V-OU1 over X | **outcome unknown**, observer App, last observed *accepted*; no inferred effect | AC-004 / VER-004 |
| XF-21 Restart before retry | L-ADAPTER-5 | If the host answers from a durable record: recorded state. If not: *outcome unknown*; one-effect recorded as unevidenced; under direct treatment the retry is not sent without a durable identity (PI-4) — **AWAITING INPUT** (XQ-5) | AC-004 / VER-004 |
| XF-22 Direct without grant | OP-C4 requested directly at r13 under ⟨set-1⟩ | **not permitted**, naming P-03 policy default *propose*; never converted | AC-003 / VER-003 |
| XF-23 Direct under grant | T15 → T16 over X | Applied RC-2 with origin mark (channel external), undo route, later-check route, both settings references; **no acceptance** recorded or displayed | AC-003, AC-005 / VER-003, VER-005 |
| XF-24 Channel-level apply restriction | Variant: host states that external changes are proposal-only (RP-4) | Direct request → *not permitted* naming the host's governing treatment; displayed as a host channel rule, not as class or grant | AC-003 / VER-003 |
| XF-25 Checkpoint constraint | V-CP1 over X with the constraint App-assured or host-held | **not permitted** naming {run 12, CP-accept, A5, OP-C4}; the separate proposal queues and becomes CP-accept's subject — **AWAITING INPUT** (U-P10) | AC-003 / VER-003 |
| XF-26 Constraint omitted | L-ADAPTER-9 (native, model-supplied carriage) | Required-tool check for OP-C4 on X *not established* (GC-3, proposed to DEL-02-03); if dispatched anyway, "omitted governing checkpoint constraint" evidence limit — **HELD** on U-X3 | AC-003 / VER-003 |
| XF-27 Reserved entry | V-R1 over X (OP-C6 on S-1) | **not permitted** (P-02), A8 offered and not auto-recorded; entry was offered, never withheld or *not exposed* for class | AC-003, AC-005 / VER-003, VER-005 |
| XF-28 No policy basis | V-NP1 over X | Direct *not permitted*; proposal queued, confers no permission; A12 widening refused; reported **held (pending OI-021)**, never pass | AC-003 / VER-003 |
| XF-29 Narrowing in flight | ACT FX-37 over X | Queued PR-2 unaffected; unapplied direct OP-C9 request re-resolved at application → *not permitted* | AC-003 / VER-003 |
| XF-30 Accepted then stale | V-S1, observed over X | "accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)"; A5 not lapsed | AC-004, AC-005 / VER-004, VER-005 |
| XF-31 Fabrication negatives | T10 *queued*; T12 receipt RC-1; an A14 accept of the T10 submission; a model message "the engineer accepted it" | None establishes A5 or any act; each attempt to record one is non-conformant (ACT FX-01/04/05) | AC-005 / VER-005 |
| XF-32 Independent act | T2 A4 on S-2, read over X | Carried with actor, recorder, bound ⟨S-2@r12⟩, direct capture; no acceptance predecessor required; not lapsed after T6; lapsed after T14 | AC-005 / VER-005 |
| XF-33 Elicitation is not capture | L-ADAPTER-4 | Answer recorded as person input only (HOSTING R9); never A5; host item stays *queued* until host capture | AC-005 / VER-005 |
| XF-34 A14 decline | L-ADAPTER-7 | No host request; recorded in R13 only; no host outcome; the proposal is not *refused* or *withdrawn* | AC-003 / VER-003 |
| XF-35 Disable while queued | L-ADAPTER-6 | New requests: *channel not enabled*; PR-2 stays queued in the host; App shows last observed *queued*, "channel since disabled"; never withdrawn or unknown for that reason | AC-002 / VER-002 |
| XF-36 Data destination | L-ADAPTER-8, T3 | Record shows destination class *user-chosen cloud*; no other destination; release of host content to it stays under U-X2 — **HELD** | AC-002 / VER-002 |
| XF-37 Origin mismatch | L-ADAPTER-10 | Host mark linked, not copied; evidence limit "origin mismatch"; author identity shown unverified | AC-001 / VER-001 |
| XF-38 Undo over X | T16a → T17 observed over X | RC-2 "applied, then reversed by RC-3"; T16a A4 shown lapsed; no act erased | AC-005 / VER-005 |
| XF-39 Generation change | Tg: read over X after restore | Bases from g1 incomparable by revision; *unknown (incomparable)*, never *unchanged* | AC-001 / VER-001 |

Coverage: AC-001 XF-08…13, 37, 39; AC-002 XF-01…07, 35, 36; AC-003 XF-08,
22…29, 34; AC-004 XF-14…21, 30; AC-005 XF-04, 16, 18, 23, 27, 30…33, 38.
AC-006 and AC-007 are served by review of §§1, 9, 12 and this inventory
(VC-X-06, VC-X-07).

---

## 11. Interfaces expected and provided

| Direction | Counterpart | Content |
|---|---|---|
| Expect from | DEL-03-01/C-v0.3 | Nine entry elements incl. element 9; five class values; C §4.1 results with reporters; read basis, subject content identities and method designation; per-item "no longer holds" rule; §8 X column; FX-PIPE-01 |
| Expect from | DEL-03-02/P-v0.3 | Change-request elements incl. governing checkpoint constraint and relied-on targets; P §9 taxonomy; retry precedence; item-left events; one route |
| Expect from | DEL-04-01/ACT-POLICY-v0.3 | A1–A14; P-01…P-06; §5.3 resolution order; §6 outcome map; V-10 external access; A13 subject |
| Expect from | DEL-04-02/AS-v0.3 | Grant display states incl. *effective (policy default)*; settings references |
| Expect from | DEL-01-01/HOSTING-v0.3 and the pin record | Supplier surfaces at 0.158.0 (§3.5); A14 origins (R7–R9); native delivery (H6) |
| Expect from | DEL-02-01 / DEL-02-03 | Checkpoint declarations and derived constraints (WD §4.2.2); hold machine; answer to GC-3/GC-5 (U-X3) |
| Expect from | External host owner (SWBPIPE) | Endpoint contract; enablement facility and its read; catalog-derived native surface and mapping; exposure on X; outcome statements; capture-evidence references; constraint receipt; identity issuance and durable de-duplication; locality; caller authentication (§12) |
| Provide to | DEL-09-09 | This account; the §10 inventory and, when executed, its candidate-bound test-double results labeled by family; the §9 register; the external requirements still missing (§12); never a joined-witness claim |
| Provide to | DEL-03-04 | §§1–9 for the guide's "Optional external catalog access" row |
| Provide to | DEL-04-03 | External dispatch entries (§5.1) for R7; faithfully recorded acts for R9; evidence limits for R11 (cited basis not observed; omitted constraint; origin mismatch; agent-written configuration; unverified identity; native hint mismatch); A14 observations for R13 |
| Provide to | DEL-02-03 | External-channel observations (§7.7); GC-3/GC-5 proposals; required-tool outcomes on X (channel not enabled; not established) |
| Provide to | DEL-04-01 | U-X1 (A13 locus) and F-4 |
| Provide to | DEL-01-01 | F-3 (MCP and elicitation surfaces to classify) |

---

## 12. Relay questions for SWBPIPE (prepared, not delivered)

For App-manager preparation and human relay to the SWBPIPE owner (DEP-001;
DEP-03-03-010/011). Writing them is not delivery, agreement or adoption.
Overlaps with LOOP §13 Q-1…Q-7 are marked; answers serve both.

- **XQ-1 Seam.** For the first increment, will you offer the external seam
  as the PR #885 CLI, an MCP server, or both? Is its operation set generated
  from (or checked against) the same catalog as your UI and embedded tools,
  and will you supply the mapping from native tool or command to catalog
  operation identity and version?
- **XQ-2 Enablement.** Is external access off by default and enabled only by
  a person's act captured by your facility, with a capture-evidence
  reference? Is PR #885's "opt-in" that act, a build feature, or a launch
  flag? When off, does a caller get an explicit *channel not enabled*? Can
  the App read the current enablement state? What happens to queued external
  proposals when access is disabled?
- **XQ-3 Constraint and run context (= Q-1).** Can your route receive a
  per-request governing checkpoint constraint, or will you hold the selected
  workflow's declaration (or a run association the App registers) and
  evaluate it yourselves? What evidence will show which?
- **XQ-4 Origin.** Which origin elements do you record for an external
  submission (author type, identity, channel, conversation, workflow run),
  and do you verify any? Can the App read your origin mark to link it?
- **XQ-5 Proposal identity (= Q-6, extended).** Who mints the proposal
  identity (submit key)? Is it available before the first submission, for
  example from the preview step? Does de-duplication precede the basis check,
  and does it survive a controller restart? Can a caller read a proposal's
  state by identity?
- **XQ-6 Basis.** Does an external read return the full basis descriptor and
  per-row subject content identities? Does a submission keep the originally
  inspected basis, not a queue-time basis (HI §11 risk)? Is the stale check
  per item on relied-on targets (= Q-6)?
- **XQ-7 Outcomes.** Does each external result state its outcome in the
  P §9 / C §4.1 terms, with evaluated basis, distinctly from transport
  status?
- **XQ-8 Grant and apply.** Does the external actor use the same grant the
  person sets per class? Is "Apply stays in the app's human review route" a
  class assignment, a channel rule, or a fixed first-increment policy, and
  will a direct external request return *not permitted* naming it?
- **XQ-9 Exposure (= Q-7).** Which entries are exposed on the external
  surface, and do you report *not exposed on this surface* from your
  exposure element?
- **XQ-10 Acts (= Q-2).** Do external reads carry captured acts with actor,
  recorder, act kind, bound content identity and a capture-evidence
  reference? Will you ever use an MCP elicitation or CLI prompt to capture a
  person's act? (This contract asks that you do not.)
- **XQ-11 Data boundary.** Do you impose a rule on which model destinations
  may receive content read over your external interface? Does V4-HOST-02 or
  another rule apply to the App's conversations?
- **XQ-12 Locality and callers.** Is the endpoint strictly local (socket or
  loopback)? How are callers authenticated, and can more than one local
  caller attach? Should the App expect its Codex sandbox to need access to
  your socket, which the App will not change on the person's behalf?

Questions for App owners (not SWBPIPE): U-X1 to DEL-04-01; U-X3 to DEL-02-03;
F-3 to DEL-01-01; U-X2 to the owner.

---

## 13. Findings (reported; scope and Wave-1 text unchanged)

- **F-1 "The external adapter carries it" presumes an adapter on the dispatch
  path.** P-v0.3 §3.3 ("Carried on every dispatch by the host loop … and the
  external adapter (DEL-03-03)"), ACT-v0.3 §4.4 ("The loop and the external
  adapter both carry it"), WD-v0.3 §4.2.2 and R2-12 assume an App process on
  the dispatch path. The SoW asks for an adapter only "as needed". In native
  realization the model composes the call, so carriage is model-supplied and
  an omission can only be recorded afterwards. Suggested wording for those
  files: "carried with an assurance of App-assured, host-held or
  model-supplied; model-supplied alone does not satisfy R2-12 for treatment"
  (GC-3). This strengthens the case for host-held evaluation (U-P10).
- **F-2 AC-002 "no host request" is achievable App-side only for the App's
  own requests.** Because the App may not veto the user's Codex configuration
  or sandbox (S-X8), agent-originated requests through the user's own Codex
  capability can reach the host whatever the App does. The authoritative
  "off" is the host's *channel not enabled*. VER-002 should read AC-002 this
  way (E-2).
- **F-3 HOSTING-v0.3 does not classify the MCP configuration and call
  surfaces.** It covers `item/tool/call` and `mcpServer/elicitation/request`
  but not `config/mcpServer/reload`, `mcpServerStatus/list`,
  `mcpServer/startupStatus/updated`, `mcpToolCall` items, or the App-initiated
  client method `mcpServer/tool/call`, which would make the **App** (not the
  agent) the caller on host content. Suggested: DEL-01-01 records these as
  receivers' surfaces and states that App-initiated tool calls carry App
  origin and are not used to act as the agent; and R9 states explicitly that
  an elicitation answer is never host act capture.
- **F-4 A13's locus is undefined for the App side.** ACT-v0.3 §2.1 gives A13
  the subject "the host's external interface on this machine". Whether the
  App-side access configuration is part of A13 is not stated; and because the
  agent can write the user's Codex configuration, App-side configuration
  cannot serve as A13 evidence (E-3). DEL-04-01 should state the capturing
  surface for A13 (U-X1).
- **F-5 ACT-v0.3 FX-25 wording.** "The external agent drives T9–T11": T11 is
  Engineer A's A5/A10, which no agent drives. Suggested: "drives T9–T10 and
  observes T11–T12".
- **F-6 SoW OUT-001 and an App-side proxy.** OUT-001 excludes prescribing "a
  new server". I-PX is an App-side MCP server; if it were chosen, the choice
  would need to be reconciled with OUT-001 through the owning route. Recorded,
  not decided.
- **F-7 C-v0.3 §4.1 reporter for *channel not enabled*.** It reads "Host (or
  App adapter observing the host's disabled state)". The App can also report
  it from its **own** configuration being off, with no host observation.
  Suggested addition: "App, from its own access configuration, with no host
  request made".
- **F-8 P-v0.3 §3.3 author identity has no *unverified* value.** Over X the
  host may be unable to verify the caller (PR #885). Suggested: author
  identity carries *unverified* as an explicit value; RS R11 lists
  "unverified caller identity" as an evidence limit.
- **F-9 Dynamic tools and the familiar set.** Choosing I-DT requires the
  experimental opt-in, which changes the server-request familiar set and
  classification (HOSTING S-F-05) for the whole App, not only this channel.
- **F-10 SoW text** TBD-001/TBD-002/REQ-003 still call OI-001/OI-002 open;
  this design applies DECISION-1 through DEL-04-01 (closeout C1).
- **F-11 Register.** DEL-03-03 `Dependencies.csv` lacks: a DOWNSTREAM mirror
  of DEP-03-04-007 (DEL-03-04 consumes this contribution); an UPSTREAM row to
  DEL-01-01 (the App's supplier surfaces; DEP-03-03-009 names only "Codex
  native-tool capability" as EXTERNAL); rows to DEL-04-02 (grant display),
  DEL-02-01/DEL-02-03 (declarations, hold, required-tool check) and DEL-04-03
  (record entries). Route to C1; genuinely new relationships through
  `project-dag` departure (R1 register findings).
- **F-12 No data-boundary owner.** SoW REQ-002 asks the adapter to carry "the
  selected local/privacy data boundary" but no deliverable or open issue
  selects it for App conversations reading host content (U-X2).

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| TBD-007 choices OC-1…OC-12 (§9): transport family, realization family, configuration locus, enablement loci, locality, authentication, carriage mechanism, native-surface derivation, encoding, read-back, hold mechanism, tool-permission interplay | App external-host integration owner with external host owner (OC-4 with DEL-04-01; OC-11 with DEL-02-03) | Before the App receiving implementation depends on the interface, and before DEL-09-09 qualification | Nothing selected; carriage assurance and hold feasibility stated per family |
| U-X1 A13 capturing surface; whether App-side access configuration is part of A13, a second A13, or an ordinary configuration change | DEL-04-01 with the owner and host owner | Before enablement implementation and VER-002 | E-3/E-4 PROPOSED; host enablement treated as authoritative |
| U-X2 Data boundary for App conversations reading host content over X | Owner with host owner (XQ-11) | Before enabling a live candidate; before VER-002 destination inspection | §3.4 carries destination display and "no added destination" only; XF-36 HELD |
| U-X3 Checkpoint holds on X: GC-3 (constraint assurance for A5 checkpoints) and GC-5 (kind (a) before dispatch) | DEL-02-03 (W7) with host owner | Before hold-machine fixtures on X; before XF-25/XF-26 execution | Proposed, not imposed; XF-26 HELD |
| U-P10 Host receipt of the governing checkpoint constraint, or host evaluation of its own declaration copy (XQ-3) | Host owner with DEL-03-02, DEL-05-01, DEL-03-03 (DEP-001) | Before V-CP1 / XF-25 execution | XF-25 AWAITING INPUT |
| Capture-evidence reference for host-captured acts (R2-20; XQ-10) | Host owner (DEP-001) | Before XF-18 positive case and any host-content checkpoint *performed* | Faithful records are record shapes only until then |
| Proposal identity minting, pre-submission availability, de-duplication order and durability across restart (XQ-5; P U-P1) | Host owner with DEL-03-02 | Before direct application over X; before XF-21 | PI-4 PROPOSED; XF-21 AWAITING INPUT |
| Caller identity verification (OC-6; XQ-4) | App owner with host owner | Before origin conformance | Author identity *unverified* |
| Enablement read and disable behavior for queued proposals (XQ-2) | Host owner | Before XF-35 execution | E-8 PROPOSED |
| Native-to-catalog mapping and derivation (OC-8; XQ-1) | Host owner with DEL-03-01 | Before AC-001 claim | NM-2: *not established* without a mapping |
| Supplier behaviors `not-observed` at 0.158.0: per-thread MCP configuration; App-added call metadata; MCP-call A14 path; supplier behavior on MCP call failure or retry; sandbox effect on MCP stdio servers and local-socket CLIs | DEL-01-01 with App implementation owner | Before implementation; at pin re-examination (D4) | §3.5 facts are generated-type facts only |
| `UNRESOLVED{OI-003}` extension promise | Owner with host contract owner | Before claiming extension or fixing AC-007's criterion | NM-4: mapping work is evidence, not disposition |
| `UNRESOLVED{OI-021}` first connected operation, its autonomy, operation-specific additions | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and live examination | All cases on invented FX-PIPE-01; OP-C11 cases held |
| `UNRESOLVED{OI-013}` / `UNRESOLVED{OI-014}` placement (including any shared catalog-schema checker, LOOP §10.2 (b)) | Shared contract owner with SWB implementation owner / App-shared contract owners | Before structural/production allocation | No placement implied |
| Host adoption of D2, D3, P-01…P-06 and R2 treatments on X (DEP-001) | Host owner / SWBPIPE | Before any host-enforcement claim (VER-003) | All treatment behavior is receiving meaning |
| Consequence vocabulary (ACT U-02) | DEL-04-01 with host policy owner | Before a consequence scope dimension is used | Fixtures use model/workspace + object set only |
| Register rows (F-11) and SoW OI text (F-10) | Register owner / closeout C1 | C1 | None on content |

---

## Verification cases

Designed, **not run**. Evidence labels per the C-v0.3 mapping. Every executed
result names the App candidate, the realization family, the endpoint
(*simulated* or an identified host candidate), the contract versions
(C-v0.3, P-v0.3, ACT-POLICY-v0.3) and the policy records used.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-X-01 Receiving comparison | For the selected family, run XF-08…13, 37, 39 against the simulated endpoint; compare identity/version (via mapping), availability reasons, standing, basis and subject identities with C-v0.3/P-v0.3 expectations | Every element preserved; mapping named; hints and Codex exposure never used as catalog elements; endpoint labeled simulated | VER-001 (AC-001) |
| VC-X-02 Enablement and locality | Run XF-01…07, 35, 36; inspect App configuration changes and every request destination the App makes | Disabled: no App request; host *channel not enabled* relayed; agent-written config never enables; enablement leaves grant display unchanged; only local destinations; supplier-initiated traffic attributed to the supplier; data boundary item held | VER-002 (AC-002) |
| VC-X-03 Same route and policy | Run XF-22…29, 34 under the identified adopted records (P-01…P-06, ⟨set-1⟩, ⟨set-2⟩); inspect App code/configuration for any path that applies outside the host route | Every outcome per RP-3; no conversion; reserved entries offered; no bypass route found; host-enforcement claims deferred to host evidence | VER-003 (AC-003) |
| VC-X-04 Adverse outcomes | Run XF-14…21, 30 with an injected intervening edit, later selection, duplicate submission, lost acknowledgment and endpoint restart | Stale with both bases; no retarget; retry answered from recorded state; *outcome unknown* observer App; no one-effect claim from transport or session de-duplication; durable conclusions deferred to DEL-09-09 | VER-004 (AC-004) |
| VC-X-05 Acts | Run XF-04, 16, 18, 23, 27, 30…33, 38; inspect the act-mapping code/configuration | No act from success, queued, receipt, A14, A8, elicitation or model text; positive faithful record with actor ≠ recorder, bound content identity and capture-evidence reference (AWAITING INPUT until supplied); independent A4 kept without acceptance | VER-005 (AC-005) |
| VC-X-06 Documentation review | Check §1 one-for-one against SoW REQ-005 exclusions; check §§3–9 and UNRESOLVED against OI-001/002 (as ruled by DECISION-1), OI-003/013/014/021, DEP-001, TBD-007 and CLM-001…004; check D2/D3 attribution (R2-11) and markings | Every excluded act has its owner; every open item has owner, point of need and effect; no wire field, transport, common service or host-delivery claim; PR #885 cited as evidence only | VER-006 (AC-006) |
| VC-X-07 Fixture inventory and handoff | Inspect §10 for coverage of AC-001…AC-005, labels, family, contract/policy identities and evidence limits; inspect the handoff to DEL-09-09 | Full coverage (table in §10.2); every case labeled simulated, AWAITING INPUT or HELD where applicable; generated versus adapter work stated; OI-003 not settled; the joined witness left to DEL-09-09 | VER-007 (AC-007) |
| VC-X-08 Carriage assurance | For each family considered, tabulate §5.2 against an executed dispatch of XF-16, XF-19 and XF-25 | Each element's assurance observed matches §5.2; any model-supplied constraint flagged per GC-3; any omission recorded per GC-4 | VER-003, VER-004 (AC-003, AC-004) |
