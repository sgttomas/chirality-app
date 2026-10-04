# macOS packaging, signing and distribution evidence

- **Contribution:** DEL-01-06/PKG-v0.1 (first Design file of this deliverable).
- **Status:** DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. Beside it: two PROPOSED schemas (JSON Schema 2020-12) with valid,
  invalid and rule-violation example sets, and a design prototype
  (`prototype/read_tree.py`, `prototype/check_pkg.py`; not product code).
  No package has been built, signed or notarised.
- **Run and node:** `APP-V4-DESIGN-PASS-4-20261003`, owner O-B (Type 2,
  Claude Opus 5.5), 2026-10-03. Frozen for review by RV2.
- **Serves:** OUT-001…OUT-004; REQ-001…REQ-005; designed cases for
  VER-001…VER-005 (§11).
- **Basis, pinned by current bytes** (`shasum -a 256`):
  - ScopeOfWork.md `08e30b97baeb06ae57b6166d6358f5c68ad1d934102df7ea094ce6cc57abd795`.
    **R23-5 re-pin:** unchanged since INIT (`ddd721a90a`); no SCA-V4-003
    block changed it, so none bears on this file.
  - `Dependencies.csv` `19c3eb3574e9bdf263cac37a4f7bb2ff0328fc239180c3f72c2e32c6d0037f86`.
  - `docs/PRD.md` `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd`
    (V4-CST-02, V4-CST-03, §9 OQ-08); `docs/ARCHITECTURE.md`
    `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c`
    (§3 V4-ARC-01/02 and "Left to the implementation session", §6, §8);
    `docs/EXAMINATION.md`
    `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0`
    (V4-EXM-01, -03, -04); `docs/HOST_INTEGRATION.md`
    `d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f` (§1).
  - Supplier: DEL-01-01 `HOSTING_BOUNDARY.md` (HOSTING-v0.9)
    `ce235650e8a9494c66ccd08677556e56a88983aa641b5ff22c576328bd8a93b6`
    (§4.2 step 1, §7.1, §7.2, §8 S-5, §10 P-02, §11, U-17);
    `PIN_SPIKE_0.158.0.md`
    `0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115`
    (§2, §3, UNRESOLVED).
  - Examination support (SCC-003 M1): DEL-09-01 `EXAMINATION_PROTOCOL.md`
    (EXP-v0.2, U1 as repaired for RV-EXP-U1)
    `fc5b8230ec2ab81a9307bd58a573752194a859afbc28eda6bce1a12ee332a20d`
    and `exam.result-record.schema.json`
    `f7871c96cef25bb974aea73feca009ed3caf843db5077d80612f13b130af2081`.
  - Bundle content designed by others (cross-references; §4.2):
    DEL-02-02 `WORKSPACE_AND_REGISTRATION.md` (WR-v0.2)
    `c5332e9333ccb18c5b4a2a3d633e9d643362b88d0f87187c762a86b5317953c4`
    (§3 rows "Bundled workflows", "Shipped-revision manifest"; LS-5, LS-8);
    DEL-02-04 `ROLE_SUPPLY.md` (ROLE-v0.2)
    `92bb421b7bccee9a02d33a037736a97bb4d4b1e2136246fa83f75c49291c7e2a`
    (§4.2 GS-1…GS-3); DEL-01-04 `APP_ACT_CONTROL.md` (AAC-v0.2)
    `062ce28c8a4ec0bc79fc6b6c421245057a59815df14b88fa779b61eeb98be7d7`
    (AAC-v0.2 at `HEAD`, the version relied on, R23-21; §6.3 SEAL-2 is
    unchanged in O-A's AAC-v0.3); DEL-01-05 `ACCOUNT_AND_PROVIDER_ACCESS.md` (ACCESS-v0.2)
    `7a2ad8e4a7423943ef6b1ffdbce6048d7c30c9dcc98b515e94cd623f6c041965`
    (§0, §20).
  - Rulings, cited by ID (R23-21): R23-2, R23-3, R23-5, R23-7, R23-11,
    R23-13, R23-17, R23-20, R23-21. Other run records:
    `OWNER_DECISIONS.md`
    `e4350f61a93edf0d2d4bfc588fcaa17ae23981baa6059617dcc430cda3008cd8`;
    O-B notes `OWNERS/O-B.md` (§ "K-4 facts", the observation record for
    §2.1).
- **Pin basis (R23-3).** Written for either pin. The design reads the
  supplier tree at whatever pin is packaged (FP-0, §7) instead of fixing
  values. Facts used: at **0.160.0** the whole published tree, read
  2026-10-03 from node VC's copy (signatures only); at **0.158.0** only
  `bin/codex` and `zsh` (the spike copy is otherwise pruned). The signing
  decision (§3) holds at both pins on those facts; a pin whose tree is not
  wholly signed by one supplier team with hardened runtime and timestamps
  fails FP-0 and reopens §3.
- **Receivers:** DEL-09-02 (DEP-09-02-014, admitted); DEL-09-01
  (DEP-09-01-016, held, SCC-003 M2); App PKG-09 (DEP-01-06-007, package);
  the owner's public-distribution decision (DEP-01-06-011, OUT-004).

## 0. Reading this file

**What it is.** How the App and its stock Codex are put in one macOS Apple
Silicon package, signed, notarised and identified; how a package is shown to
install and start; and how the written distribution-terms response is kept.

**What it is not.** No package, signature or notarisation is made here (those
use the owner's Apple account when a package is made, R23-13.2). No supplier
terms are obtained or interpreted; no legal conclusion. No joined
examination (DEL-09-01/09-02 and PKG-09). No Windows. No SWBPIPE package
(OI-011's SWB co-owner part waits with the host joins, R23-13.2).

**Labels.** SETTLED, DERIVED, INTEGRATION, PROPOSED, as in the other App v4
Design files. *General knowledge* marks statements made without network
access or a local check; each is tied to a first-package check (§7).

## 1. Owner and act boundary (REQ-005; CLM-001…CLM-004)

| Act | Actor | This file |
|---|---|---|
| Supplier hosting, pin, protocol qualification, distribution identity rule | DEL-01-01 (HOSTING §7) | Consumes S-5; proposes a U-17 value (§4.1, §13) |
| Package configuration, identity record, install/launch witness | DEL-01-06 (App packaging owner) | Defines them |
| Signing and notarising with the owner's Apple account | The owner, when a package is made (R23-13.2) | Records the act and its actor; never performs it or holds a credential |
| Signing arrangement (technical choice) | O-B, recorded here (R23-13.1) | §3 |
| OI-011's SWB co-owner part | Waits with the host joins (R23-13.2) | Not exercised |
| Written supplier position | The supplier supplies; the owner obtains | §9 records it |
| Public-distribution decision | The owner | §9 cites it; never inferred |
| Joined examination of the packaged candidate | DEL-09-01 support; DEL-09-02 and other journeys | §8 hands the package and witness over (SCC-003 M2) |

## 2. Facts the design rests on

### 2.1 The supplier's tree (observed)

Read 2026-10-03 with `codesign -dv` and `codesign -d --entitlements`; no
binary executed (O-B notes, "K-4 facts", F-K4-1). `prototype/read_tree.py`
reproduces the reading.

| Pin | Tree | Mach-O | Signer | Hardened / timestamp | Entitlements |
|---|---|---|---|---|---|
| 0.160.0 | 42 files; manifest sha256 `327effb91a5854eccb388321b4b160e059795f0402c553f594e85365189d8d12` | 30 | All team 2DC432GLL2 (OpenAI OpCo, LLC) | All yes | `bin/codex` and `bin/codex-code-mode-host`: `cs.allow-jit`, `cs.allow-unsigned-executable-memory`; `codex-resources/voice/bin/codex-voice-host`: `device.audio-input`; all others none |
| 0.158.0 | Partly read (PIN_SPIKE §3; spike copy pruned) | — | 2DC432GLL2 | yes (`bin/codex`, `zsh`) | `bin/codex`: the same two; `zsh`: none; others not read |

The 0.160.0 executables named above: `bin/codex`
`112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`;
`bin/codex-code-mode-host`
`679eedaea70529aa1cffc9bc0a0788c186412663544fa76c09d63b57f383a65a`;
`codex-voice-host`
`e408413b79d76e518966046ce1d7758523c606844269fe4dd56446bed80c1062`;
`codex-path/rg`
`7c7d5b09c3a57de864500c65dc2e9c4d2a5e96a3fc7b7d5318480c19887a739b`;
`zsh` `d715e06edcf1661edb2e7767d65fbd1b44af505edfb217281b701f0a6ae93b15`.
The tree has no symbolic links.

### 2.2 App v3 (historical exemplar, Electron, Codex 0.154.0)

`chirality-app-dev/frontend` copied the vendor tree to
`Contents/Resources/codex`, re-signed every Mach-O with the App's team
(`sign-electron-runtime-v2.mjs`: "JIT only for the Code Mode host"), compared
Codex digests only before signing ("Signing changes a Mach-O's bytes",
`verify-codex-pin.mjs`) and was notarised and stapled ("Notarized Developer
ID", `PUBLIC_RELEASE_20260913.md`). Evidence that Resources placement
notarises; no evidence about supplier-signed nested code. Inference: the v3
entitlement files, if reused at 0.160.0, would drop
`allow-unsigned-executable-memory`, JIT on `codex`, and `audio-input`.

### 2.3 Notarisation and bundling (general knowledge; confirmed or refuted by §7)

- G-1 Every executable and library in a submission must be signed with a
  Developer ID certificate, with hardened runtime and a secure timestamp, and
  without `get-task-allow`.
- G-2 The notary service checks each signature's validity, not that nested
  code has the outer App's team; another team's valid Developer ID signature
  is acceptable. *(Expected; FP-3 confirms.)*
- G-3 Hardened-runtime library validation lets a process load only libraries
  signed by Apple or its own team. The voice host and its dylibs share one
  team today.
- G-4 Code under `Contents/Resources` is sealed by the outer signature's
  resource seal; Apple prefers `Contents/MacOS` or `Contents/Helpers` for
  executables (v3 shipped Resources placement and notarised).
- G-5 Tauri 2's bundler signs the main binary and any `externalBin` sidecar
  with the configured identity; whether it re-signs Mach-O files copied as
  `resources` is not known here. *(FP-1 settles it for the configuration
  used.)*
- G-6 A protected resource entitlement (`device.audio-input`) is usable only
  with a matching usage string in the responsible App's `Info.plist`.

## 3. Signing decision (OI-011; R23-13.1)

**SIGN-1 (INTEGRATION: decided by O-B under R23-13.1, accepted by HELP_HUMAN): Option B — Codex's files
keep OpenAI's signatures; only the App's own code is signed by the App, and
the whole bundle is notarised.** Reasons:

1. **HOSTING §7 stays as written.** The packaged tree is byte-equal to the
   published one, so §7.1's distribution content identity and §7.2's rule
   ("equals the expected identity") need no split. Option A would change
   both (§10).
2. **Entitlements ship exactly as the supplier set them** at each pin
   (§2.1). No per-pin entitlement list is maintained by the App, and the v3
   failure mode (dropped entitlements) cannot occur.
3. **One team per process tree** for the voice host and its libraries (G-3).
4. **V4-CST-03** ("used through its own published interface, unmodified and
   pinned") is met literally; no reading of "unmodified" is needed.
5. The precondition is observed at both pins read (§2.1; FP-0 passes at
   0.160.0, §11).

**Its risk** is G-2 and G-5, general knowledge only. The first package
answers both before anything relies on B (FP-1, FP-3, §7).

**SIGN-2 Fallback: Option A** (the App re-signs every Codex Mach-O with its
own Developer ID, applying exactly the supplier's per-file entitlements read
at that pin, PK-R2). A is used only if FP-1 or FP-3 fails for a reason that
configuration cannot repair, and the identity record says why
(`fallback_reason`). **A would restructure HOSTING §7.1/§7.2** (a
before/after-signing identity split, §10). That restructure is a
first-increment Design change: it comes back to HELP_HUMAN before A is
adopted, and DEL-01-06 does not edit HOSTING.

**SIGN-3 The App's own signature (PROPOSED).** Developer ID Application,
hardened runtime, secure timestamp, no `get-task-allow`. App entitlements:
none known to be needed; any found necessary at FP-2/FP-4 is added with its
reason in the identity record. **App Sandbox off**, because the App's Codex
child works in the person's project folders, reads the person's
configuration through a symbolic link from an App-owned home (HOSTING §4.2
step 3) and runs Codex's own command sandbox; under App Sandbox those
children would inherit the App's container (general knowledge). App v3 also
shipped without App Sandbox (`entitlements.mac.plist`: JIT only).

**SIGN-4 Microphone.** The App offers no voice feature; its `Info.plist`
declares no microphone usage string. The voice host ships inside the
unmodified tree but is not exercised (U-PKG-4).

## 4. Package composition (OUT-001; REQ-001)

### 4.1 Layout (PROPOSED)

| Place | Content | Supplier | Notes |
|---|---|---|---|
| P-0 `Contents/MacOS/<App>` | The Tauri 2 App binary | App build | Signed by the App (SIGN-3) |
| P-1 `Contents/Resources/codex/` | The Codex vendor tree, **verbatim**: `bin/`, `codex-path/`, `codex-resources/` with the same relative layout as published | DEL-01-01 (pin, distribution identity, S-5); DEP-005 | Copied as a resources directory, not as `externalBin` (G-5: a sidecar is renamed and signed by the bundler). Byte-equal to published (FP-1) |
| P-2 `Contents/Resources/workflows/` | Bundled workflows and the shipped-revision manifest | DEL-02-02 (WR §3; LS-5, LS-8; L-4) | Read-only in the bundle |
| P-3 `Contents/Resources/instructions/` | Product guidance `AGENTS.md` and the four role files | DEL-02-04 (ROLE §4.2 GS-1) | Seeded into App data at first start; the bundle copy is never edited |
| P-4 `Contents/Info.plist` | Bundle id, version, minimum macOS, no microphone string | App build | Version equals the identity record's |
| — App data, project folders | App-owned Codex homes (H-acct, H-key, H-probe), records, seeded guidance | Runtime | **Never in the bundle**; nothing is written into the bundle at run time |

**Launcher (proposed value for HOSTING U-17).** The App starts
`Contents/Resources/codex/bin/codex` directly (the vendor binary), adding no
npm-wrapper environment. Reasons: a Tauri App ships no Node runtime for the
npm wrapper; PIN_SPIKE §3 observed the vendor binary started directly gives
the same handshake as the wrapper. The identity covers the whole vendor tree
(HOSTING §7.1 as written). U-17 stays the App implementation owner's with
this deliverable; this is a proposal to it, not an edit of HOSTING.

**Relocation (HOSTING §10 P-02; PIN_SPIKE UNRESOLVED).** P-1 keeps the
tree's relative layout, so the sibling resources stay where the binary
expects them. Running from the bundle is observed at FP-2.

### 4.2 Interfaces

| Interface | Direction | Arc (DAG-004) | Contribution | If it fails |
|---|---|---|---|---|
| I-1 Codex distribution | DEL-01-01 → here | DEP-01-06-006, admitted | Pin, published tree, HOSTING §7.1 identity elements, S-5 signing facts | No package for that pin |
| I-2 Packaging interfaces | Tauri 2 bundler; Apple tooling (DEP-005) | DEP-01-06-009, not topological | Bundling, signing, notarisation | FP-1/FP-3 decide B or A |
| I-3 Bundle content | DEL-02-02, DEL-02-04 → placed here | **No row** (Design cross-reference) | P-2, P-3 bytes and their identities | Package lists the item `missing`; not released |
| I-4 Signed App identity | Here → DEL-01-04 SEAL-2 | **No row** (AAC §6.3 relies on "the signed App") | A stable Developer ID identity per release | SEAL-2 unavailable on an unsigned build (AAC's own limit) |
| I-5 Examination support | DEL-09-01 → here | DEP-09-01-021, held (SCC-003 M1) | EXP result record for the witness (§8) | Witness recorded without EXP form; not usable by PKG-09 |
| I-6 Package and identity record | Here → DEL-09-01, DEL-09-02 | DEP-09-01-016 (held, M2); DEP-09-02-014 (admitted) | Package + OUT-002 record + OUT-003 witness | Native packaged cases `blocked` (EXP F-5) |
| I-7 Terms record | Here → the owner's distribution decision | DEP-01-06-011, not topological | §9 | Public release not possible; owner use unaffected |

**Rows for I-3 and I-4 (R23-2; none added here).** Framed as consumer →
DEL-01-06 ("the package places and signs what I ship"). Reach over both
DAG-004 layers, run 2026-10-03: DEL-01-06 reaches only DEL-01-01, DEL-01-05
and DEL-09-01, so DEL-02-02 → DEL-01-06, DEL-02-04 → DEL-01-06 and
DEL-01-04 → DEL-01-06 close no cycle. They are listed for the next amendment
(§13), because adding a row is an escalation condition of this assignment.

## 5. Package identity record (OUT-002; SCC-003 M2) — `pkg.identity-record.schema.json`

One record per package candidate. Elements: the App (revision, build
identity, version, bundle id, target `macOS arm64`, its signature, cdhash,
installer file and its sha256 before notarisation and after stapling); Codex
(pin, published and packaged tree identities — file count, Mach-O count,
manifest sha256 per `read_tree.py` —, launcher, and per Mach-O executable the
published and packaged sha256, signature and the supplier's entitlements);
bundle contents with supplier deliverable, place and sha256; signing (option,
App identity, who performed it, who recorded it, fallback reason for A);
notarisation (state, submission id, log, issues, submitter, stapled);
Gatekeeper (verdict in spctl's words, deep strict verification); the
examination support revision; date; limits.

Rules (`prototype/check_pkg.py`):

- **PK-R1** Option B: the packaged tree equals the published tree (manifest
  and every executable), and every executable carries the supplier team with
  hardened runtime and timestamp.
- **PK-R2** Option A: every re-signed executable carries the App's team,
  hardened runtime, timestamp and **exactly** the supplier's entitlements for
  that file.
- **PK-R3** The recorder is not the actor of signing or notarising.
- **PK-R4** (terms) The recorder is neither the obtainer of a response nor
  the decider of distribution.
- **PK-R5** A "Notarized" Gatekeeper verdict needs an accepted notarisation.

## 6. Operating sequence and failure behaviour

| Step | Action | By | Failure → behaviour |
|---|---|---|---|
| PS-1 | Obtain the pinned platform package; read the published tree (`read_tree.py`) | Build | Pin mismatch with HOSTING §7.1 → stop; no package |
| PS-2 | FP-0 on the published tree | Build | Fails → option B not available at this pin; §3 reopened |
| PS-3 | Build the App; place P-0…P-4 | Build | A P-2/P-3 item missing → listed `missing`; package not handed over as complete |
| PS-4 | FP-1: compare the tree inside the bundle with the published tree | Build | Differs → find the bundler step; repair the configuration; else SIGN-2 with reason |
| PS-5 | Sign the App (P-0 and the bundle) | **The owner's Apple account** (R23-13.2) | Signing fails → no package |
| PS-6 | `codesign --verify --deep --strict` on the `.app` | Build | Invalid → no package |
| PS-7 | Submit for notarisation; read the log | **The owner** (or under the owner's direction, as evidenced) | Rejected → read `issues`; supplier-signature issues → SIGN-2 with reason; other issues → repair |
| PS-8 | Staple; Gatekeeper assess (`spctl -a -vv`) | Build | Not "Notarized Developer ID" → record verdict; not a distributable package |
| PS-9 | Install and launch witness (§8) | Examiner (N-1 or N-2) | EXP outcome; failed witness is a result, not a hidden retry |
| PS-10 | Write the identity record; validate with `check_pkg.py`; hand over (I-6) | Recorder | Record invalid → not handed over |

The installer is never modified after PS-7 except by stapling; any rebuild is
a new package candidate with a new record (V4-EXM-03).

## 7. First-package check: does option B work?

Run on the first package. Each is an EXP result record (`case_id` FP-n,
`owner_deliverable` DEL-01-06).

| Check | Question | Method | Pass means |
|---|---|---|---|
| **FP-0** | Does the published tree meet B's precondition? | `check_pkg.py --tree <published tree>` (reads only) | Every Mach-O signed by one supplier team, hardened, timestamped, no `get-task-allow`, no links. **Run at 0.160.0 on 2026-10-03: pass** (§11) |
| **FP-1** | Does the bundler leave the supplier's files alone? | `read_tree.py <app>/Contents/Resources/codex --compare <published tree>` after PS-3 and again after PS-5 | `byte_equal: true` at both points. Settles G-5 for the configuration used |
| **FP-2** | Does Codex run from the bundle? | Launch the App; HOSTING §7.2 verification of the packaged tree; handshake reaches `ready` | Verification `verified`; handshake observed (relocation, HOSTING P-02) |
| **FP-3** | Does notarisation accept another team's signatures inside the App? | PS-7 log: status and `issues` | Accepted, with no issue on any `Contents/Resources/codex/` path. Settles G-2 |
| **FP-4** | Does the stapled package pass Gatekeeper and deep verification? | PS-6, PS-8 | "Notarized Developer ID"; deep strict valid |
| **FP-5** | Do the supplier's entitlements take effect? | Read `codesign -d --entitlements` of the packaged files; exercise a Codex feature that uses the code-mode host if the App offers one | Entitlements present (FP-1 implies it); runtime use observed or recorded `not-run` with the reason |

**Decision rule.** FP-1 or FP-3 failing because of signatures, and not
repairable by configuration, moves the package to SIGN-2 (A); that triggers
the HOSTING §7 escalation (§10). FP-2 failing is a layout or launcher defect,
not a signing one. FP-4 failing with FP-3 accepted is a stapling or
distribution defect.

## 8. Install/launch witness (OUT-003; REQ-003)

Written as a DEL-09-01 EXP result record (SCC-003 M1): `run_basis:
candidate`, `subject.app_candidate.packaged: true` with this package's
identity record, `route.kind: native_packaged`, platform `macOS arm64`.
The record names the WKWebView identity (EXP §8.1). The witness steps
contain no human act, so either native route applies: N-1 person-operated
with the native-step form (EXP §8.2), or N-2 UI automation once the tool
version has passed EXP-DC-N2 on this candidate (EXP §8.3).

| Step | Observation | Evidence |
|---|---|---|
| W-1 | Mount or unzip the installer; Gatekeeper verdict on the `.app` | spctl output |
| W-2 | Copy to `/Applications`; first launch shows no Gatekeeper block | Screen capture or form entry |
| W-3 | The App starts; its version equals the identity record's | About view or bundle read |
| W-4 | The App resolves and verifies its Codex (HOSTING §4.2 steps 1–2) | Verification result `verified` |
| W-5 | Codex handshake reaches `ready` under an App-owned home | Lifecycle record |
| W-6 | Entitlements of the running binaries as packaged | `codesign -d` of the installed files |

Outcome by EXP §3.1 (R23-20): with no package the witness is `not-run` with the package as missing input; an attempt stopped at its start (e.g. Gatekeeper refuses to open it) is `blocked` with that cause. Configuration
names the pin; model and model server are `not_applicable` (no conversation
is needed). DEL-01-06's witness and DEL-09-01's packaged smoke (M3) are
separate results on the same package.

## 9. Distribution-terms record (OUT-004; REQ-004) — `pkg.terms-record.schema.json`

One record per supplier: OpenAI now; Anthropic only if a Claude sign-in is
ever offered. State `unresolved` until a written response exists; then
`response_received` with the response by reference, its custody, who
obtained it (the owner), what it applies to in its own words, and the date.
The owner's distribution decision is a separate reference or `not_made`; a
response never stands for it (PK-R4; AC-005). Owner use and development are
not gated by an `unresolved` record (TBD-002).

## 10. What option A would change (for the escalation, if FP fails)

| Element | Change under A |
|---|---|
| HOSTING §7.1 distribution content identity | Two values: published (pre-sign) and packaged (post-sign) |
| HOSTING §7.2 verification rule | Must name which identity is expected at run time, or compare after removing signatures (byte equality after removal not established) — **restructure of a first-increment file → HELP_HUMAN** |
| HOSTING §10 P-01 signing facts | No longer describe the shipped files |
| Entitlements | Re-applied per file from the supplier's set at each pin (PK-R2) |
| V4-CST-03 "unmodified" | A reading must be stated |
| This file | §5 records `fallback_reason`; FP-1 no longer expects byte equality |

## 11. Verification (designed; VER-001…VER-005)

"Needs": *model* = runs on the prototype now; *package* = a built package;
*person* = the owner's account act.

| Case | Serves | Expected | Needs | Status 2026-10-03 |
|---|---|---|---|---|
| PKG-VC-01 Configuration and identities | VER-001, AC-001 | Layout P-0…P-4; launcher; Codex identity equals HOSTING §7.1 at the pin | package | Not run |
| PKG-VC-02 Identity record against the package | VER-002, AC-002 | PK-R1 (or PK-R2 under A); no inherited v3 or SWBPIPE claim | model; package | Rules run on examples (below) |
| PKG-VC-03 Install/launch witness | VER-003, AC-003 | §8 W-1…W-6 as an EXP record | package; person (signing) | Not run |
| PKG-VC-04 Terms record | VER-004, AC-004, AC-005 | `unresolved` before a response; actors kept apart | model; then the owner's act | Examples valid; PK-R4 detected |
| PKG-VC-05 Boundaries and substitutions | VER-005, AC-006 | Browser evidence, SWBPIPE success or a package's existence never claimed as the witness, terms or release | Review | Not run |
| PKG-VC-06 FP-0 at the pin | §7 | Supplier precondition for B | model on the published tree | **Pass at 0.160.0** |

**Prototype run** (`PYTHONDONTWRITEBYTECODE=1 python3 check_pkg.py --tree
<VC's 0.160.0 published tree>` in `prototype/`, jsonschema 4.26.0, Draft
2020-12; reads only), 2026-10-03: **TOTAL 36, FAIL 0** — two schemas valid;
4 valid records pass and break no rule; 7 invalid records rejected; 7
schema-valid violations each caught (PK-R1 ×2, R2, R3, R4 ×2, R5); FP-0's
five checks pass on 42 files / 30 Mach-O. The Codex values in example
PKG-EX-01 are the real 0.160.0 published values; App, installer and content
identities are placeholders, labelled in the record's `limits`.

## 12. UNRESOLVED

| ID | Item | Owner | Point of need |
|---|---|---|---|
| U-PKG-1 | G-2/G-5 confirmed (FP-1, FP-3) | DEL-01-06 at the first package | Before any reliance on B |
| U-PKG-2 | HOSTING U-17 launcher value (§4.1 proposes the vendor binary) | App implementation owner with DEL-01-06 (HOSTING U-17) | Before verification implementation |
| U-PKG-3 | Qualification pin (OI-012); VC adoption boundary | HELP_HUMAN (R23-3, R23-17) | Before qualification |
| U-PKG-4 | Voice host shipped but unused; no microphone string | App implementation owner | If voice is ever offered |
| U-PKG-5 | Minimum macOS version in `Info.plist` | App implementation owner | Before the first package |
| U-PKG-6 | OI-011 SWB co-owner part | Waits with host joins (R23-13.2) | When joins resume |
| U-PKG-7 | OI-007 written position | Owner and supplier | Before public release beyond owner use |

## 13. For other owners and the next amendment (nothing of theirs edited)

- **HOSTING (DEL-01-01):** U-17 proposal (§4.1); relocation is observed at
  FP-2; under B, §7 is unchanged.
- **Rows for the next amendment (R23-11; reach-checked, none added):**
  DEL-02-02 → DEL-01-06 (bundled workflows, shipped-revision manifest placed
  in P-2); DEL-02-04 → DEL-01-06 (guidance in P-3); DEL-01-04 → DEL-01-06
  (SEAL-2 relies on the signed App identity). Also DEL-01-06's missing
  counterpart for DEP-09-02-014 (S1-B §1.2).
- **ScopeOfWork wording (R23-11):** CLM-002 "App implementation owner with
  SWB owner" now reads with L-7 and R23-13; TBD-003's "no version" reads
  with D4.

## Changes

| Version | Change |
|---|---|
| PKG-v0.1 (2026-10-03) | First Design file: signing decision B with fallback A, composition, identity record (M2), witness, terms record; two PROPOSED schemas; prototype 36/0 incl. FP-0 at 0.160.0 |
