---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-01-05
package_id: PKG-01
decomposition_basis: execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z
project_scope_refs: [SOW-009, SOW-010, SOW-011, SOW-012, SOW-132, SOW-133, SOW-149, SOW-150]
package_objective_refs: [OBJ-002, OBJ-004]
---

# DEL-01-05 — Native ChatGPT sign-in and oMLX/local-provider access

## Purpose and Objective Traceability

This deliverable gives the person their model. Through Codex's own account and provider methods the App lets the person sign in with their ChatGPT account, use a local model server, keep both configured together, and choose between them for each conversation, with nothing chosen for them. Credentials stay with Codex. The App also shows and records what its Codex connects to at start-up, and turns off what Codex's settings allow.

It is the BACKEND_FEATURE_SLICE `DEL-01-05` of PKG-01 in the accepted decomposition, serving OBJ-002 (user-selectable Codex access) and OBJ-004 (qualified provider interfaces and the local-server requirements a host receives).

| Accepted scope | Contribution | Source |
|---|---|---|
| SOW-009 | ChatGPT account sign-in through Codex, with Codex holding the credential | PRD V4-APP-02; ARCHITECTURE V4-ARC-04 |
| SOW-010 | Standalone OpenAI API-key access is omitted from this increment | PRD V4-APP-02 |
| SOW-011 | Local model servers offered as Codex providers | PRD V4-APP-02 |
| SOW-012 | Both kinds of access configured together and chosen per conversation, without a default | PRD V4-APP-02 |
| SOW-132 | The App-owned Codex homes and what each shares | ARCHITECTURE §3 |
| SOW-133 | Applies only if the owner brings API-key access back into scope | PRD V4-APP-02 |
| SOW-149 | Account, provider and local-server interfaces qualified against the pin; the embedding protocol is `DEL-01-01`'s share | ARCHITECTURE §6 |
| SOW-150 | A compliant local server can be substituted | ARCHITECTURE §6 |

Its examination scenario is EXAMINATION V4-EXM-12. The access modes are two, as PRD V4-APP-02 has them: ChatGPT account and local provider. The decomposition row and OI-010 record three as accepted history.

## Deliverable Definition — Ontology

- **OUT-001** — Receiving of Codex's native ChatGPT sign-in, the account status shown, and the Codex account reported for the person-identity element of captured acts. Supports SOW-009, SOW-010; OBJ-002.
- **OUT-002** — Local-provider access, the per-conversation choice of model and provider, the start-up traffic settings, and the network view and its record. Supports SOW-011, SOW-012; OBJ-002.
- **OUT-003** — The App-owned Codex homes: the account home, the dedicated local home and the probe home, with what each shares with the person's own Codex and what each keeps to itself. Supports SOW-132, SOW-133; OBJ-002.
- **OUT-004** — Qualification of the account, provider and local-server interfaces on an identified candidate, the substitution of a compliant local server, and the local-server capability requirements handed to the host loop contract. Supports SOW-149, SOW-150; OBJ-002, OBJ-004.

Terms:

- **App-owned Codex home.** A Codex home directory the App creates for its own Codex, with a stable identity that is neither a credential nor a path. Every conversation belongs to exactly one home.
- **Account home.** The home for ChatGPT account conversations. It shares the person's Codex settings, providers and MCP servers through links to the person's own files and keeps its own sign-in, held by Codex. A development build can also be held to a same-machine model address by a startup input the released App does not read. If a pinned Codex cannot share settings this way, the App keeps its own settings and says so.
- **Dedicated local home.** The home for the keyed oMLX route. It has its own fixed, nonsecret configuration — provider `chirality-omlx` at `http://127.0.0.1:8000/v1` over the Responses interface, with one fixed model for the route — shares nothing with the account home, and holds the local server's key in Codex custody.
- **Probe home.** A home used only when the supplier binary is asked for its version label. It is never an account home and hosts no conversation.
- **Access entry.** One way a conversation can reach a model: the ChatGPT account, a provider from the person's shared Codex settings, or the keyed oMLX route.
- **Selection state.** For a conversation: no model selected, a model and provider selected, and the person's last explicit choice for the project.
- **Start-up traffic.** Connections the App's Codex makes when it starts or starts a thread, before any turn the person sends.

Boundary:

- **CLM-001** — Codex owns its account methods and every credential. The App owns the receiving integration. The App holds no token; a key the person enters passes once through a native secure field to Codex and is never stored, logged, written to configuration, a command line or the child's environment, or shown to the web view. External-token login is not offered.
- **CLM-002** — Standalone OpenAI API-key access is omitted from this increment. Native plumbing and a key home saved by an earlier build are kept, neither offered nor deleted. Bringing it back is an owner scope decision.
- **CLM-003** — `DEL-01-01` hosts the Codex child for each home, carries the account methods and the provider selection, qualifies the embedding protocol and states what Codex requires of a provider. `DEL-01-04` presents the conversation start, where the selection state appears, and captures acts. `DEL-01-02` lists live work before an operation that would end it.
- **CLM-004** — `DEL-05-01` owns the host loop and its model contract; the external host owner builds the host's loop and enforces its endpoint and key boundary. A host's model interface is Chat Completions with tool calls; the App's provider interface is whatever Codex requires at the pin. Qualifying one says nothing about the other.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The App offers ChatGPT account sign-in through the selected Codex-native flow and starts the intended account-backed conversation with the credential held by Codex. The account is shown as Codex reports it, with pending, failed, absent and not-yet-read kept distinct, and no part of a key, token, sign-in address or code is shown outside a pending sign-in. The Codex account of the home that runs a conversation is reported as the reported email or "ChatGPT account (no email reported)"; the plan type is shown and not recorded.
- **REQ-002** — The App presents no standalone OpenAI API-key entry and makes no qualification claim for one. A key home saved earlier is left in place.
- **REQ-003** — Local servers are offered as Codex providers through the supplier's provider interface. The keyed oMLX route uses the dedicated local home, and its key is entered in a native secure field and held by Codex. A configured key is shown as configured, not verified, until an actual conversation uses it.
- **REQ-004** — The person can keep ChatGPT account and local access configured together and choose the access entry for each conversation. Choosing one leaves the other configured. No access entry or model is applied to a new conversation until the person chooses; the last explicit choice for the project may be offered, shown as such, and is never applied silently. A conversation's selection state is reported to the views and controls that depend on it. A conversation that cannot start for want of a model reads "not started — no model selected", and a workflow run "run not started — no model selected".
- **REQ-005** — Each home exists before a Codex child is started for it, and its identity survives a relaunch. The homes behave as their terms state: the account home's sign-in is separate from the person's own Codex sign-in while the person's settings, providers and MCP servers apply in it; the dedicated local home shares nothing with the account home; the probe home holds no account.
- **REQ-007** — The account, provider and local-server interfaces are qualified against the pin on an identified candidate, naming the server, the interface and the observed result, with failures and unverified capabilities stated. A compliant local server can be substituted through supported provider settings and starts the intended conversation.
- **REQ-008** — The local-server capability requirements and the limits of what was qualified are handed to the host loop contract, keeping the App's provider interface distinct from a host's model interface.
- **REQ-009** — This deliverable performs no act that CLM-003 and CLM-004 give elsewhere: no hosting, pin definition, type generation or embedding qualification, no host loop and no host key enforcement.
- **REQ-010** — The App turns off the start-up traffic of its Codex that Codex's settings allow: analytics is off, and plugin traffic follows the person's own plugin setting. A connection that no setting stops is left on and shown. The remaining start-up connections are shown in a network view and recorded, naming for the supplier version which connections an App setting stops and which remain.

- **AC-001** — On the candidate the person completes the ChatGPT sign-in, the account status then shows the account Codex reports, an account-backed conversation runs, and no credential is found in any file, log, record or message the App wrote. The account view keeps pending, failed, absent and not-yet-read distinct and shows no part of a key, token, sign-in address or code outside a pending sign-in. For a conversation, the Codex account reported for act capture is the email Codex reports for the home that runs it, or "ChatGPT account (no email reported)" when Codex reports none, and no plan type is recorded. Verify by VER-001. [REQ-001]
- **AC-002** — The candidate offers no standalone OpenAI API-key entry, and a key home present from an earlier build is unchanged after the App has run. Verify by VER-002. [REQ-002]
- **AC-003** — With a local server running, a conversation started on the keyed oMLX route reaches that server through the dedicated local home; the key appears in no App-written file and never reaches the web view; and before first use the route is shown as configured, not verified. Verify by VER-003. [REQ-003]
- **AC-004** — With both kinds of access configured, the person runs one conversation with each and switches between them with the other still configured; a new conversation has no model until the person chooses; an offered last choice is not applied without the person's act; both not-started wordings appear where they apply; and for each conversation the reported selection state names no model, or the selected model and provider, and the last explicit choice for the project, and agrees with the provider Codex reports. Verify by VER-004. [REQ-004]
- **AC-005** — In the account home the person's Codex settings, providers and MCP servers are in effect and its sign-in is its own: signing in or out there leaves the person's own Codex sign-in unchanged, and the reverse. The dedicated local home shows none of the account home's settings or sign-in. Each home exists before a Codex child is started for it and keeps the same identity, which is neither a credential nor a path, across a relaunch; every conversation belongs to exactly one home; and the probe home holds no account after a version probe. Verify by VER-005. [REQ-005]
- **AC-007** — The qualification names the candidate, the pin, each interface exercised and each observed result, and marks what was not observed; nothing the supplier only publishes is reported as observed. Verify by VER-007. [REQ-007]
- **AC-008** — A different compliant local server, selected through supported provider settings, starts the intended conversation, and the evidence names the substitute and its observed interface behaviour. Verify by VER-008. [REQ-007]
- **AC-009** — The handoff states the local-server capabilities Codex required at the pin, what was and was not observed, and that it is the App's provider interface and not a host's model interface. Verify by VER-009. [REQ-008]
- **AC-010** — None of the acts in REQ-009 is produced by this deliverable's code. Verify by VER-010. [REQ-009]
- **AC-011** — For the pin, the network view and its record list each start-up connection of the App's Codex and whether an App setting stops it; every connection the record names as stoppable by an App setting is absent, including analytics; plugin traffic is present with the person's plugin setting on and absent with it off. Verify by VER-011. [REQ-010]

## Production and Verification Method — Praxeology

Account and provider methods are used as the pin publishes them, and what the App reads from Codex is read at run time, not assumed from the version. Recorded exchanges show the seams; sign-in, a local conversation and substitution each need the actual candidate, an actual account or server, and the person's own act. No credential is reproduced in any evidence.

- **VER-001** — Comparison with Codex's own account report and an examiner's observation: the person signs in on the candidate, with a pending, a failed and an absent sign-in and an account not yet read each shown; the account status and the account reported for a conversation are compared with what Codex reports, with and without an email; a conversation is run; and the App's files, logs and records are searched for the credential and for a plan type.
- **VER-002** — Executable check (observes the offered entries and the bytes of an earlier key home before and after a run).
- **VER-003** — Comparison with the local server's own request log: prepare the keyed route, enter the key natively, start a conversation, and search App-written files and the web view's messages for the key.
- **VER-004** — Comparison with the provider Codex reports for each conversation, witnessed by an examiner: run the scenario of EXAMINATION V4-EXM-12, start a new conversation with and without a last choice, attempt to start with no model, and read the reported selection state of each conversation.
- **VER-005** — Comparison with Codex's own configuration and account reads in each home: change a setting in the person's Codex and read it in the account home; sign in and out on each side; read the dedicated local home; start the App, relaunch it and read each home's identity and each conversation's home before and after; read the probe home after a version probe.
- **VER-007** — Comparison with the supplier's published protocol at the pin: replay recorded account and provider exchanges and read the qualification against the exchanges and the candidate's observed results.
- **VER-008** — Comparison with the substitute server's own request log: configure a second compliant server through provider settings and start a conversation.
- **VER-009** — Judgment by an independent reviewer: read the handoff against the qualification evidence and the interface split of ARCHITECTURE §6.
- **VER-010** — Judgment by an independent reviewer: trace each act of REQ-009 to its owner's code.
- **VER-011** — Comparison with connections observed outside the App: start the App's Codex with the person's plugin setting on and off and compare an operating-system level observation of its connections with the network view and the record.

## Governing Values and Decisions — Axiology

- **AX-001** — The person chooses the model and Codex holds the credentials. Better means fewer steps between the person's choice and a running conversation, and never by applying a default, choosing for the person, or bringing a credential into the App's hands.
- **AX-002** — The App's Codex contacts only what the person can see. Better means fewer start-up connections left on and more of them named in the network view, and never by using an unpublished supplier switch, overriding the person's own Codex settings, or describing operation as local-only when a connection remains.
- **AX-003** — A local server counts only when it was seen to work. Better means more of the provider interface observed on a named server, and never by reporting a published capability, a configured key or another server's result as this server's.
- **TBD-004** — Whether plugin traffic in the dedicated local home follows the person's plugin setting or is always off is undecided (owner). The person's setting applies in the account home, and the plugin clause of AC-011 is examined there.

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-002 | REQ-001, CLM-001 | AC-001 | VER-001 | Outside source: Codex's own account report and the sign-in the examiner watched. The credential search is over files the App wrote, compared with a value only the person holds. |
| OUT-001 | OBJ-002 | REQ-002, CLM-002 | AC-002 | VER-002 | The candidate's offered access entries read against PRD V4-APP-02, and the bytes of an earlier key home compared before and after the App has run. |
| OUT-002 | OBJ-002 | REQ-003, CLM-001 | AC-003 | VER-003 | Outside source: the local server's own request log; the server imports no App code. |
| OUT-002 | OBJ-002 | REQ-004 | AC-004 | VER-004 | Outside source: the provider Codex reports for each conversation, compared with the selection state the App reports, in the EXAMINATION V4-EXM-12 scenario witnessed by an examiner on the candidate. |
| OUT-003 | OBJ-002 | REQ-005 | AC-005 | VER-005 | Outside source: Codex's own configuration and account reads in each home, compared with what each home's term says it shares and keeps to itself. |
| OUT-004 | OBJ-002, OBJ-004 | REQ-007, CLM-003 | AC-007 | VER-007 | Outside source: the supplier's published protocol at the pin and exchanges recorded from the stock supplier. |
| OUT-004 | OBJ-002, OBJ-004 | REQ-007 | AC-008 | VER-008 | Outside source: the substitute server's own request log. |
| OUT-004 | OBJ-002, OBJ-004 | REQ-008, CLM-004 | AC-009 | VER-009 | An independent reviewer's reading of the handoff against the qualification evidence and the interface split of ARCHITECTURE §6. It establishes that the handoff states what was observed; it does not establish that a host's loop conforms. |
| OUT-004 | OBJ-002, OBJ-004 | REQ-009, CLM-003, CLM-004 | AC-010 | VER-010 | An independent reviewer's trace of each act of REQ-009 to its owner's code under CLM-003 and CLM-004. |
| OUT-002 | OBJ-002 | REQ-010 | AC-011 | VER-011 | Outside source: connections observed at operating-system level, independent of the App's own view, compared with the network view, the record and the traffic REQ-010 turns off or leaves to the person's plugin setting. The observation holds for the supplier version observed. |
