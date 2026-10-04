# Account and provider access

- Contribution: DEL-01-05/ACCESS-v0.2 (supersedes DEL-01-05/ACCESS-v0.1,
  committed at `63a6e0fa47`, file sha256
  b82e40395a4a19bcd0b4e5623fd62b1040b7110ab19cb01af58b15582d447da4)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. Nothing here is qualified; no App candidate exists.
- **Pass-4 closeout C2 (run `APP-V4-DESIGN-PASS-4-20261003`; R23-29 item 2; in place, no version step):** §13 gains DEP-01-05-017, the supplier-side counterpart of DEP-09-02-013 ruled in R22-7 (V22 m-7). **Re-pin (R23-5):** ScopeOfWork.md sha256 2e134b572f2676ed4fe6daa892047e21e53a637f9901cba20f482a6637f7f3d3 (SCA-V4-003 revision), was baf68c79b5b8fdf01300fc255d7cf8e433975e6275daadf67b914b4e51eca4a6. Blocks read: G-0105-01…16 (`SOW_REVISIONS_A.md` of run `APP-V4-SCA003-20261002`, sha256 42c9167a…fc07). Bearing: G-0105-02 (CLM-004: DEL-09-02 receives the account/provider inputs and focused checks), recorded by the §13 row. The other blocks carry into the ScopeOfWork what this file already designs (CLM-001, TBD-001, REQ-005: the decision record and item 6 below; REQ-002: §4; REQ-004, AC-004, VER-004: §5.4; OUT-002, REQ-010, AC-011, VER-011 and the matrix row: §8, §9; TBD-002: §10; TBD-003: item 2 below; AX-006 is the amendment reference), so none requires a change to the design text. "How this file reads the ScopeOfWork" below describes the ScopeOfWork before SCA-V4-003.
- Produced by: node D4 of run `APP-V4-DESIGN-PASS-3-20261001` (Type 2 TASK,
  Claude Opus 5.5, high effort; does not delegate): v0.1 on 2026-10-01 at
  repository HEAD `dc031b5bec`; v0.2 (D round 2) on 2026-10-02 at HEAD
  `037063ce09`.
- Companion record: [ACCOUNT_HOME_DECISION_RECORD.md](ACCOUNT_HOME_DECISION_RECORD.md)
  (OUT-003, REQ-005; the K-1 decision and its mechanism). Schemas beside this
  file (§15); prototype under [`prototype/`](prototype/) (§16).
- **Hard limit observed in producing this file (both rounds):** no sign-in,
  no API key and no token was entered, created or read by anyone; no Codex
  process and no model was run; no network was used. The 0.158.0 vendor binary was read as
  bytes with `strings` (as HOSTING F-28 did), never executed.
- Serves: OUT-001, OUT-002, OUT-003 (API-key definition record, §10),
  OUT-004 (designed method and the DEL-05-01 handoff, §11–§12); REQ-001…REQ-009
  as designs; designed cases for VER-001…VER-010.

**Basis (binding, by bytes read with `shasum -a 256`).** Accepted basis as
amended by SCA-V4-001 and SCA-V4-002: `docs/PRD.md` bb6e786f…49bd
(V4-APP-02), `docs/ARCHITECTURE.md` 317d5789…828c (V4-ARC-04, §3 "Left to
the implementation session", §6), `docs/EXAMINATION.md` 471798bc…d0
(V4-EXM-12). ScopeOfWork.md 2e134b572f2676ed…d3 (SCA-V4-003 revision; re-pinned at pass-4 closeout C2 under R23-5, was
`baf68c79b5b8fdf0…a6`, unchanged from initialization until SCA-V4-003; blocks read: see the pass-4 header line). Run records under
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

**Round-2 basis (binding; sha256 first 16 hex, recomputed 2026-10-02).**
`BRIEFS.md` 316ea29325a0d450 ("D round 2"); `OWNER_DECISIONS.md`
ea96c55710af41c9 (DECISION-L L-1…L-7; the "Sign in with ChatGPT" exchange);
`R18_RESOLUTIONS.md` abf5eee6324647ff (R18-1 C-10, C-20, C-23; R18-2;
R18-3; R18-6; R18-7 G-1; R18-9); `R19_RESOLUTIONS.md` 16930ecdcead7511
(R19-4, R19-5; R19-7 for skill roots); `ASSESSMENT_SIWC.md`
cc7e64c099021846 (with its addendum and correction);
`F/F0_JOINS.md` e93608be1c6e3eb0 (§2, §6, §7.4; rows FH-10…FH-32, FE-20,
FR-12, FL-01, FL-02); `DECISIONS_PENDING_2.md` 0ecbf87aae8d4350 (the L-n
option texts). Observation records in DEL-01-01/Design, read, not edited:
`OBS_2_0.158.0.md` 61cc34ffb811eb27 (§2, §9 O-6, §10 O-7, §11, §13,
UNRESOLVED) and `OBS_3_0.158.0.md` 554ac4451d112824 (skill roots and the
advertising side effect, W-1).

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
standing) and `inference`. Round 2 adds `observed (OBS-2 O-n)` for the
credential-free observations of 2026-10-01 and `observed through an adapter
(OBS-2), not stock behaviour` (R18-9). No cell is left "OBS-2 pending"; the
cells v0.1 marked so are filled or say why they stay open (§18).

**Version rule (R19-5).** Every supplier fact in this file is a fact **at
Codex 0.158.0** (the definition pin), whether or not the sentence repeats
the version; a fact at another version names it. Where Codex reports a
capability at run time, the App reads it rather than inferring it from the
version (§18 lists the reads and the version-bound statements a version
advance must recheck).

**How this file reads the ScopeOfWork (R17-15).** The SoW lags the owner's
answers in six places; the design follows the answers and the return file
lists the proposals for SCA-V4-003:

1. TBD-001/REQ-005: OI-009 is decided at choice level by DECISION-K3 K-1
   (shared settings, separate sign-in custodied by Codex); the mechanism is
   observed to work at 0.158.0 (OBS-2 O-6 M1; decision record).
2. TBD-003: "the unidentified supplier pin" — 0.158.0 is the
   definition/generation pin (DECISION-1 D4); qualification stays under
   OI-012.
3. REQ-004 states no default rule; K-3 adds "no model chosen until the person
   chooses" for the App (§5.4).
4. Start-up traffic (K-12) has no SoW item; HOSTING U-18 names "Owner with
   DEL-01-05" (§9).
5. K1-4's "Codex account when Codex reports one" is a supply this file makes
   to the act record (§8); no SoW line names it.
6. REQ-005 names "the Owner with the App implementation owner". This file
   reads it as **"the Owner, who is also the App implementation owner
   (DECISION-L L-7)"** (R19-4).

## Changes from v0.1

| Ruling / item | Where | Change |
|---|---|---|
| DECISION-L L-1 (A); R19-4; R18-1 C-20 | §2, §4, §17 F-A1, UNRESOLVED | K2-1 **adopted** by the owner; "pending owner" removed; U-A1 closed. One Codex process per App-owned home; generation identity {App session, App home, spawn counter} |
| DECISION-L L-3 (A); R19-4; OBS-2 O-7 | §6 Q-1, §9, schema `access.network-observation`, prototype VC-A19 | Plugins follow the person's own setting: on → the two start-up connections happen and are shown and recorded; off → the App's Codex runs with `plugins = false` and they stop. Under the link the person's file already carries the setting; the App adds a session flag only in the fallback (own configuration) |
| R18-3 (C-25); OBS-2 O-7 | §9, U-A9 | The internal environment variable is not used. The remote-control loop is shown as observed at 0.158.0: no connection without sign-in; with sign-in not observed. `remote_control` dropped as a candidate setting (a `removed` feature with no effect) |
| R18-6 (C-18) | §3; decision record §4.1 | The person's global `AGENTS.md` and `skills/` are linked into each App home like `config.toml`; the App writes nothing into the linked skills root (R19-7) |
| R18-1 C-10 | §1 I-6, §8; schema `access.state` | The Codex account is supplied as the reported email, or "ChatGPT account (no email reported)"; plan type is shown, not recorded |
| R18-2 (C-09) | §5.4 CS-1/CS-2, schema `access.conversation-selection`, prototype VC-A20 | "not started — no model selected" for an ordinary conversation; "run not started — no model selected" when the message would start a workflow run |
| DECISION-L L-6 (A) | §10, UNRESOLVED U-A2 | No sign-in or API-key observation now; the account cells stay labelled as resting on the protocol types; OI-010 stays OPEN |
| DECISION-L L-7 (A); R19-4 | Header reading 6; decision record §3 | REQ-005 reading; U-A11 closed |
| R18-7 G-1; F0 FH-19 | New §19 | Receiving comparison for seam S-4 |
| R19-4 SIWC; ASSESSMENT_SIWC.md | New §20; §11 CH-8 | The ChatGPT plan grant recorded as an alternative considered, with four triggers and the dependency notes; the host-billing point on the next-relay list |
| R19-5 | Header "Version rule"; new §18 | Supplier facts name their version; runtime reads listed; version-bound statements listed for the version-advance check |
| OBS-2 O-6 (M1, M2, M3) | §3, §5.5, §6 Q-1, decision record §4 | Linked configuration observed to work; `-c` flags form the `sessionFlags` layer; `--profile` refused for `app-server`; fallback A not needed at 0.158.0; writes through the link still not observed |
| OBS-2 §11, §13; F0 FH-26 | §9, §7 | The installation id and thread/session/turn ids in `client_metadata`, and the host time zone in every model input, are shown in the network/record view as content sent to the chosen provider |
| OBS-2 O-4 (adapter) | §11 CH-2 | The delegation tools also travel in the `namespace` tool LM Studio 0.4.16 drops (R18-9 standing) |
| RV21 (repairs from V21; in place, no version step): V21-A MINOR 10, 11 | §1 (runtime-value paragraph); §5.1 AE-12; §5.2 KE-13; §6 Q-5, Q-7, Q-11 | **MINOR 10:** sign-out and key removal ask first with DEL-01-02's **`assess live work`** (RECOVERY-v0.2 §4.1; R18-1 C-23), which returns the live turns, the outstanding requests and the active delegated children of the home, as a runtime value (no row); all three are listed. **MINOR 11:** resume overrides nothing on `thread/resume`; a model change is per turn (CS-18), one rule with RECOVERY-v0.2 §4.1 and ROLE-v0.2 §5.5 |
| Naming | §6 Q-2 | The control reads "Sign in with your ChatGPT account (through Codex)", so it is not confused with OpenAI's separate "Sign in with ChatGPT" grant (§20) |
| C0 (closeout; in place, no version step): V21b-A N-1 (V21-B m-3, ACCESS side) | §20 "Decision record" | The SIWC arrangement (no pressing need; alternative considered with its triggers; host-billing point on the next-relay list) is attributed as HELP_HUMAN's recommendation, not separately answered by the owner and not objected to, as OWNER_DECISIONS (sha256 prefix `8a5d11149045770d`) now reads; "was accepted with L-1 and L-6" removed. Substance unchanged: not adopted. Prototype rerun 2026-10-02: `run_cases.py` TOTAL 9, FAIL 0 (run `APP-V4-DESIGN-PASS-3-20261001` `closeout/C0.md`) |

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
| I-6 | Observed Codex account of the home that runs the conversation, as RS `codexAccount`: the reported email, or "ChatGPT account (no email reported)" (R18-1 C-10); plan type is not part of it | DEL-01-05 → DEL-01-04 CAP-8 / RS §6.1 (K1-4); HOSTING `actorRef` is derived from the same value | At act capture | No account or `apiKey` kind → no Codex-account element; never a guessed name |
| I-7 | Start-up network view (schema `access.network-observation`) | DEL-01-05 → the person; App diagnostics record | App start; on demand | Observation unavailable → the view says so; the per-pin expected list is still shown, labelled |
| I-8 | Local-server capability requirements and limits (schema `access.capability-handoff`) | DEL-01-05 → DEL-05-01 (DEP-01-05-014) | When DEL-05-01 receives | — |
| I-9 | Account/provider inputs and the focused sign-in and concurrent-mode checks | DEL-01-05 → DEL-09-02 (DEP-09-02-013) | Before V4-EXM-12 | — |
| I-10 | Selected pin and embedding qualification input; sign-in and substitution evidence "when needed" | DEL-01-01 ↔ DEL-01-05 (DEP-01-05-012/013; DEP-01-01-022/024; held, SCC-001) | Held arcs gate nothing | — |

A runtime value DEL-01-05 is handed is not a production input (R17-10
pattern): the live work listed by §6 Q-5 and Q-7 comes from DEL-01-02's
**`assess live work`** operation (RECOVERY-v0.2 §4.1; R18-1 C-23: the live
turns, the outstanding requests and the active delegated children of the
homes named, K-4's pattern), read at run time; no row DEL-01-05 → DEL-01-02 is proposed
(it would put DEL-01-02 into SCC-001; the return file shows the check).

## 2. Access entries

An **access entry** is one way a conversation can reach a model, kept
configured beside the others (REQ-004). The App lists them; the person picks
one per conversation (K-2, SETTLED).

| Kind | What it is | Codex home that serves it (§3) | Provider at `thread/start` | Credential and custody | Destination class (RS R5 enum) |
|---|---|---|---|---|---|
| `chatgpt-account` | The ChatGPT sign-in, which is **the Codex account** of the App's account home (K-2) | H-acct | The built-in OpenAI provider (`inference`: id `openai`; the effective id is read back from the `thread/start` response, HOSTING §8.3) | Codex's credential store of H-acct (V4-ARC-04) | `user-chosen cloud` |
| `api-key` | The API key, **a separate entry** (K-2) | H-key, a second App-owned home whose Codex account is the key (§4, K2-1, adopted by DECISION-L L-1) | As above, in H-key | Codex's credential store of H-key | `user-chosen cloud` |
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

The decision record's mechanism M-A, **observed to work at 0.158.0** (OBS-2
O-6 M1: a second home whose `config.toml` is a symbolic link to the first's
reads the first's values, the user layer is named by the second home's path,
and `account/read` in the second home returns `account: null`; no credential
existed anywhere). Under R18-6 the person's global `AGENTS.md` and `skills/`
are linked the same way (PROPOSED; not observed through a link).

| Home | Owner | Holds | Shared with the person's other Codex clients |
|---|---|---|---|
| The person's Codex home (`$CODEX_HOME` of their shell, usually `~/.codex`) | The person | Their `config.toml` (settings, providers, MCP servers, features including `plugins`), global `AGENTS.md`, `skills/`, and their own sign-in | It is theirs. The App reads it through the links and writes only `config.toml`, only on the person's act (I-2) |
| H-acct, the App's account home (App data folder) | The App | The App's own sign-in (Codex custody), threads, logs and state of the App's Codex; `config.toml`, `AGENTS.md` and `skills/` **are links** to the person's | Configuration, global guidance and skills, through the links |
| H-key, the App's key home (App data folder; created only when the person adds a key; DECISION-L L-1) | The App | The API key (Codex custody); threads of API-key conversations; the same three links | As H-acct |
| H-probe, the probe home (App data folder) | The App | What the version-label probe writes (S-F-17: `tmp/arg0/…`) | Nothing; no links; never an account home (answers HOSTING §7.2) |

**One Codex process per App-owned account home** (DECISION-L L-1 A; R19-4):
H-acct always, H-key while a key exists. DEL-01-02's stop, restart and quit
apply to each (its DEF-5/DEF-6). Generation identity is {App session, App
home, spawn counter} (R18-1 C-20; R19-4).

**The App writes nothing into a linked `skills/`** (R19-7: workflows are
not placed in any discovered skill root by the App). OBS-3 observed that at
0.158.0 every discovered skill in `$CODEX_HOME/skills` is advertised in the
developer block of every model request in that home; with the link, the
person's own skills are advertised in App conversations exactly as in their
Codex (F-A9). `instructionSources` on thread start records which guidance
files Codex reports (R18-6); OBS-2 saw only `[]` (no `AGENTS.md` in its
working folders), so whether Codex follows a linked global `AGENTS.md` is
not observed (U-A14).

The fallback (option A, each App home with its own configuration) is not
needed at 0.158.0 (O-6). It stays defined for a later version whose
`config/read` shows the link no longer read (CL-3; §18 version-bound list).

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
| K2-1 | A second App-owned home H-key whose Codex account is the key (`account/login/start {apiKey}` in H-key); API-key conversations run on H-key's child | Codex (V4-ARC-04 held) | Yes: H-acct keeps the ChatGPT sign-in | Two supplier children: **HOSTING U-12 gains a per-home dimension** (generation, register and thread keyed by home); two start-ups, so K-12 traffic per home; conversation lists merged from two homes | **ADOPTED** by the owner (DECISION-L L-1 A, 2026-10-02). The only mechanism that keeps Codex custody of both credentials at 0.158.0 on the generated types |
| K2-2 | Provider entry with `env_key`; the App supplies the key in the child's environment from its own keychain item | The App (and every descendant process environment the supplier does not filter, `inference`) | Yes | Contradicts "credentials held by Codex" | Set aside unless the owner changes V4-ARC-04 |
| K2-3 | Provider entry with `experimental_bearer_token` in a configuration layer | A plaintext configuration file; in the shared file (K-1) it would leak into the person's CLI configuration | Yes | Key in a file the person shares | Set aside |
| K2-4 | Provider entry with a command-backed `auth` element (shape not in the types) | Whatever the command reads (an OS keychain item the App wrote) | Yes | Shape unknown at 0.158.0 (`strings-in-binary` only) | Not available until observed; App custody at entry |
| K2-5 | Re-login per conversation in one home | Codex | **No**: logging in with one replaces the other (`inference` from the single `Account`); live threads of the other mode affected (not observed) | Breaks REQ-004 | Set aside |
| K2-6 | One home holding both, chosen per thread | Codex | — | No element in the generated types selects an account per thread | Not available at 0.158.0 |

**Standing.** The owner adopted K2-1 (DECISION-L L-1 A). Its premise,
one account per Codex process, rests on the generated types at 0.158.0 and
is `inference` until observed with a credential; DECISION-L L-6 (A) defers
that observation ("not now"), so the premise stays labelled. OBS-2's remark
that K-2 "needs no second home for configuration" (O-6) is true and beside
the point: the second home exists for the second credential, not for
settings. HOSTING records the per-home dimension of U-12 (R19-4; F0 FH-31);
this file does not restructure HOSTING.

**Version-bound (R19-5).** If a later Codex offers a per-thread account or a
provider credential that Codex itself holds, K2-1 is re-examined at that
version advance (§18); nothing in §5.4 or §7 depends on the number of homes.

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
| AE-12 | signed-in | `person:sign-out` | signing-out | Asks first when H-acct has live work, listing its live turns, outstanding requests and active delegated children (RECOVERY `assess live work`; K-4 pattern) |
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
| KE-13 | present | `person:remove-key` | removing | `account/logout` in H-key; asks first with live work (RECOVERY `assess live work`, as AE-12) |
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
for that project, shown as such, never applied silently. **Wording (R18-2,
C-09):** an ordinary conversation reads "not started — no model selected";
a message that would start a workflow run (R19-2: a run starts with a turn)
reads "run not started — no model selected" (R15-1). The App knows which
from whether a workflow is selected for that turn.

| ID | From | Event | To | Effect and record |
|---|---|---|---|---|
| CS-1 | no-selection | `person:message` | no-selection | Refused: "not started — no model selected", or "run not started — no model selected" when a workflow is selected for the turn (R18-2); the message stays as a draft; nothing is sent |
| CS-2 | offer-shown | `person:message` | offer-shown | Same refusal and wording rule; **the offer is not applied** |
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
`own-config` (option A for settings). One machine per linked file
(`config.toml`, `AGENTS.md`, `skills/`) per App home. Observed at 0.158.0:
reading through the `config.toml` link (CL-1, O-6 M1). Not observed: writes
through it (CL-10, CL-4; OBS-2 UNRESOLVED), and reading through the other two
links (U-A14).

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
   App's session flags (§9: `analytics.enabled = false`; `plugins = false`
   only in the fallback when the person's setting is off), carried as `-c`
   flags, which `app-server` accepts and forms into the `sessionFlags` layer
   (observed, OBS-2 O-6 M2), never the internal environment variable
   `CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED` (R18-3), and the declared capability
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
1. Person chooses "Sign in with your ChatGPT account (through Codex)" (not
   OpenAI's separate "Sign in with ChatGPT" grant, §20). If a sign-in is already pending on
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

**Q-5 Sign out (person's act).** The App calls DEL-01-02's `assess live work`
for H-acct (RECOVERY-v0.2 §4.1; runtime value, C-23); with live turns,
outstanding requests or active delegated children it asks first, listing all
three; the person may cancel. `account/logout`
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
if any and a free model identifier field (U-A7: outside OBS-2's items, so it
stays open).

**Q-10 Start.** CS-8…CS-11. Requested values recorded per HOSTING §8.3;
destination class from §2.

**Q-11 Resume.** The conversation resumes on the home that holds its thread
with its entry unchanged, and `thread/resume` carries no override (RV21: one
rule with RECOVERY-v0.2 §4.1 and ROLE-v0.2 §5.5); a model the person
chooses afterwards is sent per turn (CS-18). Changing entry is not offered at v0.1 (CS-19):
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
  source; form INTEGRATION by R18-1 C-10):** at act capture DEL-01-04
  receives from this file the account of **the home that runs the
  conversation**, as last read, in RS's `codexAccount` form: the reported
  `email`, or the text "ChatGPT account (no email reported)" when Codex
  reports a ChatGPT account with a null email. For an `apiKey` account and
  for no account there is no Codex-account element. Plan type is shown in the
  account view and **not recorded**. HOSTING's `actorRef` string is derived
  from the same value. Labelled App-observed, "identity not verified" (K1-4).
  Whether a record keeps the email or a digest of it stays RS's (U-A8).

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

**Which is which, at Codex 0.158.0 (OBS-2 O-7, observed 2026-10-01 without
sign-in; DECISION-L L-3; R18-3):**

| Start-up traffic | What stops it at 0.158.0 | App action | Standing |
|---|---|---|---|
| Featured-plugins request to chatgpt.com (401 without sign-in) | `[features] plugins = false` (O-7 v1, v6–v8) | **Follows the person's plugin setting** (L-3 A): plugins on → happens, shown and recorded; plugins off → does not happen. Under the link the person's own file carries the setting, so the App adds nothing; in the fallback (own configuration) the App passes `plugins = false` as a session flag when the person's setting is off | `observed (OBS-2 O-7)` |
| Plugin repository check or fetch, `github.com/openai/plugins` (`ls-remote` warm; ≈24 MB fetch on a fresh home) | `[features] plugins = false` (v1, v8: no `.tmp/` created on a cold home) | As above (L-3 A) | `observed (OBS-2 O-7)` |
| Remote-control loop for `chatgpt.com/backend-api/` | No configuration key: `remote_control` is a `removed` feature with no effect (v5); `remote_plugin`, `apps`, `tool_suggest` have none (v2, v3, v6). Only the internal environment variable `CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED=1` stops it (v4) | **Not turned off** (R18-3: an internal variable is not a setting). Shown as observed: without sign-in the loop retries locally about once a second and opens **no socket**; `remoteControl/status/changed` reported `disabled` at start. With a sign-in: not observed (DECISION-L L-6) | `observed (OBS-2 O-7)`; signed-in behaviour not observed |
| Analytics | `[analytics] enabled = false` (`AnalyticsConfig`, generated types) | Set off in the session flags (K-12) | Every OBS run had it off; no analytics connection was seen, so its effect when on is not observed |
| Update check | `check_for_update_on_startup` (`strings-in-binary`) | **Not set**: O-7 did not test it, and an unknown key is not sent (U-A13) | Not observed |
| Model traffic of a conversation | The person's entry | Not turned off: the chosen destination; shown with its class | HOSTING §8.3 |
| Sign-in endpoints during Q-2/Q-3 | — | Not turned off; shown as "sign-in" while pending | `inference` (LOOP N-OPEN-2 is the host counterpart) |

**Reading the person's plugin setting (L-3; R19-5 runtime read).** The App
reads it at run time, not from the version: `config/read {includeLayers:
true}` shows `features.plugins` and the layer that set it when it is set
(OBS-2: `features` appear only when set), and `experimentalFeature/list`
(stable, `observed-in-generated-types`) reports a feature's `enabled` in the
loaded configuration and its `defaultEnabled`; whether it lists `plugins`
is not observed (U-A15). With neither, the App takes the setting as **on**,
because Codex 0.158.0 made both connections with no setting (O-7 v0), and
labels the view "plugins on by Codex's default (observed at 0.158.0)". The network view states "Plugins are on in
your Codex settings, so Codex contacts chatgpt.com and github.com at start"
or "Plugins are off in your Codex settings; Codex made no start-up
connection" and the record carries the same (schema `pluginsSetting`).

**Carrier.** The App's own settings (analytics off; `plugins = false` in the
fallback only) go in the session-flags layer of the App's own child, never
into the person's configuration file, and are recorded in HOSTING's
configuration identity (§7.1). They change only the App's Codex. Whether the
person may turn analytics back on for the App remains U-A9 (Root `AGENTS.md`:
the App does not "veto the user's Codex configuration").

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

**Content sent to the chosen provider (OBS-2 §11; F0 FH-26).** At 0.158.0
every model request's `client_metadata` carries the Codex installation id
and thread, session and turn identifiers, and every model input carries the
host's time zone (observed to a loopback provider). The network view and the
App's record show these as content sent to the conversation's provider, for
local and cloud entries alike; the App does not alter them (stock supplier,
H1).

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
H-key: the API key; K2-1 adopted, DECISION-L L-1). **OI-010 remains OPEN**:
AK-5, AK-6's storage effect and AK-10 need an observation with a key, and the
owner chose not to observe sign-in or API-key flows now (DECISION-L L-6 A),
so these rows stay labelled as resting on the protocol types at 0.158.0; the
question returns at the phase review if the design needs it.

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
fixture `prototype/fixtures/capability-handoff.valid.json` is its v0.2
content).** Items, each with standing, all at Codex 0.158.0 unless named:

| ID | Statement | Interface | Standing | What it means for a host loop |
|---|---|---|---|---|
| CH-1 | The App reaches a local model through Codex's provider interface, Responses (`wire_api = "responses"`); Chat Completions is refused by 0.158.0 for providers | App Codex provider | Responses at one pair `observed` (OB-8); refusal of `chat` `strings-in-binary` (F-28) | None directly: the host loop uses Chat Completions (V4-ARC-10, LOOP §1); a server serving both does not join them |
| CH-2 | LM Studio 0.4.16 dropped `namespace` tools on Responses; MCP tools did not reach the model; the delegation tools travel in the same `namespace` tool, so delegation does not reach an LM Studio model either | App Codex provider | `observed` at one pair (OB-1; F-31); delegation part `observed (OBS-2 O-4)`, reached only through an adapter, not stock behaviour (R18-9) | Not a Chat Completions finding; LOOP's FB-CC-1 stands |
| CH-3 | A flat function tool was called through Responses at that pair | App Codex provider | `observed` (OB-2) | — |
| CH-4 | The server ignored `prompt_cache_key` and `include`, turned the developer role into system | App Codex provider | `observed` (OB-8) | The host may see the same server behaviour on its own route; to be checked on Chat Completions |
| CH-5 | Codex put the host's IANA time zone into the model context | App Codex provider | `observed` (OB-11) | Not a host matter; recorded |
| CH-6 | Credentials of the App's providers are Codex's; host credentials and endpoints are the host native layer's (LOOP NW-3, NW-6) | Both | SETTLED (V4-ARC-04, V4-ARC-12) | No App credential or provider configuration is shared with a host |
| CH-7 | No host conformance is claimed from App observations | Both | SETTLED (SoW AC-009; AX-003) | — |
| CH-8 | ChatGPT plan billing through OpenAI's "Sign in with ChatGPT" grant is Responses-only (published preview, read 2026-10-01) | Host loop | `published-only` (ASSESSMENT_SIWC.md) | **Next-relay item, not a requirement:** a host could use plan billing only if its model-interface boundary (R12-11) admits a Responses provider; host joins stay deferred (DECISION-3; R19-4) |

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
| DEP-01-05-017 (DAG-004: mirror of DEP-09-02-013, which represents the arc, SR-6) | Downstream | DEL-09-02: account/provider inputs and the focused sign-in and concurrent-mode checks for V4-EXM-12; the witness stays with DEL-09-02 | I-9; VC-A01…A05. The supplier-side counterpart of DEP-09-02-013, from CLM-004 as revised by SCA-V4-003 G-0105-02 (ledger R3-01-05-b; R22-7; V22 m-7) |
| (none yet; F0 §3 NR-07) | DEL-01-04 would consume | Access state for the start display; Codex account for CAP-8 | I-5, I-6; new row proposed (SCC-neutral: DEL-01-05 reaches only DEL-01-01) |

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
| [`access.state.schema.json`](access.state.schema.json) | DEL-01-04 (I-5); the App's settings view | Homes with link state; entries with kind, state, provider, class, account view and the RS `codexAccount` string (C-10); never a credential element (closed objects) |
| [`access.conversation-selection.schema.json`](access.conversation-selection.schema.json) | DEL-01-04 (I-5); DEL-01-01 S-4 (I-3); DEL-04-03 via §8.3 (I-4) | State per §5.4; selection with source; an offer that is never a selection; thread with requested and reported values; refusal reasons |
| [`access.network-observation.schema.json`](access.network-observation.schema.json) | The person (I-7); App diagnostics | The person's plugin setting and its source (L-3); rows with destination, process, phase, purpose, sources (`app-observed`, `expected-at-pin`), the setting's state (following the person, turned off by the App, or no setting) and the standing with its version; the lower-bound limit |
| [`access.capability-handoff.schema.json`](access.capability-handoff.schema.json) | DEL-05-01 (I-8) | Items with interface, standing and host meaning; `noHostConformanceClaimed: true` |

Valid and invalid instances: `prototype/fixtures/*.valid.json`,
`*.invalid.json` (each file holds a `description` and the `instance`). Each
invalid instance's description names the one reason it must fail, and the
run shows it failing for that reason (VC-A17).

## 16. Prototype (R17-1; R12-3)

[`prototype/`](prototype/), Python 3 standard library only, no install, no
network, no Codex. `access_model.py` holds the §5 tables, the selection,
routing, custody, link, plugin-setting and network-view models;
`run_cases.py` runs VC-A11…VC-A17, VC-A19 and VC-A20 (with the schema
checks); `jsonschema_subset.py` is a byte-identical copy
of DEL-01-01's validator (sha256 486e9286…c0ffc0). The link and probe-home
cases use a temporary folder under `$TMPDIR` with invented content, check
that no path outside it (and nothing under `~/.codex`) is touched, and remove
it. Custody is tested with invented canary strings that are not shaped like
any key, token, URL or code. Command: `cd prototype &&
PYTHONDONTWRITEBYTECODE=1 python3 run_cases.py`. v0.1 ran 2026-10-01 (TOTAL
7, FAIL 0; `prototype/results/RUN_2026-10-01.txt`, kept as history). **v0.2
ran 2026-10-02 (UTC), Python 3.13.7, macOS Darwin 25.6.0 arm64: TOTAL 9,
FAIL 0**; the output and the sha256 of every input are in
`prototype/results/RUN_2026-10-02.txt`, which pins this file's bytes before
the §20 trigger correction (sha256 75bafd81…6339; §5 tables unchanged since,
so nothing was rerun). A
"pass (model)" is evidence that the rules run as written, never a VER pass.

## 17. Findings

- **F-A1 Two homes for two cloud credentials (adopted).** At 0.158.0 a Codex
  process has one account and no per-thread account element, so a ChatGPT
  sign-in and an API key kept side by side with Codex custody need two
  App-owned Codex homes (K2-1). The owner adopted it (DECISION-L L-1 A);
  HOSTING U-12 gains a per-home dimension (R19-4). Premise `inference` from
  generated types; not observed (L-6).
- **F-A2 Capabilities are not per provider.**
  `modelProvider/capabilities/read` takes no parameters at 0.158.0, so
  `namespaceTools` (the F-31 element) cannot be read per entry without
  observing which provider it describes (U-A7).
- **F-A3 Writes through a linked configuration.** A write that replaces the
  file at the link path breaks the link silently; writes therefore pass the
  resolved target as `filePath`, and the link is checked after each write
  (VC-A11). OBS-2 confirmed reads through the link and that no case wrote
  through it; how Codex writes (in place or by replacement) is still not
  observed.
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
- **F-A8 Following the person's plugin setting costs nothing under the
  link (round 2).** Because the App home reads the person's `config.toml`,
  Codex applies their `[features] plugins` value itself; the App needs a
  session flag only in the fallback. L-3 is met by K-1's mechanism.
- **F-A9 Linked skills are advertised in every request (round 2).** OBS-3
  observed at 0.158.0 that each discovered skill is listed in the developer
  block of every model request in that home. Linking the person's `skills/`
  (R18-6) therefore puts their skills' names and descriptions into App
  conversations' context, as in their own Codex; and the App must not put
  registered workflows there (R19-7).
- **F-A10 Three encodings of one identity reduced to one (round 2).** RS's
  `codexAccount` string is the single form (R18-1 C-10); HOSTING's
  `actorRef` is derived from it.

## 18. Version standing and runtime reads (R19-5)

**Runtime reads the App uses instead of version inference:**

| Fact | Runtime read (0.158.0 method; stable unless marked) | Used in |
|---|---|---|
| Login methods allowed; credential store mode | `configRequirements/read` (`allowedLoginMethods`, `cliAuthCredentialsStore`) | §5.1 AE-4, §5.2 KE-3, CR-10 |
| Account kind and email | `account/read` | §5.1, §5.2, §8 |
| Effective configuration and its layers (link working; plugins setting; providers) | `config/read {includeLayers: true}` | §3, §5.3, §5.5, §9 |
| Feature enablement and default | `experimentalFeature/list` (`enabled`, `defaultEnabled`) | §9 (plugins) |
| Remote-control state | `remoteControl/status/changed` notification (the read method is experimental-only) | §9 |
| Models of an entry's home | `model/list` | Q-9 |
| Provider capabilities | `modelProvider/capabilities/read` (no parameters; provider not known, U-A7) | LP-2 |
| Discovered skills | `skills/list` | §3 (linked skills) |
| Guidance files Codex loaded | `instructionSources` in the `thread/start` response | §3 |
| Supplier version | Version label and `userAgent` (HOSTING §7) | Every row below |

**Version-bound statements (recheck at each version advance; R19-5's
proposed version-advance check):** one account per Codex process (§4, F-A1);
`app-server` accepts `-c` as the `sessionFlags` layer and refuses
`--profile` (O-6 M2, M3); a linked `config.toml` is read as the user layer
(O-6 M1); `plugins = false` stops the featured-plugins request and the
plugin repository check (O-7); no setting stops the remote-control loop, which
opens no socket without sign-in (O-7); `thread/resume` overrides are ignored
(O-5; Q-11); `wire_api = "chat"` refused (F-28); `explicitGatewayOauth`
semantics (F-A4); `modelProvider/capabilities/read` without parameters
(F-A2); the redaction field names of CR-2; the account and login variants of
§10; skills advertised per request (F-A9). The network view's expected list
is per version (§9).

## 19. Receiving comparison for seam S-4 (R18-7 G-1; HOSTING F-15)

HOSTING-v0.8 §8 S-4 names what the boundary supplies to DEL-01-05 and what it
does not. This is the receiving side, row for row, at 0.158.0.

| S-4 supplied (HOSTING §8) | Received here as | Verdict | F row |
|---|---|---|---|
| Carriage of supplier account methods | I-1; §5.1, §5.2; Q-1…Q-7; CR-1…CR-10 | Received; needs the §9.1 redaction categories (CR-2) | FH-26 |
| Per-conversation provider selection: `modelProvider` on thread start | I-3; CS-8 (explicit provider and model always) | Received | FH-25 |
| `modelProvider` on thread resume | Not used (Q-11: entry fixed for the conversation; resume overrides ignored at 0.158.0, O-5) | Not used, by design | — |
| `modelProvider/capabilities/read` | Not used per entry (LP-2, F-A2) | Received with a limit (U-A7) | — |
| Observed model destination per thread/turn (§8.3) | DEL-01-05 supplies the class (§2, I-4); the per-turn facts go to DEL-04-03 and are shown, not consumed | Matches; DEL-01-05 is the class's source | FH-25 |
| §8.1 account L-1…L-6 | §11 LP-1…LP-3, CH-1…CH-8 | Received and handed on to DEL-05-01 | FH-32, FL-01, FL-02 |
| Recorded-exchange evidence per §9 | §12 method; CR-2 redaction | Received; redaction categories added | FH-26 |
| The fresh-home network observation (L-4) | §9 (O-7 table; two-source view) | Received; filled by O-7 | FH-27, FH-29 |

| S-4 not supplied (HOSTING §8) | Where DEL-01-05 supplies it |
|---|---|
| Sign-in (including OAuth) and API-key flows, no default between local and cloud | §5.1, §5.2, §5.4 (K-3), Q-2…Q-7 |
| Account home (OI-009) | Decision record (option C, M-A observed) |
| Provider configuration | §5.3, Q-8 |
| Server-substitution checks | §12, VC-A08 |

**Needed of HOSTING beyond S-4's text (F's rows):** one child per App-owned
account home and generation identity {App session, App home, spawn counter}
(U-12; FH-06, FH-31); `CODEX_HOME` per home, the links, and the App's session
flags in the spawn and in the configuration identity (FH-10, FH-12, FH-14);
`explicitGatewayOauth: true` declared (FH-11); a separate probe home (FH-13);
`account/chatgptAuthTokens/refresh` known-app-unsupported (FH-15); the flows
offered (FH-24); the process set of each child for the App's socket sampling
(H11; a runtime value). **Result:** S-4 has a receiving side; F-15 can close
for S-4, citing ACCESS-v0.2 §19.

## 20. Alternative considered: the ChatGPT plan grant ("Sign in with ChatGPT")

**What it is (published preview, read by HELP_HUMAN on 2026-10-01;
ASSESSMENT_SIWC.md).** OpenAI's "Sign in with ChatGPT" lets an app obtain an
OAuth grant to use the person's ChatGPT plan (Plus and Pro) for Responses
API requests, with a per-app cap and disconnect in ChatGPT settings. For
open-source, locally hosted apps the app registers dynamically, runs its own
loopback OAuth client with PKCE and **stores the tokens itself** (access 1 h,
rotating refresh 30 d). The documented Codex route puts the access token in
the child's environment behind a custom Responses provider (`env_key`,
`requires_openai_auth = false`) and restarts app-server at each renewal.
Preview limits: no hosted tools; configurations that emit `tool_search` fail.
This is distinct from the App's Q-2 control, which signs in to **Codex's own
ChatGPT account** (renamed in v0.2 to avoid the confusion).

**Decision record.** Not adopted. After the assessment the owner asked:
"Well, there's no pressing need to go ahead with this alternative sign-in or
do you see any?" HELP_HUMAN's recommendation (no pressing need; DEL-01-05
records it as an alternative considered, with its triggers; the host-billing
point goes on the next-relay list) is HELP_HUMAN's recommendation, which the
owner did not separately answer and did not object to; L-1 and L-6 were
answered A ("I will go with your recommendations for the other six";
HELP_HUMAN's reading in OWNER_DECISIONS, "Sign in with ChatGPT" exchange, as
corrected after V21-B m-3). Reasons, from the assessment: it moves
custody to the App, against V4-ARC-04 and D-GOV-43's "custodied by Codex"
(K2-2's objection again); the documented route restarts Codex hourly, which
interrupts live turns and drops pending requests (OBS-2 O-2); it is a
preview, not versioned or pinned; Chirality's eligibility for the open-source
route is not established; it adds a second runtime supplier with no supplier
contract here.

**Triggers for reopening it (the four given to the owner on 2026-10-02;
recorded in ASSESSMENT_SIWC.md "The four triggers", sha256 4dfa320249b01a59…;
R19-4).** Any one of these would make the plan grant pressing:

| ID | Trigger |
|---|---|
| T-1 | OpenAI restricts third-party apps from using Codex's own ChatGPT sign-in and points them to Sign in with ChatGPT |
| T-2 | The owner wants a per-app usage cap and a "Chirality" entry in ChatGPT settings as product features |
| T-3 | A host needs plan billing when host joins resume (CH-8) |
| T-4 | The owner decides records should carry an account identity OpenAI has verified (K1-4, L-5) |

**Conditions before adoption** (separate from the triggers; from the
assessment's recommendations 3–5):

| ID | Condition |
|---|---|
| CA-1 | Eligibility for the open-source route settled (the owner decides whether to ask OpenAI; nothing is submitted by an agent) |
| CA-2 | The custody amendment accepted: "custodied by Codex, or, for a ChatGPT plan grant made to Chirality, by the App in protected OS storage" (V4-ARC-04; SCA-V4-003) |
| CA-3 | One observation with the owner's own Plus or Pro sign-in at the then-current Codex version, including whether `chatgptAuthTokens` accepts the token (which would remove the hourly restart) |

**If reopened, the dependency notes (the assessment's addendum):**

- A fourth access entry kind ("ChatGPT plan, connected to Chirality") with
  App-held tokens in the macOS keychain, its own Codex process, renewal only
  at idle points, the per-app cap and disconnect shown, and the preview limits
  stated; Codex's own ChatGPT sign-in stays the designed default.
- An **external supplier row** (OpenAI's authorization service), satisfaction
  pending eligibility and observation, with its own version and qualification
  record (R19-5: it is a preview with no pin).
- Renewal at idle points needs DEL-01-02's live-work state: a **runtime
  value**, not a row (a row DEL-01-05 → DEL-01-02 closes a cycle; C-23).
- Restarts through HOSTING's existing stop and start operations, written as
  use of DEL-01-01, not a new requirement on it (the other direction would
  also close a cycle).
- A verified-identity source (validated ID token, `sub`, email) for
  DEL-04-03's person record, as a runtime value; presence at an act stays
  unverified (L-5).
- Packaging items for DEL-01-06: keychain access, a loopback port, OpenAI's
  branding rules, open-source eligibility beside OI-007.
- A next-relay note for DEL-05-01: plan billing needs a Responses provider
  (CH-8).
- SoW and register: SOW-009/SOW-010 ("credentials held by Codex") and OBJ-002
  ("three user-selectable Codex access modes") change; through SCA-V4-003
  with `dependency-extract` and a `project-dag` currency check.
- Both routes face supplier churn (the assessment's correction: 0.160.0 was
  published three days after 0.158.0); the pin is a design reference, not
  lasting stability.

## UNRESOLVED

Closed in v0.2: U-A1 (DECISION-L L-1 A), U-A3 (OBS-2 O-6 M1), U-A11
(DECISION-L L-7 A), U-A12 (OBS-2 O-6 M2). U-A2 is answered "not now"
(DECISION-L L-6 A) and kept only as the point at which it returns.

| ID | Item | Owner | Point of need | Effect here |
|---|---|---|---|---|
| U-A2 | A sign-in and API-key observation (OI-010; AK-5, AK-6, AK-10; K2-1's premise) | Owner: "not now" (L-6); asked again at the phase review if the design needs it | Before API-key implementation | Rows stay labelled as resting on the protocol types at 0.158.0 |
| U-A4 | `chatgpt` login options (`codexStreamlinedLogin`, `useHostedLoginSuccessPage`, `appBrand`) | App implementation owner (the owner, L-7) | Before sign-in implementation | Left absent |
| U-A5 | What happens to H-key and its threads when the key is removed | App implementation owner | Before API-key implementation | Kept, readable |
| U-A6 | A person-initiated loopback reachability check (App-origin contact) | App implementation owner | Before local-provider UI | Not offered |
| U-A7 | Which provider `modelProvider/capabilities/read` describes; model listing for local providers | A later observation | Before per-entry capability display | Limits shown as text |
| U-A8 | Email or digest of the Codex account in act records (privacy) | DEL-04-03 with the integrator | Before act-record implementation | Supplied as RS `codexAccount` |
| U-A9 | Whether the person may turn analytics back on for the App (the internal remote-control variable is settled: not used, R18-3) | Integrator (doctrine) | Before K-12 implementation | "Yes" proposed |
| U-A10 | Whether start-up network observations enter any run record | DEL-04-03 | Before records | Diagnostics only |
| U-A13 | `check_for_update_on_startup`: whether the key exists and what it stops at 0.158.0 | A later observation | Before K-12 implementation | Not set |
| U-A14 | Whether Codex follows a linked global `AGENTS.md` and a linked `skills/` (only `config.toml` was observed through a link) | A later observation (credential-free) | Before role supply implementation (with DEL-02-04) | Linked as R18-6 says; `instructionSources` and `skills/list` show the outcome at run time |
| U-A15 | Whether `experimentalFeature/list` lists `plugins` | A later observation | Before K-12 implementation | `config/read` and the observed default are used |
| U-A16 | *Closed:* the four triggers are recorded in ASSESSMENT_SIWC.md and copied into §20 | — | — | — |
| U-R3 (record) | Writes through the link | A later observation | Before configuration-write implementation | `filePath` to the target |

## Verification cases

"Needs" says what each case requires. None can pass a VER criterion yet: no
candidate exists.

| Case | Setup | Expected | Needs | Runnable now? | Serves |
|---|---|---|---|---|---|
| VC-A01 ChatGPT sign-in | Candidate; H-acct signed out | Q-2 completes; conversation on `chatgpt-account` starts; `account/read` chatgpt; no credential in App storage, records or logs (custody scan) | **The person's own sign-in**; candidate | No | VER-001 |
| VC-A02 API-key entry | Candidate; no H-key | Q-6; KE-6; API-key conversation starts on H-key; custody scan clean | **The person's key**; candidate | No | VER-002 |
| VC-A03 Local provider | Candidate; identified local server | Q-8; conversation starts; requested = reported provider; endpoint and model identity recorded | Identified server; candidate | No | VER-003 |
| VC-A04 All three together | VC-A01…A03 configured | One conversation per entry; each starts; the other two stay configured and selectable after each | Person; key; server; candidate | No | VER-004 |
| VC-A05 Account-home record review | Decision record v0.2 | Alternatives, choice, participants (L-7), timing, observed mechanism; open items explicit | Review | Yes (review) | VER-005 |
| VC-A06 API-key definition review | §10 | Each AK row traced to its standing and version; OI-010 open | Review | Yes (review) | VER-006 |
| VC-A07 Qualification record | Candidate records | Observed passes, failures, unverified claims distinguished; DEL-01-01 input linked | Candidate | No | VER-007 |
| VC-A08 Substitution | Two local servers | Edit `base_url` (Q-8); conversation starts on the substitute; result recorded | Two servers; candidate | No (model: routing only) | VER-008 |
| VC-A09 Handoff review | §11 and the fixture | Interface distinction, limits, no conformance claim; CH-8 as a relay note | Review; schema check | Yes | VER-009 |
| VC-A10 Act boundary | §14 | Each REQ-009 act to its owner | Review | Yes (review) | VER-010 |
| VC-A11 Configuration links | Temporary folder, invented `config.toml`, `AGENTS.md` and `skills/` | Three links set; explicit-target write keeps the `config.toml` link (CL-10); replacement write → `link-broken`, both files kept; the App writes nothing into the linked `skills/`; nothing outside the folder touched | Prototype | **Yes. Ran 2026-10-02: pass (model)** | VER-004, VER-005 |
| VC-A12 K-3 selection walk | Model | CS-1/CS-2 refuse; the offer is never applied; start sends explicit provider and model; no entry switch on unavailability (NS-1) | Prototype | **Yes. Ran 2026-10-02: pass (model)** | VER-004 |
| VC-A13 Custody scan | Model with invented canary strings standing in for a key, an auth URL and a device code | Canaries only in the frame written to the child and the transient display; absent from records, logs, snapshots, errors | Prototype | **Yes. Ran 2026-10-02: pass (model)** | VER-001, VER-002 |
| VC-A14 Tables | This file and the model | §5 tables equal the model's, row for row | Prototype | **Yes. Ran 2026-10-02: pass (model)** | — |
| VC-A15 Routing (K2-1) | Model | `chatgpt-account` and local entries start on H-acct; `api-key` on H-key; H-key child exists only with a key; cross-home entry change refused | Prototype | **Yes. Ran 2026-10-02: pass (model)** | VER-004 |
| VC-A16 Network view | Model; expected list from OBS-1/1b and OBS-2 O-7; invented sockets (documentation addresses) | Rows carry sources and states; remote-control row "no setting; no connection without sign-in (observed at 0.158.0)"; an unlisted address is shown and never blocked | Prototype | **Yes. Ran 2026-10-02: pass (model)** | — |
| VC-A17 Schemas | Four schemas and fixtures; records the model emits | Valid valid; invalid invalid for the stated reason; every emitted record valid | Prototype | **Yes. Ran 2026-10-02: pass (model)** | VER-004, VER-009 |
| VC-A18 S-4 receiving review | §19 and HOSTING §8 S-4 | Every S-4 element received, used with a limit or not used by design; every "not supplied" element placed here | Review | Yes (review) | VER-007 |
| VC-A19 Plugins follow the person (L-3) | Model; the person's setting on, off and absent; linked and fallback modes | Linked: no App plugins flag in any case; fallback: `plugins = false` only when the person's setting is off; the expected start-up rows are present only when plugins are on; the internal remote-control variable is never in the child's environment; analytics flag always set | Prototype | **Yes. Ran 2026-10-02: pass (model)** | — |
| VC-A20 Refusal wording (R18-2) | Model | Ordinary conversation: "not started — no model selected"; message that would start a workflow run: "run not started — no model selected" | Prototype | **Yes. Ran 2026-10-02: pass (model)** | VER-004 |
