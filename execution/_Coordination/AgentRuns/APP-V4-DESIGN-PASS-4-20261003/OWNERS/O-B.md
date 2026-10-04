# O-B — notes and returns (DEL-01-06, DEL-09-01, DEL-09-02)

Owner O-B: Type 2 TASK (Claude Code subagent of HELP_HUMAN, Claude Opus 5.5),
standing assignment from the work graph's "Coordination" section. Method:
`workflows/coordinated-knowledge-work/WORKFLOW.md` (sha256 `44049bcd…1b18`,
checked). Write boundary: DEL-09-01, DEL-01-06, DEL-09-02 `Design/` (new
files) and this file. Read-only git; no network.

## Units

### U1 — DEL-09-01 EXP-v0.1 — FROZEN 2026-10-03; reviewed RV-EXP-U1 (REPAIR); repaired as EXP-v0.2 below

Path: `PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-01_Candidate examination infrastructure and evidence protocol/Design/`

| File | sha256 |
|---|---|
| `EXAMINATION_PROTOCOL.md` | `dc6b6a0c24a3c780e017de3e078473d3303386961f3feb576604d134648ecbc0` |
| `exam.result-record.schema.json` | `7c9944457b85338a0a5c07cd452b11615755d7f3b0a1ee7c6fdcceea9d57cd66` |
| `exam.result-record.valid.examples.json` | `fce64f2b4b83f142e501bea831e4b51113f4bcf467c8a2e9e28bd795edbe81d8` |
| `exam.result-record.invalid.examples.json` | `f042d0f5783daf09d3b8629b2d16bd2eee3e085f8045d9fbb40b77d3855492fd` |
| `exam.result-record.rule-violations.examples.json` | `75e0829168ca91e66e5d34731aeb1f65370e9586794241938be3673756f02686` |
| `exam.review-record.schema.json` | `c1c7b77009fe75a67e608d6f0664323aa38376431283dfd5d9635b64accc55f0` |
| `exam.review-record.valid.examples.json` | `1f1d6d6bbf8364f9d95b8e2aa453d7606b8142d4a6c6a7cf4656af46d7adf9da` |
| `exam.review-record.invalid.examples.json` | `4162597046559b5fbaff0da85aa3699e6e352c2e876b95bd748d2abbbd8828a0` |
| `exam.review-record.rule-violations.examples.json` | `607387041d5a7558d6b5dae127d370f138c319632bd84359ed18cdc9b2924b3f` |
| `exam.change-impact.schema.json` | `b6f2d355a4b3a2eed88cce635e77e9200c5f3a2dc3cb7dfe0fac072349e7dc91` |
| `exam.change-impact.valid.examples.json` | `a79475dabf8f677af7d56e759296b22c078de428b52fe3145ab058edfbba70e8` |
| `exam.change-impact.invalid.examples.json` | `9ff5f0cba56a911d3b42e5ded8b711cee15b08358bbfb816e6b0d8130c461d4f` |
| `exam.change-impact.rule-violations.examples.json` | `86f4f352ba61c61d81e745d320cf043a6d6da80d668ff36752200522f5a0ce64` |
| `prototype/check_exp.py` | `a9f13e1eaae1277a217cd6eac7bf0f4a709c4b387a788d5eda96c5999654c1e3` |

**Claims.**
1. DEL-09-01's 60% design: interfaces (§2, every arc with its DAG-004
   layer), data (§4, three PROPOSED schemas), states (§6.1), sequences
   (§6.2–§6.4), failure behaviour (§11, F-1…F-12) and designed verification
   for VER-001…VER-009 (§12).
2. **R23-1 applied:** outcome values are HOSTING §9.3's labels as written;
   fixture standing is HOSTING §9.2's; W14/XT and EXAMINATION words are mapped
   one to one (§3); no CA or XT text is restructured.
3. **R23-3 applied:** written for either pin; pin is a record parameter;
   pin basis named in the header (only HOSTING-v0.9 §9 definitions at
   0.158.0 are relied on, none a Codex behaviour); examples at both pins.
4. **R23-12 applied:** review protocol §7 (Codex reviewer, Claude fallback
   with an observed-unavailability reason, separation and model identity
   reported, family claim only with two exposed, different identities).
5. **R23-13 applied (native route):** choice recorded in §8 with reasons —
   N-1 person-operated is the standing route for any native step that
   contains a person's act or an OS-level action; N-2 UI automation is
   admitted only for act-free steps after its own definition check; a route
   change reopens affected results.
6. **SCC-003 R1 milestones** M1 (support revision), M2 (package + identity
   record), M3 (native packaged smoke) made concrete (§10); held arcs stay
   held; no register or graph change.
7. R23-5 re-pin: ScopeOfWork `8e536694…658a`, unchanged since INIT; no
   SCA-V4-003 block bears on it. R23-7/R23-11: overtaken TBD-001 wording
   followed by current decisions and listed (§0, §14).

**Checks run.**
- `PYTHONDONTWRITEBYTECODE=1 python3 check_exp.py` (jsonschema 4.26.0,
  Draft 2020-12): **TOTAL 52, FAIL 0** — three schemas valid; 8 valid
  records pass; 12 invalid records rejected; 8 schema-valid rule violations
  each caught by its named rule (EXP-R1, R3, R4, R5, R6 ×2, R7, R8); valid
  records violate no rule; EXP-R9 reads the actual HOSTING, W14 and XT files
  (outcome and fixture labels equal HOSTING; mapping one-to-one onto W14 and
  XT enums); examples at both pins.
- Every sha256 pinned in `EXAMINATION_PROTOCOL.md` recomputed against the
  current files by script: all match (the two run files that changed during
  the work were re-read and re-pinned).
- DAG-004 reach over both layers for each reliance considered: DEL-01-01
  does not reach DEL-09-01 (the HOSTING mapping direction is safe);
  DEL-04-03 and DEL-01-04 do reach DEL-09-01 (so no reliance row toward them
  is proposed; they are cross-references only, §3.4, §14 O-4).

**Not established / open.**
- Nothing is run on a candidate; *model* results pass no VER criterion.
- Placement of records and the form layout (U-EXP-3); runner and N-2 tool
  names (U-EXP-2); digest algorithm (U-EXP-4); qualification pin (U-EXP-1).
- For the next amendment (no row added): DEP-09-01-019 Statement widening
  (§14 O-1).
- The reviewer may wish to check: whether §3.1's meanings of `blocked` vs
  `not-run` match CA W-R5/XT SR-4 usage in edge cases; whether the native
  route reasons in §8 (AAC NA-3 cited as a cross-reference) are stated
  without creating reliance.

**No escalation needed:** no first-increment or pass-3 file changed, no row
added, no owner-reserved item touched, no check removed or narrowed.

### U1 repair — DEL-09-01 EXP-v0.2 — repaired 2026-10-03, for RV's confirmation

Same folder. The v0.1 bytes are kept in the session scratchpad
(`ob_u1_v01/`) for comparison; v0.1's hashes are in the table above.

| File | sha256 |
|---|---|
| `EXAMINATION_PROTOCOL.md` | `fc5b8230ec2ab81a9307bd58a573752194a859afbc28eda6bce1a12ee332a20d` |
| `exam.result-record.schema.json` | `f7871c96cef25bb974aea73feca009ed3caf843db5077d80612f13b130af2081` |
| `exam.result-record.valid.examples.json` | `fcbd53d8936b9c73d8177a403795e438aab9dbc5e71b32f7f87ef4b121bec72e` |
| `exam.result-record.invalid.examples.json` | `c4f15c47ac7d5f4345272664ae979c26e1086eb2a946c9d99f6afc3ddaee8772` |
| `exam.result-record.rule-violations.examples.json` | `55bc7c85bb61af3d50f170b5af47b6069631bb6ba981c943f20e84e4d03390fe` |
| `exam.review-record.schema.json` | `b3294a402197ffa67ba1beb85847b60a7cf8d7bf1edf0006703f94faf7344508` |
| `exam.review-record.valid.examples.json` | `d67f22e766609f7c4e8ea5357c4a6e66e16e67a18572c28bfab0638120d7078d` |
| `exam.review-record.invalid.examples.json` | `79e0deef0afe7a25eed2f97d03c3eab6ca629d37e2a7023fedf7d1de3aa0c90d` |
| `exam.review-record.rule-violations.examples.json` | `b7138150e606cd92cf206fdb09849c5a74e902b3c2808235295b4a47411ed79f` |
| `exam.change-impact.schema.json` | `b8fcb4586aa8d844fd9700d660f8eb66ccd66893724215b0a5d9cd468500f82f` |
| `exam.change-impact.valid.examples.json` | `d00fe2ae6266c034605bbba6b6d7e422ae54fab72c7a0fb379c4787c022cf5f9` |
| `exam.change-impact.invalid.examples.json` | `531673c0af9842726cd90af28f5500d8c1d7033cf2986193ad12c1e77e3568b4` |
| `exam.change-impact.rule-violations.examples.json` | `30e51a423262ec590da1d76f8a563d813ae8b050e328df4358d84cb3d9eaf49f` |
| `prototype/check_exp.py` | `f7e11fc7cd9dd3126ccbe49db907c2feb69612dd185b56cc0d21560119d71210` |

**Checks.** `check_exp.py`: **TOTAL 77, FAIL 0** (was 52). RV's scratch
probes `$TMPDIR/rv/probe_exp.py`, rerun unchanged against the repaired
files: P1 schema now refuses (False); P2 refused, EXP-R3 also fires; P5
refused; P6 refused; P7 refused (interface route without its runner check)
with EXP-R4 still firing; P3 and P4, see EXP-R-A and EXP-R-F below. Every
64-hex pin in `EXAMINATION_PROTOCOL.md` matched against current files by
script, except the two deliberate historical ones (v0.1's own hash, and the
AAC-v0.2 pin kept under R23-21 item 3, which equals `git show HEAD:` bytes).

**Replies to RV-EXP-U1.**

- **EXP-R-A (MAJOR) — repaired under R23-19.** New record element
  `parts_not_applicable` (part, reason, `declared_in` = case definition and
  its sha256, required). EXP-R1 aggregates the applicable `parts` only and
  fires if a part is both declared not applicable and run (EXP-RV-04), or
  if an applicable part was not run and the case says `pass` (EXP-RV-05).
  §3.1 states the rule. New valid example EXP-EX-08: four parts pass, P22-G
  declared not applicable before the run → `pass`. RV's P3 calls
  `aggregate()` with P22-G as an *applicable* `not-run` part, which still
  gives `inconclusive`, as R23-19 item 3 requires; the LHQ pattern is now
  expressed through `parts_not_applicable` instead.
- **EXP-R-B (MAJOR) — repaired under R23-20, labelled INTEGRATION.** §3.1
  meanings: `not-run` = planned for the candidate and not attempted;
  `blocked` = attempted, at start or later, stopped by a stated precondition
  or dependency, cause recorded. The schema now requires `blocked_by` for
  every `blocked` (EXP-INV-11). §6.1 adds PLANNED and "every planned case
  gets a record"; F-1a/F-1b. The SETTLED label is gone.
- **EXP-R-C (MAJOR) — repaired.** Schema: a `native_packaged` result other
  than `not-run` needs `run_basis: candidate` and
  `app_candidate.packaged: true` with `package_record` (EXP-R2). RV's P1 is
  invalid example EXP-INV-09 and now fails. EXP-EX-04, the no-package case,
  is `not-run` with the package as missing input (R23-20: not attempted).
- **EXP-R-D (MAJOR) — repaired.** §8.3 gives the definition checks content:
  EXP-DC-RUNNER (DC-R1 engine identity, R2 sensitivity with known-pass and
  known-fail probes in both engines, R3 missing target gives `blocked`, R4
  evidence digests, R5 no network but the local fixture) and EXP-DC-N2
  (DC-N1 paired steps equal a person's N-1 record, N2 cannot operate the act
  control, N3 missing window gives `blocked`, N4 evidence, N5 Accessibility
  permission recorded). Results cite their admitting record
  (`runner_definition_check`, `tool_definition_check`, schema-required;
  EXP-INV-12, -14). U-EXP-3 decided: §8.2 native-step form layout, §8.4
  placement (files under each journey's `Evidence/EXP/<candidate key>/`, no
  service or index; OI-013/OI-014). U-EXP-1/2 restated per R23-17;
  U-EXP-4 closed (sha256; criterion and declaration digests now schema
  patterns).
- **EXP-R-E (MINOR) — repaired.** §3.5 is one rule table EXP-R1…R9 with
  what enforces each. EXP-R2 is defined (basis/subject/route binding,
  schema-enforced). The prototype checks the table lists R1…R9 once each.
- **EXP-R-F (MINOR) — repaired.** Review record gains
  `reported_as_independent`; EXP-R6 fires only when it is true and
  separation does not hold. Honest `not_separate` with `false` is valid
  (EXP-RX-03). RV's P4 sets `not_separate` on a record that still says
  `reported_as_independent: true`, so EXP-R6 correctly fires there.
- **EXP-R-G (MINOR) — repaired.** `used` is `codex` or `claude_fallback`
  (`other` removed; RV's P5 = EXP-RXI-04 refused). New `review_kind`:
  `v4_ops_34` (preference required) or `additional_person` (no preference,
  never replaces the V4-OPS-34 review; EXP-RX-04 valid, EXP-RXI-05 refused).
- **EXP-R-H (MINOR) — repaired.** The schema forbids `case.scenario` on
  `rehearsal` and `definition_check` records; the prototype's EXP-R3 also
  covers every outcome but `not-run`. RV's P2 = EXP-INV-10 refused.
- **EXP-R-I (MINOR) — repaired.** §6.1: held arcs place no case in HELD and
  drive no readiness (DAG-004 reading rule 3); packaged smoke is AWAITING
  INPUT for the package. §10 M2 reworded.
- **EXP-R-J (MINOR) — repaired.** Rulings cited by ID (R23-21 item 1). AAC
  stays pinned at AAC-v0.2 (`062ce28c…`, equal to `HEAD`), the version
  relied on (R23-21 item 3); `git diff` shows O-A's AAC-v0.3 leaves NA-3 and
  VC-AAC-03 unchanged.
- **EXP-R-K (MINOR) — repaired.** Native routes require `webview`
  (WKWebView, WebKit version, OS version); §8.1 states why (REQ-007,
  AC-008). EXP-INV-13.
- **EXP-R-L, EXP-R-M (NOTE).** Agreed; no change.

**Effect on my other drafts.** DEL-01-06 PKG-v0.1 and DEL-09-02 SQ-v0.1
(both unfrozen) are updated to cite EXP-v0.2 and AAC-v0.2's pin.

## K-4 facts (signing, OI-011) — gathered for DEL-01-06

### F-K4-1 Per-executable signatures and entitlements (observed)

Method: `codesign -dv` and `codesign -d --entitlements - --xml | plutil -p -`
(signature reads only; **no binary was executed**), `shasum -a 256`, `file`.
Date 2026-10-03.

**0.160.0** — VC's copy, read in place, nothing written there:
`<scratchpad>/codex-0.160.0/pkg/package/vendor/aarch64-apple-darwin/`
(package.json version `0.160.0-darwin-arm64`). 42 files, **30 Mach-O**, every
one signed by team **2DC432GLL2** (OpenAI OpCo, LLC), hardened runtime
(`flags=0x10000(runtime)`), secure timestamp 2026-10-01.

| Executable | sha256 (prefix) | Size | Entitlements |
|---|---|---|---|
| `bin/codex` | `112fae7a5a1223e6` | 241,555,024 | `com.apple.security.cs.allow-jit`, `com.apple.security.cs.allow-unsigned-executable-memory` |
| `bin/codex-code-mode-host` | `679eedaea70529aa` | 65,391,216 | `com.apple.security.cs.allow-jit`, `com.apple.security.cs.allow-unsigned-executable-memory` |
| `codex-resources/voice/bin/codex-voice-host` | `e408413b79d76e51` | 9,900,112 | `com.apple.security.device.audio-input` |
| `codex-path/rg` | `7c7d5b09c3a57de8` | 4,030,432 | none |
| `codex-resources/zsh/bin/zsh` | `d715e06edcf1661e` | 754,208 | none |
| 25 dylibs under `codex-resources/voice/lib/` and `…/plugins/` (GStreamer, glib, opus, …) | — | — | none (signed, hardened, same team) |

**0.158.0** — the spike scratch copy is now pruned. Read 2026-10-03:
`bin/codex` (sha256 `788a818f…35c8`, matching PIN_SPIKE §3) carries the same
two entitlements; `codex-resources/zsh/bin/zsh` none; same team, hardened.
`codex-code-mode-host`, `rg` and the voice files are gone, so their
0.158.0 entitlements were **not read**.

**App v3 (historical, 0.154.0):** the App re-signed with its own team; "ordinary
Codex entitlements empty, Code Mode host JIT only"
(`BUILD_EVIDENCE_RELEASE_20260913.md`). Inference only: at 0.160.0 a re-sign
that copied v3's entitlement files would drop `allow-unsigned-executable-memory`
from both and `allow-jit` from `codex`, and `audio-input` from the voice host,
unless the per-binary sets are read from the supplier at each pin.

### F-K4-2 What notarisation requires (general knowledge, no network — to be confirmed at the first submission)

- Every executable and library in the submitted bundle is signed with a
  **Developer ID** certificate, with the **hardened runtime** enabled and a
  **secure timestamp**; no `com.apple.security.get-task-allow`; built against a
  recent enough SDK.
- To my knowledge the notary service accepts nested code signed by **another
  team's** valid Developer ID (it checks each signature's validity, hardened
  runtime and timestamp, not that every team matches the outer App). The
  supplier's binaries meet those three conditions as observed above.
- Under the hardened runtime, **library validation** makes a process load only
  libraries signed by Apple or by its own team, unless it has
  `com.apple.security.cs.disable-library-validation`. The voice host and its
  dylibs share team 2DC432GLL2 today, so keeping them together under one
  signer (all supplier, or all App) keeps them loadable; mixing would break
  it.
- Code placed under `Contents/Resources` is sealed by the outer signature's
  resource seal; Apple's guidance prefers executables in `Contents/MacOS` or
  `Contents/Helpers`. Whether Tauri 2's bundler re-signs files it is given as
  `externalBin` sidecars or `resources` is not verified here.
- An entitlement such as `device.audio-input` takes effect only with a matching
  usage string (`NSMicrophoneUsageDescription`) in the hosting App's
  `Info.plist` when the voice host is used.
- Stapling attaches the ticket to the `.app`/`.dmg`; Gatekeeper then assesses
  offline. Submission and stapling use the owner's Apple account (R23-13.2).

### F-K4-3 What each option changes in HOSTING §7 (HOSTING-v0.9, read; nothing edited)

| | Option A — App re-signs the vendor tree | Option B — vendor tree keeps OpenAI's signatures; the App signs and notarises its own code and the bundle |
|---|---|---|
| §7.1 *distribution content identity* | Packaged bytes differ from the published tree (signing rewrites the signature and code directory). Needs two values: the supplier identity (as published, checked at build) and the packaged identity (after signing, recorded by DEL-01-06 OUT-002) | Unchanged: the packaged files are byte-equal to the published tree |
| §7.2 verification rule | "distribution content identity equals the expected identity" must name which identity: either the expected value is the post-sign one recorded at packaging, or the check strips signatures first (byte-equality after stripping is not established). **Restructures §7.1/§7.2** — an escalation item | Unchanged; an optional added consistency check (signer team 2DC432GLL2, hardened runtime) fits as a new row, not a restructure |
| §7.1 *launcher record*, U-17 | Unchanged in kind | Unchanged in kind |
| §10 P-01 signing facts | No longer describe the shipped binaries | Describe the shipped binaries |
| V4-CST-03 ("unmodified") | Re-signing alters the binaries' signatures; whether that is "unmodified" is a reading to state | Binaries ship as published |
| Entitlements | Must be read from the supplier per pin and re-applied per binary (F-K4-1), or Codex features using JIT may fail | Supplier's entitlements ship as signed |
| SEAL-2 (AAC §6.3) | Key store protected by the App's identity | Same: SEAL-2 depends on the App's own signature, not Codex's |

**Leaning for DEL-01-06 (to be decided and recorded there under R23-13):**
B, because it leaves HOSTING §7 unchanged, ships the supplier's entitlements
exactly, keeps the voice host and its libraries under one team, and matches
V4-CST-03. Its open risk is general knowledge only: that notarisation and the
Tauri bundler accept and keep third-party Developer ID signatures. The
design will name a first-package check for it and option A as the fallback,
whose HOSTING §7 consequence would then come to HELP_HUMAN as an escalation.

## Frozen for RV2 (2026-10-03; ready limit two for this round)

Both units cite DEL-09-01 EXP-v0.2 (U1 as repaired, RV confirming). If RV's
confirmation changes EXP, U2 and U3 are repaired only where they rely on what
changed. Signing option B with FP-0…FP-5 and fallback A is accepted by
HELP_HUMAN under R23-13 (recorded in PKG §3 SIGN-1).

### U2 — DEL-01-06 PKG-v0.1 — FROZEN

Folder: `PKG-01_Native App and third-party harness integration/1_Working/DEL-01-06_macOS packaging and distribution evidence/Design/`

| File | sha256 |
|---|---|
| `PACKAGING_AND_DISTRIBUTION.md` | `6920cd8c50b770772b15fe9665466cefb158f8c0d82e434b749006e8dc69b411` |
| `pkg.identity-record.schema.json` | `ced1b72f3c70e8ff4b773dc15d13ca5427ba286b2eb0524720fa724e8f0e445f` |
| `pkg.identity-record.valid.examples.json` | `da2310e5c6cd821cdd0c4f90edfd4d147679569dda99dbdb76cde57cae95e413` |
| `pkg.identity-record.invalid.examples.json` | `4d76890a74384ea0608d764cbc655b8f657e3249f770ebac69b8223568da9318` |
| `pkg.identity-record.rule-violations.examples.json` | `c8e1014ee2fb7234f162ce7abcfef981cd70cf98a21c311c47ad8fe04cc97e44` |
| `pkg.terms-record.schema.json` | `722bc1f76238358d27830c91df3605832f93ed892a4b091bd6c31652e1e0d967` |
| `pkg.terms-record.valid.examples.json` | `bba22d8e6f084945f065075d69a0dfb1f99446ea796773c1d600bc22b8249e6a` |
| `pkg.terms-record.invalid.examples.json` | `02de72caf1614c0ca236e9739714c1d707c6dcca0e4155b2f92a39ab685b0a9d` |
| `pkg.terms-record.rule-violations.examples.json` | `589645a52ff78242f5f2d2ca2bd7ce79a8368224fc96168e29b34d900b6b3391` |
| `prototype/read_tree.py` | `6629250bfdc74f21d9e1bf34bc70ede3592d386e770042b95ad977543559c2bb` |
| `prototype/check_pkg.py` | `e6ac7e9e1c05268658ceea83664b754538345425bd44887e3f78f4213241283d` |

**Claims.**
1. 60% design of DEL-01-06. It covers facts (§2), the signing decision (§3),
   package composition and interfaces I-1…I-7 with arcs (§4), the identity
   record for M2 (§5), the operating sequence PS-1…PS-10 with failure
   behaviour (§6), the first-package check (§7), the install/launch witness
   as an EXP record (§8), the terms record OUT-004 (§9), option A's
   consequences (§10) and designed VER-001…005 (§11).
2. **Signing: option B.** OpenAI's signatures are kept on the Codex tree; the
   App signs its own code; the bundle is notarised. HOSTING §7 is unchanged.
   **Fallback A** applies the supplier's entitlements exactly per file
   (PK-R2) and would restructure HOSTING §7.1/§7.2, so it goes to HELP_HUMAN
   before adoption.
3. **First-package check:**
   - FP-0: the supplier's preconditions;
   - FP-1: does the bundler leave the files byte-equal (G-5)?
   - FP-2: does Codex run from the bundle (relocation)?
   - FP-3: does notarisation accept another team's signatures (G-2)?
   - FP-4: Gatekeeper and deep verification;
   - FP-5: do the entitlements take effect?
4. **Pin basis.** Written for either pin; facts at 0.160.0 were read from the
   whole tree, at 0.158.0 only partly. The design reads the tree per pin
   (FP-0).
5. **App-side choices.** App Sandbox is off, with reasons. No microphone
   string. The vendor binary is the launcher, proposed for HOSTING U-17
   (not an edit of HOSTING).
6. **R23-5:** the ScopeOfWork is unchanged since INIT; no SCA-V4-003 block
   bears on this file.

**Checks.**
- `check_pkg.py --tree <VC 0.160.0 published tree>`: **TOTAL 36, FAIL 0**.
  - Two schemas are valid.
  - 4 valid records pass and violate no rule.
  - 7 invalid records are rejected.
  - 7 rule violations are each caught (PK-R1 ×2, R2, R3, R4 ×2, R5).
  - FP-0's five checks pass on 42 files and 30 Mach-O.
- `read_tree.py`: reads only (codesign -d, sha256); nothing in VC's folder
  was executed or written.
- **Pins:** every 64-hex value was checked against current files by script.
  - AAC is pinned at AAC-v0.2, its `HEAD` bytes, the version relied on
    (R23-21 item 3). §6.3 is unchanged in AAC-v0.3.
  - Six values are VC-tree file hashes, read 2026-10-03.
- **Reach for bundle-seam rows:** DEL-02-02, 02-04 and 01-04 → DEL-01-06
  close no cycle over both layers. The rows are listed, not added.

**Open.**
- U-PKG-1: G-2/G-5 are general knowledge until FP-1/FP-3 run on the first
  package.
- U-PKG-2: U-17 launcher.
- U-PKG-3: qualification pin.
- U-PKG-4: voice host.
- U-PKG-5: minimum macOS.
- U-PKG-6: OI-011 SWB part, waiting for host joins.
- U-PKG-7: OI-007 written position.
- Next-amendment rows: bundle seams; the missing counterpart for
  DEP-09-02-014.
- For RV2:
  - whether §7's decision rule (when FP-1 or FP-3 failure justifies A)
    is sharp enough;
  - whether §4.2 I-3/I-4 correctly avoid creating reliance without rows.

### U3 — DEL-09-02 SQ-v0.1 — FROZEN

Folder: `PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-02_Standalone App candidate qualification/Design/`

| File | sha256 |
|---|---|
| `STANDALONE_QUALIFICATION.md` | `5772038725e2dacd3939707c3fe16e064b543b9b39e4c6049fca05205a61747c` |
| `sq.dossier.schema.json` | `33d33c77b6448999945aa337d7608a718396638dfc6943127bcc684ca4f7870f` |
| `sq.dossier.valid.examples.json` | `751f0059aff0228735b2622ec52a20502b01cd2694ed23bf8d958c5b0d24ee88` |
| `sq.dossier.invalid.examples.json` | `efe33945ca0ba6d788e921994bfe073df51f0cab4e6332b7bf899696289cd5ee` |
| `sq.dossier.rule-violations.examples.json` | `79bf12b56e030fb082ae5a080ce4258e6faeeed4c401f42d392af651a3a3417d` |
| `sq.step-map.json` | `cf0ece1ee481054e923aa8bca80af0c743b3d59b346e244567969b221c08db0f` |
| `prototype/check_sq.py` | `d6861946d909d82b58db72d83c25778cb69e76f0ec9ef1448659af8488b3960e` |

**Claims.**
1. 60% design of DEL-09-02:
   - interfaces I-1…I-13 and O-1 with arcs (§2);
   - case definitions (§3):
     - V4-EXM-10 is J-1…J-9 over WR SQ-J;
     - V4-EXM-11 is S11-1…S11-6, inserted at named points of the same run;
     - V4-EXM-12 is M12-1…M12-6, with H-acct, H-key and local provider
       (K-1, L-1);
   - route and configuration (§4);
   - dossier data and rules SQ-R1…R7 (§5);
   - states and sequence (§6);
   - failure behaviour SF-1…SF-7 (§7);
   - DEL-11-03 return with v3 references for its comparison (§8);
   - person-only actions (§9);
   - designed VER-001…008 (§10).
2. **Joins, not re-implementation.** Every step links its suppliers'
   designed cases; 51 citations are checked to exist in their files.
3. **Current decisions followed (R23-7).** OI-009 is decided (the carried
   wording is listed for the amendment). D2/D3 apply, D4 is the definition
   pin, the App act control is DEL-01-04's, K-7 and L-1/L-6 apply. A15
   registration is a human act; A14 grant and deny are settlements, not acts.
4. **R23-20.** Every planned step gets an EXP record once the runs are due;
   none of these steps is optional (R23-19).
5. **Pin basis.** Written for either pin; one pin per candidate.
6. **R23-5:** the ScopeOfWork is unchanged since INIT.

**Checks.**
- `check_sq.py`: **TOTAL 72, FAIL 0**.
  - The schema is valid.
  - All 51 supplier case citations exist as designed-case rows in their
    files.
  - 2 valid dossiers pass and violate no rule.
  - 4 invalid dossiers are rejected.
  - 6 rule violations are each caught (SQ-R1…R6).
- **Pins.** RS, ACT, NIR and AAC are pinned at their `HEAD` versions (RS-v0.9,
  ACT-POLICY-v0.9, NIR-v0.2, AAC-v0.2) under R23-21 item 3, because O-A is
  revising them. With `git diff` I checked that the cited cases (VC-37,
  VC-40, the VC-NIR rows, VC-AAC-01/-04) are unchanged in the new versions.
  The other pins match current files.

**Open.**
- U-SQ-1: qualification pin.
- U-SQ-2: local model and server, recorded as configuration.
- U-SQ-3: package or development build for the native steps.
- U-SQ-4: OI-010.
- Placement is decided (as EXP §8.4).
- Next-amendment list (§11):
  - OI-009 carry;
  - TBD-001/003;
  - DEP-09-02-012 should name the act control;
  - missing counterparts for DEP-09-02-014 and DEP-09-02-018;
  - REQ-006 read with L-1.
- For RV2:
  - whether the S11 insertion points (§3.2) are faithful to "during the run
    in V4-EXM-10";
  - whether reading "refines it twice" as two registered revisions (WR TT-7,
    K-7) is right.

## Repairs for RV2 (2026-10-03), for RV2's confirmation

The v0.1 bytes of U2 and U3 are in the session scratchpad (`ob_u2_v01/`,
`ob_u3_v01/`). Commit `09ca67d094` (the coordinator's checkpoint) holds the
frozen v0.1 of U3 and of `PACKAGING_AND_DISTRIBUTION.md`. It was taken
mid-repair, though, so the DEL-01-06 schemas, examples and prototype it
holds are already the repaired ones listed below; I checked them byte-equal
by script. Rulings applied: R23-22, R23-26,
R23-27. The repair order followed the coordinator's list.

### U2 repaired — DEL-01-06 PKG-v0.2

| File | sha256 |
|---|---|
| `PACKAGING_AND_DISTRIBUTION.md` | `44c0ac8856e1e2c54384065d8140a5a105494c1e89690e56166ee578af029002` |
| `pkg.identity-record.schema.json` | `a4d3e6c5199c06bf41efbed5b1b1ecc3c6d42995898baaca1b9901ca5f920dc5` |
| `pkg.identity-record.valid.examples.json` | `e0e19cbc9b74651207a303ab1f494f05a853c912ba07c91a555c3f20680f312e` |
| `pkg.identity-record.invalid.examples.json` | `51f00ce8d07f8d683f3f9613678d143d955ecd5b4c4d4e60a9c9a26f38b3d7f6` |
| `pkg.identity-record.rule-violations.examples.json` | `65304ad5ff4009cd24ba399131bed6d9f8027a207be8ecbb81fa3499d251ebc3` |
| `pkg.terms-record.schema.json` | `46ee0d3c0072fd3a94c45749fd8da14ad05e6322367f2df51500e754eb6e6af9` |
| `pkg.terms-record.valid.examples.json` | `ffbd5648a776838ecc5112f32e9b73af80f9b48bd5e418445f2f3b42e183d38f` |
| `pkg.terms-record.invalid.examples.json` | `b87e667ad34630c5cff96e15d7ccb44da276f3c0e0c20ee104325b91c16d7a84` |
| `pkg.terms-record.rule-violations.examples.json` | `d11dca9a761085a3d2ff533a2b70f94c3d8abce2d7d7c4121763649d8dafea7a` |
| `prototype/read_tree.py` | `6dacea788f0a0690ca04bc95f4d50332f4d3ddafb5bb0339147460e64b2debdb` |
| `prototype/check_pkg.py` | `e20c11081e565596f6ec01bf4ef6071deea1b2ac52c6ad6a56518596bcd757dc` |

**Checks.**
- `check_pkg.py --tree <VC 0.160.0 vendor dir>`: **TOTAL 64, FAIL 0** (was 36).
- `read_tree.py --manifest` reproduces `327effb9…8d12`.
- RV2's probes (`$TMPDIR/rv2/probe_pkg.py`) rerun unchanged:

  | Probe | Result |
  |---|---|
  | P1, P2 | Now `PK-R6` |
  | P3, P3b | Invalid. The proper form is `state: missing` (PKG-INV-06, -07; valid PKG-EX-03) |
  | P4 | The probe reads the valid A example, which now carries `escalation_ref`. The schema requires it (PKG-INV-05) |
  | P5 | The enum has `role_set` |
  | P6 | Link targets differ, detected |
  | P7 | The directory link is recorded and reported as `extra`. The probe's second expression tests a key (`'symlink' in x`) the new entry form replaced with `kind`; the FP-0 no-links check now uses `kind == "symlink"` |
  | P8 | The mode change is detected |

- Pins checked by script. AAC is pinned at AAC-v0.2, committed at
  `31d65b0be3`, the version relied on (R23-21 item 3); §6.3 is unchanged
  in the current file.

**Replies.**
- **PKG-R1 (MAJOR): repaired.**
  - New general-knowledge item G-7.
  - The witness (§8) starts from a quarantined installer: W-0 `xattr -l` of
    the installer, W-2 of the installed `.app`, W-5 the first `codex` child
    launch with its cdhash.
  - If quarantine cannot be produced, the witness is `blocked`.
  - FP-2 and FP-4 run under quarantine (§7.1).
  - The identity record's Gatekeeper element requires quarantine evidence
    when assessed (PKG-INV-08).
- **PKG-R2 (MAJOR): repaired.**
  - The signing path is SP-1…SP-4, folded into §6 (PS-3, PS-5, PS-7, PS-8):
    `tauri build` with bundler signing disabled; then `codesign
    --options runtime --timestamp` on P-0 and then on the `.app`,
    **without `--deep`**; then installer, `notarytool` with the owner's
    keychain profile, and `stapler`.
  - FP-1 is split: FP-1(a) after bundling, FP-1(b) after outer signing.
  - OUT-001 configuration elements CF-1…CF-8 are listed (§4.3).
  - The configuration space CS-1…CS-4 is defined, with an exhaustion
    criterion (§7.2).
  - P-1 is "the vendor directory as published" including
    `codex-package.json`.
- **PKG-R3 (MINOR): repaired.** §7.3 classifies every failure, at any FP
  check or in the witness, by recorded cause (termination reason,
  `codesign`/`spctl` output, `syspolicyd`/`amfid` lines). A cause not
  determinable makes the check `inconclusive`.
- **PKG-R4 (MINOR): repaired.**
  - FP-0 checks the first Authority (all 30 are "Developer ID Application:
    OpenAI OpCo, LLC (2DC432GLL2)").
  - `read_tree.py` records directory links, link targets and modes, and
    compares all three.
  - New tree cases TREE P6/P7/P8 in `check_pkg.py`, run on synthetic trees
    under `$TMPDIR` and removed afterwards.
- **PKG-R5 (MINOR): repaired.**
  - PK-R6: every Mach-O is listed (P1/P2).
  - `state: present|missing` with `complete`, and PK-R8 (P3).
  - Option A requires `escalation_ref` and `configuration_space_tried`
    (PK-R7; P4).
  - `role_set` is a bundle item and P-3 lists `roles.json` (P5).
  - The manifest is defined (§5.2) and computed by `read_tree.py
    --manifest`: path-byte order, C collation, final newline. That ordering
    reproduces `327effb9…`; ordering by the whole line does not.
  - Placement is stated in §5.3.
- **PKG-R6 (MINOR): repaired.**
  - I-6: `not-run` with the package as missing input.
  - FP-0, FP-1(a/b) and FP-3 are elements of the identity record
    (`first_package_checks`).
  - FP-2, FP-4, FP-5 and the witness are EXP records on `native_packaged`,
    citing the record (§7.1).
- **PKG-R7 (MINOR): repaired.**
  - I-4 requires the same team and bundle identifier across releases.
  - G-8 is labelled general knowledge.
  - SIGN-3 names SEAL-2's possible key-store entitlement and profile, to be
    confirmed at FP-2 (U-PKG-8).
- **PKG-R8 (MINOR): repaired.** U-PKG-3 is stated per R23-22, and FP-0 runs
  at the qualification pin.
- **PKG-R9 (MINOR): repaired.** I-3 is a build-time input to a package
  candidate. An absent item makes that candidate incomplete; it is not a
  production dependency and implies no row in either direction.
- **PKG-R10 (NOTE): applied.** SIGN-1 now cites R23-26, and OI-011 stays
  open in the register for its SWB part (§3, §13).
- **PKG-R11 (NOTE): applied.** SIGN-1 reason 2 is reworded.

### U3 repaired — DEL-09-02 SQ-v0.2

| File | sha256 |
|---|---|
| `STANDALONE_QUALIFICATION.md` | `f18f26c5c77c593c3b2db9eb2260c3a59b4c34403b3b3b5e3402f4e42db5c458` |
| `sq.dossier.schema.json` | `16f7f2325e7d51424f9e0ec34e782dca150fd6fd96a5a98c7e2272e9088f95a6` |
| `sq.dossier.valid.examples.json` | `86675c152d33367852dcba564216657aca2301bcac3dc0ad829f96cfc64d91b0` |
| `sq.dossier.invalid.examples.json` | `99e154f4a57b42848852ef42fa23d286e517752ed6813468d02124b89843fb28` |
| `sq.dossier.rule-violations.examples.json` | `b1975da675f92aa3490a5885c85eaacdbf174c7ec6512bb9bbbb8e09922a47af` |
| `sq.step-map.json` | `be50ec917f953a3ed649d0c1ea094b744efb678a433d8000f02adc4594bfc893` |
| `prototype/check_sq.py` | `a677cc9cc2fc9ed1ccfd8ed8a9a750093343aea1f3c7df0dd1773453d20db37c` |

**Checks.**
- `check_sq.py`: **TOTAL 108, FAIL 0** (was 72), with 65 citations, each a
  designed-case row in its file.
- RV2's probes (`$TMPDIR/rv2/probe_sq.py`) rerun unchanged:

  | Probe | Result |
  |---|---|
  | Q1 | `SQ-R7` (now also example SQ-RV-08) |
  | Q2 | The probe's dossier claims neither handover nor independence, so only `SQ-R9` fires (its passing steps lack declared stimuli); the handover/independence case is SQ-RV-09 (`SQ-R8`) |
  | Q3 | Schema-invalid (SQ-INV-05) |
  | Q4 | The probe now raises a KeyError, because SQ-EX-01's scenarios carry no outcome; an outcome with nothing recorded is SQ-RV-05 (`SQ-R4`) |
  | Q5, Q6 | Answered by the new enum and properties |

- Pins:
  - NIR-v0.3 is adopted (`aca40c0e…`).
  - ACT, RS and EXEC are pinned at the commits holding the version relied
    on (`dc61150559`, `61e7a0afec`), with the cited rows checked unchanged
    in the current files. The coordinator's checkpoint commit `09ca67d094`
    moved `HEAD`, so "`HEAD`" wording was replaced by commit ids.

**Replies.**
- **SQ-R-A (MAJOR): repaired under R23-27.**
  - ST-1 is the revision condition at J-8: J-7's record still names
    revision 1, whose bytes are unchanged.
  - ST-2 is a source collision placed before J-5 and observed at J-5 and
    J-7.
  - ST-3 is the unperformed-act negatives at J-6 and J-8: silence and
    timeout, the agent's claim, tool success.
  - All are declared in the digested case definition and count toward
    their scenario.
- **SQ-R-B (MAJOR): repaired under R23-27.**
  - ST-4 is a delegated child, staged at J-2, stopped with S11-1 and
    observed at S11-6. It needs a model route that carries delegation
    (HOSTING U-22); otherwise its replay is required (U-SQ-5).
  - ST-5 is a lost acknowledgment, supplied by the **required** replay of
    HOSTING X-09/X-10 on the supplier double. That replay is recorded as an
    EXP rehearsal, cited as `recorded_replay` evidence of S11-6's part and
    compared with the native observation.
  - A stimulus that is neither produced natively nor by replay leaves its
    step `blocked`; that step can never pass (SQ-R9, SF-8).
- **SQ-R-C (MINOR): repaired.** J-6, J-8 and J-9 join VC-AAC-08 and
  VC-AAC-13; J-6 also joins VC-AAC-07 and VC-AAC-03 with ST-3. VC-AAC-04 is
  dropped, and the step-map check now refuses it.
- **SQ-R-D (MINOR): repaired.**
  - NIR-v0.3 is adopted for S11-1, which observes TO-4, including an
    interrupted turn carrying `Turn.error` at 0.160.0.
  - The pin-basis sentence now names that one pin-dependent fact.
  - U-SQ-1 and §0's OI-012 are stated per R23-22.
- **SQ-R-E (MINOR): repaired.**
  - J-8R and J-9R are the TT-7 runs, recorded but `counts: false` with a
    reason, and never aggregated. SQ-EX-04 shows an added step failing
    while the scenario passes.
  - "Try" is restored in J-8 and J-9.
- **SQ-R-F (MINOR): repaired.**
  - Step states are EXP §6.1's.
  - An outcome or result record is allowed only on `recorded` steps
    (schema).
  - A scenario outcome is allowed only when every counted step is recorded
    (SQ-R4).
  - `examination_opened` marks when steps become planned.
  - `handoff.handed_over` and `reported_as_independent` are governed by
    SQ-R8.
- **SQ-R-G (MINOR): repaired.**
  - The settings precondition is declared; "no request raised" means
    `blocked` (SF-9).
  - S11-5 combines only a live turn and a waiting request in J-8's try
    conversation; WR-VC-07's process-loss reconciliation is not staged
    there.
  - S11-6 names the conversation it continues.
- **SQ-R-H (MINOR): repaired.** Each step carries `core_loop_element` (all
  seven of DEL-11-03 REQ-001's elements are covered, checked) and
  `v3_reference`.
- **SQ-R-I (NOTE): applied.** U-SQ-3 states SEAL-2's effect on a development
  build.
- **SQ-R-J (NOTE): applied.**
  - SQ-RV-08 is the example for SQ-R7.
  - VC-R-14 is cited at every S11 step (checked).
- **SQ-R-K (NOTE):** no change.

### U-EXP-1 under R23-22 (folded in, no separate freeze)

`EXAMINATION_PROTOCOL.md` closes U-EXP-1 in place under R23-22. The same
edit replaces "`HEAD`" with AAC-v0.2's commit `31d65b0be3`. No rule, schema
or example changed, and `check_exp.py` still gives 77/0. The file is now
`1371ddb22f72e80aef6dcac734ae6cf288fa3a478bbac5cc607be9e7814a6b9e`, and the
PKG and SQ pins point to it. U-PKG-3 and U-SQ-1 carry the same wording.

## RV2 confirmation items (2026-10-03), repaired in place, for RV2

RV2 confirmed U2 and U3 READY and raised PKG-R12…R14 and SQ-R-L, SQ-R-M.

### U2 — DEL-01-06 PKG-v0.2 (in place)

| File | sha256 |
|---|---|
| `PACKAGING_AND_DISTRIBUTION.md` | `95722979a8fe963782702e4ca459bc124556c43c0a5c4e0ba439559bed7077fa` |
| `pkg.identity-record.schema.json` | `efb0de357efc3cfc0a193a8ffdcb9b08d93908b99d51ece614c4c2d6b94e008a` |
| `pkg.identity-record.valid.examples.json` | `39aa4a5c98699a9ba533b88cdc5be6eed3500cc66ddabb83bc22edc360d13fbc` |
| `pkg.identity-record.invalid.examples.json` | `8fe3237bc10604c24c6d0a5921878877e414031bfb894d1f0a8a0570b245b1f2` |
| `pkg.identity-record.rule-violations.examples.json` | `e24265aeda4f89a754e23590d3fd3669d40bc9d1c7f94063a446fff24b2df14d` |
| `prototype/check_pkg.py` | `1b6f1232fe0b200ffbb0eb56dfbbdfe4a4f29dab3c83e8e1d42b195d752f8d23` |

The terms files and `read_tree.py` are unchanged.
`check_pkg.py --tree <VC 0.160.0 vendor dir>` gives **TOTAL 66, FAIL 0**.

- **PKG-R12: repaired.** In §8 and FP-4, Gatekeeper refusing to open the
  App, or refusing the `codex` child, is now `fail`, classified by §7.3.
  Missing quarantine stays `blocked`.
- **PKG-R13: repaired.**
  - §3 states that option B is not relied on until FP-1(a), FP-1(b) and
    FP-3 pass on the first package.
  - Before then the record may carry them as `not-run`, with the limit
    "option B not yet relied on: FP-1/FP-3 not passed".
  - New rule PK-R9 enforces that limit. The examples carry it, and
    PKG-RV-12 is RV2's probe.
- **PKG-R14: repaired.** The FP-0 label now prints "42 files, 10
  directories, 30 Mach-O", and §11 says so.

### U3 — DEL-09-02 SQ-v0.2 (in place)

| File | sha256 |
|---|---|
| `STANDALONE_QUALIFICATION.md` | `a2ad48cf6803c9e9690e89672582b1a5228ed771fdeb7176968cb88453af552e` |
| `sq.step-map.json` | `e57ff599c169aee2c45fc676fe579d3f2fabdfd4085f15616acf01965e826fc7` |
| `sq.dossier.valid.examples.json` | `426165ba047ac7c53edb1d81debb0f917121866ebbdd7fd7ecc00bca835de7db` |
| `sq.dossier.rule-violations.examples.json` | `eb75db6c3990d7d8488244819271359d16932ab819b9240f918c5a18bf871514` |
| `prototype/check_sq.py` | `4a141a8c3f36620aec3f54ba5ace6d193c5cbfd00129f0d7e6fff7ef1b7ef2ea` |

The schema (`16f7f232…`) and the invalid set (`99e154f4…`) are unchanged.
`check_sq.py` gives **TOTAL 114, FAIL 0**, with 65 citations.

- **SQ-R-L: repaired.**
  - SQ-R9 refuses `produced: replay` for any stimulus whose map has no
    replay counterpart (ST-1…ST-3). That is P-a, now SQ-RV-11.
  - A `not_produced` stimulus requires the step to be `blocked` (or `fail`,
    if another part failed). That is P-b, now SQ-RV-12.
  - New valid example SQ-EX-05: ST-4 not produced, S11-6 `blocked`.
- **SQ-R-M: repaired. I chose the capture route, and the reason is recorded
  in §3.4.**
  - RECOVERY VC-R-04 does stage "a written answer whose acknowledgment
    never comes". But it does so on RECOVERY's stub, whose behaviour beyond
    recorded frames is `constructed`.
  - VER-005 asks for "supported recorded seam evidence", and R23-27's
    counterpart stands in for a condition on the real supplier.
  - So ST-5's counterpart is a recording of the real Codex at the
    candidate's pin. It is in X-09's form and must contain an answer
    written to a server request, with the process ended before any
    acknowledgment arrives. It is replayed with X-10's recovery read.
  - VC-R-04 stays a definition check of the rules.
  - New U-SQ-6 records the capture: owner DEL-01-01 (§9.1 capture method)
    with DEL-01-02 (RQ-05); point of need before RUN-A; without it S11-6 is
    `blocked`.

## Next

- Wait for RV2's confirmation of the U2/U3 repairs.
