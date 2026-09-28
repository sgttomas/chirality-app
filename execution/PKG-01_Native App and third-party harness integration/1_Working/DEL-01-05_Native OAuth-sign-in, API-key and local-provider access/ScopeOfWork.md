---
schema: chirality-deliverable-sow/v1
deliverable_id: DEL-01-05
package_id: PKG-01
decomposition_basis: projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z@941c4d35f994594ce8aacd81758ab39079bddad6
project_scope_refs: [SOW-009, SOW-010, SOW-011, SOW-012, SOW-132, SOW-133, SOW-149, SOW-150]
package_objective_refs: [OBJ-002, OBJ-004]
---

# Native OAuth/sign-in, API-key and local-provider access

## Purpose and Objective Traceability

DEL-01-05 supplies the App account/provider integration owner's bounded contribution to PKG-01: connect stock Codex-native ChatGPT sign-in/OAuth, API-key access and local model providers to the App, retain their configuration together, and expose the choice for each conversation. OBJ-002 is served by those three access modes; OBJ-004 is served by qualified provider interfaces and applicable local-server capability requirements received by PKG-05. This contract defines required future production and evidence; its existence establishes neither implementation nor supplier qualification. [S1, S2, S3]

| Project scope | Local contribution | Objective | Production definition |
|---|---|---|---|
| SOW-009 | Codex-native ChatGPT account sign-in/OAuth with Codex credential custody | OBJ-002 | OUT-001; REQ-001 |
| SOW-010 | API-key access through Codex account methods with Codex credential custody | OBJ-002 | OUT-001; REQ-002 |
| SOW-011 | Local model servers offered as Codex providers | OBJ-002 | OUT-002; REQ-003 |
| SOW-012 | All modes configured together and selected per conversation | OBJ-002 | OUT-002; REQ-004 |
| SOW-132 | Account-home decision preparation and recorded choice before account integration | OBJ-002 | OUT-003; REQ-005; TBD-001 |
| SOW-133 | Supported API-key account behavior defined for the selected protocol | OBJ-002 | OUT-003; REQ-006; TBD-002 |
| SOW-149 | Account/provider receiving and local-server qualification against the selected pin; embedding qualification remains with DEL-01-01 | OBJ-002, OBJ-004 | OUT-004; REQ-007; REQ-008 |
| SOW-150 | Substitution of compliant local servers with candidate-specific evidence | OBJ-002, OBJ-004 | OUT-004; REQ-007 |

Source locators are repository-relative. S1 is the accepted decomposition authority; S2–S5 identify the specific source records used below. Historical draft labels in frozen source bytes do not supersede the acceptance recorded by S1 and S4.

- S1: `projects/chirality-app-v4/execution/_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/DECISION.md` and `ACCEPTED_MANIFEST.csv`; accepted snapshot first recorded at the commit in frontmatter.
- S2: the same snapshot's `canonical/Deliverables.csv` rows DEL-01-01, DEL-01-05 and DEL-05-01; `Packages.csv` row PKG-01; `Objectives.csv` rows OBJ-002 and OBJ-004; `ScopeLedger.csv` rows listed in frontmatter.
- S3: `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/PRD.md`, V4-APP-02; adjacent `ARCHITECTURE.md`, V4-ARC-04 and §§3, 4, 6. The source's protocol examples and supplier assumptions are subject to the selected pin, not a certification of current supplier behavior.
- S4: `projects/chirality-app-v4/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md`; `projects/chirality-app-v4/execution/_Coordination/Changes/APP-V4-CLARIFICATION-20260927/DIRECTION.md`; accepted snapshot `canonical/Open_Issues.csv`, OI-009, OI-010 and OI-012; `canonical/External_Dependencies.csv`, DEP-001 and DEP-005. Current equivalents under `_Decomposition/` preserve these relevant open matters.
- S5: `projects/chirality-app-v4/docs/PRD.md`, §§0, 2.1; `projects/chirality-app-v4/docs/ARCHITECTURE.md`, §§3, 6: consolidated expression and qualification of the accepted sources; `projects/chirality-app-v4/execution/_Coordination/_COORDINATION.md`, approved initial setup and lifecycle limits.

## Deliverable Definition — Ontology

- **CLM-001** — Accepted product behavior comprises ChatGPT account access, API-key access and local-server access, configurable together and chosen per conversation. Codex owns its account methods and credentials; Chirality owns the App receiving integration and maintenance. This does not choose a v4 account home. [S2: PKG-01 and DEL-01-05; S3: V4-APP-02, V4-ARC-04]
- **CLM-002** — The local-server contribution uses stock Codex provider methods in the App. The architecture separately describes host loops using Chat Completions with tool calls, and an App-provider Responses interface assumption; these are distinct supplier assumptions to qualify for their selected use. A named server example does not establish present compliance. [S3: §§4, 6; S5: architecture §6]
- **CLM-003** — `DEL-01-01`, the App supplier-integration owner's contribution, owns stock App Server hosting, process/protocol ownership, supplier-pin definition, generated protocol types and selected embedding qualification. DEL-01-05 consumes that identified protocol/pin and contributes the account/provider and local-server portion of joint SOW-149 qualification. [S2: DEL-01-01 and DEL-01-05; S4: OI-012, DEP-005]
- **CLM-004** — `DEL-05-01`, the App/shared embedded-integration owner's contribution, owns the minimal-loop/model receiving and conformance contract. The external host owner implements the host-specific loop/native layer and enforces the host endpoint/key boundary. DEL-01-05 supplies applicable local-server capability requirements to that receiving contribution; shared construction requires separately agreed repeated responsibility and is not assigned by this interface. [S2: DEL-01-05 and DEL-05-01; S4: DEP-001 and clarification]
- **OUT-001** — App receiving code for native ChatGPT sign-in/OAuth and API-key access through supported Codex account methods, preserving Codex credential custody. Scope: SOW-009, SOW-010. Objective: OBJ-002. Basis: CLM-001.
- **OUT-002** — Supported Codex local-provider settings and App account/provider selection, keeping account, API-key and local-server configuration together and exposing per-conversation choice. Scope: SOW-011, SOW-012. Objective: OBJ-002. Basis: CLM-001, CLM-002.
- **OUT-003** — Account-home and API-key protocol definition records, retaining open decisions until their responsible participants resolve them and identifying the supported account behavior used by dependent integration. Scope: SOW-132, SOW-133. Objective: OBJ-002. Basis: S3 §3 and S4 OI-009/OI-010.
- **OUT-004** — Candidate-bound account/provider and local-server qualification evidence, supported substitution configuration and checks, and applicable local-server capability requirements for DEL-05-01 receiving. Scope: SOW-149, SOW-150. Objectives: OBJ-002, OBJ-004. Basis: CLM-002, CLM-003, CLM-004.

## Completion and Reliance Basis — Epistemology

- **REQ-001** — The App shall offer ChatGPT account sign-in/OAuth through the selected Codex-native account flow and start the intended account-backed conversation with credentials held by Codex. Basis: CLM-001, SOW-009.
- **REQ-002** — The App shall offer API-key access through the selected Codex account methods and start the intended API-key-backed conversation with credentials held by Codex, using the supported behavior defined under REQ-006. Basis: CLM-001, SOW-010.
- **REQ-003** — The App shall offer supported local model servers as Codex model providers using the supplier interfaces established for the chosen App pin. Basis: CLM-002, CLM-003, SOW-011.
- **REQ-004** — A user shall be able to keep account, API-key and local-server access configured together and select the intended access mode for each conversation through the App. Selecting one mode shall preserve the configuration needed to choose the other modes for subsequent conversations. Basis: CLM-001, SOW-012.
- **REQ-005** — The account-home definition record shall present separated and shared Codex account state and record the choice made by the Owner with the App implementation owner before account integration depends on it. Until that choice exists, the record shall explicitly retain OI-009 as open. Basis: SOW-132, S4; TBD-001.
- **REQ-006** — The App implementation owner shall define supported API-key sign-in/account behavior against the identified pinned Codex protocol before API-key implementation or qualification depends on it, with a traceable protocol basis and implications for the three required access modes. Until supported behavior is established, OI-010 shall remain explicit. Basis: SOW-133, S4; TBD-002.
- **REQ-007** — Account/provider receiving and local-server interfaces shall be qualified against the selected supplier pin and required protocols; a compliant local server shall be substitutable through supported provider settings and shall start the intended local-provider conversation. Qualification shall identify the actual candidate, configured server, interface and observed result, with failures and unverified capabilities explicit. The required embedding-qualification input is the contribution named by CLM-003. Basis: SOW-149, SOW-150; TBD-003.
- **REQ-008** — Applicable local-server capability requirements and qualification limits shall be provided to the PKG-05 receiving contribution named by CLM-004, distinguishing the App's Codex-provider interface from the host's model/loop interface. The App contribution shall continue through stock Codex provider methods. Basis: SOW-149; CLM-002, CLM-004.
- **REQ-009** — DEL-01-05 shall perform no act owned by another deliverable: stock App Server hosting, supplier-pin definition, generated protocol-type production and embedding-protocol qualification belong to `DEL-01-01` under CLM-003; minimal-loop/model receiving-contract production belongs to `DEL-05-01` under CLM-004. Host-specific loop/native-layer construction and host endpoint/key enforcement belong to the external host owner under CLM-004. These exclusions preserve DEL-01-05's account/provider integration, local-server qualification and capability-requirement handoff. [S2, S4]

- **TBD-001** — OI-009 remains OPEN: separated or shared account home. Responsible participants: Owner with App implementation owner. Point of need: before account integration. Historical v3 overlay or Root authentication separation does not decide this v4 product choice. [S4]
- **TBD-002** — OI-010 remains OPEN: API-key sign-in details and supported account behavior of the chosen pin. Responsible participant: App implementation owner. Point of need: before API-key implementation/qualification. Required access modes remain IN. [S4]
- **TBD-003** — OI-012 and DEP-005 retain the unidentified supplier pin, published protocol and configured model-endpoint capability evidence. The App implementation owner selects the pin through the DEL-01-01 contribution before protocol generation/qualification. DEL-01-05 then establishes its mode/provider behavior against that input. No historical version, field example or named server is adopted or certified here. [S3 §3/§6; S4; S5]

- **AC-001** — Candidate-bound evidence shows the App completing the selected native Codex ChatGPT sign-in/OAuth flow and starting the intended account-backed conversation, with Codex retaining credential custody. Verifies REQ-001 by VER-001.
- **AC-002** — Candidate-bound evidence shows the App using the defined pinned-protocol API-key account flow and starting the intended API-key-backed conversation, with Codex retaining credential custody. Verifies REQ-002 and REQ-006 by VER-002.
- **AC-003** — A configured supported local server starts the intended App conversation as a Codex provider, with the selected pin and required interface identified in the evidence. Verifies REQ-003 by VER-003.
- **AC-004** — With all three modes configured, the App permits selecting each for a conversation, starts each intended conversation, and preserves the other modes' configuration for subsequent selection. Verifies REQ-004 by VER-004.
- **AC-005** — The account-home decision record identifies the separated/shared alternatives, the actual choice and its responsible participants, and shows it was available before dependent account integration; absent a choice, the obligation remains unresolved rather than passed. Verifies REQ-005 by VER-005.
- **AC-006** — The API-key definition identifies supported account behavior and its pinned-protocol evidence before dependent API-key implementation/qualification; unsupported or unverified details remain explicit and the three access-mode commitment is preserved. Verifies REQ-006 by VER-006.
- **AC-007** — Qualification identifies the account/provider and local-server interfaces exercised against the selected pin, links the DEL-01-01 embedding-qualification input, and records observed outcomes and limits without treating supplier assumptions as candidate evidence. Verifies REQ-007 by VER-007.
- **AC-008** — A compliant replacement local server is selected through supported provider settings and starts the intended local-provider conversation; evidence identifies both the substitute's required interface compliance and the observed substitution result. Verifies REQ-007 by VER-008.
- **AC-009** — The capability-requirement handoff identifies the App-provider and host-model interface distinctions, required local-server capabilities, qualification limits and DEL-05-01 receiving responsibility, without claiming host conformance from App qualification alone. Verifies REQ-008 by VER-009.
- **AC-010** — The delivery boundary assigns every act enumerated by REQ-009 to its cited contribution and retains this deliverable's own integration, qualification and handoff work. Verifies REQ-009 by VER-010.

## Production and Verification Method — Praxeology

Production begins from the accepted source commitments and keeps TBD-001 through TBD-003 visible until their stated inputs exist. Define the account-home and API-key behavior at their points of need, receive the selected supplier contract from DEL-01-01, implement the bounded App receiving paths and configuration/selection, then collect candidate-bound mode, coexistence, protocol and substitution evidence. Supply applicable requirements and limits to DEL-05-01. This ordering describes input needs, not an accepted project DAG or a scheduling commitment. Independent definition can proceed before external host/provider completion. [S2, S4, S5]

- **VER-001** — Exercise the actual selected Codex-native account sign-in/OAuth receiving flow on the candidate and observe the resulting account-backed conversation; inspect the receiving/account configuration and credential handoff for Codex custody. Retain a result record without reproducing credentials.
- **VER-002** — Exercise the defined API-key account flow on the candidate using the selected Codex protocol, observe the resulting API-key-backed conversation and inspect the credential handoff/custody against the definition record. Retain outcome evidence without reproducing the key.
- **VER-003** — Configure an identified supported local server as a Codex provider through the candidate and start a conversation; compare the actual supplier/provider exchange with the selected interface requirements and record the endpoint/model identity and result.
- **VER-004** — Run the per-conversation selection scenario with account, API-key and local-server access configured together; select and start each mode and inspect retained configuration and subsequent availability of the other modes.
- **VER-005** — Review the account-home decision record against SOW-132 and OI-009, including its actual decision custody, alternatives and timing relative to dependent account integration. Mark missing choice evidence unresolved.
- **VER-006** — Review the API-key definition against the identified protocol/pin and OI-010; trace stated behavior to supplier evidence and compare the record's availability with dependent implementation/qualification. Mark unsupported details unresolved.
- **VER-007** — Compare the qualification record, selected supplier identity, account/provider and local-server exchange evidence, and the DEL-01-01 embedding-qualification input; distinguish observed passes, failures and unverified claims for the actual candidate.
- **VER-008** — Check the replacement local server against the required App-provider interface, substitute it using supported configuration and exercise conversation start; retain the compliance and substitution observations for that identified server/candidate.
- **VER-009** — Review the requirements handed to DEL-05-01 against the accepted interface split and this deliverable's qualification evidence, checking explicit capabilities, limits and receiving responsibility.
- **VER-010** — Compare the enumerated acts in REQ-009 with CLM-003, CLM-004 and the accepted deliverable/external-owner rows, checking each act's owner and the retained DEL-01-05 contribution one for one.

Recorded exchanges and focused checks may implement these verification methods in keeping with architecture principle M-7; native sign-in and substitution criteria still require the actual candidate observations named above. Tests implement this contract and do not create new scope or decide the open technical matters. [S3 §1; S2 DEL-01-05]

## Governing Values and Decisions — Axiology

- **AX-001** — Preserve the accepted stock Codex direction and its native account/provider methods. The App owns receiving integration; Codex retains engine and credential ownership. An additional App harness is not part of these outputs. [S2 PKG-01; S3 V4-ARC-04; CLM-001]
- **AX-002** — Required account-home and API-key definition work is IN while the values remain open at their stated points of need. This initialized definition neither makes those choices nor requires their resolution merely to write an honest contract. [S4 clarification; TBD-001, TBD-002]
- **AX-003** — Local servers are substitutable only with the required selected-interface evidence. Historical examples, App qualification and host qualification are separate facts; none proves another by naming the same supplier. [S3 §6; S5 architecture §6; CLM-002]
- **AX-004** — SOW-149 is joint scope: DEL-01-05 supplies its account/provider and local-server contribution while DEL-01-01 supplies embedding/protocol qualification. Applicable PKG-05 capability receiving does not transfer host implementation here. [S2; CLM-003, CLM-004]
- **AX-005** — Accepted Group3 and initial setup authorize this source-grounded contract and checking. Production completion, lifecycle advancement, supplier-term conclusions, release and downstream adoption require their own evidence or acts. The open distribution-terms question remains at its separately recorded public-release point of need; this contract makes no legal conclusion. [S1; S5; S3 §6]

## Output and Evaluation Matrix

| Output | Objective refs | Requirement/claim refs | Acceptance refs | Verification refs | Evidence expectation |
|---|---|---|---|---|---|
| OUT-001 | OBJ-002 | REQ-001, CLM-001 | AC-001 | VER-001 | Candidate-native ChatGPT sign-in/OAuth result, intended account-backed conversation and Codex custody check |
| OUT-001 | OBJ-002 | REQ-002, REQ-006, CLM-001 | AC-002 | VER-002 | Candidate API-key account flow and conversation result tied to the protocol definition and Codex custody |
| OUT-002 | OBJ-002 | REQ-003, CLM-002, CLM-003 | AC-003 | VER-003 | Selected-pin and server identity, required interface and local-provider conversation observation |
| OUT-002 | OBJ-002 | REQ-004, CLM-001 | AC-004 | VER-004 | All-mode configuration, each per-conversation selection/start and retained configuration observations |
| OUT-003 | OBJ-002 | REQ-005 | AC-005 | VER-005 | Actual account-home choice custody and evidence of availability before dependent integration |
| OUT-003 | OBJ-002 | REQ-006 | AC-006 | VER-006 | Pinned-protocol API-key behavior definition, source support, timing and explicit limits |
| OUT-004 | OBJ-002, OBJ-004 | REQ-007, CLM-002, CLM-003 | AC-007 | VER-007 | Candidate-bound interface qualification record and identified embedding input with limits |
| OUT-004 | OBJ-002, OBJ-004 | REQ-007, CLM-002 | AC-008 | VER-008 | Identified compliant substitute, supported provider configuration and observed conversation start |
| OUT-004 | OBJ-002, OBJ-004 | REQ-008, CLM-004 | AC-009 | VER-009 | Applicable local-server requirements and limits handed to the named PKG-05 receiver |
| OUT-004 | OBJ-002, OBJ-004 | REQ-009, CLM-003, CLM-004 | AC-010 | VER-010 | One-for-one boundary/owner comparison against accepted contributions |
