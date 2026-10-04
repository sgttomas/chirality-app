# S1-B — Scoping survey: DEL-01-06, DEL-09-01, DEL-09-02

- **Run / node:** `APP-V4-DESIGN-PASS-4-20261003`, node S1-B (brief: `BRIEFS.md`
  "Common rules" and "S1 — scoping survey", sha256 prefix `3fe0abc84d6abe2e`;
  `OWNER_DECISIONS.md` prefix `0883eb7d8b88be7c`, read in its current state,
  which includes the owner's yes to the 0.160.0 download).
- **Executor:** Type 2 TASK, Claude Code subagent of the HELP_HUMAN session
  (Claude Opus 5.5); no delegation. Read-only on project state; no git writes;
  no network. This file is the only write.
- **Date:** 2026-10-03. Worktree HEAD `63d366c0e7`.
- **Standing of this file:** a survey. It proposes nothing as accepted, edits
  no contract, register or Design file, and claims no execution,
  qualification or host join.

Paths are relative to `projects/chirality-app-v4/execution` (E) unless they
start with `docs/` (= `projects/chirality-app-v4/docs/`). "States" means the
file says it; "inference" marks my reading.

## 0. Inputs read and how

| Input | Identity (sha256 prefix, current bytes) | Notes |
|---|---|---|
| DEL-01-06 `ScopeOfWork.md` / `Dependencies.csv` | `08e30b97baeb06ae` / `19c3eb3574e9bdf2` | Equal to the SCA-V4-003 closure-audit input manifest. `git log`: SoW last changed at `ddd721a90a` (INIT), register at `c1038ae5ac` |
| DEL-09-01 `ScopeOfWork.md` / `Dependencies.csv` | `8e53669468bd5885` / `96ea447bba37f122` | Same; register last changed `85dcc17c3f` |
| DEL-09-02 `ScopeOfWork.md` / `Dependencies.csv` | `327616c5f3d81633` / `8da5bece8198cc1f` | Same; register last changed `c1038ae5ac` |
| Basis `docs/` | PRD `bb6e786f…`, ARCHITECTURE `317d5789…`, EXAMINATION `471798bc…`, HOST_INTEGRATION `d4331c39…`, OPERATING_METHOD `98836b52…` | Cited clauses read directly |
| DAG-004 | `HANDOFF_STATE.md` `3c374f5e9fa4cfaa`; `DependencyEdges.csv`, `CandidateEdges.csv`, `ExcludedRows.csv` | Arc layer per row by script (§ "Method" below) |
| `_Decomposition/Open_Issues.csv`, `External_Dependencies.csv` | Open_Issues `9c2d916c277f8ce4` | Current rows for OI-001…026, DEP-004, DEP-005 |
| SCA-V4-003 | `AMENDMENT_PACKET/LEDGER.csv` (216 rows), `RECEIPT.md`, `OWNER_DECISIONS.md`, closure audit `_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-003_2026-10-03_2028/` | Filtered by script |
| Owner decisions | All App v4 runs' `OWNER_DECISIONS.md` (first increment D1–D6; intake DECISION-3…5; pass 2 DECISION-K1; pass 3 DECISION-K3, -L; SCA-V4-003 DECISION-1…3 and the OI-009 carry) | Read for applicable items |
| Design files | Every `PKG-*/1_Working/DEL-*/Design/*.md` grepped for the three IDs and for packaging/examination terms; sections cited below read in full | 20 deliverables have Design folders; none of my three does |
| Closeouts | Pass 2 `closeout/C1-A`, `C1-B`, `C1-C`, `G`; pass 3 `closeout/C1-A`, `C1-B` | Grepped for the three IDs |
| SCC case | `_DAG/cases/SCC-CASE-003/` (Case_Datasheet, Open_Questions, QA) | Members DEL-01-06; DEL-09-01 |
| Supplier facts | DEL-01-01 `HOSTING_BOUNDARY.md` (HOSTING-v0.9), `PIN_SPIKE_0.158.0.md`, `OBS_1/2/3_0.158.0.md` (grepped), committed `Design/generated/0.158.0/` | |
| Spike scratch | `<session scratchpad>/codex-0.158.0/` (exists; partially pruned, see §1.5) | Read only; one `codesign -d` read, no binary executed |
| App v3 exemplar | `projects/chirality-app-dev/frontend/{package.json,build/*.plist,scripts/sign-electron-runtime-v2.mjs,scripts/verify-codex-pin.mjs}`; `execution/_Coordination/AgentRuns/APP_V3_USER_JOURNEYS_20260912/{JOURNEY_RESULTS,BUILD_EVIDENCE_RELEASE_20260913,PUBLIC_RELEASE_20260913}.md` | Historical evidence only |

**Method.** Register rows were read with Python's `csv` module (ACTIVE only).
Each row's DAG-004 layer was looked up by `DependencyID` in
`DependencyEdges.csv` (admitted), `CandidateEdges.csv` (held, with SCC) or
`ExcludedRows.csv` (NOT_TOPOLOGICAL or MIRROR, with its representative).
Reachability was computed by script over the admitted layer and over both
layers. All counts below come from those scripts.

**Not overtaken by any amendment, as a fact.** No SCA-V4-003 ledger row has
`Deliverable` equal to DEL-01-06, DEL-09-01 or DEL-09-02, and no DEFER or
DROP row mentions them (script over all 216 rows). `git log` shows none of
the three ScopeOfWork files changed after INIT. What has moved is the basis
and the owner record around them; the items are listed under each
deliverable's §1.

---

# DEL-01-06 — macOS packaging and distribution evidence

TEST/CONFIG/DOC; INITIALIZED; responsible party "App packaging owner; owner
obtains supplier terms". No Design file exists.

## 1.1 Obligations (20: 4 OUT, 5 REQ, 6 AC, 5 VER)

Basis keys: CST-02 = PRD V4-CST-02; ARC3 = ARCHITECTURE §3 (V4-ARC-01/02 and
"Left to the implementation session"); ARC6/ARC8 = §6 supplier/terms and §8
risks; OQ-08 = PRD §9; EXM-01/03/04 = EXAMINATION §2; HI1 = HOST_INTEGRATION
§1; OPS = OPERATING_METHOD V4-OPS-31…34, §6.

| ID | Obligation (one line) | Rests on |
|---|---|---|
| OUT-001 | Packaging/signing/notarisation configuration for App + stock Codex on macOS Apple Silicon under Tauri | CST-02; ARC3; OI-011 |
| OUT-002 | Candidate-specific binary identity and entitlement record (incl. any code-mode entitlement) | ARC3; OI-011 |
| OUT-003 | Install/launch witness on the packaged target, bound to candidate/config/date/entitlements; usable by PKG-09 | EXM-01/03/04 |
| OUT-004 | Written supplier distribution-terms response, obtained by the owner before public release; unresolved until then | OQ-08; ARC6; ARC8; OI-007/DEP-004 |
| REQ-001 | Target macOS Apple Silicon; bind App + Codex binaries of the hosting basis; inherit nothing from v3 or SWBPIPE | CST-02; EXM-01/03 |
| REQ-002 | Define and evidence signing/notarisation for both binaries and required Codex entitlements at OI-011's point of need; v3 need does not establish v4's | OI-011; ARC3; original-seed ARCHITECTURE §3 |
| REQ-003 | Witness shows the packaged target starts with identified binaries and entitlements; browser examination is not the native witness | EXM-01/03/04 |
| REQ-004 | Terms obligation satisfied before public release; missing terms stay visibly unresolved; no blanket gate on owner use | OQ-08; OI-007 |
| REQ-005 | Perform no act owned elsewhere (DEL-01-01 hosting/pin, PKG-09 joined exam, SWBPIPE, OI-011 owners, supplier/owner) | HI1; OPS §6 |
| AC-001 | Package and App/Codex identities consistent with the hosting basis; config contains the signing arrangement | REQ-001/002 |
| AC-002 | Identity record links package to actual entitlement/signing evidence; no inherited resolution | REQ-001/002 |
| AC-003 | Actual install/launch witness on the target, associable with OUT-001/002 | REQ-003 |
| AC-004 | Actual written response before public release; else reported unresolved | REQ-004 |
| AC-005 | Supplier position, owner's obtaining act, owner's release decision and recorder kept distinct | REQ-004/005 |
| AC-006 | Owner boundaries, both open-issue points of need and the native-witness rule kept; no substitution claims | REQ-001/003/004/005 |
| VER-001 | Inspect config and identity references against the hosting inputs and target | AC-001 |
| VER-002 | Inspect OUT-002 against the actual package and the OI-011 definition | AC-002 |
| VER-003 | Install and launch on the target; record startup, config, date, identities, entitlements | AC-003 |
| VER-004 | Compare terms record with the actual written response, custody and actors; negative fabrication checks | AC-004/005 |
| VER-005 | Compare evidence and handoff with scope and owner claims; negative substitutions | AC-006 |

Also CLM-001…004, AX-001/002, TBD-001 (OI-011), TBD-002 (OI-007/DEP-004),
TBD-003 (DEP-005).

**Moved since INIT (the SoW text is unchanged):**

- **Pin.** TBD-003 and CLM-002 say no supplier version is established.
  First-increment DECISION-1 D4 selected Codex 0.158.0 as the
  *definition/generation* pin; the qualification pin stays under OI-012
  (OI-012 row, Consequence). The owner has now said "yes, download it" for
  `codex-0.160.0-darwin-arm64.tgz` (this run, node VC). A pin advance would
  change the distribution identity and possibly the entitlement facts this
  deliverable records.
- **Who decides OI-011.** CLM-002 names "App implementation owner with SWB
  owner". Pass-3 DECISION-L L-7 states "the App implementation owner is the
  owner" (its option text is about OI-009/DEL-01-05; later records apply it
  more widely, e.g. DEP-01-02-018 Notes "the App implementation owner (also
  the Owner, DECISION-L L-7)"). Inference: OI-011 is the owner's with the SWB
  owner. The SWB co-owner is reachable only by human relay, and host joins
  are deferred (intake DECISION-3).
- **SWBPIPE packaging knowledge (DEP-01-06-012).** None received: a search
  of `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` for signing,
  notarisation, entitlement, bundle or packaging finds no packaging content.
- **Bundle contents now designed by others** (pass 3; no register row):
  bundled workflows and the shipped-revision manifest (WR-v0.2 §3 "Layout
  and data placement", rows "Bundled workflows" and "Shipped-revision
  manifest", both "Inside the App bundle"; LS-5, LS-8; DECISION-L L-4),
  shipped product guidance and role files (ROLE-v0.2 §4.2 "The guidance
  store", GS-2/GS-3; U-R11), and the act control's key store "available only to the signed App"
  (AAC-v0.2 §6.3 SEAL-2, PROPOSED). Each puts a requirement on the package
  that DEL-01-06's SoW does not name.

## 1.2 Joins

| Row | Direction / type | Other end | DAG-004 | Maturity / satisfaction |
|---|---|---|---|---|
| DEP-01-06-006 | UPSTREAM PREREQUISITE | DEL-01-01 (stock binary and hosting basis) | **admitted** (representative); mirror DEP-01-01-023 | INITIALIZED / TBD |
| DEP-09-02-014 (DEL-09-02's row) | DEL-09-02 consumes packaged candidate + packaging evidence | DEL-09-02 | **admitted** | INITIALIZED / TBD. **No supplier-side row here**: DEL-01-06 names only PKG-09 (DEP-01-06-007) |
| DEP-09-01-016 (DEL-09-01's row) | DEL-09-01 consumes the actual package for native smoke | DEL-09-01 | **held**, SCC-003 (SCC-CASE-003) | INITIALIZED / TBD |
| DEP-09-01-021 (DEL-09-01's row) | DEL-01-06 consumes examination support | DEL-09-01 | **held**, SCC-003 | INITIALIZED / TBD |
| DEP-01-06-007 | DOWNSTREAM HANDOVER → PKG-09 | package | NOT_TOPOLOGICAL | TBD / TBD |
| DEP-01-06-008 | UPSTREAM CONSTRAINT | OI-011 | NOT_TOPOLOGICAL | TBD |
| DEP-01-06-009 | UPSTREAM INTERFACE | DEP-005 (Codex/Tauri packaging interfaces) | NOT_TOPOLOGICAL | TBD |
| DEP-01-06-010 / -011 | UPSTREAM CONSTRAINT / DOWNSTREAM HANDOVER | DEP-004 (supplier position; owner's distribution decision) | NOT_TOPOLOGICAL | TBD |
| DEP-01-06-012 | UPSTREAM INTERFACE | SWBPIPE (optional knowledge) | NOT_TOPOLOGICAL | TBD |

Reach (script): admitted, DEL-01-06 reaches only DEL-01-01; it is reached by
DEL-09-02 and DEL-11-03. With held arcs it also reaches DEL-09-01 and
DEL-01-05.

**What the first-increment Design file assumes of DEL-01-06** (DEL-01-01,
HOSTING-v0.9; PIN_SPIKE-v0.1):

- HOSTING §8, seam S-5: supplies "Distribution content identity over the
  vendor tree, version label, launcher record; spike-observed signing facts
  (Developer ID, hardened runtime) as observations only"; **not supplied**:
  "Packaging, signing, notarisation, relocation of the vendor tree
  (not-observed), distribution".
- HOSTING §4.2 step 1: "Resolve the supplier distribution … and the launcher
  (U-17; location is a packaging concern, DEL-01-06)."
- HOSTING §7.1/§7.2: verification requires the observed version label
  **and** "the distribution content identity equals the expected identity"
  over the vendor tree (`bin/codex`, `bin/codex-code-mode-host`,
  `codex-path/rg`, bundled `zsh`, voice resources).
- HOSTING §10 P-02: "relocation → DEL-01-06"; still-to-observe list:
  "relocation of the vendor tree (DEL-01-06)".
- HOSTING UNRESOLVED U-17: "Distribution-identity composition and launcher
  (wrapper vs vendor) | App implementation owner with DEL-01-06 | Before
  verification implementation".
- HOSTING §11: "Packaging, signing, notarisation, distribution | DEL-01-06
  (terms obtained by owner, OQ-08) | S-5".
- PIN_SPIKE UNRESOLVED: "Relocatability of the vendor binary apart from its
  sibling resources | DEL-01-06 | Before packaging | not-observed".

**What pass-3 Design files assume (no register row):** ACCESS-v0.2 §0 sends
"distributed sign-in terms (DEL-01-06, OI-007)" here; ACCESS §20 lists
"Packaging items for DEL-01-06: keychain access, a loopback port, OpenAI's
branding rules, open-source eligibility beside OI-007", but only for the
plan-grant alternative, which is recorded as considered, not adopted. WR,
ROLE and AAC as in §1.1.

## 1.3 Proposed contract changes still open

- **None in the SCA-V4-003 ledger, RECEIPT or closure audit** names
  DEL-01-06 (script; and the closure audit's issue log has no DEL-01-06
  finding).
- **Survey observations, not yet proposed anywhere:**
  - DEP-09-02-014 has no supplier-side counterpart in DEL-01-06 (only the
    PKG-09 package row). SCC-CASE-003's datasheet notes the same row.
  - The bundle-content seams (WR, ROLE, AAC SEAL-2) and HOSTING's relocation
    and launcher items have no row. See structural question SQ-4 for the
    direction that is SCC-safe.

## 1.4 Open items and owner choices

| Item | Shapes the design now? | Options and what the files say | Owner? |
|---|---|---|---|
| **OI-011** signing, notarisation, required Codex entitlements (owner + SWB owner; before packaged distribution witness) | **Yes, most of the file.** | (A) The App re-signs every Mach-O in the Codex vendor tree with its own Developer ID, hardened runtime and per-binary entitlements (v3 practice: `sign-electron-runtime-v2.mjs`, "JIT only for the Code Mode host"). (B) Codex binaries ship with the supplier's own signature (Developer ID OpenAI OpCo, team 2DC432GLL2, hardened runtime, timestamp: PIN_SPIKE §3) and only the App's code is signed; the whole `.app` is notarised. (C) Not bundling Codex (fetch at first run): the files give no basis for it and it conflicts with a pinned packaged identity. A vs B decides whether HOSTING §7.2's content-identity rule holds unchanged (SQ-1). Also App Sandbox on or off (v3: off; inference: Codex in App-owned homes with a symlinked `config.toml`, HOSTING §4.2 step 3, and work in project folders needs it off) | **Yes** |
| OI-011 co-owner | Yes for the record's actors | Whether the owner decides the App's arrangement now with SWBPIPE knowledge optional (DEP-01-06-012), or waits for a relay to the SWB owner while host joins are deferred | **Yes** |
| Notarisation act | Yes (sequence and actor) | Apple credentials are the owner's. v3: the owner "explicitly directed this agent to perform notarization with the existing Apple setup" (PUBLIC_RELEASE_20260913). The design must name who performs submission and stapling for v4 | **Yes** (at the point of need) |
| **OI-007 / DEP-004** written supplier position (owner and supplier; before public release beyond owner use) | No: only the record's form and the release gate | v3.0.0 was published publicly on GitHub releases (PUBLIC_RELEASE_20260913). A grep of v3 `docs/` and `_DECISIONS/` finds no record of a written terms position. Whether v4 is to be publicly released, and when, sets when OUT-004 is needed | Owner awareness; no design choice |
| **OI-012** qualification pin; 0.160.0 advance (VC) | Values, not structure | The design can be written pin-parameterized; the identity table fills per pin | No new choice (VC is approved) |
| HOSTING U-17 launcher (npm wrapper vs vendor binary) | Yes (bundle layout, environment) | Wrapper adds `CODEX_MANAGED_PACKAGE_ROOT`, `CODEX_MANAGED_BY_NPM=1` (HOSTING §7.1); v3 shipped the vendor tree as `Resources/codex` and launched the vendor binary | App implementation owner (= owner, L-7) |
| Relocatability of the vendor tree | Yes | Not observed at 0.158.0. Can be observed in scratch without sign-in (copy the tree, run `--version` with a probe home) | No (an observation) |
| WR U-WR-18 (shipped-revision manifest contents; whether v3's shipped workflows are recognized) | Minor (bundle manifest) | "owner if v3 copies should be recognized" | Minor |
| ROLE U-R11 shipped `default_for_new_chat` | No | Release data | No |

## 1.5 What exists to build on

- **Supplier facts at 0.158.0 (DEL-01-01).** npm `@openai/codex@0.158.0`,
  platform package `-darwin-arm64`; vendor tree `bin/codex` (sha256
  `788a818f…35c8`, 239,662,592 B), `bin/codex-code-mode-host`,
  `codex-path/rg`, `codex-resources/zsh/bin/zsh`, `codex-resources/voice/…`;
  `codesign`: Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2),
  hardened runtime, timestamp; `spctl` "rejected (… does not seem to be an
  app)", "not a notarisation verdict" (PIN_SPIKE §2–§3). Relocation not
  tested. Generated JSON Schema bundles committed under
  `Design/generated/0.158.0/`; TS regenerated deterministically, not
  committed (HOSTING §7.3).
- **Spike scratch folder (exists, partly pruned).**
  `codex-0.158.0/pkg/node_modules/@openai/codex-darwin-arm64/vendor/aarch64-apple-darwin/`
  now holds `bin/codex` and `codex-resources/zsh/bin/zsh`;
  `bin/codex-code-mode-host` and `codex-path/rg` are gone (directories
  empty). `shasum -a 256 bin/codex` = `788a818f…35c8` (matches PIN_SPIKE).
  **My observation, 2026-10-03, by `codesign -d --entitlements - --xml`
  (reads the signature; the binary was not run):** `bin/codex` carries
  `com.apple.security.cs.allow-jit` and
  `com.apple.security.cs.allow-unsigned-executable-memory`; flags
  `0x10000(runtime)`; team 2DC432GLL2. The bundled `zsh` is hardened-runtime,
  same team, no entitlements. The code-mode host's entitlements could not be
  read (file absent). This is a survey observation, not a Design record.
- **App v3 exemplar (historical evidence only; v3 used Electron, v4 is
  Tauri 2).** `package.json` `build.mac`: hardened runtime, custom `sign`
  hook, entitlements `entitlements.mac.plist` (allow-jit),
  `entitlements.mac.inherit.plist` (empty), `entitlements.mac.code-mode-host.plist`
  (allow-jit), DMG arm64, minimum macOS 15.0.0; vendor tree copied to
  `Resources/codex`. `verify-codex-pin.mjs` compares version and sha256 of
  `codex` and `codex-code-mode-host`, digests on the unsigned pack because
  "Signing changes a Mach-O's bytes", version-only after signing.
  `BUILD_EVIDENCE_RELEASE_20260913.md`: "ordinary Codex entitlements empty,
  Code Mode host JIT only"; Gatekeeper "Unnotarized Developer ID" before
  notarisation; `PUBLIC_RELEASE_20260913.md`: notarisation Accepted,
  stapled, Gatekeeper "Notarized Developer ID". **Inference to check, not
  established:** at v3's 0.154.0 the App re-signed `codex` with no
  entitlements, while the supplier's 0.158.0 signature carries two; whether
  the supplier's set changed between versions or v3 stripped it is not
  known from these files.
- **v3 user journeys** J01–J09 ran actual Codex sessions on an installed
  signed App and on development candidates; the record says they "do not
  qualify a subsequently signed installer" (JOURNEY_RESULTS). Useful as
  method precedent for OUT-003.

## 1.6 Design scope for this pass

1. **Package composition** (interfaces, data): bundle layout for the App
   binary, the Codex vendor tree with siblings and the launcher (U-17),
   bundled workflows and shipped-revision manifest (WR LS-5/LS-8), shipped
   guidance (ROLE GS-2/3), with each item's supplier and where the App reads
   it at run time. Relocation stated as an observation to make.
2. **Signing and entitlement design for OI-011**, written as options A/B
   with consequences, a per-executable table (signer, hardened runtime,
   entitlements, source of the value per pin), App Sandbox stance,
   notarisation and stapling, and SEAL-2's dependence on the signing
   identity. Decided by the owner at node K; the design carries both until
   then.
3. **Candidate identity record (OUT-002)**: elements and a PROPOSED schema:
   App build identity, HOSTING §7.1 distribution identity, pre-sign and
   post-sign digests (v3 lesson), signing identity and team, per-binary
   entitlements as read, notarisation submission and ticket, installer
   digest; outcome per DEL-09-01's states.
4. **Operating sequence with failure behaviour**: stage → sign → verify
   (`codesign --verify --deep --strict`) → notarise → staple → Gatekeeper
   assess → install → launch → Codex handshake under the App, with what each
   failure means (e.g. a missing JIT entitlement observed as a Codex crash
   is a failed witness, not "blocked").
5. **Install/launch witness procedure (OUT-003)** and its record, usable by
   DEL-09-01's native smoke route and DEL-09-02.
6. **Terms record template (OUT-004)** with UNRESOLVED standing and the
   three actors kept apart.
7. **Designed verification cases** VER-001…005; a small local check that
   reads signatures of a staged tree (`codesign -d`) is possible without
   credentials.

**Leave out:** any actual signing, notarisation or release (owner
credentials and acts); Windows; legal or terms conclusions; SWBPIPE's
package; installer UX beyond what the witness needs.

---

# DEL-09-01 — Candidate examination infrastructure and evidence protocol

TEST_SUITE; INITIALIZED; responsible party "App examination owner;
independent reviewer separate from each candidate author". No Design file.

## 2.1 Obligations (30: 4 OUT, 8 REQ, 9 AC, 9 VER)

Basis keys: CST-06 = PRD V4-CST-06; EXM§1/§2 = EXAMINATION §§1–2 and
V4-EXM-01…05; M-7 = ARCHITECTURE §1 M-7; OPS-34 = OPERATING_METHOD
V4-OPS-34 with D-13; HTML03/04 = DECISION_BRIEF decisions 03/04; OI-015.

| ID | Obligation | Rests on |
|---|---|---|
| OUT-001 | Invented-data and recorded-protocol fixture support with origin and configuration | CST-06; EXM-02; M-7 |
| OUT-002 | Candidate/configuration evidence capture; observations, missing inputs, verification vs validation | EXM-01; EXM§1 |
| OUT-003 | Outcomes, reopening, criterion protection and independent-review protocol | EXM-03/05; OPS-34 |
| OUT-004 | WebKit, Chromium and native packaged-app execution support with identities kept apart | EXM-04; OI-015 |
| REQ-001 | Invented material; recorded exchanges traced and replayable; few deliberate live runs; replay is not a live witness | CST-06; EXM-02 |
| REQ-002 | Every result names candidate, date, harness/model versions, model server, criterion, evidence and one of five states, defined | EXM-01; EXM§1 |
| REQ-003 | Verification vs practitioner validation; actor vs recorder; no inferred acceptance; no invented act order | EXM§1; HTML03 |
| REQ-004 | Changed candidate reopens affected scenarios; old passes stay with their candidate | EXM-03 |
| REQ-005 | Criteria protected in repair; any authorized criterion change keeps its decision | EXM-05; HTML04 |
| REQ-006 | Independent review bound to the candidate; separation, model identity, Codex preference, Claude fallback | OPS-34; D-13 |
| REQ-007 | WebKit + Chromium + macOS WebKit + native smoke of each targeted package; no Windows | EXM-04; OI-015 |
| REQ-008 | Perform no act owned by DEL-01-06, 09-02, 09-05…09-12 or feature owners | DEC rows; HI |
| AC-001…009 | One per REQ-001 (two: fixtures; replay), 002, 003, 004, 005, 006, 007, 008 | as REQs |
| VER-001…009 | Inspect fixtures; exercise replay; exercise capture incl. missing/inconclusive; human-act positive and negatives; changed-candidate reopening; repair chain; review record; WebKit/Chromium/native routes; owner mapping | as ACs |

Also CLM-001…006, AX-001…003 and TBD-001's table of ten open matters
(OI-001, 002, 003, 005, 011, 012, 016, 021, 023, 026).

**Moved since INIT:**

- **TBD-001 rows OI-001/OI-002** read "No blanket always-reserved list is
  fixed" and "without selecting a classifier policy". First-increment D2
  (five reserved acts) and D3 (routine permissions are the user's Codex
  setting in the App; no host classifier mode) now rule them for the first
  increment (Open_Issues Consequence). The OI-001/OI-002 row consistency
  point is listed open in DAG-004 HANDOFF ("Rows naming OI-001 or OI-002 stay
  ACTIVE in nine registers").
- **TBD-001 row OI-012**: D4 selected 0.158.0 for definition/generation; the
  qualification and replay pin is open. VC may advance to 0.160.0.
- **Outcome-state spellings are now split across PROPOSED designs** (see
  §2.5); REQ-002 names the states but not their spelling.
- **Independent review practice.** The project's own reviews (for example
  SCA-V4-003 V26) are run by Claude Code subagents; the standing direction is
  "Ensure you are using `opus-5.5` models on `high` reasoning for your Type 1
  and Type 2 agent instances" (pass-3 OWNER_DECISIONS, standing
  directions). V4-OPS-34 prefers a Codex reviewer, with Claude as the stated
  fallback "if the Codex session is unavailable" (SoW CLM-004). These are
  definition reviews, not candidate reviews, but the protocol must say how
  the preference is applied to candidates.
- **DEL-09-06 now names DEL-09-01 as supplier** (S-0906-3 / R-0906-3,
  INCLUDE in SCA-V4-003; DEP-09-06-035 is the admitted representative).

## 2.2 Joins

| Row | Other end | DAG-004 | Maturity / satisfaction |
|---|---|---|---|
| DEP-09-01-019 UPSTREAM CONSTRAINT | DEL-01-01 (selected pin before protocol generation and qualification) | **admitted** | **TBD** / TBD. Mirror DEP-01-01-031 says INITIALIZED: one of DAG-004's three "mirror maturity differences"; "read both rows" |
| DEP-09-01-016 UPSTREAM PREREQUISITE | DEL-01-06 (actual package for native smoke) | **held** SCC-003 | INITIALIZED / TBD |
| DEP-09-01-021 DOWNSTREAM HANDOVER | DEL-01-06 (examination support to packaging) | **held** SCC-003 | INITIALIZED / TBD |
| DEP-09-01-022 → DEL-09-02 | rep. DEP-09-02-020 | **admitted** | INITIALIZED / TBD |
| DEP-09-01-023 → DEL-09-05 | rep. DEP-09-05-011 | **admitted** | INITIALIZED / TBD |
| DEP-09-01-024 → DEL-09-06 | rep. DEP-09-06-035 (changed by rule at DAG-004) | **admitted** | INITIALIZED / TBD |
| DEP-09-01-025 → DEL-09-07 | itself the representative | **admitted** | INITIALIZED / TBD |
| DEP-09-01-026 → DEL-09-09 | rep. DEP-09-09-012 | **admitted** | INITIALIZED / PENDING (DEL-09-09's row) |
| DEP-09-01-027 → DEL-09-10 | itself | **admitted** | INITIALIZED / TBD |
| DEP-09-01-028 → DEL-09-11 | itself | **admitted** | INITIALIZED / TBD |
| DEP-09-01-029 → DEL-09-12 | itself | **admitted** | INITIALIZED / TBD |
| DEP-09-01-013, -014, -015, -017, -018 | candidate inputs; feature evidence; recorded exchanges; review record; human-act evidence | NOT_TOPOLOGICAL (UNKNOWN/DOCUMENT) | TBD |
| DEP-09-01-020 | later research fixture admission (Domains) | NOT_TOPOLOGICAL (EXTERNAL) | TBD |
| DEP-09-01-030 | results to the named independent reviewer | NOT_TOPOLOGICAL (UNKNOWN) | TBD |

Reach (script): admitted, DEL-09-01 reaches only DEL-01-01; it is reached by
DEL-03-04, 09-02, 09-05, 09-06, 09-07, 09-09, 09-10, 09-11, 09-12, 10-02 and
11-03.

**What first-increment Design files assume of DEL-09-01:**

- **DEL-01-01 HOSTING §8** (receivers table): "DEL-06-01, DEL-09-01
  (outside) | DEP-06-01-013, DEP-09-01-019 (admitted) | The selected supplier
  pin, before protocol generation and qualification | Pin note; §7.1; U-01
  (0.158.0 is the definition and generation pin only)". HOSTING §9 also
  defines the recorded-exchange fixture method (capture, redaction
  categories, standing labels `recorded`, `recorded-truncated`, `mutated`,
  `constructed`; outcome labels "`pass`, `fail`, `blocked`, `not-run`,
  `inconclusive`, bound to candidate + pin"), the X-01…X-14 seam set and a
  supplier double. No row links §9 to DEL-09-01; it overlaps DEL-09-01
  OUT-001/REQ-001.
- **DEL-09-06 CA-v0.7**: §5 "Examination infrastructure and protocol |
  DEL-09-01 | — | all examiners | Not in this undertaking (D1)"; §6 ST-1
  "App-local executable fixtures … App construction (later undertaking);
  DEL-09-01 protocol"; §8.4 W14 result record: "a shared form, if any, is
  DEL-09-01's"; §11.1 "DEL-09-01 | Supplier-side DEP-09-01-024 | Reusable
  examination support and evidence interfaces | Not in this undertaking (D1);
  not defined"; UNRESOLVED "DEL-09-01 evidence protocol … Before
  candidate-bound results | Labels per C mapping only".
- **DEL-09-09 XT**: §2 IN-03 "Shared candidate/date/configuration protocol;
  WebKit/Chromium and packaged-smoke evidence protocol | DEL-09-01 (outside
  D1; DEP-09-09-012) | §6 | Not defined in this undertaking"; §6 "until it
  exists, interface observations carry the limit 'protocol not yet
  defined'"; §3.4 "The same elements carry the same meanings as DEL-09-06's
  W14 result record … a shared form, if any, is DEL-09-01's protocol"; F-28
  (same point, "Recorded for the phase review with OI-013/OI-014"); §7
  "Reusable examination harness | App DEL-09-01 (outside D1) | Protocol need
  recorded (IN-03)".
- **Pass-2 closeout C1-C §7** lists "A shared examination-result form for
  DEL-09-01 (XT F-28). Outside the increment." as carried.

## 2.3 Proposed contract changes still open

- **None in the SCA-V4-003 ledger names DEL-09-01's own files.** Applied
  rows touching it: S-0906-3 / R-0906-3 (DEL-09-06 names DEL-09-01) and
  R-11-1 (DEL-01-01 mirror DEP-01-01-031).
- **Carried, not a ledger item:** the shared result form (XT F-28; pass-2
  C1-C §7).
- **Register owners' items from DAG-004 HANDOFF:** the DEP-09-01-019 /
  DEP-01-01-031 maturity difference (TBD vs INITIALIZED).
- **SCC-CASE-003**: CP1 confirmed tracking only; `Ruling_Register.csv` is
  header-only; R1 (explicit contribution milestones under existing owners)
  is the case's recommendation; R2 (graph merge-group) and R3 (hold) are the
  alternatives. No ruling exists.

## 2.4 Open items and owner choices

| Item | Shapes the design now? | Options / file text | Owner? |
|---|---|---|---|
| **Native macOS execution route** for packaged smoke and native journey steps (window close/reopen, quit/relaunch) | **Yes (OUT-004)** | Not discussed in any v4 file. RECOVERY VC-R-14 and NIR VC-NIR-11 already mark these as needing a candidate and **P** (the person). Options: person-operated native witness with an evidence form; scripted macOS UI automation; Playwright-style WebKit/Chromium runs for the interface only. *General knowledge, not verified in this repository:* Tauri's WebDriver route (`tauri-driver`) has not supported macOS WKWebView, so native automation on macOS would need another tool | App implementation owner (= owner, L-7) |
| **Independent candidate review**: Codex preference vs Claude fallback (V4-OPS-34, D-13; SoW CLM-004, REQ-006) | **Yes (review protocol)** | Whether candidate reviews run a Codex reviewer (possible through the stock Codex the App hosts), or whether the owner's Opus direction makes the Claude fallback the standing arrangement, recorded as such each time | **Yes** |
| Shared result form (XT F-28; CA §8.4) | **Yes (record design)** | (a) a shared core record that DEL-09-06/09-09 adopt, with per-witness extensions; (b) a vocabulary map only, each journey keeping its own schema. DEP-09-06-035 and DEP-09-09-012 already consume DEL-09-01 (admitted), so (a) needs no new arc | Integrator ruling; not owner |
| **OI-012** replay/qualification pin; VC 0.160.0 | Values | Fixtures bind to a pin; a pin change reopens affected scenarios (REQ-004) | No new choice |
| **OI-011** (via DEL-01-06) | Yes for the native route's inputs | Native smoke waits for a signed package; unsigned local builds may run but must be labelled | Through DEL-01-06 |
| OI-001/OI-002 (D2/D3) | No (record carries the ruled values) | TBD-001 text partly overtaken | No |
| OI-003 / OQ-10, OI-021, OI-023, OI-026 | No (they shape journey criteria owned elsewhere) | Carried with their owners | No (here) |
| OI-005 additional hosts | No | None presumed | No |
| OI-016 owner validation period | No (validation is DEL-09-12's) | Kept distinct | No (here) |
| Test tooling / CI for v4 | Yes (implementation details of OUT-002/004) | LOOP_INIT: "A v4 `software-workflow.json` is not yet present; do not borrow v3 commands" | App implementation owner |

## 2.5 What exists to build on

- **Vocabularies already in PROPOSED Design files** (all would map to
  DEL-09-01's record):
  - Outcome: HOSTING §9.3 prose `pass/fail/blocked/not-run/inconclusive`;
    the CA §8.4 and XT §3.4 schemas (`w14-result-record.schema.json`,
    `xt-result-record.schema.json`, the only Design schemas with `not_run`)
    use `passed/failed/blocked/not_run/inconclusive`; EXAMINATION §1 prose
    "passed, failed, blocked, not run or inconclusive". (RS's
    `RS_RECORD.schema.json` has a `passResult` enum "pass", "does not pass",
    "not established", … for compatibility reports: a different concept.)
  - Run kind and evidence label (CA, XT schemas): `joined_witness`,
    `rehearsal`, `definition_check`; `illustrative`, `test_double`,
    `actual_host`, `not_observed`, `limited`; case state `DESIGNED`,
    `AWAITING INPUT`, `HELD`; `subject_of_run` one of candidates / double /
    definition. Their `configuration` objects differ (W14:
    `acting_surface_variant`, `native_path`; XT: `realization_family`,
    `native_path`, `endpoint`).
  - "Needs" legends: RECOVERY §11.1 **D** stub/model, **F** fixture, **P**
    person, **C** candidate, **O** observation, "'Ran (model)' … passes no VER
    criterion"; NIR §13.1 *model*, *fixture*, *double*, *person*,
    *candidate*, "No case can pass a VER criterion until a candidate exists".
  - Fixture standing (HOSTING §9.2) and redaction categories (HOSTING §9.1,
    extended at v0.9 for account methods, secret answers, provider-bound
    identifiers, time zone, skill paths).
- **Prototypes**: every Design folder except DEL-03-04's has a
  `prototype/` that runs the file's designed rules over a stub or double
  (e.g. HOSTING's change table records "`run_cases.py` TOTAL 35, FAIL 0" at
  pass-3 C0). These are definition checks; DEL-09-01's
  `definition_check` run kind already names them.
- **Recorded exchanges**: eight redacted spike transcripts
  (`generated/0.158.0/_spike/transcripts/`, labelled `recorded`, "not X-01
  fixtures"); OBS-2 raw logs named as candidates for `recorded` fixtures
  (NPTD §15.1).
- **App v3 exemplar (evidence only):** a v3 PKG-09 with DEL-09-01 "Section 8
  harness validation preservation", DEL-09-02 "Section 9 runtime validation
  additions", DEL-09-03 unit/integration tests, DEL-09-05 CI artifact and
  release verification; `vitest` with 217 test files under `frontend/src`;
  scripts `validate-harness-section8/9.mjs`, `run-packaged-security-proof.mjs`,
  `verify-version-identity.mjs`, `validate-release-quality-evidence.mjs`.
  No Playwright or cross-engine test configuration was found in v3: a grep
  for playwright/webkit/chromium hits only the lockfile, two Electron
  source files (`electron/main.ts`, `electron/renderer-window-policy.ts`)
  and execution records.

## 2.6 Design scope for this pass

1. **Examination record core** (data): candidate identity, configuration
   (harness and model versions, model server, per App-owned home after
   DECISION-L L-1), date, criterion with source identity, evidence
   references with provenance category, run kind, evidence label, outcome
   with the five definitions, missing inputs, evidence limits, blocked-by;
   one PROPOSED schema with valid and invalid examples; a vocabulary map to
   HOSTING §9, CA §8.4, XT §3.4, RECOVERY/NIR "Needs".
2. **Fixture support** (OUT-001): invented-material catalogue rules; adopt
   HOSTING §9's capture/redaction/labels by reference (HOSTING is upstream;
   see SQ-2); replay vs live marking; a live-run selection record.
3. **States and sequences**: case lifecycle (designed → awaiting input →
   run → outcome), reopening on candidate, pin or configuration change
   (affected-scenario mapping), repair chain with protected criterion.
4. **Independent review protocol** (OUT-003): reviewer separation, model
   identity, preference/fallback, findings and dispositions; distinct from
   human acceptance.
5. **Execution routes** (OUT-004): WebKit and Chromium interface runs;
   native packaged smoke on macOS (route per owner choice); identity of
   engine/platform/package; unavailable route → `blocked` or `not_run`,
   never a browser substitute.
6. **SCC-003 contribution milestones** (case R1): the support revision
   DEL-01-06 uses, and the package DEL-09-01 examines, as named versions.
7. **Designed verification cases** VER-001…009 and a prototype that
   validates example records and the reopening rule.

**Leave out:** journey cases (owned by 09-02, 09-05…09-12); any product run;
CI implementation; Windows; Domains fixtures beyond the admission rule.

---

# DEL-09-02 — Standalone App candidate qualification

TEST_SUITE; INITIALIZED; responsible party "App workflow-experience
integration owner; independent candidate examiner assembles qualification".
No Design file.

## 3.1 Obligations (27: 2 OUT, 9 REQ, 8 AC, 8 VER)

Basis keys: EXM-10/11/12 = EXAMINATION §3; EXM§1/§2; EXM§7; APP = PRD
V4-APP-01/02/04; WF = V4-WF-01…05; EXE = V4-EXE-01…04; AUT = V4-AUT-03/04;
REC = V4-REC-02…05; ARC3; HI = HOST_INTEGRATION V4-HI-30…33/42; OPS-31/34.

| ID | Obligation | Rests on |
|---|---|---|
| OUT-001 | Joined V4-EXM-10/11/12 scenario definitions and candidate-bound records in one undertaking | EXM-10/11/12 |
| OUT-002 | One dossier linking feature checks, native interaction, registration/checkpoint evidence, recovery and three-mode outcomes; feeds DEL-11-03 | EXM§1–3, §7 |
| REQ-001 | All three scenarios on one identified candidate with revision/build, configuration, date; changes reopen | EXM-01/03; OPS-31/34 |
| REQ-002 | V4-EXM-10 from empty folder: plan, revise, real tools, draft, review, explicit registration, reuse on new inputs, two refinements; declared parts, source identity, no silent overwrite or rebinding | EXM-10; APP-01/04; WF-01…03 |
| REQ-003 | Human acts distinguished from execution, proposals, permissions, checking, approval, reliance; positive record and fabrication negatives | WF-02/05; EXE-02; AUT-03/04; REC-02…05; HI |
| REQ-004 | V4-EXM-11 during V4-EXM-10: stop, close/reopen, one deny and one grant, quit/relaunch, continue | EXM-11; EXE-01…04 |
| REQ-005 | Provider vs rendered state, primary vs descendants, settlement vs acknowledgment; unknown stays unknown | EXM-11; ARC3 |
| REQ-006 | V4-EXM-12: ChatGPT sign-in, API key and local server configured together; one conversation each; selection | EXM-12; APP-02; ARC3 |
| REQ-007 | Five outcome states; inputs gaps explicit; native vs browser; invented material; replay where possible | EXM§1–2; OI-015; CST-02/06 |
| REQ-008 | No act owned by 01-01…01-06, 02-01…02-03, 04-01, 04-03, 09-01, 09-05, 09-12, 11-03 | Rows |
| REQ-009 | No policy decision; the person acts; owner decides replacement | HTML03; OQ-02; OI-001/002 |
| AC-001…008 | EXM-10 complete; workflow identity/registration/no overwrite; human acts; EXM-11 sequence; recovery distinctions; EXM-12; single dossier; return to DEL-11-03 | as REQs |
| VER-001…008 | Observe EXM-10; inspect declared part and collision; join act to PKG-04 record; carry out EXM-11; inspect recovery seam; three modes; examine the dossier independently; review the handoff | as ACs |

Also CLM-001…004, AX-001…004, TBD-001…004.

**Moved since INIT (SoW unchanged):**

- **OI-009 carried wording (owner item 1, "1 yes"; this run's
  OWNER_DECISIONS and SCA-V4-003 OWNER_DECISIONS "After closure").**
  TBD-002 reads: "OI-009 remains OPEN: Owner with App implementation owner,
  before account integration, chooses separated versus shared Codex account
  state." DEP-09-02-027 (ACTIVE, EXTERNAL, target OI-009) Statement: "Consume
  the Owner with App implementation owner's separated-versus-shared Codex
  account-state disposition, needed before account integration;
  qualification does not assume the v3 overlay." Notes: "FACT: Accepted
  issue remains OPEN in the source." Current `Open_Issues.csv` OI-009:
  `RESOLVED_BY_OWNER_DECISION` (supersession D-021), "Decided at choice level
  by … DECISION-K3 K-1: the App's Codex shares the person's settings,
  providers and MCP servers and signs in separately, custodied by Codex in an
  App-owned home … sign-in with a credential is not observed (DECISION-L
  L-6), and API-key behaviour stays with OI-010." Closure audit ASC-ISS-002
  (MINOR): "DEL-09-02 ScopeOfWork TBD-002 and DEP-09-02-027 still state
  OI-009 as OPEN"; its recommended route is "a later amendment item revising
  DEL-09-02 TBD-002 … followed by a `dependency-extract` UPDATE of
  DEP-09-02-027". **Effect now:** the item is carried to the next amendment;
  no DEL-09-02 file changes before then. The design reads OI-009 from
  `Open_Issues.csv` and the decision record (DEL-01-05
  `ACCOUNT_HOME_DECISION_RECORD.md`), not from TBD-002. TBD-002's OI-008
  half stays correct (OI-008 OPEN; HOSTING §12 O-1 proposed, not selected).
- **TBD-001 (OI-001/OI-002 "remain OPEN")**: ruled for the first increment
  by D2/D3; the SoW already says "Apply settled false-attribution and
  explicit-registration rules now". Same register consistency point as
  DEL-09-01 (DEP-09-02-024/-025 Notes "Accepted issue remains OPEN in the
  source"). Candidate for the same amendment.
- **TBD-003 OI-012**: definition pin 0.158.0 (D4); qualification pin open;
  VC 0.160.0 approved.
- **The App act control is now DEL-01-04's** (SCA-V4-003 Q-5: OUT-005,
  REQ-008, AC-008, VER-008, including "an A15 act on one reviewed draft and
  an A15 act on two library entries in one act"). V4-EXM-10's "registers it"
  step is captured there. DEL-09-02's CLM-001 lists DEL-01-04 only for
  "native interaction views", and DEP-09-02-012 says "native
  interaction-view contribution and scoped request/outcome checks";
  DEL-01-04's revised CLM-001 likewise says DEL-09-02 receives "native
  interaction view and scoped request/outcome checks". Neither names the act
  control. Inference: a wording gap for the next amendment (same arc; no
  graph effect).
- **DECISION-K3 K-7**: "Only registered revisions run. A draft is tried out
  in an ordinary conversation." WR TT-7 (PROPOSED): "'refine twice'
  (V4-EXM-10) is two registered revisions, each run on new inputs". Shapes
  how AC-001's two refinements are observed.
- **DECISION-L L-1**: API-key conversations use a second App-owned Codex
  home, one Codex process per home. V4-EXM-12's "configured together" is
  two homes and a local provider; the configuration binding (REQ-001) is per
  home. **L-6**: "no sign-in or API-key observation now", so no part of
  V4-EXM-12 with credentials has been observed; the joined witness will be
  the first.
- **DEC-4 (SCA-V4-001)**: no default between local and cloud. NIR VC-NIR-12
  "No model selected" applies at the V4-EXM-12 start.
- **EXAMINATION §7**: the replacement evidence is "V4-EXM-10 and V4-EXM-11
  passed on the candidate App (the core loop at least at v3.0.1's level)".
  DEL-11-03's row DEP-11-03-006 asks for "the v3.0.1 core-loop comparison and
  applicable V4-EXM-10/11 observations". DEL-09-02's SoW does not mention a
  v3.0.1 comparison; the dossier should carry what that comparison needs.

## 3.2 Joins

All twelve supplier arcs are **admitted**, each represented by DEL-09-02's
own UPSTREAM row (INITIALIZED / TBD):

| Row | Supplier | Supplier-side mirror | What the first-increment or pass-3 Design file says about DEL-09-02 |
|---|---|---|---|
| DEP-09-02-009 | DEL-01-01 | DEP-01-01-032 | HOSTING §8: "Supplier hosting and protocol contribution and scoped feature checks, before the joined witness | §9 method and the designed cases; nothing is qualified" |
| DEP-09-02-010 | DEL-01-02 | DEP-01-02-023 | RECOVERY header Receivers: "the recovery contribution and focused checks"; §11.1 VC-R-14 "Native witness (V4-EXM-11) … During V4-EXM-10's run: stop a turn, close and reopen the window, deny one approval and grant another, quit (confirming the question) and relaunch, continue … browser evidence alone never stands for it" — Needs C, P; Not run |
| DEP-09-02-011 | DEL-01-03 | DEP-01-03-020 | NPTD header and §10.2 "fixtures and designed cases | DEL-09-02, DEL-09-05 | §15"; §14.1 "Fixtures and cases … Constructed now | Candidate needed"; §15.1 "Interface examination covers WebKit, Chromium and the packaged App smoke witness (REQ-008), on a candidate only" |
| DEP-09-02-012 | DEL-01-04 | DEP-01-04-026 | NIR §2 IF-12 "Native interaction view and scoped request/outcome checks | DEL-01-04 → DEL-09-02 | Before the joined request witness | Nothing is claimed beyond the cases run (§13)"; §13 VC-NIR-11 relaunch (candidate; Not run), VC-NIR-16 positive act (person, candidate). AAC VC-AAC-04 positive capture, VC-AAC-13 native confirmation (candidate; Not run) — no row names AAC for DEL-09-02 |
| DEP-09-02-013 | DEL-01-05 | DEP-01-05-017 (PENDING) | ACCESS §1 I-9 "Account/provider inputs and the focused sign-in and concurrent-mode checks | … Before V4-EXM-12"; §13; VC-A01 ChatGPT sign-in ("The person's own sign-in"), VC-A02 API key ("The person's key"), VC-A03 local provider, VC-A04 "All three together … the other two stay configured and selectable", all "No" (not runnable now) |
| DEP-09-02-014 | DEL-01-06 | **none** (DEL-01-06 has only the PKG-09 row) | No Design file |
| DEP-09-02-015 | DEL-02-01 | DEP-02-01-038 (PENDING) | WD §8: "DEL-09-02: the workflow declarations for the V4-EXM-10 examination (§3–§6) … 'scoped feature evidence' of DEP-09-02-015 [is] named by those rows and not yet defined or produced here" |
| DEP-09-02-016 | DEL-02-02 | DEP-02-02-018 | WR §7: "Candidate-bound fixture results and remaining limits (OUT-003), the §12 case inventory | Supplied after a candidate exists"; §0 "Not in this file … the joined V4-EXM-10 witness (DEL-09-02)"; §6 SQ-J J-1…J-9 (the V4-EXM-10 journey, owners in brackets); U-WR-19 "DEL-09-02 for qualification | Before qualification" |
| DEP-09-02-017 | DEL-02-03 | DEP-02-03-038 | EXEC §9.2: "the capability and checkpoint execution contribution (§3, §4, §7); its 'scoped feature evidence' is named by DEP-09-02-017 and not yet produced here (no case has been run; OUT-001 is definition only)" |
| DEP-09-02-018 | DEL-04-01 | **none** | ACT §10.3: "DEL-09-02 | DEP-09-02-018 | none | Not mapped in detail" |
| DEP-09-02-019 | DEL-04-03 | DEP-04-03-043 (PENDING) | RS §10: "The content-bound act and run records and scoped feature evidence for its positive actual-human-act and pending/unperformed-act witnesses … Not covered by this undertaking (D1); stated from the register row only. The record never performs the act" |
| DEP-09-02-020 | DEL-09-01 | DEP-09-01-022 | No Design file |

Consumer: **DEL-11-03** via DEP-11-03-006 (UPSTREAM PREREQUISITE,
INITIALIZED / PENDING), **admitted**; DEP-09-02-021 is its MIRROR.

Non-topological rows: DEP-09-02-022 (candidate/configuration), -023 (a
person's actual act), -024…-030 (OI-001, 002, 008, 009, 010, 011, 012),
-031 (DEP-005).

Cross-reference without a row: CA §2.1 "The App's standalone workflow-making
loop (OBJ-001, DEL-09-02) proceeds independently of this activity"; CA §10
excludes standalone qualification as DEL-09-02's act.

Reach (script): DEL-09-02's admitted reach is exactly its twelve suppliers;
only DEL-11-03 reaches it. With held arcs it also reaches DEL-02-04, 03-01,
03-02, 03-03, 04-02, 05-01, 05-02 and 09-09.

## 3.3 Proposed contract changes still open

- **Carried (owner-decided):** DEL-09-02 TBD-002 OI-009 wording and
  DEP-09-02-027, to the next amendment (§3.1). Draft basis for that item:
  OI-009 decided at choice level by DECISION-K3 K-1 with DECISION-L L-7;
  configuration sharing observed at 0.158.0 without a credential (OBS-2
  O-6); separation with a credential present not observed (L-6); API-key
  behaviour under OI-010.
- **Not in any ledger; candidates the survey found** (for the integrator to
  put into the next amendment if wanted):
  1. TBD-001 and DEP-09-02-024/-025: OI-001/OI-002 ruled for the first
     increment (D2/D3); same pattern as the DAG-004 "OI-001/OI-002
     constraint rows" consistency point.
  2. TBD-003 and DEP-09-02-030: record D4's definition pin.
  3. CLM-001 and DEP-09-02-012: name DEL-01-04's App act control (OUT-005)
     as the capture point of V4-EXM-10's registration and of the deny/grant
     acts where they are acts.
  4. Missing supplier-side counterparts for DEP-09-02-014 (DEL-01-06) and
     DEP-09-02-018 (DEL-04-01). DAG-004's list of "five expected mirror rows
     not extracted" does not include these two; the arcs exist through
     DEL-09-02's rows, so there is no graph effect.
- **No DEFER or DROP row** names DEL-09-02.

## 3.4 Open items and owner choices

| Item | Shapes the design now? | Options / file text | Owner? |
|---|---|---|---|
| **OI-011** (packaged witness) | Yes for staging: what the native observations run on | A signed package (DEL-01-06) or an unsigned development candidate labelled as such; v3's journeys ran on both and said they "do not qualify a subsequently signed installer" | Through DEL-01-06 |
| **Credentialed observations (L-6)** | Yes for VER-006 staging and evidence | V4-EXM-12 needs the person's own sign-in and key (ACCESS VC-A01/A02). Every sign-in and key entry is the person's act (ACCESS §0). When the owner permits the first credentialed run decides when V4-EXM-12 can move from AWAITING INPUT | **Yes** (at the point of need) |
| **OI-010** API-key protocol detail | Yes for V4-EXM-12's API-key case | Open with the App implementation owner | Owner (= App implementation owner) |
| **OI-012** qualification pin; VC 0.160.0 | Values | All three scenarios bind to the same pin | No new choice |
| **OI-008** process division | Little (observations are at the App seam) | HOSTING §12 O-1 proposed | Not for this design |
| OI-009 | No (decided) | Carried wording only | Decided |
| OI-001/OI-002 | No for settled parts; dependent criteria use D2/D3 | VER-003 checks settled rules | No |
| OI-007 | No (public-release only) | Not an owner-use gate (TBD-004) | No |
| V4-EXM-11 native automation | Yes (method) | Same as DEL-09-01's native route; VC-R-14 already assumes the person | Via DEL-09-01 |
| Which local model and server for V4-EXM-12 | Values | OBS-1 used a local LM Studio model (HOSTING §10 v0.8 note); on that Responses route MCP tools and the delegation tool set are dropped at 0.158.0 (HOSTING U-22) — a limit to state if V4-EXM-10 relies on delegation | Owner if a download is needed |

## 3.5 What exists to build on

- **Journey already designed by suppliers:** WR §6 SQ-J J-1…J-9 (plan → try
  → draft → try draft → review → register at the act control → reuse →
  refine → refine again) with each step's owner and failure; RECOVERY
  VC-R-14; NIR VC-NIR-05/-10/-11/-16; AAC VC-AAC-04/-13; ACCESS
  VC-A01…A05; NPTD NV-01…NV-07; EXEC and RS records for the act witnesses.
  DEL-09-02's design can be a join over these rather than new cases.
- **Supplier facts:** HOSTING §9.4 X-01…X-14 (X-04/X-05 tool-permission
  accept and decline, X-09/X-10 kill and restart) are the recorded seams the
  replay part of V4-EXM-11 can use; OBS-2 observed the live effect of
  `turn/interrupt`, post-restart thread reads and a never-answered request
  across a stop at one local pairing (HOSTING §10 v0.9 note).
- **App v3 exemplar (evidence only):** `JOURNEY_RESULTS.md` J01–J09 with
  real Codex sessions: J05 "Created a reusable project workflow, then
  selected it in a fresh chat", J07 three cycles with a saved and refined
  workflow, J08 keyboard Stop "showed Stopping and ended Stopped. Same chat
  continued", J09 "Denied write left no file; renewed exact approval created
  one exact line". These match parts of V4-EXM-10/11 in form and give a
  v3.0.1 comparison baseline for DEL-11-03; they qualify nothing in v4.

## 3.6 Design scope for this pass

1. **Case definitions** for V4-EXM-10/11/12 as a join over the suppliers'
   designed cases: a step table keyed to WR SQ-J with, per step, the
   observation, the supplier evidence it links (case IDs above), the actor
   (person, agent, App), and where V4-EXM-11's interruptions are inserted
   (stop during a run, close/reopen while a request waits, deny one A14 and
   grant another, quit with a waiting card, relaunch, continue).
2. **V4-EXM-12 configuration** under K-1/L-1: H-acct, H-key, local provider;
   per-conversation selection; no default (DEC-4; NIR VC-NIR-12); what is
   recorded and what is never recorded (credentials).
3. **Dossier structure** (data): one record per case and part using
   DEL-09-01's core record; links to feature evidence with identity and
   limits; the DEL-11-03 return, including what the v3.0.1 comparison needs.
4. **States and failure behaviour**: case states, input gaps → `blocked`,
   partial runs, changed candidate → reopen list, criteria protected.
5. **Act boundary**: the person performs sign-in, key entry, review,
   registration, grant and deny; the examiner observes; positive and
   fabrication-negative cases (VER-003).
6. **Designed verification** VER-001…008, marked "needs candidate" and
   "needs person" throughout.

**Leave out:** any run; any qualification or replacement claim; the host
witness (DEL-09-07); fleet recovery (DEL-09-05); policy beyond D2/D3; the
SoW wording fixes (next amendment).

---

# 4. Owner choices across the three deliverables, ranked

Ranked by how much design text depends on the answer.

1. **OI-011 signing arrangement (DEL-01-06; feeds 09-01, 09-02).** A: the App
   re-signs the Codex vendor tree with its Developer ID and per-binary
   entitlements (v3's practice); B: Codex binaries keep the supplier's
   signature and only the App is signed and the whole bundle notarised.
   Includes App Sandbox off/on and who performs notarisation. Most of
   DEL-01-06's Design text and HOSTING §7's verification rule depend on it
   (SQ-1). Inputs that would help: the supplier's entitlements per
   executable at the qualification pin (I read two on `bin/codex` at
   0.158.0; the code-mode host's set could not be read), which node VC can
   record at 0.160.0 with `codesign -d --entitlements` without running
   anything.
2. **OI-011 co-ownership with the SWB owner while host joins are
   deferred.** Decide the App's arrangement now (SWBPIPE knowledge optional)
   or relay first. Sets the actors in DEL-01-06's records.
3. **Native macOS execution route** (DEL-09-01 OUT-004; DEL-09-02 V4-EXM-11;
   DEL-01-06 OUT-003): person-operated native witness with a recorded form,
   or a UI-automation tool to be chosen. App implementation owner's choice
   (= owner, L-7).
4. **Independent candidate review: Codex reviewer or Claude fallback as the
   standing arrangement** (V4-OPS-34, D-13; DEL-09-01 REQ-006). Shapes the
   review protocol and every journey's examiner record.
5. **When the first credentialed observation is allowed** (L-6 revisit;
   DEL-09-02 V4-EXM-12, also DEL-01-05 VC-A01/A02). Shapes staging, not
   structure.
6. **Public release intent and timing for v4** (OI-007 / OQ-08). Sets when
   OUT-004 is needed; no design text depends on it beyond the gate.
7. Minor: WR U-WR-18 (recognize v3's shipped workflows in the manifest);
   which local model/server for V4-EXM-12 if a download is needed.

Not owner choices: the shared result form (integrator ruling, §2.4); the
qualification pin (OI-012 handled by node VC and later re-examination);
OI-009 (decided; wording carried).

# 5. Structural questions

- **SQ-1 — Re-signing vs HOSTING §7 (could restructure a first-increment
  Design file).** HOSTING-v0.9 §7.2: verified means the version label
  matches "**and** the distribution content identity equals the expected
  identity" over the vendor tree. If OI-011 goes to option A, signing
  changes the Mach-O bytes (v3: "Signing changes a Mach-O's bytes", so its
  pin check compared digests only before signing). HOSTING §7.1/§7.2 and
  U-17 would need a pre-sign/post-sign split or an identity that ignores the
  signature, plus a record of who signed. Option B leaves §7 as written.
  Either way U-17 (launcher) and relocation must be settled with DEL-01-06.
- **SQ-2 — One examination vocabulary, and the direction of reliance.**
  Four vocabularies exist (§2.5), including two spellings of the outcome
  states. DEL-01-01 cannot consume DEL-09-01: DEL-09-01 already consumes
  DEL-01-01 (admitted), and the DAG-004 guard says a reverse row from
  DEL-01-01 "would merge SCCs". So DEL-09-01 must map to HOSTING §9 rather
  than govern it; HOSTING may align its spelling on its own authority. If
  DEL-09-01 defines a shared core record, CA §8.4 and XT §3.4 (and their
  PROPOSED schemas) would be restructured to extend it; both already consume
  DEL-09-01 through admitted arcs, and the guards XT F-28 cites (DAG-003
  E-1, E-2: neither of DEL-09-06 and DEL-09-09 consumes the other) are
  untouched.
- **SQ-3 — SCC-003 (DEL-01-06 ↔ DEL-09-01) is designed in this pass by the
  same tranche.** The case recommends R1 (named support revision and named
  package as milestones) and has no ruling. Designing both deliverables now
  is the natural point to make R1's contributions concrete; no
  first-increment file is affected.
- **SQ-4 — Bundle-content seams and SCC safety.** WR (bundled workflows,
  shipped-revision manifest), ROLE (shipped guidance) and AAC (SEAL-2 key
  store for "the signed App") rely on the package with no row. By script
  over both DAG-004 layers, DEL-02-02, DEL-02-04 and DEL-01-04 each already
  reach DEL-01-06 through held arcs, so a row **DEL-01-06 → (02-02, 02-04 or
  01-04)** would close a cycle and merge SCC-003 into SCC-002 (an
  SCC-forming departure). Rows the other way (**02-02, 02-04, 01-04 →
  DEL-01-06**, "the package places and signs what I ship") form no cycle,
  since DEL-01-06 reaches only DEL-01-01, DEL-01-05 and DEL-09-01. Framing
  the seam the safe way needs no change to the pass-3 files beyond a
  cross-reference.
- **SQ-5 — DEL-09-02's act-control seam is unnamed** (DEP-09-02-012 and
  both SoWs). A wording/register item on an existing admitted arc; no
  restructuring.
- **SQ-6 — Pin advance (VC, 0.160.0).** HOSTING records sibling executables
  and signing facts per pin; a change in the vendor tree or entitlements
  would change DEL-01-06's tables and the fixtures DEL-09-01 binds. Writing
  both designs pin-parameterized avoids rework.

No question found here forces restructuring of DEL-09-06's or DEL-09-09's
journey design beyond their result-record sections (SQ-2), or of any pass-3
file beyond cross-references.
