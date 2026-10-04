# O-B — notes and returns (DEL-01-06, DEL-09-01, DEL-09-02)

Owner O-B: Type 2 TASK (Claude Code subagent of HELP_HUMAN, Claude Opus 5.5),
standing assignment from the work graph's "Coordination" section. Method:
`workflows/coordinated-knowledge-work/WORKFLOW.md` (sha256 `44049bcd…1b18`,
checked). Write boundary: DEL-09-01, DEL-01-06, DEL-09-02 `Design/` (new
files) and this file. Read-only git; no network.

## Units

### U1 — DEL-09-01 EXP-v0.1 — FROZEN 2026-10-03, waiting for review

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

## Next

- DEL-01-06 design (signing choice recorded with reasons, package
  composition, identity record, witness), then DEL-09-02.
