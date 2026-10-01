# Account-home decision record (OI-009)

- Contribution: DEL-01-05/ACCOUNT-HOME-RECORD-v0.1 (first version)
- Status: DECISION RECORDED AT CHOICE LEVEL (owner, DECISION-K3 K-1);
  MECHANISM PROPOSED, to be confirmed or refused by OBS-2 O-6. Not
  implemented, not accepted as a production contract.
- Produced by: node D4 of run `APP-V4-DESIGN-PASS-3-20261001`, 2026-10-01.
  Companion: [ACCOUNT_AND_PROVIDER_ACCESS.md](ACCOUNT_AND_PROVIDER_ACCESS.md)
  (ACCESS-v0.1), whose basis and labels apply here.
- Serves: OUT-003 (account-home definition record), REQ-005, AC-005,
  VER-005; TBD-001; register constraint DEP-01-05-015.
- **Not changed here:** `_Decomposition/Open_Issues.csv` still lists OI-009
  OPEN, and the ScopeOfWork's TBD-001 still says OPEN. An executor does not
  write them (BRIEFS common rules); the return file proposes the change for
  SCA-V4-003.

## 1. The question (OI-009, SOW-132)

"Choose separated versus shared Codex account state" (Open_Issues OI-009,
owner "Owner with App implementation owner", point of need "Before account
integration"; consequence: "Do not silently carry current v3 overlay or Root
behavior into new product choice"). ARCHITECTURE §3 "Left to the
implementation session": "whether Chirality keeps sign-in separate from the
user's other Codex clients (v3's overlay home) or shares it".

## 2. Alternatives (as presented to the owner, DECISIONS_PENDING.md K-1)

| Option | Sign-in | Settings, providers, MCP servers | Conversation history | Start-up traffic (HOSTING L-4, OB-9) | Effect on the person's Codex CLI | HOSTING consequences |
|---|---|---|---|---|---|---|
| A. A Chirality home of its own | Separate | Separate: the person configures providers and MCP servers again for the App | Separate | Each App home is "fresh" once: plugin fetch (F-14); remote-control loop per home | None | §4.2 step 3 names the App home; §7.2 probe home separate; F-14 per home |
| B. The person's existing Codex home | Shared: signing in or out in the App signs in or out for the CLI too | Shared | Shared: App threads appear to the CLI and the reverse | Same as the CLI's | The App writes sessions, state and logs into the person's home; an App sign-out ends the CLI's sign-in | §4.2 step 3 names the person's home; the probe would write into it (S-F-17) unless separate; F-18 (the person's own Codex process was present during the spike) bears directly |
| **C. Shared settings, separate sign-in (recommended)** | Separate, custodied by Codex in an App-owned home | Shared: the App sees the person's configuration | Separate | Per App home, as A | Only person-directed configuration writes reach the person's file | §4.2 step 3 names the App home and the shared configuration; §7.2 probe home separate; F-14 per App home |

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
`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`,
sha256 9d18c40d…1b1b; the revision of the same day changed K-10 and K-12
only.) K-1 as accepted reads: "Shared settings, separate sign-in
(recommended). The App sees your Codex settings, providers and MCP servers,
and signs in on its own. … The mechanism is designed as PROPOSED and
confirmed by a local observation; if Codex 0.158.0 cannot do it, the design
falls back to A and says so." R17-2 places it here.

**Participants (REQ-005: "the Owner with the App implementation owner").**
The owner decided; the recommendation was HELP_HUMAN's (integrator). No
separate App implementation owner is identified in the run records, and no
record shows that party's participation. This record states that fact and
does not infer it (U-A11 in ACCESS-v0.1).

**Timing (AC-005).** Recorded before any account integration: no App
candidate or account code exists in v4 (`_STATUS.md` of DEL-01-05:
INITIALIZED).

## 4. Mechanism (PROPOSED; OBS-2 O-6 pending)

**Supplier facts.** The Codex home is selected by `CODEX_HOME` (HOSTING §4.2;
OBS-1 §2; `InitializeResponse.codexHome`). The user configuration layer is a
file in that home: `ConfigLayerSource` `user {file, profile}` ("the path to
the user's config.toml file, though it is not guaranteed to exist"); other
layers include `system`, `project`, `sessionFlags`, managed and MDM layers
(`observed-in-generated-types`). `config/value/write` and `config/batchWrite`
accept an explicit `filePath` ("defaults to the user's config.toml when
omitted") and `expectedVersion` (`observed-in-generated-types`). No
environment variable in the binary's strings names a separate configuration
file location (`strings-in-binary`, by search of the `CODEX_*` names: only
`CODEX_HOME` and `CODEX_SQLITE_HOME` relate to locations). Credentials are
stored per home (`auth.json` in the strings; store modes in the generated
types); whether a `keyring` entry is keyed per home is not observed.

**Mechanisms considered:**

| ID | Mechanism | Sharing | Separation of sign-in | Risks | Assessment |
|---|---|---|---|---|---|
| M-A | App-owned home whose `config.toml` is a **symbolic link** to the person's configuration file | Live: edits by either side are seen by both | By home (credential store in the App home) | A write that replaces the file at the link path breaks the link silently (F-A3) → writes pass `filePath`, link checked (ACCESS §5.5); only `config.toml` is shared, not other home resources (§4.1) | **PROPOSED** |
| M-B | App-owned home; the person's settings passed as `-c` flags at each spawn | Snapshot at spawn; edits in the App cannot go back | By home | Settings visible in the process list; changes made in the CLI need a restart; large flag sets | Set aside |
| M-C | App-owned home with a **copy** of the person's file | Snapshot; divergence | By home | Silent divergence | Set aside (it is option A with an initial copy) |
| M-D | The person's own home with `cli_auth_credentials_store = "ephemeral"` set for the App | Full | Only if ephemeral mode never reads the stored sign-in (not observed) | App threads and logs written into the person's home (B's history effect); an App logout might remove the stored credential (strings: "Failed to remove auth.json"); sign-in lost each start | Set aside |
| M-E | Option A (own configuration) | None | By home | The person configures twice | **Fallback** (K-1) |

**What O-6 must show for M-A (R17-16 O-6: "observed by `config/read` and
`account/read` only"):** in two scratch homes, the first with an invented
configuration, the second empty except for the link, `config/read
{includeLayers: true}` on the second returns the first's values with the
user layer's `file` naming the link path (or its target), and `account/read`
on the second returns `account: null` while the second has no credential.
Separation of a *real* sign-in cannot be observed under K-11 (no sign-in);
it rests on the per-home credential store (`inference` for `keyring`).

**Fallback rule.** If O-6 shows that the linked file is not read as the user
layer, or that 0.158.0 refuses the link, the App uses M-E (option A) and its
settings view says "the App keeps its own Codex settings at <path>; your
Codex CLI settings are not used" (ACCESS CL-3). If O-6 is inconclusive, the
cell stays OBS-2 pending; nothing falls back silently.

### 4.1 What is shared and what is the App's own (PROPOSED)

| Resource in a Codex home | Under M-A | Reason |
|---|---|---|
| `config.toml` (settings, model providers, MCP servers, features, profiles) | Shared (link) | K-1 names settings, providers and MCP servers |
| Credentials (`auth.json` or keyring entry) | App's own, per App home | K-1 separate sign-in; V4-ARC-04 custody by Codex |
| Sessions, thread history, state and log databases | App's own | Not settings; option C separates history |
| Plugin cache and sync state (`.tmp/plugins`, `plugins.sha`) | App's own | Supplier working state (F-14 per App home) |
| Global `AGENTS.md`, skills and prompts in the home | **Not linked at v0.1** (U-R1) | Supplied guidance is DEL-02-04's (K-9, S-6); linking the person's global instructions would add an unrecorded guidance input to every App conversation; DEL-02-04 decides |
| Installation identity | App's own | It is per home; OB-9 logged it beside the remote-control lines |

## 5. Consequences for the first-increment files (join list; node F edits)

| File, section | Was | Now needed |
|---|---|---|
| HOSTING §4.2 step 3 | "account-home/environment element is `UNRESOLVED{OI-009}`" | K-1 decided (C); the spawn environment carries `CODEX_HOME=<App home>` (H-acct; H-key under K2-1); mechanism M-A PROPOSED, O-6 pending; fallback A |
| HOSTING §7.2 | "Which home the label probe uses … is part of U-03/OI-009" | A separate App-owned probe home (H-probe); never an account home and never the person's home |
| HOSTING H9 | "The account-home element remains `UNRESOLVED{OI-009}`" | Decided; settings are carried from the person's own configuration through the link; the App's session flags carry only the K-12 traffic settings (ACCESS §9) |
| HOSTING F-14 | "a separate App account home would be 'fresh' at least once per home" | Stands, per App home (H-acct, H-key); whether the plugins feature setting stops the fetch is O-7 |
| HOSTING F-18 | Relevant to OI-009, no conclusion | Under C the App never writes the person's home except by person-directed configuration writes |
| HOSTING U-03 | Open | Closed at choice level; mechanism open until O-6 |
| HOSTING U-12 | "One active child assumed" | Under K2-1 one child per App account home (ACCESS §4): a per-home dimension (R17-2: reported, not restructured here) |

## 6. Status line for OI-009

Choice: **made** (owner, DECISION-K3 K-1, 2026-10-01: option C).
Mechanism: **PROPOSED** (M-A), pending OBS-2 O-6; fallback A on refusal.
Open: the App implementation owner's participation (U-A11); the global
guidance resources (U-R1, with DEL-02-04).

## UNRESOLVED

| ID | Item | Owner | Point of need |
|---|---|---|---|
| U-R1 | Whether the App's Codex sees the person's global `AGENTS.md`, skills and prompts | DEL-02-04 with the integrator | Before role supply implementation |
| U-R2 | Whether a `keyring` credential entry is separated per home | Observation with a sign-in (owner, K-11) | Before account integration |
| U-R3 | How Codex writes `config.toml` (in place or by replacement) through a link | OBS-2 (not in O-6's read-only scope) or a later observation | Before configuration-write implementation |
