# Account and provider access

- Contribution: DEL-01-05/ACCESS-v0.1 (first version; no predecessor)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. Nothing here is qualified; no App candidate exists.
- Produced by: node D4 of run `APP-V4-DESIGN-PASS-3-20261001` (Type 2 TASK,
  Claude Opus 5.5, high effort; does not delegate), 2026-10-01, at
  repository HEAD `dc031b5bec`.
- Companion record: [ACCOUNT_HOME_DECISION_RECORD.md](ACCOUNT_HOME_DECISION_RECORD.md)
  (OUT-003, REQ-005; the K-1 decision and its mechanism). Schemas beside this
  file (§15); prototype under [`prototype/`](prototype/) (§16).
- **Hard limit observed in producing this file:** no sign-in, no API key and
  no token was entered, created or read by anyone; no Codex process and no
  model was run; no network was used. The 0.158.0 vendor binary was read as
  bytes with `strings` (as HOSTING F-28 did), never executed.
- Serves: OUT-001, OUT-002, OUT-003 (API-key definition record, §10),
  OUT-004 (designed method and the DEL-05-01 handoff, §11–§12); REQ-001…REQ-009
  as designs; designed cases for VER-001…VER-010.

**Basis (binding, by bytes read with `shasum -a 256`).** Accepted basis as
amended by SCA-V4-001 and SCA-V4-002: `docs/PRD.md` bb6e786f…49bd
(V4-APP-02), `docs/ARCHITECTURE.md` 317d5789…828c (V4-ARC-04, §3 "Left to
the implementation session", §6), `docs/EXAMINATION.md` 471798bc…d0
(V4-EXM-12). ScopeOfWork.md baf68c79b5b8fdf0…a6 (unchanged since
initialization). Run records under
`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/`: `BRIEFS.md`
b2613941…05c1 (row D4), `OWNER_DECISIONS.md` 9d18c40d…1b1b (DECISION-K3 as
revised: K-1, K-2, K-3, K-11, K-12 bind this file), `R17_RESOLUTIONS.md`
b0af81bc…e198 (R17-1, R17-2, R17-5, R17-10, R17-13…R17-16),
`DECISIONS_PENDING.md` 431ec4eb…dd86 (the K-n option texts the owner
accepted), `SURVEY/S1-B.md` c947d4d4…2159 (Part B; its B.6 is the starting
list). Earlier owner records: DECISION-K1 K1-4 (person identity) of
`APP-V4-DESIGN-PASS-2-20260930`; DECISION-4 D4-3 (no default; cloud by
OAuth sign-in or API key) of `APP-V4-SWBPIPE-INTAKE-20260928`; DECISION-1 D4
(0.158.0 is the definition/generation pin).

**Joined first-increment files (read, not edited; R17-14).**
DEL-01-01/HOSTING-BOUNDARY-v0.8 (`HOSTING_BOUNDARY.md` 3cf0381c…78b1; §1,
§2, §3 H1/H9/H11, §4.1–§4.2, §6.1, §6.8, §7, §8 S-4, §8.1 L-1…L-6, §8.3,
§10.1 OB-1…OB-12, §11, §12, §13 F-14/F-18/F-21/F-24/F-28/F-31/F-32,
UNRESOLVED U-03/U-12/U-18/U-20/U-22); `OBS_1_0.158.0.md` 7b984b54…cc43 (§2,
§8, §9 HOSTING rows, B.1, B.2, B.5); `PIN_SPIKE_0.158.0.md` 0e090a4c…b115
(P-11, P-12, S-F-10, S-F-17, by HOSTING's citation); DEL-05-01/LOOP-v0.8
(`LOOP_RECEIVING_CONTRACT.md` f8b7776c…0e61; §1, §5.1, §10.3, §10.4).
DEL-04-03/RS-v0.8 R5 and its schema enum `destinationClass` were read for
the class values (§3). EXEC CAP-8 and RS §6.1 were read for K1-4.

**Supplier evidence.** Generated types at 0.158.0, read only from
`…/scratchpad/codex-0.158.0/gen/ts-experimental/run1`; 22 files this file
relies on were checked against the committed
`DEL-01-01/Design/generated/0.158.0/MANIFEST.sha256` (prefix
`ts/experimental/`): **22/22 equal**. Strings of the vendor binary (sha256
788a818f…35c8, the same as SPIKE §3) were extracted with `strings -n 6` into
the session scratch folder and searched.

**Standing labels.** Design labels as R9/R17: SETTLED, DERIVED, INTEGRATION,
PROPOSED. Supplier-fact labels as R17-13: `observed` (OBS-1/1b or the
spike), `observed-in-generated-types`, and two more used here:
`strings-in-binary` (present as text in the binary; **not behaviour**, F-28's
standing) and `inference`. Cells that OBS-2 will settle are marked **OBS-2
pending** with the item (O-5…O-7).

**How this file reads the ScopeOfWork (R17-15).** The SoW lags the owner's
answers in five places; the design follows the answers and the return file
lists the proposals for SCA-V4-003:

1. TBD-001/REQ-005: OI-009 is decided at choice level by DECISION-K3 K-1
   (shared settings, separate sign-in custodied by Codex); the mechanism is
   PROPOSED (decision record).
2. TBD-003: "the unidentified supplier pin" — 0.158.0 is the
   definition/generation pin (DECISION-1 D4); qualification stays under
   OI-012.
3. REQ-004 states no default rule; K-3 adds "no model chosen until the person
   chooses" for the App (§5.4).
4. Start-up traffic (K-12) has no SoW item; HOSTING U-18 names "Owner with
   DEL-01-05" (§9).
5. K1-4's "Codex account when Codex reports one" is a supply this file makes
   to the act record (§8); no SoW line names it.

---

## 0. What this file is, and what it is not

It is the App's design for **receiving** Codex's own account and provider
methods: the access entries the person keeps configured, the per-conversation
choice, the sign-in, key and local-provider sequences, the custody rules, the
start-up network view, the API-key definition record and the handoff to
DEL-05-01.

It is not: the supplier boundary (DEL-01-01 carries every frame; this file
never writes to the Codex pipe except through HOSTING's generic request path,
§12 O-1 PROPOSED); request cards or the act control (DEL-01-04); durable
recovery (DEL-01-02); the host loop's credentials and endpoints (the host
native layer, LOOP §5.1 NW-3/NW-6); distributed sign-in terms (DEL-01-06,
OI-007); qualification evidence (needs a candidate).

**Every sign-in and every key entry is the person's own act.** No agent and
no App rule starts, completes or answers a sign-in, enters, reads or
replaces a key, or changes the access configuration (DERIVED from V4-ARC-04
and REQ-001/002; the same rule as LOOP NW-4 for host loops, PROPOSED here for
the App). An agent may ask the person in conversation; nothing more.

## 1. Interfaces

| ID | Exchange | Supplier → receiver | Condition of use | When the exchange fails |
|---|---|---|---|---|
| I-1 | Codex account methods: `account/read`, `account/login/start`, `account/login/cancel`, `account/logout`, `configRequirements/read`; notifications `account/login/completed`, `account/updated`, `modelProvider/authRecoveryStarted`/`Completed` (all stable, `observed-in-generated-types`) | Codex → DEL-01-05, carried by DEL-01-01 S-4 | `ready(g)` of the home's child (HOSTING §4.1) | A request with no response is *unknown* (HOSTING H10); the entry goes to `unknown` and is re-read after the next `ready`; nothing is retried automatically that carries a credential (CR-6) |
| I-2 | Codex configuration: `config/read {includeLayers: true}` (origins, layer versions), person-directed `config/batchWrite` with explicit `filePath` and `expectedVersion` (stable) | Codex ↔ DEL-01-05 | Person's act for every write (HOSTING §6.8 row; H9) | Version conflict → the write is not retried; the person sees both values and decides. `configWarning` notifications are shown with their path |
| I-3 | Conversation start: explicit `modelProvider` and `model` on `thread/start`; per-turn `model` on `turn/start` | DEL-01-05 → DEL-01-01 S-4 | A selection exists (§5.4) | Error response → `start-failed`, no other entry tried (NS-1) |
| I-4 | Destination class of the chosen entry | DEL-01-05 → DEL-01-01 §8.3 → DEL-04-03 RS R5 | Per conversation | The class is never inferred from an address; with no selection there is no class (HOSTING §8.3; LOOP N-OPEN-1 closure, applied here by analogy) |
| I-5 | Access state snapshot and the conversation's selection state (schemas `access.state`, `access.conversation-selection`) | DEL-01-05 → DEL-01-04 (conversation start display, K-3) | On change | A display without a snapshot shows "access state unknown", never a default |
| I-6 | Observed Codex account of the home that runs the conversation (kind, `email` as reported or null, `planType`) | DEL-01-05 → DEL-01-04 CAP-8 / RS §6.1 (K1-4) | At act capture | No account or `apiKey` kind → no Codex-account element; never a guessed name |
| I-7 | Start-up network view (schema `access.network-observation`) | DEL-01-05 → the person; App diagnostics record | App start; on demand | Observation unavailable → the view says so; the per-pin expected list is still shown, labelled |
| I-8 | Local-server capability requirements and limits (schema `access.capability-handoff`) | DEL-01-05 → DEL-05-01 (DEP-01-05-014) | When DEL-05-01 receives | — |
| I-9 | Account/provider inputs and the focused sign-in and concurrent-mode checks | DEL-01-05 → DEL-09-02 (DEP-09-02-013) | Before V4-EXM-12 | — |
| I-10 | Selected pin and embedding qualification input; sign-in and substitution evidence "when needed" | DEL-01-01 ↔ DEL-01-05 (DEP-01-05-012/013; DEP-01-01-022/024; held, SCC-001) | Held arcs gate nothing | — |

A runtime value DEL-01-05 is handed is not a production input (R17-10
pattern): the live-turn list used by §6 Q-5 and Q-7 comes from HOSTING's
lifecycle and register at run time; no row DEL-01-05 → DEL-01-02 is proposed
(it would put DEL-01-02 into SCC-001; the return file shows the check).

## 2. Access entries

An **access entry** is one way a conversation can reach a model, kept
configured beside the others (REQ-004). The App lists them; the person picks
one per conversation (K-2, SETTLED).

| Kind | What it is | Codex home that serves it (§3) | Provider at `thread/start` | Credential and custody | Destination class (RS R5 enum) |
|---|---|---|---|---|---|
| `chatgpt-account` | The ChatGPT sign-in, which is **the Codex account** of the App's account home (K-2) | H-acct | The built-in OpenAI provider (`inference`: id `openai`; the effective id is read back from the `thread/start` response, HOSTING §8.3) | Codex's credential store of H-acct (V4-ARC-04) | `user-chosen cloud` |
| `api-key` | The API key, **a separate entry** (K-2) | H-key, a second App-owned home whose Codex account is the key (§4, PROPOSED K2-1) | As above, in H-key | Codex's credential store of H-key | `user-chosen cloud` |
| `local-provider:<id>` | A provider definition in the person's Codex configuration whose definition carries no credential element (§11 LP-1) | H-acct | `<id>` | None | `local model server` |
| `other-provider:<id>` | Any other provider in the configuration (gateway OAuth, Bedrock, a definition with `env_key`, `experimental_bearer_token`, `auth`, `aws`, `gateway_oauth` or `requires_openai_auth = true`) | — | — | Not handled by the App at v0.1 | — |

`other-provider` entries are listed with the reason "not offered by the App
at this version" and are not selectable (PROPOSED; V4-APP-02 names three
modes; the forms behind these entries are `strings-in-binary` only, §10
AK-7). This keeps the person's configuration visible without the App
carrying a credential it would have to custody.

The destination class follows the **entry kind the person chose**, never the
address (I-4). A `local-provider` entry whose `base_url` is not a loopback
address is still `local model server` by the person's configuration; the
view shows its address so the person can see it (PROPOSED; LOOP N-OPEN-1's
closure, R12-7, reasons the same way for hosts).

## 3. Codex homes

Summary of the decision record's mechanism (PROPOSED; confirmed or refused by
OBS-2 O-6):

| Home | Owner | Holds | Shared with the person's other Codex clients |
|---|---|---|---|
| The person's Codex home (`$CODEX_HOME` of their shell, usually `~/.codex`) | The person | Their `config.toml` (settings, providers, MCP servers) and their own sign-in | It is theirs. The App reads its configuration through the link and writes it only on the person's act (I-2) |
| H-acct, the App's account home (App data folder) | The App | The App's own sign-in (Codex custody), threads, logs and state of the App's Codex; `config.toml` **is a link** to the person's configuration file | Configuration only, through the link |
| H-key, the App's key home (App data folder; created only when the person adds a key) | The App | The API key (Codex custody); threads of API-key conversations; same configuration link | Configuration only |
| H-probe, the probe home (App data folder) | The App | What the version-label probe writes (S-F-17: `tmp/arg0/…`) | Nothing; never an account home (answers HOSTING §7.2) |

If O-6 shows that 0.158.0 cannot read a linked configuration as its user
layer, the fallback is option A (each App home keeps its own configuration),
and the App says so in its settings view (K-1 as recorded; decision record
§4, "Fallback rule").

## 4. Keeping a ChatGPT sign-in and an API key side by side (K-2)

**Supplier facts.** `GetAccountResponse.account` is one value per Codex
process: `apiKey` · `chatgpt {email | null, planType}` · `amazonBedrock`
(`observed-in-generated-types`). `account/login/start` takes one variant and
has no thread or provider element; nothing in `thread/start`, `turn/start`
or `thread/resume` selects an account (`observed-in-generated-types`). The
provider definition form is not in the generated types (P-11); its fields
are `strings-in-binary`: `base_url`, `model_catalog_url`, `env_key`,
`env_key_instructions`, `experimental_bearer_token`, `auth`,
`gateway_oauth`, `aws`, `wire_api`, `query_params`, `http_headers`,
`env_http_headers`, retry and timeout elements, `requires_openai_auth`,
`supports_websockets`, `supports_standalone_web_search`. The strings also
name environment authentication ("provide an API key through a supported
auth env var"; `OPENAI_API_KEY`, `CODEX_API_KEY`, `CODEX_ACCESS_TOKEN`) —
not behaviour.

**Mechanisms considered** (the owner's K-2 fixes the presentation: the key is
a separate entry; the mechanism is this file's to propose):

| ID | Mechanism | Custody | REQ-004 (others preserved) | Consequence | Assessment |
|---|---|---|---|---|---|
| K2-1 | A second App-owned home H-key whose Codex account is the key (`account/login/start {apiKey}` in H-key); API-key conversations run on H-key's child | Codex (V4-ARC-04 held) | Yes: H-acct keeps the ChatGPT sign-in | Two supplier children: **HOSTING U-12 gains a per-home dimension** (generation, register and thread keyed by home); two start-ups, so K-12 traffic per home; conversation lists merged from two homes | **PROPOSED.** The only mechanism that keeps Codex custody of both credentials at 0.158.0 on the generated types |
| K2-2 | Provider entry with `env_key`; the App supplies the key in the child's environment from its own keychain item | The App (and every descendant process environment the supplier does not filter, `inference`) | Yes | Contradicts "credentials held by Codex" | Set aside unless the owner changes V4-ARC-04 |
| K2-3 | Provider entry with `experimental_bearer_token` in a configuration layer | A plaintext configuration file; in the shared file (K-1) it would leak into the person's CLI configuration | Yes | Key in a file the person shares | Set aside |
| K2-4 | Provider entry with a command-backed `auth` element (shape not in the types) | Whatever the command reads (an OS keychain item the App wrote) | Yes | Shape unknown at 0.158.0 (`strings-in-binary` only) | Not available until observed; App custody at entry |
| K2-5 | Re-login per conversation in one home | Codex | **No**: logging in with one replaces the other (`inference` from the single `Account`); live threads of the other mode affected (not observed) | Breaks REQ-004 | Set aside |
| K2-6 | One home holding both, chosen per thread | Codex | — | No element in the generated types selects an account per thread | Not available at 0.158.0 |

**Standing.** K2-1's need for a second home rests on the generated types
(one account per process) and is `inference` until observed. K-11 allows no
sign-in or API-key observation without a separate owner answer, and OBS-2
does not exercise it. R17-2 says: if this needs more than one Codex home,
report the HOSTING U-12 dimension and do not restructure HOSTING here. This
file reports it (return file, join list) and designs the App side for K2-1;
UNRESOLVED U-A1 carries the owner question.

**What changes if K2-1 is not adopted.** Only H-key and the API-key routing
rows of §2 and §6 Q-6/Q-7; the selection states (§5.4) and the custody rules
(§7) do not change.

## 5. States

Transition tables are PROPOSED. Each event is named by a code in backticks;
the prototype holds the same tables and checks them against this file (VC-A14).

### 5.1 ChatGPT account entry (one per H-acct)

States: `unknown` (before the first `account/read` of a generation, or after
an outcome not observed), `signed-out`, `signing-in`, `signed-in`,
`needs-reauth`, `signing-out`, `not-permitted` (the effective login methods
exclude ChatGPT: `ConfigRequirements.allowedLoginMethods`, or the person's
`forced_login_method = "api"`).

| ID | From | Event | To | Effect and record |
|---|---|---|---|---|
| AE-1 | unknown | `read:null` | signed-out | `account/read` returned `account: null` |
| AE-2 | unknown | `read:chatgpt` | signed-in | Account view: kind, `email` as reported (may be null), `planType` |
| AE-3 | unknown | `read:other-kind` | signed-out | H-acct holds another kind; shown as "this App home holds an <kind> account, not a ChatGPT sign-in" |
| AE-4 | signed-out | `policy:excluded` | not-permitted | The reason and the layer that set it (`config/read` origins) are shown |
| AE-5 | not-permitted | `policy:permitted` | signed-out | After a configuration re-read |
| AE-6 | signed-out | `person:sign-in` | signing-in | Person's act; `account/login/start` `chatgpt` or `chatgptDeviceCode`; `loginId` kept |
| AE-7 | signed-out | `start:error` | signed-out | Error response to the start; text shown after redaction (CR-4) |
| AE-8 | signing-in | `completed:success` | signed-in | `account/login/completed` with the kept `loginId`, then `account/read` confirms |
| AE-9 | signing-in | `completed:failure` | signed-out | `success: false`; `error` shown after redaction |
| AE-10 | signing-in | `person:cancel` | signed-out | `account/login/cancel`; status `canceled` or `notFound` recorded |
| AE-11 | signing-in | `generation:closed` | unknown | Sign-in outcome unknown; re-read after the next `ready`; never restarted by the App |
| AE-12 | signed-in | `person:sign-out` | signing-out | Asks first when live turns run on H-acct, listing them (K-4 pattern) |
| AE-13 | signing-out | `logout:ok` | signed-out | — |
| AE-14 | signing-out | `logout:failed` | unknown | Error or no response; re-read |
| AE-15 | signed-in | `auth:recovery-started` | needs-reauth | `modelProvider/authRecoveryStarted {threadId, turnId, provider, message}` |
| AE-16 | needs-reauth | `auth:recovery-completed` | signed-in | `modelProvider/authRecoveryCompleted` |
| AE-17 | needs-reauth | `read:null` | signed-out | — |
| AE-18 | signed-in | `generation:closed` | unknown | — |
| AE-19 | signed-out | `generation:closed` | unknown | — |
| AE-20 | needs-reauth | `person:sign-in` | signing-in | As AE-6 |

Rules: a `account/login/completed` naming another `loginId` changes nothing
and is shown as "a sign-in the App did not start" (AR-1). Every
`account/updated` triggers one `account/read`; the notification alone never
moves a state (AR-2). Whether `account/updated` arrives on token refresh is
not observed.

### 5.2 API-key entry (one per H-key; K2-1)

States: `unknown`, `absent`, `entering` (the key is in transit for one
request and nowhere else), `present`, `failing` (a model request was refused
for authentication), `removing`, `not-permitted` (login methods exclude
`api`).

| ID | From | Event | To | Effect and record |
|---|---|---|---|---|
| KE-1 | unknown | `read:null` | absent | — |
| KE-2 | unknown | `read:apiKey` | present | `Account {type: "apiKey"}` carries no identity |
| KE-3 | absent | `policy:excluded` | not-permitted | As AE-4 |
| KE-4 | not-permitted | `policy:permitted` | absent | — |
| KE-5 | absent | `person:enter-key` | entering | Person's act; H-key created if absent; `account/login/start {type: "apiKey", apiKey}` |
| KE-6 | entering | `login:ok` | present | Response `{type: "apiKey"}`; validity unknown until first use (AK-5) |
| KE-7 | entering | `login:error` | absent | Error shown after redaction |
| KE-8 | entering | `generation:closed` | unknown | Outcome unknown; **the key is never re-sent** by the App (CR-6) |
| KE-9 | present | `use:auth-failed` | failing | A turn on this entry failed for authentication (supplier error or auth recovery) |
| KE-10 | failing | `use:ok` | present | A later turn completed |
| KE-11 | present | `person:replace-key` | entering | A new login replaces the stored key in Codex; the App never held the old one |
| KE-12 | failing | `person:replace-key` | entering | — |
| KE-13 | present | `person:remove-key` | removing | `account/logout` in H-key; asks first with live turns |
| KE-14 | failing | `person:remove-key` | removing | — |
| KE-15 | removing | `logout:ok` | absent | — |
| KE-16 | removing | `logout:failed` | unknown | — |
| KE-17 | present | `generation:closed` | unknown | — |
| KE-18 | absent | `generation:closed` | unknown | — |

### 5.3 Local-provider entry (one per provider id in the effective configuration)

States: `not-configured`, `listed`, `in-use`, `failing`, `not-offered`
(the definition carries a credential element, §2).

| ID | From | Event | To | Effect and record |
|---|---|---|---|---|
| LE-1 | not-configured | `config:local` | listed | From `config/read`; `base_url` and `wire_api` shown |
| LE-2 | not-configured | `config:needs-credential` | not-offered | Reason shown |
| LE-3 | listed | `start:reported` | in-use | `thread/start` response reported this provider |
| LE-4 | listed | `use:failed` | failing | Start or turn failed reaching the server; no switch (NS-1) |
| LE-5 | in-use | `use:failed` | failing | — |
| LE-6 | failing | `use:ok` | in-use | — |
| LE-7 | listed | `config:gone` | not-configured | Conversations that used it keep their record; new turns refused "provider no longer configured" |
| LE-8 | in-use | `config:gone` | not-configured | — |
| LE-9 | failing | `config:gone` | not-configured | — |
| LE-10 | not-offered | `config:gone` | not-configured | — |
| LE-11 | listed | `config:needs-credential` | not-offered | Definition changed |
| LE-12 | not-offered | `config:local` | listed | Definition changed |

Whether the App also offers a person-initiated reachability check of a
loopback `base_url` (an App-origin contact) is left open (U-A6); v0.1 learns
reachability only from use.

### 5.4 Conversation selection (K-3; one per App conversation)

States: `no-selection`, `offer-shown`, `selected`, `starting`, `started`,
`start-failed`, `entry-unavailable`.

**K-3 (SETTLED by DECISION-K3):** a new conversation has no model chosen
until the person chooses. The App may offer the person's last explicit choice
for that project, shown as such, never applied silently. The refusal wording
reuses R15-1's "run not started — no model selected" (R17-2).

| ID | From | Event | To | Effect and record |
|---|---|---|---|---|
| CS-1 | no-selection | `person:message` | no-selection | Refused: "run not started — no model selected"; the message stays as a draft; nothing is sent |
| CS-2 | offer-shown | `person:message` | offer-shown | Same refusal; **the offer is not applied** |
| CS-3 | no-selection | `app:last-choice-exists` | offer-shown | Offer labelled "your last choice for this project: <entry>, <model>" |
| CS-4 | offer-shown | `person:accept-offer` | selected | Selection source `offered-last-choice-accepted`; the acceptance is the person's act |
| CS-5 | no-selection | `person:choose` | selected | Source `person` |
| CS-6 | offer-shown | `person:choose` | selected | Source `person`; the offer is withdrawn |
| CS-7 | selected | `person:choose` | selected | Changed before start |
| CS-8 | selected | `person:message` | starting | `thread/start` with explicit `modelProvider` and `model` on the entry's home (I-3) |
| CS-9 | starting | `start:ok` | started | Requested and reported provider/model recorded separately (HOSTING §8.3) |
| CS-10 | starting | `start:error` | start-failed | Error shown; the choice is kept; no other entry tried |
| CS-11 | starting | `generation:closed` | start-failed | Outcome unknown (a thread may exist; the App lists threads after `ready` and shows any found, never assumes) |
| CS-12 | start-failed | `person:choose` | selected | — |
| CS-13 | start-failed | `person:message` | starting | Retry is the person's act |
| CS-14 | selected | `entry:unavailable` | entry-unavailable | E.g. signed out, key removed, provider removed |
| CS-15 | started | `entry:unavailable` | entry-unavailable | Turns refused with the reason; no switch |
| CS-16 | entry-unavailable | `entry:available-unstarted` | selected | — |
| CS-17 | entry-unavailable | `entry:available-started` | started | — |
| CS-18 | started | `person:change-model` | started | Per-turn `model` on `turn/start`; recorded as a model change, never a new run (RS R5) |
| CS-19 | started | `person:change-entry` | started | Refused: "start a new conversation for another access mode" (v0.1; §6 Q-11) |
| CS-20 | entry-unavailable | `person:message` | entry-unavailable | Refused with the reason; no other entry tried |
| CS-21 | started | `person:message` | started | Ordinary `turn/start` |

**No silent switch (NS-1, DERIVED from K-3 and D4-3; the same rule as LOOP
NW-5 for hosts).** No failure, unavailability, re-route or configuration
default ever moves a conversation to another entry or provider. A supplier
`model/rerouted` is recorded and shown (HOSTING §8.3), and
`allowProviderModelFallback` is never requested (PROPOSED).

**Codex's configured default is never applied silently (NS-2, DERIVED from
K-3).** The person's configuration may carry `model` and `model_provider`;
because the App always sends both explicitly on `thread/start` (CS-8), the
configured default never selects a conversation's model. `Model.isDefault`
from `model/list` may be shown as Codex's own label, never preselected.

### 5.5 Configuration link (one per App home; K-1)

States: `not-set-up`, `linked`, `target-missing`, `link-broken`,
`own-config` (option A for settings).

| ID | From | Event | To | Effect and record |
|---|---|---|---|---|
| CL-1 | not-set-up | `setup:target-exists` | linked | Link created in the App home; the person is told which file the App reads |
| CL-2 | not-set-up | `setup:target-absent` | target-missing | The person has no configuration file yet; Codex treats the user layer as absent (`ConfigLayerSource` "not guaranteed to exist") |
| CL-3 | not-set-up | `setup:mechanism-unworkable` | own-config | Fallback A, recorded and shown (O-6 refused the link) |
| CL-4 | linked | `check:replaced` | link-broken | The App-home file is no longer a link (for example a write replaced it); shown; **never re-linked or copied silently** |
| CL-5 | linked | `check:target-gone` | target-missing | — |
| CL-6 | target-missing | `check:target-back` | linked | — |
| CL-7 | link-broken | `person:relink` | linked | The divergent App-home file is kept as a dated backup in the App home, never deleted |
| CL-8 | link-broken | `person:keep-own` | own-config | — |
| CL-9 | own-config | `person:link` | linked | — |
| CL-10 | linked | `check:intact` | linked | Checked at every start of a home's child and after every App-issued write |

## 6. Operating sequences

Each step names its failure behaviour. "Person's act" means a control the
person operates in the App's interface; under R17-5 (PROPOSED) the main
process receives it from a native interface event, so no agent tool can
operate it.

**Q-1 App start (per home).**
1. Resolve homes (§3). H-key only if it exists. Failure to create a home →
   that entry `unknown` with the reason; other homes continue.
2. Configuration link check (§5.5). A broken link does not stop the start;
   it is shown.
3. Spawn and handshake through HOSTING §4.2 with `CODEX_HOME=<home>`, the
   K-12 session flags (§9; **OBS-2 pending, O-6/O-7**: whether `app-server`
   accepts `-c` session flags) and the declared capability
   `explicitGatewayOauth: true` (I-1; PROPOSED: so no gateway browser
   authorization starts without the person's act — the capability text says
   it replaces "automatic browser authorization"). The App passes none of
   `OPENAI_API_KEY`, `CODEX_API_KEY`, `CODEX_ACCESS_TOKEN` into the child's
   environment, even if the App inherited them (CR-7). Handshake failure →
   HOSTING's handling; a refusal caused by the person's own configuration
   (F-32: `approval_policy = "untrusted"` in the file) is shown as such and
   never "fixed" by the App.
4. `configRequirements/read` and `config/read {includeLayers: true}`:
   login methods allowed, credential store mode, provider definitions
   (§2), layer origins. Failure → entries `unknown`, shown.
5. `account/read` (never with `refreshToken: true`, CR-5) → §5.1/§5.2.
6. Start the network observation of this child's process tree (§9).

**Q-2 ChatGPT sign-in, browser (person's act).**
1. Person chooses "Sign in with ChatGPT". If a sign-in is already pending on
   H-acct, the App offers to cancel it first (one at a time).
2. `account/login/start {type: "chatgpt"}`; the optional elements
   (`codexStreamlinedLogin`, `useHostedLoginSuccessPage`, `appBrand`) are left
   absent (supplier defaults; U-A4). Error → AE-7.
3. Response `{loginId, authUrl}`: the App opens `authUrl` in the person's
   default browser, never in an App webview (CR-3), and shows "waiting for
   sign-in in your browser" with Cancel. The URL is not recorded or logged.
4. `account/login/completed {loginId, success, error}` → AE-8 or AE-9.
   The local callback the browser returns to is Codex's own (`inference`);
   the App does not handle it.
5. No completion within the App's wait → nothing happens automatically; the
   person may cancel (AE-10). Silence never completes or fails a sign-in
   (HOSTING H8 applied).

**Q-3 ChatGPT sign-in, device code (person's act).** As Q-2 with
`chatgptDeviceCode`; the response gives `verificationUrl` and `userCode`;
the App shows both to the person for the duration of the sign-in only, never
records them (CR-3).

**Q-4 Cancel.** `account/login/cancel {loginId}`; `canceled` or `notFound`
both end in `signed-out` (AE-10); `notFound` is shown as "Codex had no
pending sign-in".

**Q-5 Sign out (person's act).** Live turns on H-acct (runtime value from
HOSTING) → ask first, listing them; the person may cancel. `account/logout`
→ AE-13/AE-14. Conversations on `chatgpt-account` go `entry-unavailable`
(CS-15).

**Q-6 Add or replace an API key (person's act; K2-1).**
1. The person types or pastes the key into a native secure field. The
   interface passes it to the main process once; neither keeps it after the
   request is written (CR-1).
2. H-key absent → create it, link its configuration (§5.5), start its child
   (Q-1).
3. `account/login/start {type: "apiKey", apiKey}` on H-key's child. The
   recording tap and the client-request record keep the method and
   `type` only (CR-2).
4. Response → KE-6/KE-7; no response → KE-8 (the key is not re-sent; the
   person re-enters it if they choose).

**Q-7 Remove the API key (person's act).** As Q-5 on H-key → KE-13…KE-16.
H-key's threads stay readable from H-key; the App does not delete the home
(U-A5).

**Q-8 Add, edit or remove a local provider (person's act).**
1. The person fills name, `base_url`, `wire_api` (only `responses` is
   offered: `wire_api = "chat"` is refused by 0.158.0 per its strings, F-28;
   Responses observed at one pair, L-2).
2. The App shows that the change is written to **their Codex
   configuration**, which their other Codex clients also read (K-1).
3. `config/batchWrite {edits: [model_providers.<id>.*], filePath: <the
   person's configuration file, resolved>, expectedVersion: <from Q-1 step
   4>}`. Writing through the explicit target path keeps the link intact
   (VC-A11 shows the hazard of writing at the link path). `okOverridden` →
   the overriding layer and effective value are shown. Version conflict →
   nothing retried (I-2).
4. Never a key in a provider definition (CR-8). Re-read → §5.3.

**Q-9 New conversation (K-3).** `no-selection`; if the project has a last
explicit choice, `offer-shown` (CS-3). The model list per entry: for
`chatgpt-account` and `api-key`, `model/list` on the entry's home; for a
local provider, `model/list` does not name a provider (no element in
`ModelListParams`), so the App offers the configured model of that provider
if any and a free model identifier field (U-A7, OBS-2 pending in round 2).

**Q-10 Start.** CS-8…CS-11. Requested values recorded per HOSTING §8.3;
destination class from §2.

**Q-11 Resume.** The conversation resumes on the home that holds its thread
with its entry unchanged. Changing entry is not offered at v0.1 (CS-19):
across homes a thread cannot move (K2-1), and within H-acct whether a
`thread/resume` provider override is adopted by a loaded thread is not
observed (P-15 pattern; O-5 tests the developer-instruction case only).
PROPOSED.

**Q-12 Authentication trouble during a turn.** `authRecoveryStarted` →
`needs-reauth` (AE-15) for that entry's conversations; turns are not
re-sent elsewhere (NS-1). The person may sign in again (AE-20).

**Q-13 Provider unreachable or model error.** The turn ends as Codex reports
it; the entry goes `failing` (LE-4/LE-5 or KE-9); the conversation stays on
its entry; the message to the person names the entry and the supplier's
error after redaction.

**Q-14 Configuration changed outside the App.** `configWarning` → shown with
its path. The App re-reads the configuration at the next idle point of each
home (never mid-turn) and at each start; entries move per §5.3. Whether a
running Codex re-reads its configuration file after an outside edit is not
observed; the generated types say only that an App-issued
`config/batchWrite` with `reloadUserConfig: true` hot-reloads runtime
settings into loaded threads, while model, effort and tier defaults are
session-static (`observed-in-generated-types`). So the App's view says an
outside change applies at the next child start unless observed otherwise.

## 7. Credential custody rules (PROPOSED unless marked)

| ID | Rule |
|---|---|
| CR-1 | An API key exists in App memory only between the person's entry and the written `account/login/start` frame; the interface field is cleared and the buffer released after the write. Never stored, cached, logged, recorded, put in an error, a URL, a command line or an environment variable (DERIVED from V4-ARC-04: credentials held by Codex) |
| CR-2 | The recording tap (HOSTING §9.1) and the client-request record (`hosting.client-request-record`) keep, for `account/login/start`, the method, `type` and `loginId`; the parameters `apiKey`, `accessToken`, `secretAccessKey`, `sessionToken` and the response elements `authUrl`, `verificationUrl`, `userCode` are replaced by a redaction marker before anything is written (join to HOSTING §9.1) |
| CR-3 | `authUrl` opens in the system browser; `verificationUrl` and `userCode` are shown only while the sign-in is pending |
| CR-4 | Supplier error texts from account methods are shown and recorded after the CR-2 redaction is applied to them as text (a key echoed in an error is removed) |
| CR-5 | `getAuthStatus` (TS-only) is never called with `includeToken: true`; `account/read` is not called with `refreshToken: true` by an App rule |
| CR-6 | No request carrying a credential is retried or replayed automatically, including after a restart (HOSTING H10: unknown stays unknown) |
| CR-7 | The child environment carries no `OPENAI_API_KEY`, `CODEX_API_KEY` or `CODEX_ACCESS_TOKEN`. The strings name environment authentication ("auth is provided by environment"; `strings-in-binary`); that it takes precedence over the home's stored credential is `inference`, so passing one could silently change which credential a home uses |
| CR-8 | The App never writes a credential into any configuration file or `-c` flag (sets K2-2/K2-3 aside) |
| CR-9 | External-token login (`chatgptAuthTokens`) is not offered: the App would hold tokens. So `account/chatgptAuthTokens/refresh` stays **known-app-unsupported** with an explicit error (confirms HOSTING §6.1's row; U-20 for that kind) |
| CR-10 | The credential store mode (`cli_auth_credentials_store`: `file`, `keyring`, `auto`, `ephemeral`) is the person's setting in the shared configuration, carried unchanged (H9); the App shows it and what it means for the App (with `ephemeral`, the App's sign-in ends with each start) |

## 8. What the App shows of an account, and identity supply (K1-4)

- Shown: the entry kind; for `chatgpt-account` the `email` as Codex reports
  it (or "no email reported") and the `planType`; for `api-key` only "API key
  stored by Codex"; never any part of a key, token, URL or code.
- **Identity supply (I-6; SETTLED by K1-4 that the Codex account is a
  source; the form is PROPOSED):** at act capture DEL-01-01/DEL-01-04 receive
  from this file the account of **the home that runs the conversation**, as
  last read: `{kind: "chatgpt", email|null, planType}`; for `apiKey` and for
  no account, no Codex-account element. Labelled App-observed, "identity not
  verified" (K1-4). Whether a record stores the email or a digest of it is
  the record owner's (RS §6.1) — U-A8 names the privacy question.

## 9. Start-up traffic and the network view (K-12)

**K-12 (SETTLED by DECISION-K3 revised):** the App turns off whatever Codex's
settings allow of its start-up traffic, shows the rest in its network view
and records it; the design names which is which. **Codex does not report its
own connections in its event stream.** Searched in the 0.158.0 notification
list and types: no notification reports a network connection Codex makes;
the `Network*` types concern tool sandbox permissions. The one partial signal
is `remoteControl/status/changed {status: disabled | connecting | connected
| errored, …}` (stable; OBS-1 saw it arrive with the initialize response),
which reports the remote-control state, not destinations or other traffic
(`observed-in-generated-types`). So the App learns its Codex's connections
by **both** means below (PROPOSED), and shows the remote-control status
beside them.

**Which is which (per pin; OBS-2 O-7 settles the "App action" column):**

| Start-up traffic (OBS-1 §8, B.5) | Candidate Codex setting | App action | Standing |
|---|---|---|---|
| Remote-control loop to `chatgpt.com/backend-api/` (retries about once a second without sign-in) | Feature key `remote_control` (`strings-in-binary`; also requirement `allow_remote_control`); runtime `remoteControl/disable` (experimental-only client method, `observed-in-generated-types`; acts after start, so not for the first contact); environment `CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED` (`strings-in-binary`; internal, not a setting) | Turn the feature off in the App's session flags at spawn if O-7 shows it stops the loop; the internal environment name is not used (it is not a Codex setting; using it needs an integrator ruling, U-A9) | **OBS-2 pending (O-7)** |
| Featured-plugins request to chatgpt.com (401 without sign-in) | Feature key `plugins` (`strings-in-binary`) | As above, if O-7 shows the effect; consequence shown: plugins unavailable in the App's Codex | **OBS-2 pending (O-7)** |
| Plugin repository sync, `github.com/openai/plugins` (full fetch ≈24 MB on a fresh home; `git ls-remote` on a synced one) | Feature key `plugins`; `remote_installed_plugin_sync` (`strings-in-binary`) | As above | **OBS-2 pending (O-7)** |
| Analytics | `[analytics] enabled = false` (`AnalyticsConfig`, generated types) | Set off in the session flags | OBS-1: off does **not** stop the three rows above; whether it stops analytics traffic itself is not observed |
| Update check | `check_for_update_on_startup` (`strings-in-binary`) | Set off in the session flags if O-7 confirms the key | **OBS-2 pending (O-7)** |
| Model traffic of a conversation | The person's entry | Not turned off: it is the chosen destination; shown with its class | HOSTING §8.3 |
| Sign-in endpoints during Q-2/Q-3 | — | Not turned off; shown as "sign-in" while pending | `inference` (LOOP N-OPEN-2 is the host counterpart) |

**Carrier.** The App's traffic settings go in the session-flags layer of the
App's own child (`ConfigLayerSource` `sessionFlags` is in the generated
types; that `-c` flags form this layer is `inference`, OBS-2 pending O-6), never
into the person's configuration file, and they are recorded in HOSTING's
configuration identity (§7.1). They change only the App's Codex. The
network view lists each as "turned off by the App". Whether the person may
turn one back on for the App is PROPOSED **yes** (an App setting, shown and
recorded), because Root `AGENTS.md` says the App does not "veto the user's
Codex configuration" and an App-scoped flag the person controls keeps that
true (U-A9 for the integrator).

**How the App learns connections (both, PROPOSED):**

1. **Per-pin expected list.** From OBS-1/1b and OBS-2 O-7: for each traffic
   row, destination, process, phase and the setting that stops it. Shown as
   "expected at Codex 0.158.0"; replaced at each pin by the upgrade
   comparison (HOSTING §9.5).
2. **The App's own observation** of the sockets of its supplier process tree
   (the process set HOSTING H11 already tracks), sampled with operating-system
   facilities (mechanism unselected; OBS-1 used `lsof`). Limits stated in the
   view: a sample is a **lower bound** (a connection shorter than the
   sampling interval can be missed: OBS-1b's 30 ms command was missed by
   250 ms samples); it shows addresses, and a host name only where the
   expected list or a lookup supplies it, labelled. Codex's own internal log
   files are not read (unpublished format).

A connection seen but not on the expected list is shown as **unlisted** and
recorded; it is never blocked by the App (no App-side gate exists for the
App's Codex, HOSTING §2). The record (`access.network-observation`) is an
App diagnostics record, App-observed, never run evidence and never authority
for what Codex sent; whether any of it enters a run record is DEL-04-03's
(U-A10). A person using only a local model and not signed in sees the
remaining start-up rows, so "nothing leaves the machine" is never implied.

## 10. API-key definition record (OUT-003, REQ-006; OI-010 stays OPEN)

Supported API-key behaviour at the definition pin 0.158.0, with standing.
Nothing here is observed live: no key has ever been used in this project.

| ID | Statement | Standing |
|---|---|---|
| AK-1 | Carrier: `account/login/start {type: "apiKey", apiKey: string}` → `{type: "apiKey"}`; stable | `observed-in-generated-types` |
| AK-2 | After login, `account/read` reports `{type: "apiKey"}`, which carries no identity | `observed-in-generated-types` |
| AK-3 | One account per Codex process; no per-thread account selection | `observed-in-generated-types` (absence of an element), hence K2-1 |
| AK-4 | Stored by Codex in the store selected by `cli_auth_credentials_store` (`file`, `keyring`, `auto`, `ephemeral`); location not observed; the strings name `auth.json` | Mode list `observed-in-generated-types`; location `strings-in-binary` |
| AK-5 | Whether the key is validated at login is not known; the App treats validity as known only at first use (KE-6, KE-9) | `inference` |
| AK-6 | `account/logout` removes the stored credential; storage effect not observed | Method `observed-in-generated-types` |
| AK-7 | Provider-level credential elements (`env_key`, `experimental_bearer_token`, `auth`, `aws`, `gateway_oauth`, `requires_openai_auth`) exist as definition field names; not used (CR-8; §4) | `strings-in-binary` |
| AK-8 | Login may be restricted: `allowedLoginMethods` (`chatgpt`, `api`), `forced_login_method` in the person's configuration | `observed-in-generated-types` |
| AK-9 | Environment variables can provide credentials; precedence over the stored credential not observed (CR-7) | Existence `strings-in-binary`; precedence `inference` |
| AK-10 | Effect of an API-key login on a ChatGPT sign-in in the same home (replacement) | `inference`; the reason for K2-1 |

**Implications for the three modes (AC-006).** All three stay required and
configurable together through K2-1 (H-acct: ChatGPT and local providers;
H-key: the API key). **OI-010 remains OPEN**: AK-5, AK-6's storage effect and
AK-10 need an observation with a key, which K-11 does not allow without a
separate owner answer (U-A2).

## 11. Local providers and the handoff to DEL-05-01 (REQ-003, REQ-008)

**What the App offers (REQ-003, PROPOSED):**

- LP-1 A local provider is a definition in the person's configuration with
  `base_url`, `wire_api = "responses"` and no credential element (§2).
  Built-in names `lmstudio` and `ollama` and the environment names
  `CODEX_OSS_BASE_URL`, `CODEX_OSS_PORT` exist as `strings-in-binary` (F-28);
  the App lists built-ins only if `config/read` reports them.
- LP-2 Capability shown per entry: `modelProvider/capabilities/read` returns
  `{namespaceTools, imageGeneration, webSearch}` but **takes no parameters**
  (`observed-in-generated-types`), so which provider it describes is not
  known (`inference`: the process's configured provider). Until observed, the
  App does not show these per entry; it shows F-31 as a stated limit:
  "on LM Studio 0.4.16 through Responses, MCP tools did not reach the model"
  (U-A7).
- LP-3 A local server that needs a key is `not-offered` at v0.1 (v3's oMLX
  helper held its own key; App v3 is evidence only, not a commitment).

**Handoff to DEL-05-01 (REQ-008; I-8; schema `access.capability-handoff`;
fixture `prototype/fixtures/capability-handoff.valid.json` is its v0.1
content).** Items, each with standing:

| ID | Statement | Interface | Standing | What it means for a host loop |
|---|---|---|---|---|
| CH-1 | The App reaches a local model through Codex's provider interface, Responses (`wire_api = "responses"`); Chat Completions is refused by 0.158.0 for providers | App Codex provider | Responses at one pair `observed` (OB-8); refusal of `chat` `strings-in-binary` (F-28) | None directly: the host loop uses Chat Completions (V4-ARC-10, LOOP §1); a server serving both does not join them |
| CH-2 | LM Studio 0.4.16 dropped `namespace` tools on Responses; MCP tools did not reach the model | App Codex provider | `observed` at one pair (OB-1; F-31) | Not a Chat Completions finding; LOOP's FB-CC-1 stands |
| CH-3 | A flat function tool was called through Responses at that pair | App Codex provider | `observed` (OB-2) | — |
| CH-4 | The server ignored `prompt_cache_key` and `include`, turned the developer role into system | App Codex provider | `observed` (OB-8) | The host may see the same server behaviour on its own route; to be checked on Chat Completions |
| CH-5 | Codex put the host's IANA time zone into the model context | App Codex provider | `observed` (OB-11) | Not a host matter; recorded |
| CH-6 | Credentials of the App's providers are Codex's; host credentials and endpoints are the host native layer's (LOOP NW-3, NW-6) | Both | SETTLED (V4-ARC-04, V4-ARC-12) | No App credential or provider configuration is shared with a host |
| CH-7 | No host conformance is claimed from App observations | Both | SETTLED (SoW AC-009; AX-003) | — |

LOOP §10.3 says this input is "not consumed by this file"; whether DEL-05-01
consumes it is DEL-05-01's (pass-2 proposal R-0501-4; return file).

## 12. Qualification and substitution (REQ-007, OUT-004) — designed only

No candidate exists, so nothing is qualified. The method: on a candidate,
for each entry kind, run VC-A01…VC-A04 with the person; record pin and
distribution identity (HOSTING §7.1), the configured server (name, version,
address), the provider definition, `wire_api`, the exchanges (recorded per
HOSTING §9 with CR-2 redaction) and the result. Substitution (AC-008): the
person edits the provider's `base_url` or adds a second local provider
(Q-8); the substitute is compliant if a conversation starts and a turn
completes, with tool calling checked separately (L-3); a failure is recorded
as such, never hidden by a switch.

## 13. Receivers and register rows

| Row (DAG-003 layer) | Direction | Other end | Where this file holds it |
|---|---|---|---|
| DEP-01-05-012, -013 (held, SCC-001) | Upstream | DEL-01-01: pin, embedding qualification input | Basis; §12 |
| DEP-01-05-014 (admitted) | Downstream | DEL-05-01 | §11 |
| DEP-01-05-015, -016 (constraint) | — | OI-009, OI-010 | Decision record; §10 |
| DEP-01-01-022 (mirror of -012) | — | DEL-01-01 | S-4 carriage, §8.1 |
| DEP-01-01-024 (held, SCC-001; no counterpart here) | DEL-01-01 consumes | Sign-in and substitution evidence "when needed" | §12 (designed); return file proposes a mirror row |
| DEP-09-02-013 (admitted) | DEL-09-02 consumes | Account/provider inputs; focused checks | I-9; VC-A01…A05 |
| (none yet) | DEL-01-04 would consume | Access state for the start display; Codex account for CAP-8 | I-5, I-6; new row proposed in the return file (SCC-neutral: DEL-01-05 reaches only DEL-01-01) |

## 14. Owner and act boundary (REQ-009, AC-010)

| Act | Owner | This file |
|---|---|---|
| Stock hosting, pin, generated types, embedding qualification | DEL-01-01 (CLM-003) | Consumes S-4; asks for joins only |
| Loop/model receiving contract | DEL-05-01 (CLM-004) | Hands §11 |
| Host loop, native layer, host endpoints and keys | External host owner | None |
| Sign-in, key entry, sign-out, key removal, provider configuration | **The person** | Designs the receiving; performs none |
| Account-home choice | Owner with App implementation owner (OI-009) | Decision record |
| Request cards, act control, start display | DEL-01-04 | Supplies I-5, I-6 |
| Start-up traffic acceptability | Owner (K-12 decided) | §9 |

## 15. Data formats (PROPOSED; JSON Schema 2020-12)

| Schema | Handed to | Content |
|---|---|---|
| [`access.state.schema.json`](access.state.schema.json) | DEL-01-04 (I-5); the App's settings view | Homes with link state; entries with kind, state, provider, class, account view; never a credential element (closed objects) |
| [`access.conversation-selection.schema.json`](access.conversation-selection.schema.json) | DEL-01-04 (I-5); DEL-01-01 S-4 (I-3); DEL-04-03 via §8.3 (I-4) | State per §5.4; selection with source; an offer that is never a selection; thread with requested and reported values; refusal reasons |
| [`access.network-observation.schema.json`](access.network-observation.schema.json) | The person (I-7); App diagnostics | Rows with destination, process, phase, purpose, sources (`app-observed`, `expected-at-pin`), the App setting's state, and the lower-bound limit |
| [`access.capability-handoff.schema.json`](access.capability-handoff.schema.json) | DEL-05-01 (I-8) | Items with interface, standing and host meaning; `noHostConformanceClaimed: true` |

Valid and invalid instances: `prototype/fixtures/*.valid.json`,
`*.invalid.json` (each file holds a `description` and the `instance`). Each
invalid instance's description names the one reason it must fail, and the
run shows it failing for that reason (VC-A17).

## 16. Prototype (R17-1; R12-3)

[`prototype/`](prototype/), Python 3 standard library only, no install, no
network, no Codex. `access_model.py` holds the §5 tables, the selection,
routing, custody, link and network-view models; `run_cases.py` runs VC-A08…
VC-A16 and the schema checks; `jsonschema_subset.py` is a byte-identical copy
of DEL-01-01's validator (sha256 486e9286…c0ffc0). The link and probe-home
cases use a temporary folder under `$TMPDIR` with invented content, check
that no path outside it (and nothing under `~/.codex`) is touched, and remove
it. Custody is tested with invented canary strings that are not shaped like
any key, token, URL or code. Command: `cd prototype &&
PYTHONDONTWRITEBYTECODE=1 python3 run_cases.py`. **Ran 2026-10-01 (UTC),
Python 3.13.7, macOS Darwin 25.6.0 arm64: TOTAL 7, FAIL 0**; the output and
the sha256 of every input are in `prototype/results/RUN_2026-10-01.txt`. A
"pass (model)" is evidence that the rules run as written, never a VER pass.

## 17. Findings

- **F-A1 Two homes for two cloud credentials.** At 0.158.0 a Codex process
  has one account and no per-thread account element, so a ChatGPT sign-in
  and an API key kept side by side with Codex custody need two App-owned
  Codex homes (K2-1). HOSTING U-12 needs a per-home dimension (R17-2).
  `inference` from generated types; not observed.
- **F-A2 Capabilities are not per provider.**
  `modelProvider/capabilities/read` takes no parameters, so `namespaceTools`
  (the F-31 element) cannot be read per entry without observing which
  provider it describes.
- **F-A3 Writes through a linked configuration.** A write that replaces the
  file at the link path breaks the link silently; writes therefore pass the
  resolved target as `filePath`, and the link is checked after each write
  (VC-A11). How Codex writes (in place or by replacement) is not observed.
- **F-A4 Gateway OAuth would open a browser by itself.** The handshake
  capability `explicitGatewayOauth` replaces "automatic browser
  authorization"; the App declares it true (join to HOSTING §4.2 step 4).
- **F-A5 Codex reports no connections.** Apart from the remote-control
  status notification, nothing in the event stream names a connection, so
  K-12's record needs the App's own observation plus a per-pin list; the
  observation is a lower bound.
- **F-A6 Environment authentication.** The binary's strings name environment
  variables that provide credentials; the App passes none (CR-7).
- **F-A7 v3 chose a separate home (option A in practice).** App v3's settings
  text says its home "never reads, copies, or links your ambient
  `~/.codex`" (`frontend/src/components/settings/account-consent-settings.tsx`
  line 231), while Root `AGENTS.md` describes shared configuration with
  separate authentication. Evidence only; K-1 decides v4.

## UNRESOLVED

| ID | Item | Owner | Point of need | Effect here |
|---|---|---|---|---|
| U-A1 | Adopt K2-1 (two App homes; HOSTING U-12 per-home dimension) or change V4-ARC-04's custody for the API key (K2-2/K2-4) | Owner with App implementation owner | Before account integration | §4 designs K2-1 |
| U-A2 | An API-key and sign-in observation (OI-010; AK-5, AK-6, AK-10; K2-1's premise): with the owner's own key and sign-in, or with an invented non-functional key string in a scratch home | Owner (K-11 requires a separate answer) | Before API-key implementation | Rows stay `inference` |
| U-A3 | K-1 mechanism (linked configuration) | OBS-2 O-6, then integrator | Before account integration | Decision record §4; fallback A |
| U-A4 | `chatgpt` login options (`codexStreamlinedLogin`, `useHostedLoginSuccessPage`, `appBrand`) | App implementation owner | Before sign-in implementation | Left absent |
| U-A5 | What happens to H-key and its threads when the key is removed | App implementation owner | Before API-key implementation | Kept, readable |
| U-A6 | A person-initiated loopback reachability check (App-origin contact) | App implementation owner | Before local-provider UI | Not offered |
| U-A7 | Which provider `modelProvider/capabilities/read` describes; model listing for local providers | Next observation (round 2 or later) | Before per-entry capability display | Limits shown as text |
| U-A8 | Email or digest of the Codex account in act records (privacy) | DEL-04-03 with the integrator | Before act-record implementation | Supplied as reported |
| U-A9 | K-12 levers: whether the internal environment name may be used; whether the person may turn a traffic setting back on for the App | Integrator (doctrine) | After O-7 | Settings table; "yes" proposed |
| U-A10 | Whether start-up network observations enter any run record | DEL-04-03 | Before records | Diagnostics only |
| U-A11 | The App implementation owner's participation in the K-1 choice (REQ-005 names both) | Owner | Before account integration | Decision record §3 |
| U-A12 | `-c` session flags accepted by `app-server` | OBS-2 O-6/O-7 | Before K-12 implementation | Carrier PROPOSED |

## Verification cases

"Needs" says what each case requires. None can pass a VER criterion yet: no
candidate exists.

| Case | Setup | Expected | Needs | Runnable now? | Serves |
|---|---|---|---|---|---|
| VC-A01 ChatGPT sign-in | Candidate; H-acct signed out | Q-2 completes; conversation on `chatgpt-account` starts; `account/read` chatgpt; no credential in App storage, records or logs (custody scan) | **The person's own sign-in**; candidate | No | VER-001 |
| VC-A02 API-key entry | Candidate; no H-key | Q-6; KE-6; API-key conversation starts on H-key; custody scan clean | **The person's key**; candidate; U-A1 | No | VER-002 |
| VC-A03 Local provider | Candidate; identified local server | Q-8; conversation starts; requested = reported provider; endpoint and model identity recorded | Identified server; candidate | No | VER-003 |
| VC-A04 All three together | VC-A01…A03 configured | One conversation per entry; each starts; the other two stay configured and selectable after each | Person; key; server; candidate | No | VER-004 |
| VC-A05 Account-home record review | Decision record | Alternatives, choice, participants, timing; open items explicit | Review | Yes (review) | VER-005 |
| VC-A06 API-key definition review | §10 | Each AK row traced to its standing; OI-010 open | Review | Yes (review) | VER-006 |
| VC-A07 Qualification record | Candidate records | Observed passes, failures, unverified claims distinguished; DEL-01-01 input linked | Candidate | No | VER-007 |
| VC-A08 Substitution | Two local servers | Edit `base_url` (Q-8); conversation starts on the substitute; result recorded | Two servers; candidate | No (model: routing only) | VER-008 |
| VC-A09 Handoff review | §11 and the fixture | Interface distinction, limits, no conformance claim | Review; schema check | Yes | VER-009 |
| VC-A10 Act boundary | §14 | Each REQ-009 act to its owner | Review | Yes (review) | VER-010 |
| VC-A11 Configuration link | Temporary folder, invented configuration | Write with explicit target keeps link (CL-10); write by replacement at the link path → `check:replaced` → `link-broken`, both files kept; nothing outside the folder touched | Prototype | **Yes. Ran 2026-10-01: pass (model)** | VER-004, VER-005 |
| VC-A12 K-3 selection walk | Model | CS-1/CS-2 refuse with "run not started — no model selected"; the offer is never applied; start sends explicit provider and model; no entry switch on unavailability (NS-1) | Prototype | **Yes. Ran 2026-10-01: pass (model)** | VER-004 |
| VC-A13 Custody scan | Model with invented canary strings standing in for a key, an auth URL and a device code | Canaries only in the frame written to the child and the transient display; absent from records, logs, snapshots, errors | Prototype | **Yes. Ran 2026-10-01: pass (model)** | VER-001, VER-002 |
| VC-A14 Tables | This file and the model | §5 tables equal the model's, row for row | Prototype | **Yes. Ran 2026-10-01: pass (model)** | — |
| VC-A15 Routing (K2-1) | Model | `chatgpt-account` and local entries start on H-acct; `api-key` on H-key; H-key child exists only with a key; cross-home entry change refused | Prototype | **Yes. Ran 2026-10-01: pass (model)** | VER-004 |
| VC-A16 Network view | Model; expected list from OBS-1/1b; invented sockets (documentation addresses) | Rows carry sources; an unlisted address is shown and never blocked; settings marked "OBS-2 pending" until O-7 | Prototype | **Yes. Ran 2026-10-01: pass (model)** | — |
| VC-A17 Schemas | Four schemas and fixtures; records the model emits | Valid valid; invalid invalid for the stated reason; every emitted record valid | Prototype | **Yes. Ran 2026-10-01: pass (model)** | VER-004, VER-009 |
