# Account-home decision record (OI-009)

- Contribution: DEL-01-05/ACCOUNT-HOME-RECORD-v0.2 (supersedes
  DEL-01-05/ACCOUNT-HOME-RECORD-v0.1, committed at `63a6e0fa47`, file sha256
  8761b4f9ec66e87d1a44f051e2097870da7f18d3dcd8d9bfae65387e1f9eaa9d)
- Status: DECISION RECORDED AT CHOICE LEVEL (owner, DECISION-K3 K-1; the
  owner is also the App implementation owner, DECISION-L L-7). MECHANISM
  OBSERVED TO WORK AT CODEX 0.158.0 without a credential (OBS-2 O-6 M1);
  separation of a real sign-in not observed (DECISION-L L-6: not now). Not
  implemented, not accepted as a production contract.
- Produced by: node D4 of run `APP-V4-DESIGN-PASS-3-20261001`; v0.1 on
  2026-10-01, v0.2 (D round 2) on 2026-10-02. Companion:
  [ACCOUNT_AND_PROVIDER_ACCESS.md](ACCOUNT_AND_PROVIDER_ACCESS.md)
  (ACCESS-v0.2), whose basis, labels and version rule (R19-5: every supplier
  fact is at Codex 0.158.0 unless another version is named) apply here.
- Serves: OUT-003 (account-home definition record), REQ-005, AC-005,
  VER-005; TBD-001; register constraint DEP-01-05-015.
- **Not changed here:** `_Decomposition/Open_Issues.csv` still lists OI-009
  OPEN, and the ScopeOfWork's TBD-001 still says OPEN. An executor does not
  write them (BRIEFS common rules); the D4 return file proposes the change for
  SCA-V4-003.

## Changes from v0.1

| Ruling / item | Where | Change |
|---|---|---|
| OBS-2 O-6 (M1…M5) | §4 | M-A observed to work; M-B observed (a copy in the `sessionFlags` layer); `--profile` refused for `app-server` (new M-F); M-D not distinguishable without a credential; fallback not needed at 0.158.0; "what O-6 must show" replaced by what it showed |
| DECISION-L L-7 (A); R19-4 | §3 | Participants: the owner is also the App implementation owner; REQ-005's reading recorded |
| R18-6 (C-18) | §4.1 | Global `AGENTS.md` and `skills/` linked like `config.toml`; U-R1 closed |
| DECISION-L L-1 (A); R19-4 | §5 | HOSTING U-12 per-home dimension is now firm (K2-1 adopted) |
| DECISION-L L-6 (A) | UNRESOLVED U-R2 | Not observed now |
| R19-5 | §4, §6 | Version named for every supplier fact; the link's working is version-bound |

## 1. The question (OI-009, SOW-132)

"Choose separated versus shared Codex account state" (Open_Issues OI-009,
owner "Owner with App implementation owner", point of need "Before account
integration"; consequence: "Do not silently carry current v3 overlay or Root
behavior into new product choice"). ARCHITECTURE §3 "Left to the
implementation session": "whether Chirality keeps sign-in separate from the
user's other Codex clients (v3's overlay home) or shares it".

## 2. Alternatives (as presented to the owner, DECISIONS_PENDING.md K-1)

| Option | Sign-in | Settings, providers, MCP servers | Conversation history | Start-up traffic (HOSTING L-4, OB-9; OBS-2 O-7) | Effect on the person's Codex CLI | HOSTING consequences |
|---|---|---|---|---|---|---|
| A. A Chirality home of its own | Separate | Separate: the person configures providers and MCP servers again for the App | Separate | Each App home is "fresh" once: plugin fetch (F-14) unless plugins are off | None | §4.2 step 3 names the App home; §7.2 probe home separate; F-14 per home |
| B. The person's existing Codex home | Shared: signing in or out in the App signs in or out for the CLI too | Shared | Shared: App threads appear to the CLI and the reverse | Same as the CLI's | The App writes sessions, state and logs into the person's home; an App sign-out ends the CLI's sign-in | §4.2 step 3 names the person's home; the probe would write into it (S-F-17) unless separate; F-18 bears directly |
| **C. Shared settings, separate sign-in (chosen)** | Separate, custodied by Codex in an App-owned home | Shared: the App sees the person's configuration | Separate | Per App home; follows the person's plugin setting (DECISION-L L-3) | Only person-directed configuration writes reach the person's file | §4.2 step 3 names the App home and the shared configuration; §7.2 probe home separate; F-14 per App home |

The doctrine text: Root `AGENTS.md` describes the App as hosting Codex
"against the user's shared Codex configuration and resources, with
authentication separated for Chirality and custodied by Codex (D-GOV-43)".
OI-009 says not to carry this silently into v4; option C carries it only
because the owner chose it.

App v3 (evidence only, not a v4 commitment): its settings text says the App's
Codex home "never reads, copies, or links your ambient `~/.codex`
directory" (`projects/chirality-app-dev/frontend/src/components/settings/account-consent-settings.tsx`,
line 231), which is option A in practice, while the same repository's doctrine
describes C.

## 3. The choice

**Decided:** option C, by the owner, 2026-10-01.

> I accept 1-6, 8-9, and 11 as recommended.

(DECISION-K3; custody: the owner's chat message to HELP_HUMAN, recorded in
`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`;
the revision of the same day changed K-10 and K-12 only.) K-1 as accepted
reads: "Shared settings, separate sign-in (recommended). The App sees your
Codex settings, providers and MCP servers, and signs in on its own. … The
mechanism is designed as PROPOSED and confirmed by a local observation; if
Codex 0.158.0 cannot do it, the design falls back to A and says so."

**Participants (REQ-005).** REQ-005 names "the Owner with the App
implementation owner". DECISION-L L-7 (A), 2026-10-02: the App
implementation owner is the owner, and the K-1 answer covers both. This
record therefore reads REQ-005 as "the Owner, who is also the App
implementation owner (DECISION-L L-7)" (R19-4). The recommendation was
HELP_HUMAN's (integrator).

**Timing (AC-005).** Recorded before any account integration: no App
candidate or account code exists in v4 (`_STATUS.md` of DEL-01-05:
INITIALIZED).

## 4. Mechanism (observed at Codex 0.158.0)

**Supplier facts at 0.158.0.** The Codex home is selected by `CODEX_HOME`
(HOSTING §4.2; OBS-1 §2; `InitializeResponse.codexHome`). The user
configuration layer is a file in that home: `ConfigLayerSource` `user {file,
profile}`; other layers include `system`, `project`, `sessionFlags`, managed
and MDM layers (`observed-in-generated-types`). `config/value/write` and
`config/batchWrite` accept an explicit `filePath` and `expectedVersion`
(`observed-in-generated-types`). No environment variable in the binary's
strings names a separate configuration file location (`strings-in-binary`).
The effective default credential store is `file` (OBS-2 O-6 M0–M2), so a
separate `CODEX_HOME` gives separate credential storage by construction
(`inference` from that default and the file name `auth.json` in the strings;
not observed with a credential).

**Mechanisms and what OBS-2 O-6 showed (2026-10-01; scratch homes; no
credential anywhere; `config/read` and `account/read` only):**

| ID | Mechanism | O-6 result at 0.158.0 | Assessment |
|---|---|---|---|
| M-A | App-owned home whose `config.toml` is a **symbolic link** to the person's | **Works** (M1): the second home reads the first's values; the user layer is named by the second home's path; `account/read` → `account: null`, `requiresOpenaiAuth` false; the first home's file byte-identical before and after | **Chosen** |
| M-B | App-owned home; the person's settings passed as `-c` flags at each spawn | Works as a **copy** (M2): the values appear in a `sessionFlags` layer above an empty user layer; the App would have to read and re-send the person's file | Set aside for sharing; `-c` is the carrier for the App's own settings (ACCESS §9) |
| M-C | App-owned home with a copy of the person's file | Not run | Set aside (option A with an initial copy; silent divergence) |
| M-D | The person's own home with `cli_auth_credentials_store = "ephemeral"` or `"keyring"` for the App | Runs (M4, M5); separation of authentication **not distinguishable** without a credential | Set aside (writes the App's history into the person's home) |
| M-F | `codex --profile <name> app-server` | **Refused at launch** (M3): `--profile` "only applies to runtime commands and `codex mcp`" | Not available |
| M-E | Option A (own configuration) | — | Fallback, **not needed at 0.158.0**; kept for a later version where `config/read` no longer shows the linked file as the user layer (ACCESS CL-3, §18) |

**Still not observed:** writes through the link (O-6 did not exercise
`config/value/write` or `config/batchWrite`; through a symlink they would
land in the person's file, `inference`), hence the App writes with an
explicit `filePath` to the resolved target (ACCESS Q-8, F-A3; U-R3); and
the separation of a real sign-in between homes (L-6; U-R2).

### 4.1 What is shared and what is the App's own

| Resource in a Codex home | Under M-A | Reason |
|---|---|---|
| `config.toml` (settings, model providers, MCP servers, features including `plugins`, profiles) | Shared (link); **observed read** at 0.158.0 | K-1 names settings, providers and MCP servers; L-3 follows the person's plugin setting through it |
| Global `AGENTS.md` | Shared (link), **R18-6** | So that Codex's native discovery in the App matches the person's Codex; `instructionSources` records what Codex reports. Following a linked file not observed (U-A14) |
| `skills/` | Shared (link), **R18-6**; the App writes nothing into it (R19-7) | As above. OBS-3: every discovered skill in `$CODEX_HOME/skills` is advertised in every model request of that home (ACCESS F-A9). Following a linked folder not observed (U-A14) |
| Prompts, rules and other files of the person's home | Not linked | R18-6 names `AGENTS.md` and skills only |
| Credentials (`auth.json` or keyring entry) | App's own, per App home | K-1 separate sign-in; V4-ARC-04 custody by Codex |
| Sessions, thread history, state and log databases | App's own | Not settings; option C separates history |
| Plugin cache and sync state (`.tmp/plugins`, `plugins.sha`) | App's own | Supplier working state (F-14 per App home, when plugins are on) |
| Installation identity | App's own | Per home; sent to the provider in `client_metadata` (OBS-2 §11) |

## 5. Consequences for the first-increment files (join list; node F edits)

| File, section | Was | Now needed |
|---|---|---|
| HOSTING §4.2 step 3 | "account-home/environment element is `UNRESOLVED{OI-009}`" | K-1 decided (C); spawn with `CODEX_HOME=<App home>` per App-owned account home (H-acct; H-key, K2-1 adopted, L-1); the person's `config.toml`, `AGENTS.md` and `skills/` linked (M-A observed for `config.toml`, O-6 M1; R18-6 for the other two); the App's session flags by `-c` (O-6 M2) |
| HOSTING §7.2 | "Which home the label probe uses … is part of U-03/OI-009" | A separate App-owned probe home H-probe, with no links |
| HOSTING H9 | "The account-home element remains `UNRESOLVED{OI-009}`" | Decided; settings carried from the person's configuration through the link |
| HOSTING F-14 | "a separate App account home would be 'fresh' at least once per home" | Per App home, and only when the person's plugins are on (O-7 v8: with `plugins = false` a cold home creates no `.tmp/` and fetches nothing) |
| HOSTING F-18 | Relevant to OI-009, no conclusion | Under C the App writes the person's home only by person-directed configuration writes |
| HOSTING U-03 | Open | Closed at choice level; mechanism observed (O-6 M1); separation with a credential not observed |
| HOSTING U-12 | "One active child assumed" | One child per App-owned account home (K2-1 adopted, DECISION-L L-1; R19-4); generation identity {App session, App home, spawn counter} (R18-1 C-20) |

## 6. Status line for OI-009

Choice: **made** (owner, who is also the App implementation owner;
DECISION-K3 K-1 and DECISION-L L-7). Mechanism: **observed to work at Codex
0.158.0** (M-A, O-6 M1), without a credential. Open: writes through the link
(U-R3); a real sign-in's separation (U-R2, deferred by L-6); whether Codex
follows linked `AGENTS.md` and `skills/` (ACCESS U-A14). Version-bound:
rechecked at each version advance (R19-5).

## UNRESOLVED

| ID | Item | Owner | Point of need |
|---|---|---|---|
| U-R1 | *Closed (R18-6):* the person's global `AGENTS.md` and skills are linked into the App homes | — | — |
| U-R2 | Whether a credential store (`file` per home, or `keyring`) keeps two homes' sign-ins apart, observed with a credential | Owner: not now (DECISION-L L-6) | Before account integration, if the design needs it |
| U-R3 | How Codex writes `config.toml` (in place or by replacement) through a link | A later observation | Before configuration-write implementation |
