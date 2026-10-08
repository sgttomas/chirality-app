> **PROPOSED SUCCESSOR — STAGED ONLY; NOT ADOPTED; NO CONSUMER RELIANCE.**
> This preserves the full amendment text from `4c5f691c82d887d943849bf15a5efb9a99eec455` below.
> The canonical `PACKAGING_AND_DISTRIBUTION.md` remains the accepted bytes from `45796bc1159ef7903db37863d0c4a192975c0071`.
> References below to candidate HOSTING §7.4 or PKG §§4.4/5.5 mean the
> corresponding `_CC-HOSTING-DISTRIBUTION-01_PROPOSED.md` successor, not the
> accepted canonical documents. “Selected” and “authoritative candidate” below
> describe proposed choices only: U-08/U-17 are not selected or closed by staging.
> DISTRIBUTION_IDENTITY.md is likewise proposed staging. No current consumer
> adopts these requirements by this commit. Versioned lifecycle/PKG and full
> qualification records, atomic producer/consumer/fixture migration, independent
> review and explicit technical adoption remain required before new-method reliance.
> All obligations and owner-reserved acts in the preserved text remain unchanged.

# macOS packaging, signing and distribution evidence

**CC-HOSTING-DISTRIBUTION-01 amendment candidate:** additions in §§4–5 select
full-tree comparison and launcher evidence jointly with HOSTING §7.4. Pending
independent Design review and HELP_HUMAN integration/adoption. The PKG-v0.2
headers, schemas, examples, prototypes and historical observations retain their
original standing; they do not implement the new full-record requirements.

- **Contribution:** DEL-01-06/PKG-v0.2. It supersedes PKG-v0.1 (frozen unit
  U2, file sha256 `6920cd8c50b770772b15fe9665466cefb158f8c0d82e434b749006e8dc69b411`),
  repaired for review `reviews/RV2-PKG-U2.md` under R23-22 and R23-26 (see
  "Changes").
- **Status:** DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. Beside it: two PROPOSED schemas (JSON Schema 2020-12) with valid,
  invalid and rule-violation example sets, and a design prototype
  (`prototype/read_tree.py`, `prototype/check_pkg.py`; not product code).
  No package has been built, signed or notarised.
- **Run and node:** `APP-V4-DESIGN-PASS-4-20261003`, owner O-B (Type 2,
  Claude Opus 5.5), 2026-10-03. Repaired for RV2's confirmation.
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
    `5401f26d9a2a739a725771c8ce83c62ac5fa07be69b0338ee5670b9453d76d87` (C1 re-pin, R23-21 item 4)
    (§4.2 step 1, §7.1, §7.2, §8 S-5, §10 P-02, §11, U-17);
    `PIN_SPIKE_0.158.0.md`
    `0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115`
    (§2, §3, UNRESOLVED).
  - Examination support (SCC-003 M1): DEL-09-01 `EXAMINATION_PROTOCOL.md`
    (EXP-v0.2, confirmed READY by RV; U-EXP-1 closed in place)
    `ff0187dafd9e1f0268a19f9266914bdba64f39e0c8befdcaf20d3da7a7206a93` (C1 re-pin, R23-21 item 4)
    and `exam.result-record.schema.json`
    `f7871c96cef25bb974aea73feca009ed3caf843db5077d80612f13b130af2081`.
  - Bundle content designed by others (cross-references; §4.2):
    DEL-02-02 `WORKSPACE_AND_REGISTRATION.md` (WR-v0.2)
    `5ed5da8842b32b87ae68db3476192a55fc8ff151802684b10bdca16eaa8b8d8b` (C1 re-pin, R23-21 item 4)
    (§3 rows "Bundled workflows", "Shipped-revision manifest"; LS-5, LS-8);
    DEL-02-04 `ROLE_SUPPLY.md` (ROLE-v0.2)
    `c8474d919bceec7d6b5b9dc328b03569b2c64f9d849ff950a2e33062cc1034cf` (C1 re-pin, R23-21 item 4)
    (§4.2 GS-1…GS-3); DEL-01-04 `APP_ACT_CONTROL.md` (AAC-v0.2)
    `062ce28c8a4ec0bc79fc6b6c421245057a59815df14b88fa779b61eeb98be7d7`
    (AAC-v0.2, committed at `31d65b0be3`, the version relied on, R23-21
    item 3; §6.3 SEAL-2 is unchanged in O-A's later versions, checked
    against the working file 2026-10-03); DEL-01-05 `ACCOUNT_AND_PROVIDER_ACCESS.md` (ACCESS-v0.2)
    `ff7f3a2bbb18fd93923b4fe45e4e822dae7691ca606de1ea262f6c52bd862ebb` (C2 re-pin, R23-21 item 4)
    (§0, §20).
  - Rulings, cited by ID (R23-21): R23-2, R23-3, R23-5, R23-7, R23-11,
    R23-13, R23-17, R23-20, R23-21, R23-22, R23-26. Other run records:
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
  fails FP-0 and reopens §3. The qualification pin is chosen by R23-22's
  rule when a candidate is built (U-PKG-3); FP-0 runs at that pin.
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
| 0.160.0 | 42 files (incl. `codex-package.json`), no links; manifest sha256 (§5.2) `327effb91a5854eccb388321b4b160e059795f0402c553f594e85365189d8d12` | 30 | All team 2DC432GLL2; first Authority "Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2)" on all 30 | All yes | `bin/codex` and `bin/codex-code-mode-host`: `cs.allow-jit`, `cs.allow-unsigned-executable-memory`; `codex-resources/voice/bin/codex-voice-host`: `device.audio-input`; all others none |
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

- G-7 **Quarantine and first launch.** Gatekeeper assesses an App at first
  launch only when it carries the `com.apple.quarantine` attribute, which a
  browser download sets and a local copy normally does not. Executables
  inside a quarantined, notarised App are covered by its stapled ticket
  when launched. *(Expected; the witness starts from a quarantined
  installer and records it, §8.)*
- G-8 **Key store and signing identity.** A key an App keeps in the
  operating system's key store stays usable by a later release only if the
  App's designated requirement (team and bundle identifier) is the same;
  the data-protection keychain usually needs a keychain-access-group or
  application-identifier entitlement, which for a Developer ID App also
  needs a provisioning profile. *(Expected; confirmed at FP-2 once SEAL-2 is
  implemented, §3 SIGN-3.)*

## 3. Signing decision (OI-011; R23-13.1; R23-26)

**SIGN-1 (INTEGRATION; decided by O-B under R23-13.1, accepted by HELP_HUMAN;
R23-26: it settles the App-side signing arrangement for design, while OI-011
stays open in the register for its SWB co-owner part and for the next
amendment): Option B — Codex's files keep OpenAI's signatures; only the
App's own code is signed by the App, and the whole bundle is notarised.**
Reasons:

1. **HOSTING §7 stays as written.** The packaged tree is byte-equal to the
   published one, so §7.1's distribution content identity and §7.2's rule
   ("equals the expected identity") need no split. Option A would change
   both (§10).
2. **Entitlements ship exactly as the supplier set them** at each pin
   (§2.1). No per-pin entitlement list is maintained by the App, and the
   failure mode a reused v3 entitlement set would cause (dropped
   entitlements; an inference in §2.2, not a recorded v3 failure) cannot
   arise.
3. **One team per process tree** for the voice host and its libraries (G-3).
4. **V4-CST-03** ("used through its own published interface, unmodified and
   pinned") is met literally; no reading of "unmodified" is needed.
5. The precondition is observed at both pins read (§2.1; FP-0 passes at
   0.160.0, §11).

**Its risk** is G-2, G-5 and G-7, general knowledge only. The first package
answers them before anything relies on B (FP-1, FP-3, FP-4, the witness;
§7, §8). **Option B is not relied on until FP-1(a), FP-1(b) and FP-3 pass on
the first package.** Before then an identity record may carry them as
`not-run`, and it then carries the limit "option B not yet relied on:
FP-1/FP-3 not passed" (PK-R9); such a package is not handed over as relying
on B.

**SIGN-2 Fallback: Option A** (the App re-signs every Codex Mach-O with its
own Developer ID, applying exactly the supplier's per-file entitlements read
at that pin, PK-R2). A is used only when a failure is attributed to
signatures by its recorded cause (§7.3) and the configuration space of §7.2
is exhausted; the identity record then names the fallback reason, the space
tried and the ruling that adopted A (`fallback_reason`,
`configuration_space_tried`, `escalation_ref`; PK-R7). **A would restructure
HOSTING §7.1/§7.2** (a before/after-signing identity split, §10). That
restructure is a first-increment Design change: it comes back to HELP_HUMAN
before A is adopted, and DEL-01-06 does not edit HOSTING.

**SIGN-3 The App's own signature (PROPOSED).** Developer ID Application,
hardened runtime, secure timestamp, no `get-task-allow`. App entitlements:
none known to be needed now. **One possible need is named:** SEAL-2's key
store (AAC §6.3) may need a keychain-access-group or application-identifier
entitlement and a provisioning profile (G-8, general knowledge); it is
confirmed at FP-2 once SEAL-2 is implemented and, if needed, recorded in the
OUT-001 configuration with its reason. **App Sandbox off**, because the
App's Codex child works in the person's project folders, reads the person's
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
| P-1 `Contents/Resources/codex/` | **The vendor directory as published, verbatim**: `bin/`, `codex-path/`, `codex-resources/` and `codex-package.json` (42 files at 0.160.0), same relative layout, links and modes | DEL-01-01 (pin, distribution identity, S-5); DEP-005 | Mapped as a resources directory, not as `externalBin` (G-5: a sidecar is renamed and signed by the bundler). Equal to published (FP-1) |
| P-2 `Contents/Resources/workflows/` | Bundled workflows and the shipped-revision manifest | DEL-02-02 (WR §3; LS-5, LS-8; L-4) | Read-only in the bundle |
| P-3 `Contents/Resources/instructions/` | Product guidance `AGENTS.md`, the four role files and the role set `roles.json` | DEL-02-04 (ROLE §4.1, §4.2 GS-1) | Seeded into App data at first start; the bundle copy is never edited |
| P-4 `Contents/Info.plist` | Bundle id, version, minimum macOS, no microphone string | App build | Version equals the identity record's |
| — App data, project folders | App-owned Codex homes (H-acct, H-key, H-probe), records, seeded guidance | Runtime | **Never in the bundle**; nothing is written into the bundle at run time |

**Launcher (CC-HOSTING-DISTRIBUTION-01 candidate for HOSTING U-17).** The App starts
`Contents/Resources/codex/bin/codex` directly (the vendor binary), adding no
npm-wrapper environment. Reasons: a Tauri App ships no Node runtime for the
npm wrapper; PIN_SPIKE §3 observed the vendor binary started directly gives
the same handshake as the wrapper. The identity covers the whole vendor tree
(HOSTING §7.1 as written). The candidate HOSTING §7.4 / DISTRIBUTION_IDENTITY.md now supplies the joint
method: prepend the resolved `codex-path` for probe and server; reject a prefix
containing `:` or otherwise unrepresentable as one PATH entry; preserve inherited
PATH remainder semantics; remove inherited npm managed-package variables; record
actual nonsecret App configuration and separate H-probe/account homes. This
selection remains pending named review and HELP_HUMAN adoption.

**Relocation (HOSTING §10 P-02; PIN_SPIKE UNRESOLVED).** P-1 keeps the
tree's relative layout, so the sibling resources stay where the binary
expects them. Running from the bundle is observed at FP-2.

### 4.2 Interfaces

| Interface | Direction | Arc (DAG-004) | Contribution | If it fails |
|---|---|---|---|---|
| I-1 Codex distribution | DEL-01-01 → here | DEP-01-06-006, admitted | Pin, published tree, HOSTING §7.1 identity elements, S-5 signing facts | No package for that pin |
| I-2 Packaging interfaces | Tauri 2 bundler; Apple tooling (DEP-005) | DEP-01-06-009, not topological | Bundling, signing, notarisation | §7.2 configuration space, then §7.3 |
| I-3 Bundle content | DEL-02-02, DEL-02-04 bytes, **a build-time input** to a package candidate | **No row**, in either direction | P-2, P-3 bytes and their identities | That candidate is recorded incomplete (`complete: false`, the item `missing`; PK-R8) and is not handed over as a package. This is a property of the candidate, not a production dependency of DEL-01-06 on DEL-02-02/02-04 (as R23-2 treats a decision package as a runtime value) |
| I-4 Signed App identity | Here → DEL-01-04 SEAL-2 | **No row** (AAC §6.3 relies on "the signed App") | **The same Developer ID team and bundle identifier across releases** (G-8), and any key-store entitlement SIGN-3 confirms | SEAL-2 unavailable on an unsigned build (AAC's own limit); a changed team or bundle id loses earlier keys |
| I-5 Examination support | DEL-09-01 → here | DEP-09-01-021, held (SCC-003 M1) | EXP result record for FP-2, FP-4, FP-5 and the witness (§7, §8) | Those recorded without EXP form; not usable by PKG-09 |
| I-6 Package and identity record | Here → DEL-09-01, DEL-09-02 | DEP-09-01-016 (held, M2); DEP-09-02-014 (admitted) | Package + OUT-002 record + OUT-003 witness | Native packaged cases `not-run` with the package as missing input (EXP U-EXP-5; R23-20) |
| I-7 Terms record | Here → the owner's distribution decision | DEP-01-06-011, not topological | §9 | Public release not possible; owner use unaffected |

**Rows for I-3 and I-4 (R23-2; none added here).** Framed as consumer →
DEL-01-06 ("the package places and signs what I ship"). Reach over both
DAG-004 layers, run 2026-10-03 and confirmed by RV2: DEL-01-06 reaches only
DEL-01-01, DEL-01-05 and DEL-09-01, so DEL-02-02 → DEL-01-06, DEL-02-04 →
DEL-01-06 and DEL-01-04 → DEL-01-06 close no cycle; the reverse direction
would (RV2 PKG-R9 shows the path). They are listed for the next amendment
(§13), because adding a row is an escalation condition of this assignment.

### 4.3 The OUT-001 configuration (elements)

The configuration is one file kept with the App source, digested into the
identity record (`configuration.sha256`). It holds:

| Element | Value for B |
|---|---|
| CF-1 Signing identity | The Developer ID Application identity name and team, by name only (never a credential) |
| CF-2 Bundler signing | **Disabled** for the bundling step (no identity configured; SP-1) |
| CF-3 Resources mapping | P-1 from the published vendor directory; P-2, P-3 from their suppliers' build outputs |
| CF-4 Outer signing command | `codesign --sign <CF-1> --options runtime --timestamp` on P-0, then on the `.app`, **without `--deep`**; App entitlements file (empty unless SIGN-3 adds one) |
| CF-5 Info.plist keys | Bundle id (stable across releases, I-4), version, `LSMinimumSystemVersion` (U-PKG-5), no microphone string |
| CF-6 Installer | `dmg`, built from the signed `.app`, itself signed with CF-1 |
| CF-7 Notarisation | `xcrun notarytool submit --wait --keychain-profile <name>`; the profile is the owner's, stored in the owner's keychain; only its name is configured, no credential enters a file or record |
| CF-8 Stapling | `xcrun stapler staple` on the installer |

### 4.4 Full-tree configuration addition (CC-HOSTING-DISTRIBUTION-01; candidate)

OUT-001 also identifies method `codex-vendor-tree-v1`, the immutable qualified
supplier-reference artifact and its exact-byte SHA-256, bundle-relative vendor
root and direct executable, PATH-prefix convention and wrapper-variable removal.
The expected artifact is outside the measured tree. App build identity binds its
bytes; it does not contain a self-referential final package identity. Until a
qualified reference exists, record that missing input; no development digest
substitutes. Preserve CF-1…8 and the existing signing/owner-act boundaries.

## 5. Package identity record (OUT-002; SCC-003 M2) — `pkg.identity-record.schema.json`

### 5.1 Elements

One record per package candidate: the App (revision, build identity,
version, bundle id, target `macOS arm64`, its signature with authority,
cdhash, installer file and its sha256 before notarisation and after
stapling); Codex (pin, published and packaged tree identities — file count,
Mach-O count, manifest sha256 (§5.2) —, launcher, and **every** Mach-O file
with its published and packaged sha256, signature (team, first authority,
hardened runtime, timestamp, entitlements) and the supplier's entitlements);
bundle contents with supplier deliverable, place, `present` or `missing`,
and sha256 when present; `complete`; the OUT-001 configuration reference and
digest; the first-package checks FP-0, FP-1(a), FP-1(b), FP-3 (§7.1); signing
(option, App identity, who performed it, who recorded it, and for A the
fallback reason, configuration space tried and the escalation ruling);
notarisation (state, submission id, log, issues, submitter, stapled);
Gatekeeper (verdict in spctl's words, deep strict verification, quarantine
evidence); the examination support revision; date; limits.

### 5.2 Manifest

`manifest_sha256` is the sha256 of the lines `<sha256>  <relative path>\n`
of every regular file of the tree, ordered by the relative path's UTF-8
bytes (C collation), each line ending in one newline, the last included;
equal to `find . -type f | sed 's|^./||' | LC_ALL=C sort | xargs shasum -a
256 | shasum -a 256` run in the tree, and to `read_tree.py <tree>
--manifest`. At 0.160.0 it is `327effb9…8d12` (§2.1).

### 5.3 Where records live

As EXP §8.4: files, no service. DEL-01-06 keeps
`Evidence/PKG/<candidate key>/package-identity.json` (candidate key = App
revision short form and build identity prefix) and
`Evidence/PKG/terms/<supplier>.json`; its EXP records (FP-2, FP-4, FP-5, the
witness) go under `Evidence/EXP/<candidate key>/` per EXP §8.4.

### 5.4 Rules (`prototype/check_pkg.py`)

- **PK-R1** Option B: the packaged tree equals the published tree (manifest
  and every executable); every executable carries the supplier team, a
  Developer ID Application authority of that team, hardened runtime and
  timestamp; FP-1(a) and FP-1(b) did not fail.
- **PK-R2** Option A: every re-signed executable carries the App's team, a
  Developer ID Application authority, hardened runtime, timestamp and
  **exactly** the supplier's entitlements for that file.
- **PK-R3** The recorder is not the actor of signing or notarising.
- **PK-R4** (terms) The recorder is neither the obtainer of a response nor
  the decider of distribution.
- **PK-R5** A "Notarized" Gatekeeper verdict needs an accepted notarisation.
- **PK-R6** Every Mach-O file of the packaged tree is listed once
  (`len(executables) == packaged.macho_files`), under either option.
- **PK-R7** Option A records the whole configuration space CS-1…CS-4 as
  tried (and, by schema, the escalation ruling).
- **PK-R8** `complete` only when no bundle item is `missing`.
- **PK-R9** Option B with any of FP-1(a), FP-1(b), FP-3 not `pass` carries
  the limit "option B not yet relied on: FP-1/FP-3 not passed" (§3).

### 5.5 Full inventory successor (CC-HOSTING-DISTRIBUTION-01; candidate)

HOSTING §7.4 / DISTRIBUTION_IDENTITY.md defines the authoritative candidate
method for published and packaged trees: exact file/directory/root-mode inventory,
file sizes/digests and the unchanged §5.2 file-manifest encoding. Its inventory
schema and pure-value prototype are maintained in DEL-01-01 Design. Reject
unsupported links/types, invalid paths, unstable traversal or unavailable comparison
as specified there; never omit them. The legacy shell pipeline in §5.2 is a
historical illustration, not the production traversal for arbitrary names.

A versioned successor to PKG-v0.2 must carry both full inventory artifact references
and their exact-byte digests, method and qualified supplier-reference binding.
PK-R1's successor must compare exact inventories as well as existing signature
obligations; v0.2's manifest/counts/executable list alone is insufficient. The
successor schema, examples, checker and maintained app/examination consumer must
propagate together. They are not delivered by this text amendment. Existing v0.2
schema/prototype passes retain historical meaning and cannot satisfy the new rule.

FP-1(a)/(b) compare the actual packaged tree, published tree and qualified reference
under this method, including root mode and empty directories; packaging preserves
them or records a mismatch. Their successor evidence binds the observations,
reference and comparison outcome. Pending qualification may be recorded as missing
input while offline package preparation proceeds; no Option B reliance or FP-2/W-4
pass follows from that state. FP-0 signature facts and FP-3 notarisation are
separate requirements. FP-2/W-4 additionally consumes the complete runtime
verification artifact for the same installed candidate. Runtime revalidation and
stable-bundle custody are specified by HOSTING; this packaging text grants no
execution authority. SIGN-2 remains the required escalation for Option A.

## 6. Operating sequence and failure behaviour

| Step | Action | By | Failure → behaviour |
|---|---|---|---|
| PS-1 | Obtain the pinned platform package; read the published vendor directory (`read_tree.py`) | Build | Pin mismatch with HOSTING §7.1 → stop; no package |
| PS-2 | **FP-0** on the published directory | Build | Fails → option B not available at this pin; §3 reopened |
| PS-3 | **SP-1** `tauri build` with bundler signing disabled (CF-2), placing P-0…P-4 (CF-3) | Build | A P-2/P-3 item absent → that item `missing`, `complete: false`; candidate not handed over |
| PS-4 | **FP-1(a)**: compare P-1 with the published directory | Build | Not equal → §7.2 configuration space |
| PS-5 | **SP-2** sign P-0, then the `.app`, with CF-4 (no `--deep`) | **The owner's Apple account** (R23-13.2) | Signing fails → no package |
| PS-6 | **FP-1(b)**: compare P-1 again; `codesign --verify --deep --strict` on the `.app` | Build | Not equal → §7.2; invalid → no package |
| PS-7 | **SP-3** build and sign the installer (CF-6); submit for notarisation (CF-7); read the log (**FP-3**) | **The owner** (or under the owner's direction, as evidenced) | Rejected → classify by recorded cause (§7.3) |
| PS-8 | **SP-4** staple (CF-8); `spctl -a -vv` on the `.app` | Build | Not "Notarized Developer ID" → record verdict; not a distributable package |
| PS-9 | Write the identity record (FP-0, FP-1, FP-3 inside); validate with `check_pkg.py` | Recorder | Record invalid → not handed over |
| PS-10 | From a **quarantined** installer: FP-2, FP-4, FP-5 and the witness (§8) as EXP records citing the identity record; hand over (I-6) | Examiner (N-1 or N-2) | EXP outcome; a failure is classified by §7.3 |

The installer is never modified after PS-7 except by stapling; any rebuild is
a new package candidate with a new record (V4-EXM-03).

## 7. First-package check: does option B work?

### 7.1 The checks and where each is recorded

FP-0, FP-1 and FP-3 run before a package record exists, so they are elements
of the identity record (`first_package_checks`, each with an EXP outcome,
evidence and, for `fail` or `blocked`, its cause). FP-2, FP-4, FP-5 and the
witness run on the finished package and are EXP result records
(`run_basis: candidate`, packaged subject citing the identity record,
`route: native_packaged`; EXP-R2).

| Check | Question | Method | Pass means |
|---|---|---|---|
| **FP-0** | Does the published tree meet B's precondition? | `check_pkg.py --tree <published directory>` (reads only) | Every Mach-O signed by the supplier team with a Developer ID Application authority, hardened, timestamped, no `get-task-allow`; no file or directory links. **Run at 0.160.0 on 2026-10-03: pass** (§11) |
| **FP-1(a)** | Did bundling leave the supplier's files alone? | `read_tree.py <app>/Contents/Resources/codex --compare <published directory>` after SP-1 | `equal: true` (content, link targets, modes, no missing or extra entry). Settles G-5 for CF-2/CF-3 |
| **FP-1(b)** | Did outer signing leave them alone? | The same comparison after SP-2 | `equal: true`. Settles that CF-4 without `--deep` does not re-sign nested code |
| **FP-2** | Does Codex run from the bundle under quarantine? | From a quarantined installer: launch; HOSTING §7.2 verification of the packaged tree; the first `codex` child launch and handshake to `ready`; the child's cdhash (`codesign -dv` of the installed file) | Verification `verified`; the child starts and handshakes (relocation, HOSTING P-02; G-7) |
| **FP-3** | Does notarisation accept another team's signatures inside the App? | PS-7 log: status and `issues` | Accepted, with no issue on any `Contents/Resources/codex/` path. Settles G-2 |
| **FP-4** | Does the stapled package pass Gatekeeper under quarantine, and deep verification? | `xattr -l` of the installer and the installed `.app`; `spctl -a -vv`; first-launch result | Quarantine present; "Notarized Developer ID"; deep strict valid; first launch not refused. A refusal is `fail`, classified by §7.3; no quarantine is `blocked` |
| **FP-5** | Do the supplier's entitlements take effect? | `codesign -d --entitlements` of the installed files; exercise a Codex feature that uses the code-mode host if the App offers one | Entitlements present; runtime use observed, or `not-run` with the reason |

### 7.2 Configuration space before the fallback

A failure attributed to signatures (§7.3) is first met by trying, in order:

- **CS-1** Placement after bundling: copy P-1 into the bundle after SP-1 and
  before SP-2, instead of the resources mapping.
- **CS-2** Outer signing strictly without `--deep`, P-0 signed explicitly
  first (checks that no step adds deep signing).
- **CS-3** Any bundler or signing-tool option that re-signs nested code
  turned off, if one is found acting despite CF-2.
- **CS-4** Placement of the tree under `Contents/Helpers/codex/` instead of
  `Contents/Resources/codex/` (G-4), with the launcher path changed.

The space is exhausted when CS-1…CS-4 have each been tried and the failure
persists with the same recorded cause. Only then is SIGN-2 proposed to
HELP_HUMAN (escalation, §10).

### 7.3 Decision rule, by recorded cause

Every failure at any FP check or in the witness is classified by its
**recorded cause**, never by which check it occurred at: the termination or
crash reason, `codesign`/`spctl` output, and the `syspolicyd`/`amfid` log
lines around it.

- **Attributed to signatures** (a nested signature invalid after placement;
  notarisation issues on supplier paths; Gatekeeper refusing nested code
  under quarantine; library validation; a JIT-dependent feature failing for
  lack of an entitlement) → §7.2, then SIGN-2 if exhausted.
- **Attributed to layout or launcher** (a missing sibling, a wrong path) →
  repair the layout; B stands.
- **Attributed to stapling or distribution** (ticket not stapled, installer
  damaged) → repair; B stands.
- **Cause not determinable** → the check is `inconclusive` with its limit;
  B is not relied on for that candidate until the cause is found.

## 8. Install/launch witness (OUT-003; REQ-003)

Written as a DEL-09-01 EXP result record (SCC-003 M1): `run_basis:
candidate`, `subject.app_candidate.packaged: true` with this package's
identity record, `route.kind: native_packaged`, platform `macOS arm64`.
The record names the WKWebView identity (EXP §8.1). The witness steps
contain no human act, so either native route applies: N-1 person-operated
with the native-step form (EXP §8.2), or N-2 UI automation once the tool
version has passed EXP-DC-N2 on this candidate (EXP §8.3).

**It starts as a person receives the App (G-7):** the installer reaches the
test Mac by a transfer that sets `com.apple.quarantine` (a download from the
authorized test location), or the attribute is set on it and that is
recorded. If quarantine cannot be produced, the witness is `blocked` with
that cause, never `pass`.

| Step | Observation | Evidence |
|---|---|---|
| W-0 | The installer carries `com.apple.quarantine` | `xattr -l` of the installer |
| W-1 | Mount the installer; Gatekeeper verdict on the `.app` | spctl output |
| W-2 | Copy to `/Applications`; the installed `.app` carries quarantine; first launch is assessed and not refused | `xattr -l` of the `.app`; screen capture or form entry |
| W-3 | The App starts; its version equals the identity record's | About view or bundle read |
| W-4 | The App resolves and verifies its Codex (HOSTING §4.2 steps 1–2) | Verification result `verified` |
| W-5 | The first `codex` child launches from inside the quarantined App and its handshake reaches `ready` under an App-owned home | Lifecycle record; child cdhash |
| W-6 | Entitlements of the installed binaries as packaged | `codesign -d` of the installed files |

Outcome by EXP §3.1 (R23-20): with no package the witness is `not-run` with
the package as missing input; an attempt stopped at its start because
quarantine could not be produced is `blocked` with that cause. **Gatekeeper
refusing to open the App, or refusing the `codex` child, is a `fail`**: it is
the observation W-2, W-5 and FP-4 test, and §7.3 classifies it by its
recorded cause (a refusal of nested code is attributed to signatures).
Configuration names the pin; model and model server are `not_applicable`
(no conversation is needed). DEL-01-06's witness and DEL-09-01's packaged
smoke (M3) are separate results on the same package.

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
| PKG-VC-01 Configuration and identities | VER-001, AC-001 | CF-1…CF-8; layout P-0…P-4; launcher; Codex identity equals HOSTING §7.1 at the pin | package | Not run |
| PKG-VC-02 Identity record against the package | VER-002, AC-002 | PK-R1 (or PK-R2/PK-R7 under A), PK-R6, PK-R8; no inherited v3 or SWBPIPE claim | model; package | Rules run on examples (below) |
| PKG-VC-03 Install/launch witness | VER-003, AC-003 | §8 W-0…W-6 from a quarantined installer, as an EXP record | package; person (signing) | Not run |
| PKG-VC-04 Terms record | VER-004, AC-004, AC-005 | `unresolved` before a response; actors kept apart | model; then the owner's act | Examples valid; PK-R4 detected |
| PKG-VC-05 Boundaries and substitutions | VER-005, AC-006 | Browser evidence, SWBPIPE success or a package's existence never claimed as the witness, terms or release | Review | Not run |
| PKG-VC-06 FP-0 at the pin | §7 | Supplier precondition for B, incl. Developer ID authority | model on the published tree | **Pass at 0.160.0** |
| PKG-VC-07 Tree comparison | FP-1 | Link targets, directory links and modes are compared, not only content | model on synthetic trees | Pass (TREE P6–P8) |

**Prototype run** (`PYTHONDONTWRITEBYTECODE=1 python3 check_pkg.py --tree
<VC's 0.160.0 published vendor directory>` in `prototype/`, jsonschema
4.26.0, Draft 2020-12; reads the vendor directory only; builds and removes
small synthetic trees under `$TMPDIR`), 2026-10-03, at PKG-v0.2 with
RV2's confirmation items: **TOTAL 66, FAIL 0** — two schemas valid; 6 valid records pass and break no rule; 13
invalid records rejected; 14 schema-valid violations each caught (PK-R1 ×4,
R2, R3, R4 ×2, R5, R6 ×2, R7, R8, R9); four tree-comparison cases (RV2
P6–P8 and equality); FP-0's seven checks pass on 42 files and 10
directories / 30 Mach-O, every first
Authority "Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2)", and the
manifest reproduces `327effb9…8d12`. The Codex values in PKG-EX-01 are the
real 0.160.0 published values (all 30 Mach-O); App, installer, configuration
and content identities are placeholders, labelled in `limits`.

## 12. UNRESOLVED

| ID | Item | Owner | Point of need |
|---|---|---|---|
| U-PKG-1 | G-2, G-5, G-7 confirmed (FP-1, FP-3, FP-4, the witness) | DEL-01-06 at the first package | Before any reliance on B |
| U-PKG-2 | HOSTING U-17 launcher value (CC-HOSTING-DISTRIBUTION-01 candidate, §4.1; review/adoption pending) | App implementation owner with DEL-01-06 (HOSTING U-17) | Before verification implementation |
| U-PKG-3 | Qualification pin | **Decided by rule (R23-22):** 0.158.0 stays the definition and generation pin; 0.160.0 is checked and design-compatible; the qualification pin is the newest version that has passed a version-advance check when a candidate is built. FP-0 runs at that pin | When a candidate is built |
| U-PKG-4 | Voice host shipped but unused; no microphone string | App implementation owner | If voice is ever offered |
| U-PKG-5 | Minimum macOS version (CF-5) | App implementation owner | Before the first package |
| U-PKG-6 | OI-011 SWB co-owner part | Waits with host joins (R23-13.2, R23-26) | When joins resume |
| U-PKG-7 | OI-007 written position | Owner and supplier | Before public release beyond owner use |
| U-PKG-8 | SEAL-2 key-store entitlement and profile (G-8) | DEL-01-06 with DEL-01-04, when SEAL-2 is implemented | FP-2 of that candidate |

## 13. For other owners and the next amendment (nothing of theirs edited)

- **HOSTING (DEL-01-01):** U-17 proposal (§4.1); relocation is observed at
  FP-2; under B, §7 is unchanged.
- **Rows for the next amendment (R23-11; reach-checked, none added):**
  DEL-02-02 → DEL-01-06 (bundled workflows, shipped-revision manifest placed
  in P-2); DEL-02-04 → DEL-01-06 (guidance and role set in P-3); DEL-01-04 →
  DEL-01-06 (SEAL-2 relies on the signed App identity, I-4). Also
  DEL-01-06's missing counterpart for DEP-09-02-014 (S1-B §1.2).
- **ScopeOfWork wording (R23-11):** CLM-002 "App implementation owner with
  SWB owner" now reads with L-7, R23-13 and R23-26; TBD-003's "no version"
  reads with D4 and R23-22.
- **OI-011 in the register:** stays open for its SWB part and its record at
  the next amendment (R23-26); no executor edits the register.

## Changes

| Version | Change |
|---|---|
| PKG-v0.1 (2026-10-03) | First Design file: signing decision B with fallback A, composition, identity record (M2), witness, terms record; two PROPOSED schemas; prototype 36/0 incl. FP-0 at 0.160.0 |
| PKG-v0.2 (2026-10-03) | Repair for RV2-PKG-U2. PKG-R1: witness, FP-2 and FP-4 start from a quarantined installer (W-0, `xattr -l`, child cdhash); G-7. PKG-R2: signing path SP-1…SP-4 with bundler signing disabled and outer signing without `--deep`; FP-1(a)/(b); OUT-001 configuration CF-1…CF-8 (§4.3); configuration space CS-1…CS-4 (§7.2); P-1 is the published vendor directory incl. `codex-package.json`. PKG-R3: decision rule by recorded cause (§7.3). PKG-R4: FP-0 checks the Developer ID authority; `read_tree.py` records directory links, link targets and modes and compares them. PKG-R5: every Mach-O listed (PK-R6); `present`/`missing` bundle items and `complete` (PK-R8); option A carries the escalation ruling and space tried (PK-R7); role set; manifest defined (§5.2) and computed by `read_tree.py --manifest`; record placement (§5.3). PKG-R6: I-6 `not-run`; FP-0/1/3 in the identity record, FP-2/4/5 and the witness as EXP records (§7.1). PKG-R7: I-4 same team and bundle id across releases; SIGN-3 names SEAL-2's possible entitlement (G-8). PKG-R8: U-PKG-3 per R23-22. PKG-R9: I-3 is a build-time input. PKG-R10: SIGN-1 under R23-26. PKG-R11: SIGN-1 reason 2 reworded. Schemas `…:0.2`, records `PKG-v0.2`. Prototype 64/0 |
| PKG-v0.2, in place (2026-10-03) | RV2 confirmation items: PKG-R12 Gatekeeper refusal is `fail` (§8, FP-4); PKG-R13 B not relied on until FP-1/FP-3 pass, PK-R9 limit (§3, §5.4); PKG-R14 FP-0 label counts 42 files and 10 directories. Prototype 66/0 |
