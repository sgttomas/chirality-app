# F0 — join consolidation (design pass 3, after D round 1 and OBS-2)

- Run `APP-V4-DESIGN-PASS-3-20261001`, node **F0**. Executor: Type 2 TASK
  (Claude Opus 5.5), harness-native descendant of the HELP_HUMAN session; does
  not delegate. Written 2026-10-01 at HEAD `949a19a257`.
- Boundary kept: read-only on everything; the only file written is this one
  (and the folder `F/`). No first-increment Design file, D-node file,
  ScopeOfWork, register, `_STATUS.md` or DAG file was edited. No network, no
  Codex or model run. Scratch scripts under `$TMPDIR/f0/` (not in the
  repository).
- **Standing.** This is a consolidation for the integrator. It decides
  nothing: every "recommended resolution" below is a proposal for a ruling.
  What a file *states* is quoted with its line number; what this node *infers*
  is marked "(inference)".

Paths are relative to `projects/chirality-app-v4/execution` (E).

## Inputs (sha256, first 16 hex)

| Input | sha256 |
|---|---|
| `RUN/BRIEFS.md` | `b261394112d7264e` |
| `RUN/OWNER_DECISIONS.md` (DECISION-K3 revised) | `9d18c40dd7d894dc` |
| `RUN/R17_RESOLUTIONS.md` | `b0af81bcbad9bc52` |
| `RUN/D/D1.md` … `D6.md` | `4f7a12a5a663f1c3`, `d0cdeb85f6f585c4`, `84c9d712806d81fa`, `2f01e9a9923b012f`, `8af0f970cb021672`, `c5431913e75119cc` |
| `RUN/D/OBS-2.md`; `DEL-01-01/Design/OBS_2_0.158.0.md` | `a9fc32e0daa23e85`; `61cc34ffb811eb27` |
| New Design files (equal to the hashes the D returns record) | RECOVERY `455678a699290249`, NPTD `a3b36a454d497e28`, NIR `96765105cec82d16`, AAC `7e98118c774fcd9c`, ACCESS `b82e40395a4a19bc`, ACCOUNT-HOME `8761b4f9ec66e87d`, WR `0b51ee6c7ea9c571`, ROLE `692873d1d025b4ab` |
| First-increment targets (equal to the hashes the D nodes read) | HOSTING-v0.8 `3cf0381c42358fec`, EXEC-v0.6 `64e732d502d0b91d`, RS-v0.8 `b25cc90e9e252f50` (schema `b63a7e421b885854`), ACT-v0.8 `6fb6b9e883fa8d20`, AS-v0.8 `d6f26801b0146800`, WD-v0.8 `517821d18fc95830`, WD-EX-v0.8 `275ea54d32cd8f48`, CA-v0.6 `58167f7accaf356e`, ADAPTER-v0.6 `7cad04c873c0f115`, XT-v0.6 `daf6c9c946ec1520`, LOOP-v0.8 `f8b7776c82614738`, GUIDE-v0.5 `5b87996d9c16d5d2`, PANEL-v0.8 `70d9a23ed45def4e`; `hosting.server-request-entry.schema.json` `dda16758d28b4c20` |
| DAG-003 `DependencyEdges.csv`, `CandidateEdges.csv` | `4716ca287d23835c`, `07b969209e273310` |
| Pass-2 closeout `C1-A.md`, `C1-B.md`, `C1-C.md` | `e2cb79e22ea5cf75`, `c819ba9be9b92577`, `9c4b9a37a738740a` |

**How checked.**
(1) Every "current text" below was searched in the target file by a script
that normalises whitespace and line wraps and reports the line number
(`$TMPDIR/f0/chk.py`); quotes that missed were opened and read (three were
paraphrases or split by Markdown bold; noted per row). (2) A second script
listed every remaining "later / D1 / outside this undertaking / no Design
file" pointer to the six pass-3 deliverables in the first-increment files, to
find stale text no D node claimed (§1.14). (3) Schema shapes were compared by
loading the JSON schemas. (4) SCC effects by Tarjan over DAG-003 admitted +
held arcs (§3). (5) `multiAgentMode` "@deprecated Ignored" was confirmed in
the committed bundle `DEL-01-01/Design/generated/0.158.0/json-schema/experimental/*.json`.

Item IDs: `D1 H-n`, `D2 J-n`, `D3 J-xn`, `D4 #n` (D4's join table has no IDs;
numbered here in its row order 1–23), `D5 J-n`, `D6 J-n`. Consolidated rows
here carry `F*-nn` IDs.

---

## 0. Counts

| Target file | Consolidated rows | D items merged into them | Premise wrong / quote paraphrased | Unclaimed stale pointers (§1.14) |
|---|---|---|---|---|
| HOSTING-v0.8 (+ server-request schema) | 44 | 44 (D1 8, D2 4, D3 9, D4 16, D5 1, D6 6); plus 3 OBS-2-only rows and 1 sweep row | 2 (D2 J-1 location; D6 J-6 no quotable text) | 3 |
| EXEC-v0.6 | 20 | 21 (D1 4, D2 1, D3 8, D4 1, D5 6, D6 1) | 0 (D3 J-E1 split by bold, correct) | 5 |
| RS-v0.8 (+ schema, examples) | 14 | 16 (D1 4, D3 5, D4 2, D5 3, D6 2) | 0 | 3 |
| ACT-POLICY-v0.8 | 8 | 10 (D3 4, D5 6) | 0 | 2 |
| AS-v0.8 | 2 | 2 | 0 (D3 J-S1 split by bold, correct) | 0 |
| WD-v0.8 | 13 | 13 | 0 (D5 J-7 split by bold, correct) | 8 |
| WD-EX-v0.8 | 2 | 2 | 0 | 3 |
| CA-v0.6 | 1 (multi-locus) | 1 | 0 | 13 |
| ADAPTER-v0.6 | 1 | 1 | 0 | 2 |
| XT-v0.6 | 1 | 1 | 0 | 0 |
| LOOP-v0.8 | 2 | 2 | 0 | 0 |
| GUIDE-v0.5 | 3 | 2 (+1 gap) | 1 (D6 J-13 paraphrase; text is G-1) | 3 |
| PANEL-v0.8 | 1 | 1 (pointer) | 0 | 0 |
| **Total** | **112** | **116** placements (D4 #19 counted under EXEC and RS) | 3 | 42 |

Rows that merge items from two or more D nodes: 15 (FH-03, FH-05, FH-11, FH-15, FH-19, FH-20, FH-33, FE-07, FR-04, FR-05, FR-06, FA-02, FA-03, FA-04, FA-05); exact duplicates are marked "=" in the rows.

---

## 1. Per target file

Columns: **F-ID** · **D items** · **Section (line)** · **Current text (verified)** · **What is needed** · **Source** · **OBS-2**.
"OBS-2" says whether the row's text depends on the OBS-2 record (O-n) and
which way it went (see §7 for detail): **conf** confirms, **chg** changes the
D text, **open** leaves it open, "—" independent.

### 1.1 HOSTING-v0.8 — `DEL-01-01/Design/HOSTING_BOUNDARY.md` (+ `hosting.server-request-entry.schema.json`)

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FH-01 | D1 H-1 | §4.5 opening (L411); §4.6 stop row "Caller" (L435) | "A stop is an explicit act (person quits the App or chooses stop)"; "The person: quit or stop (V4-EXE-01)" | Name the operation DEF-5a (stop the Codex process), reached by a confirmed quit (DEF-6) or the person's explicit Codex stop/restart; a turn stop is DEF-3 `turn/interrupt`, never a process stop; cite RECOVERY-v0.1 §2 (R17-3). Add from OBS-2: a graceful stop (stdin close) exits in ≈21 ms and writes Codex's own "user interrupted … on purpose" marker into history; a plugin `git` child can outlive a stop made soon after start, so a deliberate stop ends the process group (H11, U-16) | D1; R17-3, R17-14 | conf (O-2, §11 H11) |
| FH-02 | D1 H-2 | §4.5 step 2 (L416–418); U-10 (L1719) | "…either explicitly declined by the App with origin `app-rule:on-stop` or left to end with the process — a DEL-01-02 recovery decision (U-10)" | "left to end with the process (`ended-unanswered(process-exit)`); no App decline at stop or quit (RECOVERY §6 U-10)"; close U-10 | D1 | conf (O-2: no re-raise, no resolution sent) |
| FH-03 | D3 J-H2 = D1 H-6 (U-11 part) | §6.3 R3 (L652–655); U-11 (L1720) | "Any automatic decline after a period is not defined here (U-11) … never automatic by default"; U-11 "Not defined" | "No App rule declines a waiting request after any period, and the native `timed_out` form is never sent (R17-9). A supplier's own resolution is `resolved-by-supplier` (RT-10)." Close U-11 | D3, D1; R17-9 | conf (O-3) |
| FH-04 | D1 H-3 | §6.5 title (L722) and last sentence (L730); U-14 (L1723); F-01 (L1518) | "(to reconcile when DEL-01-02 is defined)"; "under D1 the reconciliation happens in the later undertaking that defines DEL-01-02" | Reconciled: the split stands as written (RECOVERY §1); close U-14 and F-01 | D1; R17-14 | — |
| FH-05 | D1 H-4 + D2 J-3 | §4.6 observe-lifecycle failure cell (L437); §5 Order; §12 "Open within O-1" (L1501) | "Observer loss loses nothing: events are kept and re-read from a position"; "which interface component re-attaches after reload (DEL-01-02)" | Realization: bounded in-memory journal per generation, replayed from the observer's position (OA-01); otherwise snapshot + Codex history reads with a gap marker (OA-02); each window's observer re-attaches, the main process holds the journal (RECOVERY §3.3, §4.1). **D2 J-3 asks the opposite question** (closed-generation re-read) — conflict **C-03**; apply after the ruling | D1, D2 | — |
| FH-06 | D1 H-5 (+ D4 #15 U-12) | H5 (L284) | "Each spawn receives a new *generation* at spawn time." | Add: generation identity unique across App sessions (includes the App session) (RECOVERY §6, F-R6). If owner adopts K2-1 (U-A1), also keyed by App-owned home — conflict **C-11** | D1, D4 | — |
| FH-07 | D1 H-6 (U-09, U-16) | U-09 (L1718); U-16 (L1725) | U-09 "…Candidate source named; semantics open…the before-reply trigger is not observed"; U-16 "policy open" | U-09: RT-12 reading adopted; **before-reply trigger now observed** (O-3: `turn/interrupt` with a held approval → `turn/completed` then `serverRequest/resolved`, no client answer; a late answer silently ignored) → close or narrow U-09. U-16: PROPOSED policy RECOVERY §6 (end the tree only at a deliberate stop), still with the App implementation owner; OBS-2 §11 shows why the tree must be ended | D1; OBS-2 | chg (O-3 fills) |
| FH-08 | D1 H-7 | H3 (L277); §6.4 last row (L720); §8 S-1 row, "Not supplied here" cell (L960); S-7 last cell (L966); §11 custody row (L1468) | "Durable custody across relaunch is DEL-01-02's (§6.5)"; "DEL-01-02 (custody of in-flight requests; outside this increment, D1)"; "…DEL-01-02's separate contribution (S-1; outside this increment, D1)" | Point to RECOVERY-v0.1 (§3.5, §5, §7) instead of "outside this increment, D1" | D1 | — |
| FH-09 | D1 H-8 | §6.7 HP-2 (L789) | "If the App sends it for another purpose (a person's explicit stop, V4-EXE-01), the outcome is recorded as observed…" | Cite DEF-3 and SR (RECOVERY §3.4) | D1 | — |
| FH-10 | D4 #1 | §4.2 step 3 (L348–351) | "The account-home/environment element is `UNRESOLVED{OI-009}` (DEL-01-05 owns the choice's integration)" | K-1 decided (option C); spawn with `CODEX_HOME=<App home>` per home; configuration through a symlinked `config.toml` (M-A) — **now observed to work** (O-6 M1: user layer named by B's path, content A's, `account/read` null); `-c` overrides also work (copy, `sessionFlags` layer, O-6 M2); `--profile` refused for `app-server` (M3). Fallback (option A) not needed at 0.158.0. App session flags carry K-12 settings only (ACCESS §3, §9; record §4) | D4; K-1 | conf (O-6) |
| FH-11 | D2 J-1 + D4 #2 | §4.2 step 4 (L352–356); F-13 (L1551–1555); U-21 (L1730) | Step 4: "at 0.158.0: `experimentalApi` and `requestAttestation`, both required booleans; optional elements include `optOutNotificationMethods`…". F-13: "The App must declare the experimental opt-in to use plan mode" | **Premise note (D2 J-1):** the quoted words "required to use plan mode" are F-13's (L1553), not §4.2 step 4's; the edit lands at both. Needed: under K-5 the App declares `experimentalApi: true` and records it per generation (NPTD EX-2); add `explicitGatewayOauth: true` so no gateway browser authorization starts without the person's act (ACCESS Q-1, F-A4; PROPOSED). OBS-2: plan mode (`collaborationMode` on `turn/start`) and `remoteControl/status/read` need the opt-in; delegation does **not** (stable feature `multi_agent`) | D2, D4; K-5 | conf (O-8, O-7) |
| FH-12 | D4 #3 | §7.1 configuration identity | Launcher, arguments, environment (D4's paraphrase; §7.1 lists them) | Also the home identity and the K-12 session flags; never a credential (CR-7, CR-8) | D4 | — |
| FH-13 | D4 #4 | §7.2 (L895) | "Which home the label probe uses … is part of U-03/OI-009" | A separate App-owned probe home H-probe (ACCESS §3) | D4 | — |
| FH-14 | D4 #5 | H9 (L311) | "The account-home element remains `UNRESOLVED{OI-009}`" | Decided; settings carried from the person's configuration through the link; carriers per element: K-12 traffic settings in session flags; the person's approval and sandbox choices unchanged (F-32 refusals shown, never "fixed") | D4 | conf (O-6) |
| FH-15 | D3 J-H1 + D4 #6 | §6.1 partition table (L572), row `account/chatgptAuthTokens/refresh` (L585); U-20 (L1729) | "PROPOSAL for the App implementation owner with DEL-01-04/01-05, U-20"; "known-app-unsupported unless DEL-01-05 adopts external-token login"; U-20 "Proposal only; R9 classes fixed as INTEGRATION, membership open" | Record DEL-01-04's answer path per kind (NIR §4.1) and decline form per kind (NIR §4.3 DM-1…DM-6); DEL-01-05 does not adopt external-token login (CR-9) → that kind is known-app-unsupported, explicit error. U-20 narrows to the App implementation owner's confirmation only (both D3's and D4's halves now answered) | D3, D4 | — |
| FH-16 | D3 J-H3 | §6.2.1 RT-08 guard (L621); §6.4 *answer* | RT-08 "…the answer is a decline or cancel form" | Name the negative forms per kind (`decline`, `cancel`; legacy `denied`, `abort`; elicitation `decline`/`cancel`; PROPOSED empty answer map for `item/tool/requestUserInput` and empty grant for `item/permissions/requestApproval`), or take the submission's `submittedAs`. Add OBS-2: `cancel` on a command approval ended the item `declined` **and** the turn `interrupted` (decline + interrupt) | D3 | conf (O-3 side obs.) |
| FH-17 | D3 J-H4 | §6.1 *settlement* (L561); schema `settlement.nativeContent` | "Native answer content…" (kept unchanged) | Answers to `isSecret` questions are not kept readable after the reply is written: redaction marker in the entry; DEL-01-02's persistence the same (NIR SE-1…SE-3) | D3 | — |
| FH-18 | D3 J-H5 | §6.1 origin row (L561); schema `origin.actorRef` (schema L34) | "(A14 by the person, actor supplied by DEL-01-04)"; "As supplied by DEL-01-04; never inferred" | Form "person:‹name set in the App›/‹OS account›/‹Codex account› (identity not verified)", sources per AAC §7 (K1-4). Shape vs RS `person` object and D4's account object — conflict **C-10** | D3 | — |
| FH-19 | D3 J-H6 + D1 (S-1) + D2 (S-2) + gap (S-4) | §8 seams S-3 (L962); F-15 (L1565–1567) | S-3 "Not supplied here: Request cards, answer UX, attachments, outcome presentation"; F-15 "DEL-01-02…05 definitions are a later undertaking; seams S-1…S-4 have no receiving comparison in this one" | Cite NIR §4–§6 as S-3's receiving side. Close F-15 per seam: S-1 by RECOVERY §1 (D1), S-2 by NPTD §2 (D2), S-3 by NIR (D3). **Gap:** D4 returned no explicit receiving comparison of S-4; F-15 stays open for S-4 until DEL-01-05 states one (gap **G-1**) | D1, D2, D3 | — |
| FH-20 | D3 J-H7 + D1 H-7 (§11 part) | §11 rows (L1468, L1470, L1477) | "Request cards, answers, outcomes, attachments \| DEL-01-04 \| S-3 \| Cards, answer UX"; "Durable session/request custody… \| DEL-01-02"; "A14 answer tool permission \| The person (via DEL-01-04)…" | Point to NIR §4, AAC, RECOVERY; no change of meaning. The DEL-01-03 row (L1469) and DEL-01-05 row (L1471) also gain pointers to NPTD and ACCESS (no D row asked; consistency) | D3, D1 | — |
| FH-21 | D3 J-H8 | §6.3 R9 person-input bullet (L700) | "the App may answer it by presenting its own act control (EXEC CAP-2)" | Cite AAC (PROPOSED) and NIR LB-4: an "Open the App act control" entry on every question card, never pre-filled from an arrival | D3 | — |
| FH-22 | D3 J-H9 | U-26 (L1734) | "App implementation owner with DEL-01-04 (answer path) and DEL-01-02 (custody)" | DEL-01-04 accepts the order and gives each reason words (NIR §4.4) | D3 | — |
| FH-23 | D4 #7 | §6.8 configuration-write row (L844) | "App, only as **person-directed** through the owning interface (DEL-03-03 OC-3; DEL-01-05)" | DEL-01-05 writes with explicit `filePath` and `expectedVersion`; no credential written (Q-8, CR-8). OBS-2: writes through a symlinked `config.toml` were not exercised (UNRESOLVED of the record) | D4 | open (O-6) |
| FH-24 | D4 #8 | §8.1 L-5 (L1011) | "Which flows the App offers is DEL-01-05's (S-4)" | Offered: `chatgpt` (browser), `chatgptDeviceCode`, `apiKey` (in H-key under K2-1). Not offered: `chatgptAuthTokens`, `amazonBedrock*`, gateway OAuth (v0.1). "In H-key" waits on U-A1 | D4 | — |
| FH-25 | D4 #9 | §8.3 (L1086) | "class … derived from the provider configuration the person chose (DEL-01-05)" | Class from entry kind: `chatgpt-account`/`api-key` → `user-chosen cloud`; `local-provider` → `local model server` (RS R5 values unchanged) | D4 | — |
| FH-26 | D4 #10 (+ OBS-2) | §9.1 redaction; U-13 (L1722) | U-13 "Categories extended (§9.1)" | Add `account/login/start` `apiKey`, `accessToken`, `secretAccessKey`, `sessionToken`; responses `authUrl`, `verificationUrl`, `userCode`; error texts as text; `account/read` `email` as identity category (CR-2, CR-4). **Add from OBS-2 §6.1, §11:** every model request's `client_metadata` carries the installation id and thread/session/turn ids to the provider, and the host time zone is in every model input | D4; OBS-2 | chg (adds categories) |
| FH-27 | D4 #11 | F-14 (L1556–1559) | "…a separate App account home would be "fresh" at least once per home" | Stands per App home; **O-7: `[features] plugins = false` stops the fresh-home ≈24 MB fetch and the warm `ls-remote`** (v1, v8) | D4 | chg (O-7 answers) |
| FH-28 | D4 #12 | F-18 (L1578) | "`~/.codex` changed during the spike window…" (relevant to OI-009) | Under K-1 option C the App writes the person's home only by person-directed configuration writes | D4 | — |
| FH-29 | D4 #13 + OBS-2 | §8.1 L-4 (L1010); U-18 (L1727) | L-4 "…whether a setting disables it: not-observed"; U-18 "Owner with DEL-01-05" | K-12 decided; settings table and two-source network view are ACCESS §9. **O-7 fills the "App action" column:** `plugins = false` stops both start-up connections (chatgpt.com featured plugins; github.com plugin repo); `remote_plugin`, `apps`, `remote_control` (feature `removed`) do not; the remote-control loop stops only with the internal env var `CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED=1` and opened no socket without sign-in. Whether the App may use an internal env var is integrator item **C-25** | D4; OBS-2 | chg |
| FH-30 | D4 #14 | U-03 (L1712) | "`UNRESOLVED{OI-009}` account home…" | Closed at choice level (K-1); mechanism observed (O-6 M1/M2); separation of credentials with a credential not observed (M4/M5) | D4 | conf / open (M4–M5) |
| FH-31 | D4 #15 | U-12 (L1721) | "One active child assumed" | **Per-home dimension** if K2-1 stands (owner U-A1): one child per App account home; generation, register, thread keyed by home. Report only (R17-2). Conflict **C-11** with RECOVERY's single process | D4 | — |
| FH-32 | D4 #16 | U-22 (L1731) | "L-2 provider wire interface (Responses) and L-3 \| DEL-01-05…" | Carried into ACCESS §11 CH-1…CH-3. **Add from O-4:** the delegation tool set also travels in the `namespace` tool LM Studio drops, so on that route delegation is unavailable too (extends F-31) | D4; OBS-2 | chg (O-4) |
| FH-33 | D2 J-2 = D6 J-3 | §8.4 HCG-A08 (L1168) | "`multiAgentMode` on thread and turn start (experimental-only)" | `multiAgentMode` is "@deprecated Ignored" (verified in the committed bundle). Replacement signal is conflict **C-04** (D2: replace with `Model.multiAgentVersion`; D6: add it). OBS-2: delegation gated by feature `multi_agent` (stable, default on) / `multi_agent_v2`; tools offered only inside a `namespace` tool; `config/read` shows no `features` unless set | D2, D6 | chg (O-4, O-8) |
| FH-34 | D6 J-4 | §8.4 / F-20 (L1594) | F-20: `instructionSources` "routed to DEL-04-03 and DEL-02-04 as candidate evidence" | Consumed by ROLE §4.3. Add child-role facts `Thread.parentThreadId`, `Thread.agentRole`, `SubAgentSource.thread_spawn.agent_role` — **now observed** (O-4 via adapter: child `thread/read` shows them; `agentNickname` too). OBS-2 also: no `thread/started` for a child; children absent from `thread/list`, present in `thread/loaded/list`; every `instructionSources` was `[]` (cwd had no AGENTS.md) | D6 | conf (O-4, O-4a) |
| FH-35 | D2 J-4 | VC-09 (L1758) | "revision identity left to DEL-01-03" | Cite NPTD §5.2 RV-1, RV-2. OBS-2 O-8: in plan mode only a `plan` item (`item/plan/delta`), no `turn/plan/updated` | D2 | chg (O-8) |
| FH-36 | D6 J-1 | §8 seams S-6 (L965) | Receiver "DEL-02-04 (inputs from DEL-02-01/02-02)"; carriers "`baseInstructions` and `developerInstructions` on thread start and resume"; not supplied "Guidance composition, role files, workflow semantics, idle-boundary change policy" | Composition and idle-point policy defined in ROLE §5.1, §5.4; App uses `developerInstructions` only, never `baseInstructions` (R17-8); `thread/fork` also carries both (F-R1). **O-5: on `thread/resume` the input is accepted and ignored** (loaded or not), so "on … resume" must read "accepted, not applied at 0.158.0" | D6; R17-8 | chg (O-5) |
| FH-37 | D6 J-2 + OBS-2 | §8.2 (L1020–1024) | "the base/developer instruction elements of thread start and thread resume"; "the source identity supplied by the composing owner" | Add carriers: `thread/fork`; experimental `turn/start` `collaborationMode.settings.developer_instructions` (O-5b: **applied, added** to the thread's own text); thread `config` keys `instructions`, `developer_instructions`, `agents.<ROLE>.config_file` (O-4a: role file's `developer_instructions` **replace** the parent's for the child). Source identity = ROLE supply record. P-15 is now observed (resume ignored) | D6; OBS-2 | chg (O-5, O-5b, O-4a) |
| FH-38 | D6 J-5 + unclaimed | §8 receivers table DEL-02-04 row (L982); rows L985–L986; F-16 (L1568) | "DEL-02-04 (outside the first increment)"; "DEL-01-02, -03, -04, -06 (outside; D1)"; "DEL-01-05 (outside; D1)" | DEL-02-04 row cites ROLE-v0.1; mirror row still a register proposal (C1-B R-11-1). **Unclaimed:** L985–986 still say "(outside; D1)" for DEL-01-02…05 — point to RECOVERY, NPTD, NIR/AAC, ACCESS | D6; F0 sweep | — |
| FH-39 | D6 J-6 | §5.1 / S-4 (thread `config` map) | **Premise:** no current text; D6 says "Not stated for role supply" (confirmed: HOSTING has no sentence on the App's per-thread `config` for roles) | Add: App's per-thread `config` from DEL-02-04 limited to additive `agents.<ROLE>.description/config_file`, omitted for names the person's configuration defines; never `features.*`, `agents.enabled`, `agents.max_depth`, approval or sandbox (ROLE §5.2, §5.3; K-10; H9). O-4a confirms `agent_type` lists the role beside built-ins `default`, `explorer`, `worker` | D6 | conf (O-4a) |
| FH-40 | D5 J-28 | §8 S-6; §11 "Workflow semantics / making / registration" | — | No change needed (record only): DEL-02-02 supplies DEL-02-04 the selection record and resolved revision (R17-8; WR §7) | D5 | — |
| FH-41 | OBS-2 (no D item) | §10.1 OBS-1/OBS-1b; U-19 (L1728); PIN-SPIKE P-15 references | §10.1 lists OBS-1 and OBS-1b only; U-19 "Recorded as not observed…" | Add an OBS-2 row set (O-1…O-8 summary, standing "dated observation, not qualification", the adapter caveat for O-4) and narrow U-19 to what remains (interrupt during an `agentMessage`; signed-in remote control; M4/M5; writes through a symlink) | OBS-2 | new |
| FH-42 | OBS-2 (no D item) | U-05 / §4.4 restart rules; recovery reads | — | O-2: after restart `thread/read` works before `thread/resume` (thread `notLoaded`); `thread/read {includeTurns}` and `thread/resume` without `excludeTurns` emit `deprecationNotice` (use `thread/turns/list`, `thread/items/list`). Bears on RECOVERY R-4 and NPTD SQ-4 | OBS-2 | new |
| FH-43 | OBS-2 (no D item) | §6.2.1 RT-10 | RT-10 `resolved-by-supplier` (PROPOSED reading) | Provoked live (O-3): after `turn/interrupt`, `serverRequest/resolved` arrives **after** `turn/completed`; the command item never completes and is not in history | OBS-2 | conf |
| FH-44 | (header) | Header L13; "Changes" | L13 "…the standalone-App definitions DEL-01-02…05 are a later undertaking…" | Version step v0.9 header line naming the pass-3 receivers; change logs (e.g. L86) are history and stay unchanged | F0 sweep | — |

### 1.2 EXEC-v0.6 — `DEL-02-03/Design/EXECUTION_COMPATIBILITY.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FE-01 | D1 E-1 | §2.5.2 AE-7 (L649); §4.9 RE-6 (L1320); CE-17 | "The person's stop (V4-EXE-01) or the run owner's end (RE-6)"; "*The person* names the person's own stop (V4-EXE-01; PANEL RI-3)" | "The person's end of the run (DEF-4)"; a turn interrupt (DEF-3), quit (DEF-6), supplier exit (DEF-5b) never end a run; relaunch leaves the run interrupted (RE-4) | D1; R17-3, R17-14 | — |
| FE-02 | D1 E-2 | AE-6 (L648); §2.6 A-4 (L703) | "HOSTING §4.3 unexpected exit; recovery through thread reads (post-restart results not observed, PIN-SPIKE P-13)"; A-4 "Notification stream lost or the supplier exits" | Observed from DEL-01-02's `observation_lost`/`observation_recovered`; window close is not observation loss (DEF-1); no separate "stream lost" cause (DEF-2). O-2 now observes post-restart reads: the turn reads `interrupted` after both stop and kill | D1 | conf (O-2) |
| FE-03 | D1 E-3 | §2.7 last paragraph (L743) | "The in-flight request register and custody across restart are DEL-01-02's (HOSTING S-1, outside this increment); the recorder only reads what is delivered." | Point to RECOVERY-v0.1; the run starter tags the conversation with its run reference (RECOVERY §4.1) so RE-4 finds the thread after relaunch | D1 | — |
| FE-04 | D1 E-4 | §4.9 RE-4 (L1307); §2.6 A-11 (L710) | "…an App restart or a loop restart without a run-ended event leaves the run **interrupted** and resumable as the same run" | Cite `app_restart_interruption` and the tag lookup; otherwise unchanged | D1 | — |
| FE-05 | D2 J-5 (+ D6 J-3) | §3.4 EV-3a row `agent-delegation` (L835) | "The thread's start reports a `multiAgentMode` (…none of them withdraws delegation…)"; rule "**Active** (experimental opt-in)" | `multiAgentMode` constant/ignored → no information. Replacement signal per ruling **C-04**; label per **C-05** (delegation is stable at 0.158.0). OBS-2: delegation also needs a provider that accepts `namespace` tools (O-4), so the reading should mirror `mcp-tool-call`'s `namespaceTools` limit | D2 | chg (O-4) |
| FE-06 | D3 J-E1 | §5 closing (L1496–1497) | "Construction of the control is DEL-01-04's (later undertaking, D1). App-side positive capture cases are therefore **AWAITING INPUT** (CH-23)." (script miss was the bold; text confirmed) | "Designed in DEL-01-04/AAC-v0.1, PROPOSED until SCA-V4-003 carries SC2-01-04-1 as amended (SC3-01-04-1). CH-23 (ii) ran on DEL-01-04's model; a candidate and a person are still needed." | D3 | — |
| FE-07 | D3 J-E2 = D5 J-17 | §5 CAP-1 (L1486), CAP-2 wording list (L1487) | "It also covers A12 where an App control is the control that establishes the setting"; wording list "mark checked" A4 … "set grant" A12 | CAP-1: add A15 on a reviewed workflow draft, composed from DEL-02-02's A15 descriptor (K-8); CAP-2: add "register workflow revision" (A15); decline only where ACT §2.3 defines one | D3, D5; K-8 | — |
| FE-08 | D3 J-E3 | §5 CAP-3 (L1488) | Capture-evidence elements listed | Format is `aac.capture-evidence.schema.json` | D3 | — |
| FE-09 | D3 J-E4 | §2.4.4 opening (L529) | "The display is built by the App's interface owner (DEL-01-04, later); its meanings go to DEL-05-02 and DEL-04-02 (§9.2)." | R17-7 wording: DEL-04-02 defines components (AS §13 K-5, K-6); DEL-01-04 places them and owns behaviour (NIR §9); SD-1…SD-5 are the meanings shown | D3; R17-7, R17-14 | — |
| FE-10 | D3 J-E5 | §2.4.1 RC-6 (L449) | "(CAP-2; construction DEL-01-04, later; its obligation proposed…)" | "(CAP-2; DEL-01-04/AAC-v0.1, PROPOSED…)" | D3 | — |
| FE-11 | D3 J-E6 | §2.5.2 AE-2 standing (L644) | "AWAITING INPUT (DEL-01-04's control)" | "DESIGNED (DEL-01-04/AAC-v0.1, PROPOSED); positive case needs a candidate and a person" | D3 | — |
| FE-12 | D3 J-E7 | §9.1 row DEL-01-04 (L1799); §10 row (L1834) | "Not in this undertaking. DEL-01-04 has no Design file, and its ScopeOfWork does not name an act control…"; "App act control construction \| DEL-01-04 (later, D1)" | AAC-v0.1 and NIR-v0.1 exist; SoW still lacks the obligation (SC3-01-04-1) | D3 | — |
| FE-13 | D3 J-E8 (conditional) | §2.4.1 RC-4 or §2.4.4 SD-3 | — | Only if the integrator accepts U-NIR-5: "Opening the App act control from an arrival's row by the person's own click … is not reacting" | D3 | — |
| FE-14 | D5 J-12 | §6.5 HR-4 (L1587) | "New tuple: … derived-from = host tuple" | Add: new revision of the App slot when the host tuple's lineage reaches it (K-6; WR DS-2), new workflow when empty (DS-1), else refused (DS-3) | D5; K-6 | — |
| FE-15 | D5 J-13 | §6.5 closing (L1592); §11 F-12 | "The changed-draft return path belongs to DEL-02-02 and is not compared in this undertaking (D1); see finding F-12" | Cite WR §6 SQ-H; F-12 closable at the next comparison | D5 | — |
| FE-16 | D5 J-14 | §7.3 RT-6 (L1724), RT-7 (L1725) | "registration is DEL-02-02's (later)"; "no silent overwrite (slot policy DEL-02-02, U-10)" | RT-6 cites WR SQ-H, prototype P-32; RT-7 cites K-6 (WR §4.1) and SL-2 | D5 | — |
| FE-17 | D5 J-15 | U-E19 (L1931) | "Selection slot policy and host precedence (WD U-10); registration as an act (AP U-08) \| DEL-02-02 (later)…" | Second half stale (ACT closed U-08 at R12-5); slot policy decided by K-6; App selection PROPOSED (WR SL-2/SL-3); host precedence open (DECISION-3) | D5; R17-14 | — |
| FE-18 | D5 J-16 | §9.1 row DEL-02-02 (L1800); §9.2; §10 row (L1825) | "DEL-02-02 (later, D1…)"; "Review, registration, selection policy, drafts \| DEL-02-02 (later, D1)" | Point to WR-v0.1 §4, §6, §7; the selection record (WR §8) is what A-1/CK-1 receive | D5 | — |
| FE-19 | D6 J-10 | §2.6 A-3 (L702); §6.1 *supplied* (L1518) | "…through the supplier's additive guidance inputs (HOSTING S-6; DEL-02-04)"; "App: DEL-01-01 HOSTING §8.2 via DEL-02-04" | Cite ROLE §5.1, §6.1; the check receives the role in force, possibly **no role**; ROLE SL-7 proposes "shown before the run, recorded, person may proceed" for a role outside the compatible roles (U-R10, EXEC owns the reading) | D6 | — |
| FE-20 | D4 #19 | §5 CAP-8 (L1493); also L116, L1920 | "…the Codex account when Codex reports one" | Supplied by DEL-01-05 as `{kind: chatgpt, email\|null, planType}` of the home that runs the conversation; none for `apiKey`. Shape vs RS: **C-10** | D4 | — |

### 1.3 RS-v0.8 — `DEL-04-03/Design/RECORD_SEMANTICS.md` (+ `RS_RECORD.schema.json`, examples)

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FR-01 | D1 J-RS-1 | §3 run-ended row (L232) | "That the run stopped (V4-EXE-01): who stopped it…" | "That the run ended (DEF-4 of RECOVERY-v0.1)…"; a turn interrupt is never a run end. (Whether RS records a turn interrupt at all is D1 U-R6, RS's call) | D1; R17-3, R17-14 | — |
| FR-02 | D1 J-RS-2 | §4 R13 Supplier cell (L286); schema `toolPermissionSettlement.settlement` (schema L1902–1907) | "DEL-01-01 observed facts in this undertaking; DEL-01-02 later (D1)"; enum `answered`, `declined`, `errored` | Supplier: "DEL-01-01 observed facts; DEL-01-02 custody facts (RECOVERY §8.2)"; add settlement *ended unanswered (process exit)* with context, and *resolved by supplier* (DEL-01-01's fact) — the latter **now observed** (O-3) | D1 | conf (O-3) |
| FR-03 | D1 J-RS-3 | U-20 (L1231) | "U-20 R13 feed beyond DEL-01-01 observed facts \| DEL-01-02 (later, D1)…" | Closed: exactly two DEL-01-02 facts (`request_ended_unanswered`; `acknowledgment_not_observed` → R11 "lost acknowledgement") | D1 | — |
| FR-04 | D1 J-RS-4 + D3 J-R5 + D5 J-22 + D6 J-12 (§10 part) | §10 row "DEL-01-02, DEL-01-04, DEL-02-02, DEL-02-04" (L661); §10.1 rows (L699 and the DEL-01-04/02-02/02-04 rows) | "…Outside this undertaking (D1)"; "role bytes"; "the registration control that captures A15"; "(a later undertaking, D1; U-20)" | One row edit, four contributions: RECOVERY §8 (custody-event format; R11 "App-restart interruption" from `app_restart_interruption`); AAC (X-1 designed, PROPOSED); WR (registration designed; A15 captured by DEL-01-04's control; `library_entry` cites the A15 record); ROLE (supply record) | D1, D3, D5, D6 | — |
| FR-05 | D3 J-R1 = D5 J-21 (HA-10 part) | §6.2 HA-10 (L507) | "at the registration control (DEL-02-02's, a later undertaking, D1)" | "at DEL-01-04's App act control (K-8)" | D3, D5; K-8, R17-14 | — |
| FR-06 | D3 J-R2 = D5 J-21 | §6.1 Relations (L474, L510); schema `$defs.humanAct.relations` + A15 `allOf` (schema L774, L1378, L1405, L2073); `RS_RECORD.valid.act-log.example.jsonl` line 1 (`"relations": {"derivedFrom": "draft:supports-adjust@d-12"}`); VC-37 | "for A15, **derived from ⟨draft⟩** … required for A15"; schema requires `derivedFrom` for A15 | `reviewedDraft` (required for A15) and `priorRevision` (null for a first revision); rewrite the A15 `allOf`; update record 1 and VC-37 (R17-11). D5 P-36 shows the schema refuses the new names today. **Shape is conflict C-01** (string vs object) | D3, D5; R17-11, R17-14 | — |
| FR-07 | D3 J-R3 | §6.1 "Capture evidence references … App interface per EXEC CAP-1…" (L472); §9 | No object format | Capture evidence = `aac.capture-evidence.schema.json`, resolved by `cap:` reference | D3 | — |
| FR-08 | D3 J-R4 (conditional on SEAL-2) | §14.2 R-7; §4 R11 | — | Reader rule "capture not verifiable" for an App-interface entry without a valid seal; matching R11 label. Waits on U-AAC-3 | D3 | — |
| FR-09 | D6 J-11 | §4 R3 (L275); §13.3 `supplied_guidance`; `$defs.suppliedGuidance` (schema L543, L1837); `RS_RECORD.valid.app-run.example.jsonl` line 16 | "supplied ≠ adopted"; one `sourceIdentity` string and one `content` per entry | Body = ROLE supply record by relative-path reference; R3 "limits" = ROLE limit account reference; new entry kind `role_limit_observation`; re-express fixture line 16 (`"sourceIdentity": "role:WORKING_ITEMS"`). O-5: supply on resume is not applied — "supplied ≠ adopted" now has an observed instance | D6 | conf (O-5) |
| FR-10 | D6 J-12 (R5a part) | §4 R5a (L278) | Supplier "DEL-05-01 / DEL-02-01" | App runs: role in force from the ROLE supply record's selection, or "no role" | D6 | — |
| FR-11 | D5 J-23 | U-05; §14.2 R-1 (L1136) | "where the logs live is OI-014's, U-05" | DEL-02-02 needs a per-library location for act records made outside a run (A15), travelling with the library; WR placeholder `<library>/.chirality/records/acts.jsonl` (AAC agrees, leaves U-05 open) | D5 | — |
| FR-12 | D4 #19 | §6.1 *Decision actor* (L465); schema `$defs.person.codexAccount` (string) | "…the Codex account when Codex reports one" | DEL-01-05 supplies `{kind, email\|null, planType}`; RS keeps a string — mapping is **C-10**; email vs digest is RS's (D4 U-A8) | D4 | open (O-6 had no credential) |
| FR-13 | D4 #20 | R5 / schema `destinationClass` | `local model server`, `user-chosen cloud`, `unknown` | No change; record that DEL-01-05 maps entry kinds onto these values | D4 | — |
| FR-14 | unclaimed | L16, L1223, L1236 | "DEL-01-04 and DEL-02-02 are outside this undertaking (D1)"; "the registration control stays DEL-02-02's (later, D1)"; "control construction DEL-01-04 (later, D1)" | Pointer refresh to AAC/WR (same meaning as FR-04/FR-05) | F0 sweep | — |

### 1.4 ACT-POLICY-v0.8 — `DEL-04-01/Design/ACT_AND_POLICY_CONTRACT.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FA-01 | D3 J-A1 | §2.6 row A4/A6/A7 on App content (L495) | "The control is built by DEL-01-04 in a later undertaking." | "…designed in DEL-01-04/AAC-v0.1 (PROPOSED)" | D3; R17-6 | — |
| FA-02 | D3 J-A2 = D5 J-20 | §2.6 A15 row (L498) | "The App's registration control, operated by the person (DEL-02-02; built in a later undertaking, D1)"; non-evidence list includes "a successful trial run" | Capturing surface: DEL-01-04's App act control, composed from DEL-02-02's A15 descriptor (K-8). Non-evidence: "a trial in conversation (K-7: drafts are not run)"; add "a registration ledger line without a capture" | D3, D5; K-7, K-8, R17-14 | — |
| FA-03 | D5 J-18 (+ D3 J-A2 §2.1 part) | §2.1 A15 row (L317); also L112 | "Capture evidence from the registration control (DEL-02-02, later undertaking, D1)"; content "the revision identity and the draft it derives from"; purpose "make it available in the project" | Evidence from DEL-01-04's act control (K-8; R17-6) from the A15 descriptor; content "revision identity (= reviewed draft content identity) and, for a new revision, the prior revision (R17-11)"; purpose "…in the project library" / "…in the user library" (AAC already uses "project library") | D5, D3 | — |
| FA-04 | D3 J-A3 = D5 J-19 | §2.5 A15 row (L425) | "Revision identity … with *derived from ⟨draft⟩*" | "with *reviewed draft* ⟨draft, content identity⟩ and, for a new revision, *prior revision* ⟨tuple⟩ (R17-11)" — element shape per **C-01** | D3, D5; R17-11, R17-14 | — |
| FA-05 | D3 J-A2 (§4.7 part) = D5 J-24 | §4.7 RC-3 (L1158) and A15 paragraph (L1164–1165) | "the registration control for A15"; "the registration control captures the A15; the record binds the revision identity and the draft it derives from" | "the App act control (DEL-01-04) for A15"; "binds the revision identity, the reviewed draft content and, for a new revision, the prior revision" | D3, D5 | — |
| FA-06 | D3 J-A4 | §10.3 row DEL-01-04 (L1708) | "§10.1 (V-01, V-05, V-07, V-08, V-21)" (mapped, no receiving side) | Point to NIR §8 (V-01, V-07, V-08), §4 (V-21), §9/AS facets (V-05) | D3; R17-14 | — |
| FA-07 | D5 J-25 | §10.3 row DEL-02-02 (L1709) | "DEP-02-02-016 · none · Not mapped in detail (U-08)" | "§2.1 A15, §2.5, §2.6, §4.7, FX-56 (WR §4.3, §9)" | D5 | — |
| FA-08 | D5 J-26 (+ unclaimed L1651, L1947) | §13 FX-56 (a) (L1905); L1651; L1947 | "registers revision rev-4 … at the registration control"; "A15 also DEL-02-02 (later, D1)"; "the registration control stays DEL-02-02's (later undertaking, D1)" | "… at the App act control (DEL-01-04)"; (b), (c) stand (WR P-08, P-15 run them on doubles). L1651/L1947 pointer refresh | D5; F0 sweep | — |

### 1.5 AS-v0.8 — `DEL-04-02/Design/AUTONOMY_AND_STANDING_EXCHANGE.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FS-01 | D3 J-S1 | §13 (L844) | "**No option is chosen here** (R12-2)" (script miss was the bold) | Record R17-7: for App surfaces DEL-04-02 defines K-5/K-6 and DEL-01-04 builds them in the App (CS-3's split; NIR §9); code placement stays OI-014 | D3; R17-7 | — |
| FS-02 | D3 J-S2 | §12 receivers (L763); §12.1 (L792) | DEL-01-04 absent | DEL-01-04 receives §4, §8, §9 and K-5, K-6 (new row NR-1, held) | D3 | — |

### 1.6 WD-v0.8 — `DEL-02-01/Design/WORKFLOW_DECLARATION.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FW-01 | D5 J-1 | §3.9 OS-1, OS-2 (L493–494) | "App drafts are DEL-02-02's (later)"; "…non-regular entry: revision not established (RV-2)"; "DEL-02-02 (later)" | Cite WR §4, §6; OS-2: "A15, captured by DEL-01-04's App act control and bound to the reviewed content (K-8); a non-regular entry is refused before review (WR HY-3)" | D5; K-8 | — |
| FW-02 | D5 J-2 | §3.9 OS-3 (L495) | "The person selects a full identity tuple (C-2)…" | Add "a draft is not selectable (K-7); a selection stays on its revision (WR SL-2)" | D5; K-7 | — |
| FW-03 | D5 J-3 | §6.1 after RV-5 (L1346) | "Whether registration refuses them [OS files] is DEL-02-02's" | "Registration refuses them, naming them (WR HY-4, PROPOSED)" | D5 | — |
| FW-04 | D5 J-4 | §6.3 C-4 (L1371) | "Whether a selection follows a new revision of the same slot or stays pinned is a selection policy of DEL-02-02 (App) and the host" | App side: pinned, newer shown, following is a new selection event (WR SL-2, PROPOSED; owner only if a following default is wanted, U-WR-13). Host side unchanged | D5; K-6 | — |
| FW-05 | D5 J-5 | §6.3 C-5; §12 U-10 (L1573) | "DEL-02-02 (later undertaking) with DEL-02-01 and host owner" | App side PROPOSED in WR SL-3; U-10 open for the host part (DECISION-3) | D5 | — |
| FW-06 | D5 J-6 | §6.4 row 3 (L1387) | "A refinement is a draft (DEL-02-02) and, once registered, a new identity with derived-from = the host tuple" | Add: "registered as the next revision of the App slot its lineage reaches (K-6; WR SP-3, DS-2), otherwise a new workflow" | D5; K-6 | — |
| FW-07 | D5 J-7 | §7 row "Drafts in `.chirality/workflow-drafts/`…" (L1423) | "**Not part of this contract**; DEL-02-02" (script miss was the bold) | "WR §3, §4: drafts kept there; registration through DEL-01-04's act control; a revision series per slot, nothing overwritten (K-6, K-8)" | D5 | — |
| FW-08 | D5 J-8 | §8 receivers row DEL-02-02/DEL-02-04 (L1444); §12 U-17 | "Not exercised in this undertaking"; "(later undertaking per D1)" | WR receives §3, §6, §4.6 (WR §7); references `$defs/workflow_identity` by `$id`; a record, not a placement confirmation (OI-014). DEL-02-04 half → ROLE (with FW-12/FW-13) | D5, D6 | — |
| FW-09 | D5 J-9 | §13.1 VC rows (L1690) | "Library and selection doubles (DEL-02-02, later)" | Doubles exist in WR `prototype/wrproto.py` (P-22…P-29) | D5 | — |
| FW-10 | D2 J-6 | §4.2.5 row `agent-delegation` standing (L630) | "`multiAgentMode` … is experimental-only" | Add "and deprecated (ignored)"; delegation needs no opt-in to be seen (O-8 confirms: feature `multi_agent` stable). Signal and label per **C-04/C-05** | D2 | chg (O-4, O-8) |
| FW-11 | D6 J-7 | §5.2 App column (L1286–1287) | "Person selects a role (DEL-02-04)"; "Product `AGENTS.md` plus role guidance"; distribution `UNRESOLVED{OI-018}` | "Person selects a role or none (R17-9; ROLE §3)"; guidance from the seeded editable copy (K-9; ROLE §4.2); OI-018 answered for the App by K-9, open for hosts | D6; K-9, R17-9 | — |
| FW-12 | D6 J-8 | §3.9 OS-7 (L499); §3.5 CR-7 (L365) | "The agent is given `WORKFLOW.md` (prose and block together) with its role guidance"; "The agent receives the prose and the block together when it reads the file" | OS-7: the registered revision's `WORKFLOW.md` is composed into `developerInstructions` after product guidance and role, re-verified at composition (ROLE CO-3, CO-4). CR-7: "when it is supplied, or reads the file"; other files read by tools are not supply evidence (R17-8). O-5: composition reaches a thread only at start/fork (resume ignored) | D6; R17-8 | chg (O-5) |
| FW-13 | D6 J-9 | §7 "Four-section role files" (L1427); §9 A-6 (L1496); §12 U-14 (L1580) | "Leave to DEL-02-04 / OI-018"; "DEL-02-04 (later)" | ROLE §4.2: four role files in the App store, structure not checked; A-6 consumer ROLE-v0.1; U-14 narrowed to hosts | D6 | — |

### 1.7 WD-EX-v0.8 — `DEL-02-01/Design/EXAMPLES.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FX-01 | D5 J-10 | E3 last column (L1047–1048) | "a refinement is a DEL-02-02 draft until reviewed and registered"; "…if registered as a new App workflow" | "registered in LIB-A1 as the next revision of `supports-adjust` (⟨rev-A3⟩; K-6), derived-from = host tuple ⟨rev-3⟩" | D5; K-6 | — |
| FX-02 | D5 J-11 | E4 step 3 (L1070) | "whether the run follows ⟨rev-4⟩ is host/DEL-02-02 policy (U-10)" | App side: pinned (WR SL-2); host side open | D5 | — |

### 1.8 CA-v0.6 — `DEL-09-06/Design/CONNECTED_ACTIVITY_CONTRACT.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FC-01 | D5 J-27 | §2.1 "Workflow maker" row; §3.1 opening; §4 rows; §6 ST-5; §8.2 W14-01, W14-09; §8.5; §12 F-1 (L957); UNRESOLVED row (L1210) | "OUT-003 cannot complete in this undertaking (DEL-02-02 registration outside D1)"; "DEL-02-02 registration (later undertaking, D1)" | Registration designed in WR-v0.1 (PROPOSED; not built); ⟨rev-A3⟩ is revision 2 of LIB-A1's `supports-adjust`, derived-from ⟨rev-3⟩; F-1's first reason narrows to "not built"; its SWBPIPE reason stands. **Executor check list** (same meaning, same pass): L29, L47, L109, L308 (DEL-01-04 act control "later"), L513, L559, L562, L629, L709, L713 (DEL-01-04 "later"), L717, L878, L1217. `FACTS_SQ01_SQ32.md` and `RELAY_ANSWERS_SWBPIPE.md` are never edited | D5; F0 sweep | — |

### 1.9 ADAPTER-v0.6 — `DEL-03-03/Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FD-01 | D1 J-AD-1 (+ unclaimed L101, L1238) | §5.6 PI-6 (L898–899); XF-41 (L1336); UNRESOLVED (L1748); L101; L1238 | "Custody of the in-flight native item across relaunch is DEL-01-02's (later undertaking, D1)"; "in-flight custody **AWAITING INPUT** (DEL-01-02, later undertaking, D1)"; L101 "(with DEL-01-04/01-05 in a later undertaking, D1)" | `observation_lost.inFlightItems` gives item/turn/thread; `app_restart_interruption` the relaunch; recovery reads Codex's status; the adapter's outcome rule stands. O-2/O-3: an in-flight command item at a stop or interrupt is **absent from history** (never completed) — the adapter reads "not recovered", never "completed". L101/L1238 pointer refresh; L1589 is change history, unchanged | D1; F0 sweep | conf (O-2, O-3) |

### 1.10 XT-v0.6 — `DEL-09-09/Design/EXTERNAL_TRACE_CASES.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FT-01 | D1 J-XT-1 | XC-06 (L184) | "App-restart custody DEL-01-02 (later, D1)" | Cite RECOVERY §5 SQ-R and §8.2 (and optional row NR-D1-3) | D1 | — |

### 1.11 LOOP-v0.8 — `DEL-05-01/Design/LOOP_RECEIVING_CONTRACT.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FL-01 | D4 #17 | §10.3 row "Local-server capability requirements" (L2338) | "Not supplied, and not consumed by this file. DEL-01-05 is a later undertaking (D1)" | Supplied (PROPOSED) as ACCESS §11 and `capability-handoff.valid.json`; whether LOOP consumes it is DEL-05-01's (pass-2 R-0501-4) | D4 | — |
| FL-02 | D4 #18 | §1 table, App "Model interface" (L341) | "…It is **unobserved** on an identified candidate (HOSTING L-2/P-11…)" | Observed at one pair (OBS-1 OB-8), not qualified; CH-1. OBS-2 adds that LM Studio drops `namespace` tools, so delegation tools do not reach the model either | D4; OBS-2 | chg (O-4 adds) |

### 1.12 GUIDE-v0.5 — `DEL-03-04/Design/HOST_INTEGRATION_GUIDE.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FG-01 | D6 J-13 | Row 8 (L343); M8.6 (L440); X-06 (L495); G-1 (L876); CC-2; header (L58) | **Quote paraphrased:** D6 quotes "DEL-02-04 has no Design file; M8.6 rests on SoW meaning plus HOSTING S-6"; the file says (G-1, L876) "Additive role supply (DEL-02-04) and the App act control (DEL-01-04) have no Design file; M8.6 rests on SoW meaning plus HOSTING S-6, and M5.3 on EXEC §5". Premise holds | M8.6 rests on ROLE-v0.1 §3–§6 with HOSTING S-6/§8.2 and WD §5; G-1's role-supply half closes; input table gains ROLE-v0.1 | D6 | — |
| FG-02 | **gap** (D6 assigns to D3; D3 returned no GUIDE row) | G-1 act-control half (L876); M5.3; L399 ("App act control for App content (built by DEL-01-04, D1)"; "DEL-01-04 has no Design file and offers nothing") | as quoted | G-1's act-control half closes against AAC-v0.1 (PROPOSED); M5.3 rests on EXEC §5 with AAC; L399 pointer refresh. Gap **G-2** | F0 | — |
| FG-03 | D5 note | M8.2, M8.5, M8.7, HC-8.6 (L343, L439, L441, L771) | "Registration, drafts and selection policy DEL-02-02 *(outside undertaking, D1)*" | Pointer to WR-v0.1 when GUIDE is re-pinned (header L58 lists DEL-02-02, DEL-02-04, DEL-01-04 as without Design files) | D5 | — |

### 1.13 PANEL-v0.8 — `DEL-05-02/Design/PANEL_RECEIVING_CONTRACT.md`

| F-ID | D items | Section (line) | Current text (verified) | What is needed | Source | OBS-2 |
|---|---|---|---|---|---|---|
| FP-01 | D5 note | §6 (L842, L881) | "The App's registration control (DEL-02-02, later undertaking)"; "App workflow experience (DEL-02-02, later undertaking per D1)" | Pointer only: A15 captured by DEL-01-04's act control from WR's descriptor. Optional in this pass (D5: "only a pointer … when GUIDE is re-pinned") | D5 | — |

### 1.14 Unclaimed stale pointers (sweep result)

Lines in first-increment files that still call a pass-3 deliverable "later",
"(D1)", "outside this undertaking/increment" or "without a Design file", and
that no D join names. Each needs only a pointer to the new file, with no
change of meaning; change-log sections stay as history.

| File | Lines | Already in a row above |
|---|---|---|
| HOSTING | L13 (header), L985, L986 | FH-38, FH-44 (L86 is change history: leave) |
| EXEC | L25, L291, L293, L1773, L1920 (and L1800, L1825 via FE-18) | add to FE-12/FE-18 |
| RS | L16, L1223, L1236 | FR-14 |
| ACT | L1651, L1947 | FA-08 |
| WD | L1491, L1492, L1495, L1496, L1523, L1524, L1580, L1583 | add to FW-08/FW-13 |
| WD-EX | L10, L948, L1259 | add to FX-01 |
| CA | 12 lines listed in FC-01 | FC-01 |
| ADAPTER | L101, L1238 (L1589 history) | FD-01 |
| GUIDE | L58, L343, L399, L439–441, L771 | FG-01…FG-03 |
| PANEL | L842, L881 | FP-01 |

The pass-2 closeout also listed "outside mirrors noted, not proposed (D1)"
(C1-A after the R2 table): DEL-04-01 → DEL-01-02, 01-04, 02-02; DEL-04-03 →
DEL-01-04, 02-02; DEL-02-01 → DEL-02-02, 02-04; DEL-02-03 → DEL-02-02. No D
node proposed these supplier-side mirrors; they become proposable now that
the consumers have Design files (§3, row M-x).

---

## 2. Conflicts and gaps between D nodes (for integrator rulings)

Each item: the two texts, and a recommended resolution with its reason. None
is decided here.

| # | Topic | Text A | Text B | Recommended resolution | Reason |
|---|---|---|---|---|---|
| **C-01** | Shape of the A15 relations | D3 `aac.offer` / `aac.capture-evidence`: `reviewedDraft {draft: **string**, content}`, `priorRevision`: **string or null** (camelCase) | D5 `workspace-registration.schema.json`: `reviewed_draft {draft: **draft_key object** {draft_location, draft_root, name}, content}`, `prior_revision`: **revision tuple object** or null (snake_case); D3 J-W2 names the draft difference, not the prior-revision one | RS (FR-06) defines the persisted form in camelCase: `reviewedDraft {draft: WR ID-3 string "draft:<location>:<name>@<content identity>", content}`, `priorRevision`: RS `$defs/workflowTuple` or null. D3's offer/capture follow RS (prior revision becomes a tuple); WR keeps its internal object and writes the ID-3 string through the RS writer | RS is the cross-deliverable record and already has `workflowTuple`; WR ID-3 defines the string for exactly this use; under K-6 a prior revision is a tuple, not a free string |
| **C-02** | `draft_transition` extra elements (J-W1) | D3 `nir.draft-transition.schema.json` adds optional `a15_record` (`^rec:`) and `revision`, "requested addition (J-W1)" | D5 `draft_transition` has neither, and `additionalProperties: false`; D5 finished before D3's request (peer request not taken up) | D5 round 2 adds both as optional on *registered* and *registration not completed* | D3 otherwise reads them from `library_entry`; a WR record carrying them would fail WR's own schema |
| **C-03** | Re-reading a closed generation's events | D1 RECOVERY OA-02, U-R10: "This file says no" — after a generation closes, views rebuild from Codex history | D2 NPTD RV-4 / J-3 asks HOSTING to say they "stay re-readable" so checklist revisions survive a supplier restart within a session | Adopt D1's reading; D2 RV-4 states closed-generation checklists "not recoverable", as after a relaunch (R17-4) | Simpler custody; one rule for restart and relaunch; O-8 lowers the stake (plan mode yields a `plan` item, no `turn/plan/updated`; no `update_plan` tool appeared in any captured tool list) |
| **C-04** | `multiAgentMode` replacement signal (HOSTING HCG-A08, EXEC EV-3a, WD §4.2.5) | D2 J-2/J-5: **replace** with `Model.multiAgentVersion` (`disabled` → missing; `v1`/`v2` → present; null → not read) | D6 J-3: **add** `Model.multiAgentVersion` "as the per-model signal" beside the current text | Replace: `multiAgentMode` is "@deprecated Ignored" (verified in the bundle) and carries no information. Availability = `Model.multiAgentVersion` ≠ `disabled` **and** the provider receives `namespace` tools (`modelProvider/capabilities/read` → `namespaceTools`, as `mcp-tool-call` already uses); a `features.multi_agent = false` in the effective config, when present, reads missing | O-4: delegation tools travel only inside a `namespace` tool, dropped by LM Studio 0.4.16; O-8: gate is the stable feature `multi_agent`, not shown by `config/read` unless set. `Model.multiAgentVersion` itself is `observed-in-generated-types` only (O-4 did not read `model/list`) |
| **C-05** | "Experimental" label on delegation | K-5 (R17-2): "Use Codex's experimental plan mode and delegation surfaces, labelled 'experimental'"; EXEC EV-3a "**Active** (experimental opt-in)"; WD §4.2.5 "experimental-only" | D2 F-2 / NPTD EX-1: delegation items are stable; only plan mode needs the opt-in; O-8: `multi_agent` stable, default on | Label plan mode "experimental"; label delegation by EX-1 (b) only (no stable-surface label), and bring F-2 to the owner as visibility, not a re-decision | K-5's premise (that both are experimental) holds for plan mode only; labelling a stable surface "experimental" would misstate the supplier |
| **C-06** | Does DEL-01-04 consume DEL-01-03? | D2 proposes row DEL-01-04 → DEL-01-03 (item anchors on request cards; plan-mode element in turn composition; TA-4 act display) and J-9 to D3 | D3: "nothing consumed from DEL-01-03 (R17-10)"; "no row to DEL-01-03 is needed"; NIR has no anchor or plan-mode element (grep) | Decide who composes `collaborationMode` on `turn/start`. Recommend: DEL-01-04 composes (it owns the composer), consuming NPTD's plan-mode element and item anchors; adopt D2's row (admitted, SCC-free, §3) and ask D3 round 2 to place them | NPTD PS-1 says "DEL-01-04 composes and sends"; NIR is silent, so today nobody sends it. O-8: plan mode persists until the default mode is sent, so the composer must send it explicitly |
| **C-07** | Does DEL-02-04 consume DEL-01-03? | D2 proposes row DEL-02-04 → DEL-01-03 (delegation export for the K-10 account; children's `agentRole`) | D6 ROLE §7.3: "DEL-02-04 reads the delegation items from DEL-01-01 directly (C-3) and needs nothing from DEL-01-03" | Drop D2's row unless D6 adopts the export; keep the K-10 label as a runtime value from DEL-02-04 to DEL-01-03 (ROLE O-6) | A row with no consuming text is a dangling contribution; both routes are SCC-free, so this is a design choice, not a graph constraint |
| **C-08** | K-10 standing values | D2 `npt.delegation-export` `delegatingRole.statement` const `stated-not-enforced` | D6 `role-limit-account` standing enum `stated-not-enforced` · `enforced-by-supplier` · `unknown` (a modified TASK guidance copy → `unknown`) | D2's export carries D6's standing as handed (enum of three), not a constant | Otherwise the export claims "stated" for a modified guidance copy that may not state the limit |
| **C-09** | K-3 refusal wording | D3 NIR ST-3: "not started — no model selected" | D4 ACCESS CS-1/CS-2 and R17-2: "run not started — no model selected" (R15-1's wording) | Use R17-2's exact words, or rule that a non-workflow conversation drops "run" (both files then change) | R17-2 names the wording; two files must not differ |
| **C-10** | Person identity shape | D3 J-H5: HOSTING `actorRef` string "person:‹name›/‹OS›/‹Codex› (identity not verified)" | D4 I-6: `{kind: "chatgpt", email\|null, planType}`; RS `$defs/person`: `displayName`, `osAccount`, `codexAccount` (**string**), `identityVerified` | RS `codexAccount` = the reported email, or "ChatGPT account (no email reported)"; `planType` is not an identity element and is not recorded; HOSTING `actorRef` stays a string derived from the same three values; email vs digest remains RS's (U-A8) | One identity, three encodings today; RS's object is the record of reliance |
| **C-11** | One Codex process or several | D4 ACCESS §4 K2-1: API-key conversations run in a second App-owned home H-key (plus H-acct, and H-probe for the label probe) → one child per App account home | D1 RECOVERY: one Codex process per App session (AS/CV tables; DEF-5 "the Codex process"; quit stops "the supplier"); HOSTING U-12 "One active child assumed" | Hold for owner U-A1. If K2-1 is adopted, D1 round 2 makes DEF-5/DEF-6/quit apply to each App-owned process and keys generation by home (with C-20); F records HOSTING U-12's per-home dimension only (R17-2) | Structural; R17-2 forbids restructuring HOSTING in D. OBS-2's inference "K-2 needs no second home for configuration" (O-6) does not address one-account-per-home, which is K2-1's reason |
| **C-12** | Who offers "Stop/Restart Codex" | D1 U-R9: "restart Codex" control, DEL-01-04 or DEL-01-05 | D3 NIR §5.2 places "Stop Codex" (no restart); D4 silent | DEL-01-04 offers both "Stop Codex" and "Restart Codex", each asking first with live work; DEF-5a covers both | D3 already owns the control surface; DEL-01-05 changes settings, not the process |
| **C-13** | Interrupt caused by a `cancel` answer | D3 NIR TO-4: "interrupted after your `cancel` tool-permission answer" | D1 `recovery.stop-request` `cause` enum: `person-interrupt`, `quit` only; SR tables have no such cause | D1 round 2 adds an observed CV outcome cause "after a cancel answer" (not a stop request) | O-3 side observation: `cancel` = decline **and** interrupt; D1 would otherwise label it "cause not observed" |
| **C-14** | How a draft reaches a trial conversation | D3 NIR AT-8: "supply record of form `draft-package` … How the draft reaches the conversation is DEL-02-02's (with DEL-02-04 for guidance carriage)" | D5 WR TT-2/TT-3: DEL-02-04 composes no workflow; the App pre-fills (does not send) a message naming the draft; D6: a draft is never composed (K-7) | D3 AT-8 drops "with DEL-02-04 for guidance carriage": a draft reaches a trial only as a message or attachment the person sends | K-7 (owner): a trial is an ordinary conversation, not supplied guidance |
| **C-15** | Role selector in the start display | D6 O-8 (peer join): the role selector's state sits in the conversation start display (K-3) | D3 NIR ST-1…ST-4: model only; no role element (grep: no "role selector" or "role in force") | D3 round 2 adds ST-5: role preselection from `default_for_new_chat`, clearable, "no role" allowed (R17-9) | Peer request not taken up |
| **C-16** | What a delegated child receives | R17-9 and D6 CR-4: where native child roles are unsupported "children inherit the parent's guidance" (inference) | O-4a: native child roles **are** supported; the role file's `developer_instructions` **replace** the parent's for that child | Integrator revises R17-9's fallback sentence; D6 round 2: CR-1 composition (product guidance + role) is required; CR-4 applies only to children spawned without `agent_type` (not observed) | Observed supplier behaviour contradicts the stated inference |
| **C-17** | Changing guidance on an existing thread | D6 IP-3/§5.5 and D1 §4.1 "resume inputs" (composition handed at R-6) rely on `thread/resume` `developerInstructions` | O-5: accepted and **silently ignored**, loaded or not; nothing reports it | Route B holds. Integrator picks the route-B means for K-9: (a) new thread / `thread/fork` with the new composition (fork's uptake not observed); (b) per-turn `collaborationMode.settings.developer_instructions` (O-5b: applied, added; experimental; persists like plan mode); (c) change applies to new conversations only, "change not applied" shown. Possibly an owner item (K-9 "takes effect at the next idle point") | Both D1 and D6 text change; K-9's effect at 0.158.0 depends on the choice |
| **C-18** | Person's global Codex guidance in the App home | D4 decision record U-R1 (to D6): whether the App's Codex sees the person's global `AGENTS.md`, skills and prompts (M-A links `config.toml` only) | D6 ROLE: not addressed (grep: no CODEX_HOME / skills / account-home text) | D6 round 2 states it; integrator decides whether the App links them | Peer request not taken up; affects what `instructionSources` can show |
| **C-19** | Custody of the role supply-record log | D6 asked D1 to keep it | D1 U-R11: owners keep their own App-kept records (else an SCC) | Resolved as D1 says; DEL-02-04 holds its log (ROLE §6.1 already appends to an App-kept log) | No action beyond noting |
| **C-20** | Generation identity | D1 H-5: unique across App sessions (includes the App session) | D4 (U-12 dimension): generation, register and thread keyed by home | Generation identity = {App session, App-owned home, spawn counter}; home part only if U-A1 adopts K2-1 | Both are needed together under K2-1 |
| **C-21** | `derived_from` in the A15 offer | D5 `a15_descriptor.relations` carries `derived_from` | D3: "WR's `derived_from` is not carried by the act control" | No conflict: R17-11 keeps derived-from in WD's tuple; the act record carries reviewed draft and prior revision only. Note only | — |
| **C-22** | A15 order and vocabulary | D5.md §2.1 lists D3's in-progress names (`draft-created`, `derivedFrom {reviewedDraftContent,…}`) | D3 final: D5's names and order adopted (D3 §0) | Resolved; D5.md §2.1's table is superseded | Read-order artefact |
| **C-23** | Restart-Codex question on sign-out / key removal | D4 → D1: sign-out and key removal ask first with live turns | D1 offers `assess live work` as a runtime value (no row; DEL-01-05 → DEL-01-02 would form a cycle, confirmed §3) | Resolved | — |
| **C-24** | App-level indicator of waiting requests with no window; several windows | D1 → D3: DEL-01-04 places an App-level indicator of requests waiting with no window; U-R5 several windows on one conversation | D3 NIR: no such indicator (grep "window": only PL-1, NR-2, L367) | D3 round 2 adds it | Peer request not taken up |
| **C-25** | K-12 remote-control loop | D4 §9 candidate setting `remote_control`; U-A9 asks whether the App may turn a setting back on given "does not veto the user's Codex configuration" | O-7: `remote_control` is a `removed` feature with no effect; only the **internal** env var `CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED=1` stops the loop; no socket without sign-in | Integrator ruling: K-12 turns off "whatever Codex's settings allow"; an internal env var is not a documented setting → recommend not using it, show the loop in the network view as "local only when not signed in (observed)" | Avoid depending on an internal name that can change without notice |

**Gaps (no D node covers them):**

- **G-1** HOSTING F-15 for seam S-4: D4 gave no explicit receiving comparison (FH-19).
- **G-2** GUIDE G-1 act-control half and M5.3 (FG-02).
- **G-3** Goals surface seen in OBS-2: tools `get_goal`, `create_goal`, `update_goal` in every captured tool list and the notification `thread/goal/cleared` after resume. No D file places them (NPTD grep: none). Proposed for DEL-01-03 round 2 or HOSTING §8.4 grouping.
- **G-4** Items opened and never completed: O-1 (reasoning item) and O-3 (command item) never receive `item/completed` and are absent from history. NPTD TI (tool-item) table, NIR TO and RECOVERY need a "not completed (turn ended)" settlement by turn end.
- **G-5** The graceful-stop history marker (O-2): Codex writes "The user interrupted the previous turn on purpose" into history on a stdin-close stop, so after a K-4 quit the model's next turn reads it as the person's interrupt. No D file mentions it; owner visibility under K-4.

---

## 3. Proposed new register rows (de-duplicated)

Computed over DAG-003 `DependencyEdges.csv` (124 admitted arcs) and
`CandidateEdges.csv` (78 held), consumer → supplier (UPSTREAM From→Target;
DOWNSTREAM Target→From), Tarjan SCC (`$TMPDIR/f0/scc.py`). Base SCCs over
admitted + held: {DEL-01-01, DEL-01-05}, {DEL-01-06, DEL-09-01}, {DEL-10-02,
DEL-10-04}, {DEL-11-01, DEL-11-03}, {DEL-07-01, DEL-07-02, DEL-08-01}, SCC-002
(13: DEL-01-04, DEL-02-01…02-04, DEL-03-01…03-03, DEL-04-02, DEL-04-03,
DEL-05-01, DEL-05-02, DEL-09-09). Admitted layer alone: no SCC.

| ID (merged) | Row and register | Direction (consumer → supplier) | Arc today | Layer if added | SCC effect | Proposed by |
|---|---|---|---|---|---|---|
| NR-01 | DEL-02-03 UPSTREAM INTERFACE → DEL-01-02 (custody events, tag lookup; EXEC AE-6, RE-4, §2.7) | DEL-02-03 → DEL-01-02 | none | admitted (new arc) | none | D1 NR-D1-1 |
| NR-02 | DEL-03-03 UPSTREAM INTERFACE → DEL-01-02 (in-flight items, relaunch fact; PI-6, XF-41) | DEL-03-03 → DEL-01-02 | none | admitted (new arc) | none | D1 NR-D1-2 |
| NR-03 (optional) | DEL-09-09 UPSTREAM INTERFACE → DEL-01-02 (XC-06) | DEL-09-09 → DEL-01-02 | none | admitted (new arc) | none | D1 NR-D1-3 |
| NR-04 (optional) | DEL-02-02 UPSTREAM INTERFACE → DEL-01-02 (stop definitions; App-start reconciliation WR SQ-X) | DEL-02-02 → DEL-01-02 | none | admitted (new arc) | none | D5 NR-1 |
| NR-05 | DEL-01-04 UPSTREAM INTERFACE → DEL-01-03 (+ DOWNSTREAM mirror in DEL-01-03) | DEL-01-04 → DEL-01-03 | none | admitted (new arc) | none | D2 — **disputed, C-06** |
| NR-06 | DEL-02-04 UPSTREAM INTERFACE → DEL-01-03 (+ mirror) | DEL-02-04 → DEL-01-03 | none | admitted (new arc) | none | D2 — **disputed, C-07** |
| NR-07 | DEL-01-04 UPSTREAM INTERFACE → DEL-01-05 (access and selection state, K-3; Codex account, K1-4) | DEL-01-04 → DEL-01-05 | none | admitted (new arc) | none | D3 NR-3 = D4 NR-1 |
| NR-08 | DEL-01-04 UPSTREAM INTERFACE → DEL-04-02 (K-5/K-6 components, R17-7) | DEL-01-04 → DEL-04-02 | none | **held** (inside SCC-002) | membership unchanged | D3 NR-1 |
| NR-09 | DEL-01-04 UPSTREAM INTERFACE → DEL-02-03 (SD-1…SD-5; arrival references) | DEL-01-04 → DEL-02-03 | none | **held** (inside SCC-002) | membership unchanged | D3 NR-2 |
| NR-10 | DEL-02-04 UPSTREAM INTERFACE → DEL-02-02 (selection record, resolved revision) | DEL-02-04 → DEL-02-02 | none | **held** (inside SCC-002) | membership unchanged | D5 NR-2 = D6 = R17-8 |
| M-1 | DEL-01-02 DOWNSTREAM INTERFACE → DEL-01-03 (mirror of DEP-01-03-012) | DEL-01-03 → DEL-01-02 | admitted | mirror | none | D1 R3-01-02-a |
| M-2 | DEL-01-02 DOWNSTREAM HANDOVER → DEL-09-02 (mirror of DEP-09-02-010) | DEL-09-02 → DEL-01-02 | admitted | mirror | none | D1 R3-01-02-b |
| M-3 | DEL-01-03 DOWNSTREAM mirrors of DEP-06-01-007, DEP-09-02-011, DEP-09-05-008 | DEL-06-01/09-02/09-05 → DEL-01-03 | admitted (3) | mirror | none | D2 |
| M-4 | DEL-01-05 DOWNSTREAM HANDOVER → DEL-01-01 (mirror of DEP-01-01-024) | DEL-01-01 → DEL-01-05 | **held** (SCC-001) | mirror | none new | D4 P-9/NR-2 (C1-B §5.5 observed it, did not propose) |
| M-5 | DEL-05-01 UPSTREAM INTERFACE → DEL-01-05 (mirror of DEP-01-05-014) | DEL-05-01 → DEL-01-05 | admitted | mirror | none | D4 NR-3 = **pass-2 C1-C R-0501-4** |
| M-6 | DEL-01-01 DOWNSTREAM → DEL-02-04 (mirror of DEP-02-04-010) | DEL-02-04 → DEL-01-01 | admitted | mirror | none | D6 restates **pass-2 C1-B R-11-1** |
| M-7 | DEL-01-04 DOWNSTREAM HANDOVER → DEL-02-03 (mirror of DEP-02-03-027, X-1) | DEL-02-03 → DEL-01-04 | held | mirror | none | D3 restates **pass-2 C1-A R2-01-04-a** |
| M-x (not proposed by any D node) | Supplier-side mirrors listed by C1-A "outside mirrors noted, not proposed (D1)" (§1.14) | various | existing | mirror | none | pass-2 C1-A note |
| ST-1 | DEP-01-04-010 Statement: add "and the App act control that captures workflow registration (A15)" | — | — | statement | non-topological | D3 SC3-01-04-9 (pair of ST-2) |
| ST-2 | DEP-02-02-013 Statement: add the App act control and capture evidence | — | — | statement | non-topological | D5 SC3-02-02-6 (pair of ST-1) |
| ST-3 | DEP-02-02-016/-017 Statements: name A15 and its RS record kind | — | — | statement | non-topological | D5 SC3-02-02-7 = **pass-2 C1-A note** ("DEL-02-02's register should name A15 and its RS record kind", B4 §7) |
| ST-4 | DEP-02-04-010 Statement: add the status, delegation-item and configuration-read surfaces | — | — | statement | non-topological | D6 SC3-02-04-8 |

**All proposals together:** SCC set unchanged (same six SCCs); admitted
layer still acyclic. **Pairwise:** no pair of proposals changes any SCC (all
153 pairs of the 18 proposals checked). New admitted arcs NR-01…NR-07 are each a departure for
DAG currency (a `project-dag` update), as D3 and D5 note.

**Not proposed, confirmed cyclic** (each would change an SCC): DEL-01-05 →
DEL-01-02 (forms {DEL-01-01, DEL-01-02, DEL-01-05}); DEL-01-03 → DEL-02-04
(pulls DEL-01-03 into SCC-002); DEL-01-02 → DEL-02-04 (pulls DEL-01-02 and
DEL-01-03 into SCC-002). R17-10's guard holds for every proposal: none has
DEL-01-02 or DEL-01-03 as consumer of DEL-01-04, DEL-02-02, DEL-02-03,
DEL-04-02, DEL-04-03 or DEL-06-01.

---

## 4. SCA-V4-003 proposals

### 4.1 Count per deliverable

| Deliverable (proposing node) | ScopeOfWork | Register / Open_Issues | Total | IDs |
|---|---|---|---|---|
| DEL-01-02 (D1) | 8 | 2 | 10 | SC3-01-02-1…8; R3-01-02-a, -b |
| DEL-01-03 (D2) | 7 | (rows in §3) | 7 | SC3-01-03-1…7 |
| DEL-01-04 (D3) | 8 | 1 | 9 | SC3-01-04-1…8; SC3-01-04-9 |
| DEL-01-05 (D4) | 7 (P-7 conditional on U-A1) | 2 (P-8 Open_Issues OI-009; P-9 register) | 9 | P-1…P-9 |
| DEL-02-02 (D5) | 5 (incl. optional -5) + 1 on DEL-01-04's obligation | 2 | 8 | SC3-02-02-1…8 |
| DEL-02-04 (D6) | 7 | 1 | 8 | SC3-02-04-1…8 |
| **Total** | **43** | **8** | **51** | |

D4's P-1…P-9 have no SC3 IDs; suggest renaming SC3-01-05-1…9 at the
amendment node for consistency.

### 4.2 Index

| ID | Subject (one line) | Overlap / duplicate |
|---|---|---|
| SC3-01-02-1 | REQ-002: interrupt a turn ≠ end a run ≠ stop Codex (R17-3) | pairs with SC3-01-04-7 |
| SC3-01-02-2 | AC-002/VER-002: "turn interrupt" wording | with -1 |
| SC3-01-02-3 | REQ-005/AC-006/VER-006: quit asks first; "interrupted by quit"; resume offer (K-4) | — |
| SC3-01-02-4 | REQ-003: no automatic decline; pending at stop ends unanswered (R17-9) | pairs with SC3-01-04-3 |
| SC3-01-02-5 | CLM-004/TBD-003: OI-001/002 overtaken by D2/D3 | same class as SC3-01-03-2, SC3-02-04-1 (SCA-V4-002 Impact V-4) |
| SC3-01-02-6 | TBD-001: D4 pin 0.158.0 for definition; OI-008 per R17-5 | same class as SC3-01-03-1, P-3, SC3-02-04-1/-7; related C1-B S-11-1 (DEL-01-01) |
| SC3-01-02-7 | REQ-006/OUT-004: supplier facts direct to DEL-04-03; only references kept (R9-7, R17-4) | — |
| SC3-01-02-8 | CLM-001: names DEL-01-03 and DEL-09-02 as consumers | enables M-1, M-2 |
| R3-01-02-a, -b | Mirror rows (M-1, M-2) | — |
| SC3-01-03-1 | TBD-001: D4 pin | class of SC3-01-02-6 |
| SC3-01-03-2 | CLM-004, AX-002, TBD-003: OI-001/002 decided for this scope | class of SC3-01-02-5 |
| SC3-01-03-3 | REQ-005: act names the person, "identity not verified" (K1-4) | class of P-6, SC3-01-04-4; pass-2 SC2-02-03-5, R2-02-03-j |
| SC3-01-03-4 | REQ-001/AC-001: checklists not copied; plan items recovered (R17-4) | interacts with C-03 |
| SC3-01-03-5 | REQ-003: task-agent delegation recorded, "stated, not enforced" (K-10) | duplicate in substance of SC3-02-04-4 |
| SC3-01-03-6 | REQ-004: experimental surfaces labelled; fully usable without (K-5) | wording depends on C-05 |
| SC3-01-03-7 | REQ-005: "carry out this plan" is ordinary input (R17-9) | — |
| SC3-01-04-1 | New REQ/OUT/AC/VER: the App act control incl. A15, consumers incl. DEL-02-02 | **amends pass-2 SC2-01-04-1 (C1-A) = X-1 (C1-B)**; subsumes SC3-02-02-8 |
| SC3-01-04-2 | REQ-006/CLM-004: A15 capture here, registration in DEL-02-02 (K-8) | pairs with SC3-02-02-4 |
| SC3-01-04-3 | REQ-001: native answer forms only; explicit decline per kind; no auto-decline | pairs with SC3-01-02-4 |
| SC3-01-04-4 | REQ-005: DECISION-K1 K1-1…K1-4 in the SoW | class of SC3-01-03-3 |
| SC3-01-04-5 | OUT-002/CLM-001: placement of DEL-04-02 overlay and facets (R17-7) | — |
| SC3-01-04-6 | REQ-002: "no model selected" start display (K-3) | duplicate in substance of P-4; wording C-09 |
| SC3-01-04-7 | REQ-002: three stop operations shown distinct (R17-3) | pairs with SC3-01-02-1 |
| SC3-01-04-8 | VER-005: positive case through the App act control | — |
| SC3-01-04-9 | DEP-01-04-010 Statement (ST-1) | mirror pair of SC3-02-02-6 |
| P-1 (SC3-01-05-1) | TBD-001: OI-009 decided by K-1; fallback rule | with P-8 |
| P-2 | CLM-001: "account home is chosen under TBD-001" | follows P-1 |
| P-3 | TBD-003: D4 pin; qualification separate | class of SC3-01-02-6 |
| P-4 | REQ-004/AC-004/VER-004: no model until chosen; last choice offered, never applied (K-3) | = SC3-01-04-6 in substance |
| P-5 | New REQ-010/AC-011/VER-011: start-up traffic off where settings allow, network view (K-12) | content now fillable from O-7 |
| P-6 | OUT-002 or REQ-011: supply the Codex account for act identity (K1-4) | class of SC3-01-03-3 |
| P-7 | REQ-002 reading: API key in a separate App-owned home (only if U-A1 adopts K2-1) | conditional |
| P-8 | `_Decomposition/Open_Issues.csv` OI-009: decided at choice level | — |
| P-9 | Register: DOWNSTREAM mirror of DEP-01-01-024 (M-4) | C1-B §5.5 observed, not proposed |
| SC3-02-02-1 | REQ-001: draft tried in ordinary conversation; only registered revisions run (K-7) | — |
| SC3-02-02-2 | REQ-003: slot policy, revisions kept, no overwrite (K-6) | — |
| SC3-02-02-3 | REQ-002: registration via DEL-01-04's act control, bound to reviewed bytes (K-8) | — |
| SC3-02-02-4 | CLM-002/REQ-008: act control belongs to DEL-01-04 | pairs with SC3-01-04-2 |
| SC3-02-02-5 (optional) | "host-supplied" → "host (origin `host`)" | — |
| SC3-02-02-6 | DEP-02-02-013 Statement (ST-2) | mirror pair of SC3-01-04-9 |
| SC3-02-02-7 | DEP-02-02-016/-017 name A15 (ST-3) | **= pass-2 C1-A register note (B4 §7)** |
| SC3-02-02-8 | SC2-01-04-1 consumer list adds DEL-02-02 and A15 | **subsumed by SC3-01-04-1**; amends pass-2 SC2-01-04-1 |
| SC3-02-04-1 | Open-matter table: OI-001/002/012/017 lags | class of SC3-01-02-5/-6 |
| SC3-02-04-2 | OI-018 row: answered for the App by K-9 | — |
| SC3-02-04-3 | REQ-002: workflow supply composed with guidance and role (R17-8) | — |
| SC3-02-04-4 | REQ-003/AC-003: task role "stated, not enforced" (K-10) | = SC3-01-03-5 in substance |
| SC3-02-04-5 | REQ-001/AC-001: no-role conversations; preselection as data (R17-9) | — |
| SC3-02-04-6 | REQ-002/CLM-004: native child roles, else inherit | **text changes under C-16** (O-4a: children do not inherit when a role is configured) |
| SC3-02-04-7 | TBD-001: OI-018 answered; pin 0.158.0 | class of SC3-01-02-6 |
| SC3-02-04-8 | DEP-02-04-010 Statement (ST-4) | — |

**Overlap with the pass-2 closeout (C1-A, C1-B, C1-C):** SC2-01-04-1 / X-1
(amended by SC3-01-04-1 and SC3-02-02-8); R2-01-04-a (M-7); R-11-1 (M-6);
R-0501-4 (M-5); the C1-A register note on DEP-02-02-016/-017 (SC3-02-02-7);
related, not duplicate: SC2-02-03-5 and R2-02-03-j (DEL-02-03's statements of
the act control and K1-4 identity, which SC3-01-04-1 makes true), C1-B S-11-1
(DEL-01-01 TBD-002 pin pointer, same class as the D4-pin lags), C1-B R-11-3
(DEP-01-01-022 notes on the `namespace` route limit, which O-4 extends to
delegation). Pass-2 C1-B §5.5 observed DEP-01-01-024's missing mirror without
proposing it; D4 P-9 proposes it.

---

## 5. Owner items raised by D nodes (and by OBS-2's findings)

| ID | Raised by | Item | Options stated |
|---|---|---|---|
| U-A1 | D4 | API-key conversations in a second App-owned home (K2-1), giving HOSTING U-12 a per-home dimension | (a) adopt K2-1 (two App homes; D4's choice); (b) change V4-ARC-04's custody rule for the key instead |
| U-A2 | D4 | Observation of sign-in and API-key flows (K-11 excludes them) | (a) the owner's own sign-in and key; (b) an invented non-functional key string in a scratch home; (c) none (cells stay inference) |
| U-A11 | D4 | REQ-005 names "the Owner with the App implementation owner"; no record shows the latter's part in K-1 | record that participation, or amend REQ-005 (not stated as options in D4; inferred) |
| U-AAC-1 | D3 | Placement of act capture (OI-008, phase review) | P-1, P-2 native confirmation in the host (PROPOSED), P-3 |
| U-AAC-2 | D3 | An OS password or biometric check per act (P-3 presence check) | none; some kinds; all kinds |
| U-AAC-7 | D3 | Contract standing of the act control | through SCA-V4-003 (SC3-01-04-1) |
| U-WR-4 | D5 | Pre-v4 library content without a registration record is not runnable until registered in place (K-7 migration cost) | (a) register in place (one review and A15 per workflow; D5's design); (b) run it with its standing shown |
| U-WR-13 | D5 | Selection pinned vs following new revisions | pinned (D5); following default — owner only if wanted |
| U-R9 (D6) | D6 | Release upgrade of unmodified guidance copies | automatic (D6 PROPOSED); ask the person |
| F-2 (D2) | D2 | Visibility: K-5's "experimental" premise holds for plan mode only | not a re-decision (see C-05) |
| U-R3 (D1) | D1 | Ledger retention and what deleting a conversation removes | "with the owner for privacy"; no options stated |
| OBS-K9 | OBS-2 O-5 (framed here) | K-9 "takes effect at the conversation's next idle point" cannot be met through `thread/resume` at 0.158.0 | (a) new thread / fork with the new composition; (b) per-turn experimental `collaborationMode` developer text (added, persists); (c) new conversations only, "change not applied" shown (C-17) |
| OBS-K5 | OBS-2 O-4 (framed here) | Delegation is unavailable to LM Studio-served local models at 0.158.0 (namespace tools dropped); K-5's "views absent" then applies to every local-model conversation | visibility; or an adapter (not proposed) |
| OBS-K4 | OBS-2 O-2 (framed here) | After a K-4 quit, Codex's history tells the model "the user interrupted the previous turn on purpose" | visibility (G-5) |
| OBS-K12 | OBS-2 O-7, §11 (framed here) | Installation id and thread/session/turn ids go to the provider in `client_metadata`; host time zone in every model input; remote-control loop only stoppable by an internal env var | visibility; C-25 for the env var |

Integrator (not owner) items named by the D nodes: U-NIR-5 (D3; J-E8),
U-AAC-5 (home of "the name set in the App"), U-A9 (D4; overlaps C-25),
U-R10 (D1; C-03), U-R10 (D6; compatible-roles mismatch display, with DEL-02-03),
and the OBS-2 S-9 continuation question (OBS-2 return).

---

## 6. Suggested F split

Fences are disjoint by file. "Version step" per R17-14 (one per file); the
labels below are suggestions so GUIDE and cross-pins can be written once.

| Executor | Write fence | Rows | Waits on |
|---|---|---|---|
| **F-A** | `DEL-01-01/Design/HOSTING_BOUNDARY.md` (→ v0.9); `hosting.server-request-entry.schema.json` and its examples/prototype fixtures under `DEL-01-01/Design/prototype/` only where FH-17/FH-18 change the schema. Never `OBS_*.md`, `PIN_SPIKE_*.md`, `generated/` | FH-01…FH-44 | Rulings C-03 (FH-05), C-04/C-05 (FH-33), C-10 (FH-18), C-11/C-20 (FH-06, FH-31), C-25 (FH-29). Everything else can go now |
| **F-B** | `DEL-02-03/Design/EXECUTION_COMPATIBILITY.md` (→ v0.7); `checkpoint-record-entries.schema.json` only if FR-01 needs EXEC's `runEnded` changed (RS references it by `$ref`) | FE-01…FE-20 + §1.14 EXEC lines | C-04/C-05 (FE-05), U-NIR-5 (FE-13), C-10 (FE-20) |
| **F-C** | `DEL-04-03/Design/` (RECORD_SEMANTICS.md → v0.9, `RS_RECORD.schema.json`, `RS_RECORD.*example*`, `prototype/` fixtures); `DEL-04-01/Design/ACT_AND_POLICY_CONTRACT.md` (→ v0.9); `DEL-04-02/Design/AUTONOMY_AND_STANDING_EXCHANGE.md` (→ v0.9) | FR-01…FR-14, FA-01…FA-08, FS-01, FS-02 | **C-01** (FR-06, FA-04, FA-05), C-10 (FR-12), SEAL-2 (FR-08, may be left conditional). Coordinate with F-B only on `runEnded` (FR-01 ↔ EXEC schema) |
| **F-D** | `DEL-02-01/Design/WORKFLOW_DECLARATION.md` (→ v0.9), `EXAMPLES.md` (→ v0.9); `DEL-09-06/Design/CONNECTED_ACTIVITY_CONTRACT.md` (→ v0.7) (never `FACTS_*`, `RELAY_*`) | FW-01…FW-13, FX-01, FX-02, FC-01 + §1.14 lines | C-04/C-05 (FW-10), C-17 (FW-12 sentence on resume) |
| **F-E** (last) | `DEL-03-03/…/ADAPTER_ENABLEMENT_AND_RECEIVING.md` (→ v0.7); `DEL-09-09/…/EXTERNAL_TRACE_CASES.md` (→ v0.7); `DEL-05-01/…/LOOP_RECEIVING_CONTRACT.md` (→ v0.9); `DEL-05-02/…/PANEL_RECEIVING_CONTRACT.md` (optional); `DEL-03-04/…/HOST_INTEGRATION_GUIDE.md` (→ v0.6) | FD-01, FT-01, FL-01, FL-02, FP-01, FG-01…FG-03 | GUIDE re-pins every other file: run after F-A…F-D, or give it their final labels and hashes |

**Not F's (round 2 of the D nodes, inside their own fences):** D1 (C-11/C-20
if U-A1, C-13, C-17 resume inputs, OBS-2 variants: O-2 "interrupted" after
stop and kill, no re-raise; O-3), D2 (C-03, C-04 text, C-06, C-07, C-08,
G-3, G-4, O-4/O-8 cells), D3 (C-02 read side, C-06, C-09, C-12, C-14, C-15,
C-24; remove the "asked again after restart" note), D4 (G-1; O-6/O-7 cells),
D5 (C-02), D6 (C-16, C-17 route B, C-18, C-3 premise: no `thread/started`
for a child).

**OBS-2.** The record exists (`DEL-01-01/Design/OBS_2_0.158.0.md`,
`61cc34ffb811eb27`), so no row waits for it. Rows whose text depends on it
(they cite the record): FH-01, FH-02, FH-03, FH-07, FH-10, FH-11, FH-14,
FH-16, FH-23, FH-26, FH-27, FH-29, FH-30, FH-32, FH-33, FH-34, FH-35, FH-36,
FH-37, FH-39, FH-41, FH-42, FH-43; FE-02, FE-05; FR-02, FR-09, FR-12; FW-10,
FW-12; FD-01; FL-02.

---

## 7. OBS-2 consequences

Source: `OBS_2_0.158.0.md` (sections cited as OBS §n) and `D/OBS-2.md`.
Standing: dated observations at Codex 0.158.0 with LM Studio 0.4.16+2 and
`qwen/qwen3.5-9b`; O-4/O-4a/O-4b only **through an OBS-2 adapter** that
flattens the `namespace` tool (OBS §6.2), not stock behaviour. Verdicts:
**confirms**, **changes**, **open**.

### 7.1 D1 — DEL-01-02 (RECOVERY-v0.1)

| Cell | OBS-2 found | Verdict |
|---|---|---|
| §3.4 SR-04…SR-07; §5 SQ-I I-4, I-5 (O-1) | `turn/interrupt` → `{}` in ≈21 ms; `thread/status/changed idle`; `turn/completed` status `interrupted` (OBS §4). Two deltas arrived after sending, before the response. The open reasoning item never got `item/completed` and is not in history | **Confirms** "the empty result is not the interruption"; **adds** G-4 (items never completed) |
| §6 U-10 rationale; §3.5 RQ-03 (O-1/O-3) | A request pending in the interrupted turn is resolved **by the supplier**: `serverRequest/resolved` after `turn/completed`; a late client answer is silently ignored; the command item never completes and is absent from history (OBS §5.1) | **Confirms** U-10 (no App decline needed); selects the "resolved by supplier" stub variant as the live one; the register must refuse any answer after `resolved` |
| §3.4 SR-09; §5 R-4, R-5; §13 F-R7 (O-2) | After a graceful stop (stdin close) and after SIGKILL alike, `thread/read` shows the turn `interrupted` with the command item absent; a graceful stop writes a "user interrupted … on purpose" marker into history (OBS §5.2) | **Confirms** the `interrupted → recovered-from-supplier` variant for both causes; the `inProgress → unknown` and missing-turn variants did not occur. Codex's status cannot tell quit from crash, so "interrupted by quit" must come from the App ledger, as designed. G-5 for the marker |
| §3.5 RQ-07; §5 R-7 (O-2) | Pending approval **not re-raised** on resume; no resolution sent; no model request on resume | **Changes**: the "re-raised = new entry" path is unused at 0.158.0 (keep as a defence, label not observed); outstanding requests end `ended-unanswered(process-exit)` for good |
| §5 R-4 order (O-2) | `thread/read` before `thread/resume` works in a new process (thread `notLoaded`); `includeTurns` emits `deprecationNotice` | **Confirms**; prefer `thread/turns/list` (FH-42) |
| §6 U-09 (O-3) | Before-reply `serverRequest/resolved` provoked by `turn/interrupt` | **Changes** (fills): U-09 can close for this trigger |
| §3.4 descendants; §5 I-6; §4.1 child interrupt (O-4) | Via adapter: child notifications arrive on the same connection with the child's threadId; no `thread/started`; children not in `thread/list`, present in `thread/loaded/list`. Interrupting a child or cascading a parent interrupt was **not observed** | **Open** (DR-6/I-6 stay PROPOSED); relaunch listing must not rely on `thread/list` for children |
| §4.1 resume inputs (O-5) | `developerInstructions` on `thread/resume` accepted and ignored, loaded or not; nothing reports it (OBS §7) | **Changes**: a changed composition cannot be passed at R-6; the thread keeps its original developer text after relaunch (observed: ALPHA kept in a new process). C-17 |
| §7 standing table (O-6) | Only configuration sharing observed; sessions live under each `CODEX_HOME` (inference from the home layout) | **Open** for the session-store question |
| U-16 (OBS §11) | A plugin `git ls-remote` child outlived a stop ≈0.7 s after spawn and was re-parented | **Confirms** the need to end the process tree at a deliberate stop |

### 7.2 D2 — DEL-01-03 (NPTD-v0.1)

| Cell | OBS-2 found | Verdict |
|---|---|---|
| §4 EX-1 (b) feature names (O-4/O-8) | Delegation gated by `multi_agent` (stable, default on) and `multi_agent_v2` (stable, off); plan mode not gated by a listed flag in use (`collaboration_modes` `removed`); `config/read` shows no `features` unless set | **Changes** (fills): no feature makes delegation experimental; the "experimental" label rests on plan mode only (C-05) |
| §7.1 feature gate (O-4) | `[features] multi_agent = false` removes the delegation tools; with `multi_agent_v2` the namespace is `collaboration` with different tools (`followup_task`, `interrupt_agent`, `list_agents`, `send_message`, `spawn_agent`, `wait_agent`) | **Changes**: availability needs the feature and the provider's `namespace` support (C-04); the v2 tool set is a second shape to render |
| Delegation on local models (O-4) | Delegation tools travel only inside a `namespace` tool; LM Studio 0.4.16 drops it; no setting flattens them (`tool_namespace` must not be empty) | **Changes**: the delegation view is absent for LM Studio conversations at 0.158.0 (K-5 "views absent"); OBS-K5 |
| §7.3 DR-6 child interrupt (O-1, O-4) | Not observed | **Open** |
| §7.4 CO-1 / CO-2 (O-4) | Child frames reach the App on the same connection (CO-1 holds); the child is readable by `thread/read` with `parentThreadId`, `agentRole`, `agentNickname`, `source.subAgent` (CO-2 available); no `thread/started` for the child | **Confirms** both; **adds** "no `thread/started`": the child node is created from `collabAgentToolCall.receiverThreadIds` |
| §15.2 NV-04 (primary completed, descendant active) | Not observed (the parent waited for the child) | **Open** |
| DR-4 / NV-05 task-agent delegation (O-4b) | A TASK-guided parent delegated anyway (`spawnAgent`, `sendInput`, `wait`), all recorded | **Confirms** K-10 "stated, not enforced" |
| U-P1 plan surfaces live (O-8) | Plan mode yields one `plan` item via 188 `item/plan/delta`, no agentMessage, **no `turn/plan/updated`**, no `update_plan` tool | **Changes**: the checklist surface (CL table, RV-2) was not produced in any observed configuration; keep it designed, label "not observed at 0.158.0" |
| U-P2 `collaborationMode` persistence (O-8) | Plan mode **persists** on a later turn sent without `collaborationMode` | **Confirms** PS-5's rule to send the mode explicitly (needed to leave plan mode) |
| U-P3 / F-3 plan mode vs developer instructions (O-8, O-5b) | The thread's developer text is still sent beside the plan-mode text; a non-null `collaborationMode.settings.developer_instructions` is **added**; whether the model gives the mode precedence could not be separated from adherence | **Changes** in part: role/workflow supply is not set aside at the transport level; the precedence question stays **open** |
| (new) goals | `get_goal`, `create_goal`, `update_goal` tools and `thread/goal/cleared` | **Open**: G-3 |

### 7.3 D3 — DEL-01-04 (NIR-v0.1, AAC-v0.1)

| Cell | OBS-2 found | Verdict |
|---|---|---|
| NIR §5.1 TO-4 (O-1) | Turn status `interrupted` after `turn/interrupt` | **Confirms**; "interrupted by you" comes from the App's own record, as designed |
| NIR §4.4 note "asked again after restart"; VC-NIR-11 (O-2) | Pending requests are not re-raised after restart and resume | **Changes**: drop the note; the card ends CS-7 "Ended unanswered" |
| NIR §4.4 CS-6 (O-3) | Supplier resolution after an interrupt; a late answer is silently ignored | **Confirms** CS-6; the card must not offer an answer once resolved |
| NIR §4.3 decline under `untrusted` | `cancel` ended the item `declined` and the turn `interrupted` (OBS §5.1) | **Confirms** the card's warning; C-13 for DEL-01-02's label |
| NIR §5.5 descendants (O-4) | Via adapter: `collabAgentToolCall` items `spawnAgent`, `sendInput`, `wait` with `receiverThreadIds` and `agentsStates` | **Confirms** the source of the descendant line; local LM Studio conversations have no delegation at all |
| AAC §7 Codex account under K-1 (O-6) | Each home reports its own account (B `null` while sharing A's configuration); no credential existed | **Open** for a signed-in account; the design ("account of the home that runs the conversation") is consistent with what was seen |

### 7.4 D4 — DEL-01-05 (ACCESS-v0.1, decision record)

| Cell | OBS-2 found | Verdict |
|---|---|---|
| Decision record §4; ACCESS §3, CL-1/CL-3 (O-6) | M1: symlinked `config.toml` → B reads A's values, user layer named by B's path, `account/read` null (`requiresOpenaiAuth` false); M2: `-c` overrides → `sessionFlags` layer (a copy); M3 `--profile` refused for `app-server`; A's file unchanged by all cases | **Confirms** M-A; fallback (option A) not needed. **Open**: writes through the symlink (CL-10/CL-4), M4/M5 with a credential |
| ACCESS Q-1 step 3; §9 carrier; U-A12 (O-6/O-7) | `app-server` accepts `-c` and forms the `sessionFlags` layer | **Confirms** session flags as the K-12 carrier |
| ACCESS §9 rows (O-7) | `plugins = false` stops the featured-plugins request (chatgpt.com, 401) and the plugin repository check/fetch (github.com), cold or warm; `remote_plugin`, `apps`, `remote_control` do not; remote-control loop stoppable only by `CODEX_INTERNAL_APP_SERVER_REMOTE_CONTROL_DISABLED=1`, and it opened no socket without sign-in; `check_for_update_on_startup` not tested | **Changes** (fills the "App action" column); `remote_control` drops out as a candidate; C-25 for the env var; update check **open** |
| Q-9, LP-2, U-A7 local model list | Not in O-1…O-8 | **Open** |
| Q-11 resume provider override (O-5 related) | Only `developerInstructions` tested: ignored on resume | **Open**, with an adverse inference that resume overrides may be ignored generally |
| K2-1 premise (U-A1) | OBS-2 infers "K-2 needs no second home for configuration" | Does not bear on one-account-per-home; U-A1 **unchanged** |
| §9 network view (new) | Installation id and thread/session/turn ids in `client_metadata` to the provider; host time zone in every model input; no non-loopback socket from Codex during turns | **Adds** rows to the network/record view (FH-26; OBS-K12) |

### 7.5 D5 — DEL-02-02 (WR-v0.1)

No cell was marked OBS-2 pending. O-5 does not touch WR: a trial
conversation composes no workflow (TT-2). **No change.**

### 7.6 D6 — DEL-02-04 (ROLE-v0.1)

| Cell | OBS-2 found | Verdict |
|---|---|---|
| B-8; §5.4 IP-4; VC-R7 (O-5) | `thread/resume` `developerInstructions` accepted and silently ignored, loaded or not | **Changes**: **route B** holds. IP-3's resume never applies a change; T-2 "re-supplying" always ends *change not applied*. Route-B means (fork, per-turn `collaborationMode` text, or new conversations only) is C-17 / OBS-K9 |
| §5.5; VC-R8 (O-2, O-5) | After restart, resume with new text (CHARLIE) is ignored; the persisted text (ALPHA) stays in effect | **Changes**: relaunch resumes with the *original* supply; a changed composition needs route B |
| B-15; §5.3 CR-1/CR-4; VC-R11 (O-4a) | `agents.<role>.description` + `config_file` honoured: `spawn_agent` gains `agent_type` listing the role beside `default`, `explorer`, `worker`; `Thread.agentRole` = the role; the child's developer messages are the role file's `developer_instructions`, the skills and permissions blocks, **not the parent's**; the child has no delegation tools at default depth | **Confirms** CR-1 (and CR-5); **changes** CR-4's inference and R17-9's fallback for role-configured children (C-16): the composition in the role file must include the product guidance |
| §6.3 DL-6; VC-R3 (O-4, O-4b) | `collabAgentToolCall` delivered; a TASK-guided delegation happened and was recorded | **Confirms** L-TASK-1 / K-10; on stock LM Studio delegation never reaches the model at all |
| B-6 `instructionSources` | Every value was `[]` (the cwd held no `AGENTS.md`) | **Open** |
| VC-R2 supply reaching the provider prompt (O-5) | The tap shows the thread's developer text in every model request | **Confirms** for one role |
| C-3 "sub-agent `thread/started`" | No `thread/started` for a child | **Changes** (premise wrong): use `receiverThreadIds` and `thread/read` |

### 7.7 HOSTING (node F)

P-15 is now observed (ignored; FH-36, FH-37); RT-10 provoked (FH-43); U-09
closable (FH-07); H11 child survival (FH-01); L-4/U-18 filled (FH-29); F-14
answered (FH-27); U-19 narrowed and §10.1 extended (FH-41); L-3/F-31 extended
to delegation (FH-32); §9.1 categories (FH-26); `deprecationNotice` on full
reads (FH-42).

---

## 8. Files

| File | sha256 |
|---|---|
| `RUN/F/F0_JOINS.md` (this file) | reported in the hand-back (a file cannot carry its own hash) |

Scratch, not in the repository: `$TMPDIR/f0/chk.py` (quote check),
`$TMPDIR/f0/scc.py` (SCC check).
