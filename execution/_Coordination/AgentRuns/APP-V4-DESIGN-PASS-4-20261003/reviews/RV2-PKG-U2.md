# RV2-PKG-U2 — review of DEL-01-06 PKG-v0.1 (packaging, signing, distribution evidence)

- Reviewer: RV2 (Type 2 TASK, Claude Opus 5.5), run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-03. Method: `coordinated-knowledge-work` §3.
- Unit: `PKG-01_Native App and third-party harness integration/1_Working/DEL-01-06_macOS packaging and distribution evidence/Design/`.
- **Hashes.** `PACKAGING_AND_DISTRIBUTION.md` is `6920cd8c…b411`, as expected. I also checked the ten other files listed in `OWNERS/O-B.md` "Frozen for RV2" with `shasum -a 256`, and all of them match. I reviewed the frozen bytes.
- Basis read:
  - the ScopeOfWork (`08e30b97…d795`, matches the pin);
  - `Dependencies.csv`;
  - HOSTING-v0.9 §4.2, §7.1, §7.2, §8 S-5 and §10 P-01/P-02, plus U-17;
  - PIN_SPIKE §3 and UNRESOLVED;
  - AAC §6.3 at `HEAD` and in the working diff;
  - ROLE §4.1 and §4.2;
  - WR §3 and LS-5/LS-8;
  - ACCESS §20;
  - EXP-v0.2 §3.1, §6.1, §8, F-5 and its result schema;
  - R23-1…R23-23;
  - `RV-EXP-U1.md`.

## Verdict: **REPAIR**

There is no BLOCKING finding. There are 2 MAJOR, 7 MINOR and 2 NOTE findings. One NOTE (PKG-R10) is cross-owner and goes to HELP_HUMAN.

Several parts stand as they are and can be kept: signing option B, the HOSTING §7 reading under B, the layout, the identity and terms records, the separate install/launch witness, and the reach statement.

Option B is sound against HOSTING §7 as written. §7.1 defines the distribution content identity as "Per-file content identities of the vendor tree the supplier executes", and §7.2 says "the distribution content identity equals the expected identity". With a byte-equal tree both hold unchanged. SEAL-2 in AAC §6.3 depends on "the signed App", not on Codex's signatures. The weak points are in how the first package and the witness would show that B works, not in the choice itself.

## Findings

### PKG-R1 — MAJOR — the witness and FP-4 do not ensure that Gatekeeper actually assesses the package as a person would receive it (§8 W-1, W-2, W-5; §7 FP-2, FP-4; OUT-003; REQ-003)

- **Evidence.**
  - §8, W-1: "Mount or unzip the installer; Gatekeeper verdict on the `.app`".
  - §8, W-2: "Copy to `/Applications`; first launch shows no Gatekeeper block".
  - §7, FP-2: "Launch the App; HOSTING §7.2 verification of the packaged tree; handshake reaches `ready`".
  - §7, FP-4: "PS-6, PS-8", that is, `codesign --verify --deep --strict` and `spctl -a -vv` on the `.app`.

  No step says that the installer carries the download quarantine attribute, or how it comes to carry it. A grep of the file for "quarantin" finds nothing.
- **Inference (general knowledge, not checked here).**
  - On macOS, Gatekeeper assesses an App at first launch only when the App carries the quarantine attribute, which a browser download sets. A package built on the build machine and copied to `/Applications` does not normally carry it.
  - Executables nested inside a quarantined App are covered by the App's notarisation ticket when they are launched.
  - Without quarantine, W-2 passes trivially, and W-5 (the supplier-signed `codex` child starting from inside a different-team App) passes without that launch path ever being exercised.
  - `spctl -a` in PS-8 assesses the outer `.app` only.
- **Consequence.**
  - The question option B depends on is whether a person's Mac runs OpenAI-signed nested code from inside an App signed by another team. The design names that risk itself in §3: "Its risk is G-2 and G-5".
  - As written, the witness could record `pass` without the condition under test ever being present. This is the same class of gap as EXP-R-C: a control that is claimed but not present.
- **Repair.**
  - Make the witness and FP-2 start from a quarantined installer. That means transferring it the way a person would, or setting `com.apple.quarantine` and recording it, with `xattr -l` of the installer and of the installed `.app` as evidence.
  - Record the first-launch result and the first `codex` child launch under that condition. The cdhash of the child could also be recorded.
  - If quarantine cannot be produced, the witness is `blocked` or `inconclusive`, never `pass`.
  - State in §2.3, as a G-item, that this rests on general knowledge until observed.

### PKG-R2 — MAJOR — the signing step is not defined, so FP-1 cannot say whether "the bundler" re-signs, and "repairable by configuration" has no defined space (§6 PS-3, PS-5; §7 FP-1 and the decision rule; §2.3 G-5; OUT-001 CONFIG; AC-001)

- **Evidence.**
  - PS-3: "Build the App; place P-0…P-4", by "Build".
  - PS-5: "Sign the App (P-0 and the bundle)", by "**The owner's Apple account**".
  - FP-1: "`read_tree.py … --compare <published tree>` after PS-3 and again after PS-5 … Settles G-5 for the configuration used".
  - G-5: "Tauri 2's bundler signs the main binary and any `externalBin` sidecar with the configured identity; whether it re-signs Mach-O files copied as `resources` is not known here".
  - Decision rule: "FP-1 or FP-3 failing because of signatures, and not repairable by configuration, moves the package to SIGN-2".
  - OUT-001 in the ScopeOfWork is the CONFIG output: the "packaging, signing and notarisation configuration".
- **What is missing.** The file never says which tool performs PS-5, nor the conditions under which it does so. The two possibilities differ:
  - **The bundler signs during `tauri build`.** This is one step with the identity configured, so PS-3 and PS-5 merge. FP-1 "after PS-3" is then already a post-signing comparison, and the actor of PS-3 becomes the owner's account.
  - **A separate `codesign` of the outer bundle signs.** Then G-5 does not arise. The question becomes whether that command signs nested code, for example with `--deep` (general knowledge: `--deep` signing is the usual way nested code gets re-signed).

  In either case:
  - FP-1 detects a change but cannot attribute it.
  - The "configuration" that might repair a failure is unnamed: placing the tree after bundling and before the outer signature, a resources mapping, signing options.
  - So the boundary between "repair" and "fall back to A" — the A fallback being an escalation that restructures HOSTING §7 — is left to judgement at the package.
- **Smaller parts of the same gap.**
  - P-1 lists the tree as "`bin/`, `codex-path/`, `codex-resources/`". The published vendor directory that FP-0 read also holds `codex-package.json`: 42 files, which I checked with `find`. A copy of only the three directories would fail FP-1's `missing` check.
  - The App-side configuration elements are not listed: signing identity, hardened runtime, the entitlements file (none), `minimumSystemVersion` (U-PKG-5), the resources mapping, the notarisation tool, and how its credential is supplied without entering any record.
- **Consequence.** At the 60% level, an implementer cannot build OUT-001 without making the one choice that decides whether B survives. FP-1 also cannot answer the question the brief and O-B pose: does the bundler re-sign?
- **Repair.**
  - Name the signing path for B. For example: bundling with signing disabled, placement of P-1 verified by FP-1(a), then outer signing without `--deep`, verified by FP-1(b). Alternatively, bundler signing with a stated configuration.
  - Say what FP-1 compares at each point.
  - Make P-1 "the vendor directory as published, including `codex-package.json`".
  - List the configuration elements OUT-001 holds.
  - Define the configuration space to try before SIGN-2, and when it is exhausted.

### PKG-R3 — MINOR — the decision rule prejudges the cause of FP-2 and FP-5 failures (§7, decision rule)

- **Evidence.** "FP-2 failing is a layout or launcher defect, not a signing one. FP-4 failing with FP-3 accepted is a stapling or distribution defect."
- **Consequence.** A child killed at launch for a code-signing reason would be classified as a layout defect, so the SIGN-2 and HOSTING escalation route would not be taken. Examples are library validation, an invalid nested signature after placement, or a Gatekeeper refusal of nested code under quarantine (PKG-R1).
- **Repair.**
  - Classify by recorded cause: the crash or termination reason, and the `codesign` or `syspolicyd` log lines.
  - Route any failure attributed to signatures, whatever FP number it occurs at, through the same rule as FP-1 and FP-3.
  - Treat FP-5 the same way if a JIT-dependent feature fails.

### PKG-R4 — MINOR — FP-0 and `read_tree.py` omit checks that G-1 and FP-1 rely on (§7 FP-0, FP-1; `prototype/read_tree.py`, `check_pkg.py fp0()`)

- **Evidence.**
  - FP-0 checks team, hardened runtime, timestamp, `get-task-allow` and links (`check_pkg.py fp0()`).
  - G-1 requires "a Developer ID certificate". No check reads `Authority=`.
  - I read it myself with `codesign -dvv` on all 30 Mach-O at 0.160.0: every one is "Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2)". So there is no present defect, only a missing check.
- **Scratch probes** (`$TMPDIR/rv2/probe_pkg.py`, importing the prototype unchanged):
  - P6: two trees whose file symbolic links point to different targets compare `byte_equal: true`, because a link has no `sha256` and `None == None`.
  - P7: a symbolic link to a directory is not recorded at all, because `os.walk` lists it under directories. FP-0's "no links" check would still pass.
  - P8: a tree whose executable bit was stripped compares `byte_equal: true`. FP-2 would catch that only indirectly.
- **Repair.** Add the following assertions:
  - FP-0: every Mach-O's first `Authority` is "Developer ID Application" for the supplier team.
  - `read_tree`: record directory links and link targets, and compare file modes, or state that modes are FP-2's.

### PKG-R5 — MINOR — the identity record does not hold what §5, §6 and §4.2 say it carries (`pkg.identity-record.schema.json`; PK-R1, PK-R2; §4.2 I-3; §6 PS-3; SIGN-2; ROLE §4.1)

Scratch probes, against the prototype's own validator and rules:

- **P1 / P2: executables are not tied to the Mach-O count.** An option-B record listing 1 of 30 Mach-O, and an option-A record listing only `bin/codex` as re-signed, are both schema-valid with no rule fired.
  - Under B, manifest equality covers this.
  - Under A, PK-R2 never sees the 25 voice dylibs. A record could show `codex-voice-host` re-signed by the App team while its dylibs keep 2DC432GLL2, which is the G-3 mixing that §3 reason 3 warns against.
  - Repair: under A, require `len(executables) == packaged.macho_files`, or a per-Mach-O list.
- **P3: a missing item cannot be recorded.** I-3 says "Package lists the item `missing`", and PS-3 says "listed `missing`". However `bundle_contents[].identity` is a required sha256, and both "missing" and an absent identity are refused. The failure behaviour cannot be written down.
- **P4: an option-A record needs no escalation reference.** SIGN-2 says A "comes back to HELP_HUMAN before A is adopted". `signing` holds only `option`, `app_identity`, `performed_by`, `recorded_by` and `fallback_reason`, so an A record without that ruling is valid.
- **P5: the role set has no place.** ROLE §4.1 says "The App release contains a role set `roles.json`… Its content identity is recorded with each start". P-3 lists only "`AGENTS.md` and the four role files", and the item enum has no role-set value. `other` would hide it.
- **The manifest is not computed by the tool the schema names.** The `tree_identity.manifest_sha256` description says "(prototype/read_tree.py)", but `read_tree.py` does not compute it.
  - I reproduced §2.1's `327effb9…8d12` as the sha256 of the sorted `"<sha256>  <path>\n"` lines, in C collation with a trailing newline. The value is right.
  - The definition omits collation and the final newline, so two implementers could get different values.
- **Placement is not stated.** The file does not say where the identity record and the terms record live. EXP §8.4 places EXP records only.

### PKG-R6 — MINOR — EXP mapping: I-6's failure value and the claim that every FP check is an EXP result record (§4.2 I-6; §7 opening; §8)

- **Evidence: I-6's failure value.**
  - I-6, "If it fails": "Native packaged cases `blocked` (EXP F-5)".
  - §8: "with no package the witness is `not-run` with the package as missing input".
  - EXP-v0.2 U-EXP-5: "`native_packaged` cases `not-run` (AWAITING INPUT) until then".
  - R23-20: `blocked` only for a case that was attempted.
- **Evidence: the FP checks as EXP records.** §7 says "Each is an EXP result record (`case_id` FP-n, `owner_deliverable` DEL-01-06)". Three of the checks do not fit that form:
  - FP-0 reads a published tree with no candidate. Its result for 0.160.0 exists only as a prototype run. EXP has `definition_check` with a `definition` subject, but this is a read of real supplier bytes, not a model.
  - FP-1 and FP-3 run before PS-10 writes the package record. EXP-R2 needs that record (`package_record`) for any `native_packaged` record.
  - None of FP-0, FP-1 or FP-3 is a route EXP defines.
- **Repair.**
  - I-6 → `not-run` with the package as missing input.
  - Say which `run_basis`, subject and route each FP check uses. Alternatively, make FP-0, FP-1 and FP-3 elements of the identity record, and keep the EXP form for FP-2, FP-4 and FP-5 and for the witness.

### PKG-R7 — MINOR — I-4/SEAL-2 interface: identity stability across releases, and the entitlements the key store may need (§4.2 I-4; §3 SIGN-3; AAC §6.3)

- **Evidence.**
  - I-4 contributes "A stable Developer ID identity per release".
  - AAC §6.3 (unchanged in AAC-v0.3; `git diff` read): "a per-installation key in the operating system's protected key store, available only to the signed App".
  - SIGN-3: "App entitlements: none known to be needed".
- **Inference (general knowledge).**
  - Keychain access control for an App follows its designated requirement, which is team and bundle identifier. A key created by one release stays usable by the next only if both stay the same across releases, not merely within one release.
  - The data-protection keychain usually needs a keychain-access-group or application-identifier entitlement. For a Developer ID App outside the App Store, that also needs a provisioning profile.
- **Consequence.** SIGN-3's "no entitlements" and I-4's "per release" may each defeat SEAL-2. That would only show up after implementation.
- **Repair.**
  - I-4: "the same team and bundle identifier across releases".
  - SIGN-3: name SEAL-2's key-store needs as a possible entitlement, to be confirmed at FP-2, with the general-knowledge label.

### PKG-R8 — MINOR — U-PKG-3 does not follow R23-22 (§12 U-PKG-3; header "Rulings")

- **Evidence.**
  - U-PKG-3: "Qualification pin (OI-012); VC adoption boundary | HELP_HUMAN (R23-3, R23-17)".
  - R23-22 item 2: "The qualification pin … is chosen when a candidate is built: the newest version that has passed a version-advance check of this kind by then … no new owner decision is needed". R23-22 is not cited.
- **Repair.** Restate U-PKG-3 per R23-22, cite it, and say that FP-0 runs at that pin.

### PKG-R9 — MINOR — I-3 adds no row, but its failure behaviour creates reliance in the reverse direction; it should be stated as a build-time input (§4.2 I-3; §6 PS-3). This answers O-B's question on I-3/I-4.

- **Evidence.**
  - I-3, "If it fails": "Package lists the item `missing`; not released".
  - PS-3: "package not handed over as complete".
  - So DEL-01-06's handover waits on DEL-02-02 and DEL-02-04 bytes, the direction R23-2 says never to frame as a row.
- **Reach, both layers, my own script over `_DAG/DAG-004` `DependencyEdges.csv` and `CandidateEdges.csv`.** DEL-02-02, DEL-02-04 and DEL-01-04 each already reach DEL-01-06. For example: DEL-02-02 →(DEP-02-02-014, held) DEL-02-01 →(DEP-02-01-017, held) DEL-03-01 →(DEP-03-01-030, held) DEL-09-09 →(DEP-09-09-012, admitted) DEL-09-01 →(DEP-09-01-016, held) DEL-01-06. A DEL-01-06 → DEL-02-02 row would therefore close a cycle.
- **What holds.**
  - I-4 is framed correctly (DEL-01-04 consumes the signed identity).
  - I-3's own row direction is correct.
  - O-B's reach statement is confirmed: "DEL-01-06 reaches only DEL-01-01, DEL-01-05 and DEL-09-01".
- **Repair.** Say in I-3 that the bundle content is a build-time input to a package candidate, the way R23-2 treats a decision package as a runtime value. It is not a production dependency of DEL-01-06 and implies no row in that direction.

### PKG-R10 — NOTE, cross-owner, for HELP_HUMAN — the standing of SIGN-1 against the ScopeOfWork's decision owner for OI-011 (§3 SIGN-1; ScopeOfWork CLM-002, REQ-005, TBD-001)

- **Evidence.**
  - SIGN-1: "INTEGRATION: decided by O-B under R23-13.1, accepted by HELP_HUMAN".
  - REQ-005: "deciding the unresolved OI-011 arrangement belongs to the App implementation owner with SWB owner in CLM-002 … the packaging author or recorder does not acquire those decision rights by preparing the record".
  - R23-13.1: "Technical choices. O-B makes them on the facts and records them."
  - L-7: the App implementation owner is the owner.
  - §13 carries CLM-002's wording to the next amendment.
- **What I infer.** The owner's "Scope of owner questions" direction returned K-4 to HELP_HUMAN, and R23-13 rests on it. That likely covers the App-side technical choice, with the SWB co-owner part deferred (R23-13.2). The registers still show OI-011 OPEN.
- **Asked of HELP_HUMAN.** Confirm in one line that SIGN-1 disposes of OI-011's App part for design purposes, with the owner's account act at packaging (PS-5, PS-7) as the person's act and the SWB part waiting. Alternatively, say that it stays PROPOSED until the owner acts. No repair is needed from O-B either way.

### PKG-R11 — NOTE — wording, and what was confirmed

- **Wording.** SIGN-1 reason 2 says "the v3 failure mode (dropped entitlements) cannot occur". v3 recorded no such failure; §2.2 rightly calls it an inference. "The failure mode a reused v3 entitlement set would cause" would be accurate.
- **Confirmed.**
  - The §2.3 G-items are labelled general knowledge, and each is tied to an FP check.
  - SIGN-3's App Sandbox reason is labelled general knowledge.
  - The v3 quotations exist:
    - `sign-electron-runtime-v2.mjs` lines 16–17;
    - `verify-codex-pin.mjs` line 17;
    - `PUBLIC_RELEASE_20260913.md` line 37;
    - `entitlements.mac.plist`, JIT only.
  - PIN_SPIKE line 80 supports the launcher reason ("same handshake as via the wrapper") and the relocation being not observed.

## What I checked and how

- **Hashes.** All 11 frozen files match `O-B.md`. Every 64-hex value in the file was checked by script against the project tree and against the `HEAD` bytes of modified files:
  - 14 match current files;
  - AAC `062ce28c…` equals `HEAD` (AAC-v0.2, pinned under R23-21 item 3);
  - the six VC-tree values (`112fae7a…`, `679eedae…`, `e408413b…`, `7c7d5b09…`, `d715e06e…`, and manifest `327effb9…`) I recomputed from VC's extracted 0.160.0 vendor directory with `shasum` (read only).
- **Signing facts.**
  - `codesign -dvv` on all 30 Mach-O, with `Authority`, team, runtime flag and timestamp read only.
  - `find -type l` found 0 links, and there are 42 files.
  - O-B's F-K4-1 and §2.1 facts at 0.160.0 are confirmed.
  - The 0.158.0 row rests on PIN_SPIKE §3, which I read: "Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2); hardened runtime flag".
- **HOSTING §7 under B.** I read §7.1, §7.2, §4.2 steps 1–2, §8 S-5, §10 P-01/P-02 and U-17. Option B leaves them unchanged. §10's option-A table correctly identifies §7.1/§7.2 as the restructure.
- **AAC.** `git diff HEAD` of `APP_ACT_CONTROL.md`: the v0.3 change adds the A16 row, AI-9 and the header. §6.3 SEAL-2 is unchanged, as O-B states.
- **Bundle-content suppliers.** WR §3 rows "Bundled workflows" and "Shipped-revision manifest", LS-5 and LS-8; ROLE §4.1 and §4.2 GS-1…GS-3. These are consistent with P-2 and P-3, except for `roles.json` (PKG-R5).
- **Reach (cycles).** My own script over both DAG-004 layers. Consumer → supplier, with `UPSTREAM` read From→Target and `DOWNSTREAM` read Target→From. O-B's statement is confirmed (PKG-R9).
- **Prototype rerun, not rebuilt.** `PYTHONDONTWRITEBYTECODE=1 python3 check_pkg.py --tree <VC 0.160.0 vendor dir>` gave **TOTAL 36, FAIL 0**, as reported. No `__pycache__` was left (checked with `ls`).
- **Missing assertions.** I added these as scratch probes `$TMPDIR/rv2/probe_pkg.py` P1–P8, reported in PKG-R4 and PKG-R5. Nothing was written into the unit or into VC's folder.
- **ScopeOfWork mapping.**
  - OUT-001 → §4, §6 (gap PKG-R2).
  - OUT-002 → §5 (gaps PKG-R5).
  - OUT-003 → §8 (gap PKG-R1).
  - OUT-004 → §9; the terms record is adequate for AC-004/AC-005 at model level, and PK-R4 is exercised.
  - REQ-005 → §1 (PKG-R10).
  - AC-006 → U-PKG-6/7, PKG-VC-05.
- **60% level.** What is missing for an implementer:
  - the signing path and the configuration elements (PKG-R2);
  - the quarantined install path (PKG-R1);
  - record placement and a representable `missing` content item (PKG-R5);
  - SEAL-2's identity constraint (PKG-R7).

  States, sequence and failure behaviour are otherwise present (PS-1…PS-10).

## Not checked

- Whether Tauri 2 re-signs resources, what notarisation accepts, and Gatekeeper's quarantine behaviour. These are general knowledge for me as for O-B. No network was used, and nothing was built, signed or executed.
- 0.158.0's other Mach-O files (pruned, as O-B says).
- The terms-record example contents beyond the prototype run.
- DEL-09-01 EXP-v0.2 itself. RV confirmed it READY (`DISPATCH.md`); I checked only the elements PKG uses.

## Repair confirmation (PKG-v0.2, 2026-10-03)

### Verdict: **READY** — repairs confirmed

All of PKG-R1…PKG-R11 are adopted in the returned files. I raise one new MINOR (PKG-R12) and two NOTEs (PKG-R13, PKG-R14). There is no BLOCKING or MAJOR finding.

**What I checked.**

- **Bytes.** All 11 files match O-B.md "Repairs for RV2" (`shasum -a 256`). `PACKAGING_AND_DISTRIBUTION.md` is `44c0ac88…9002`.
- **Prototype.** `PYTHONDONTWRITEBYTECODE=1 python3 check_pkg.py --tree <VC 0.160.0 vendor dir>` gives **TOTAL 64, FAIL 0**, as reported. `read_tree.py --manifest` gives `327effb9…8d12`, which equals my own computation from round 1. No `__pycache__` was left.
- **Earlier probes.** I reran my round-1 probes (`$TMPDIR/rv2/probe_pkg.py`) unchanged:
  - P1 and P2 now fire PK-R6.
  - P3 is refused. `state: missing` is the form for an absent item.
  - P4: `signing` now holds `escalation_ref` and `configuration_space_tried`, and option A requires both.
  - P5: `role_set` is in the enum.
  - P6 detects the different link target and reports the directory link as `extra`.
  - P8 detects the stripped mode.
  - P7's second expression tests a key that the new entry form replaced with `kind`. O-B is right about that, and FP-0 now tests `kind == "symlink"`.
- **New probes** (`$TMPDIR/rv2/probe_pkg2.py`):
  - An option-B record whose packaged manifest differs fires PK-R1.
  - An option-A record with only CS-1 tried fires PK-R7.
  - The remaining gap is in PKG-R13.
- **Pins.**
  - The AAC pin names commit `31d65b0be3`. `git show 31d65b0be3:<AAC>` hashes to `062ce28c…`. That commit is the file's last change before v0.3 and is an ancestor of `HEAD`.
  - I checked every other 64-hex value by script. They match current files, or the VC-tree values I recomputed in round 1, or `HEAD` for the v0.1 self-reference (`09ca67d094` holds v0.1).

**Per finding.**

| Finding | State | Evidence in v0.2 |
|---|---|---|
| PKG-R1 | **Confirmed** | See "PKG-R1" below |
| PKG-R2 | **Confirmed** | See "PKG-R2" below |
| PKG-R3 | **Confirmed** | §7.3 classifies every failure by its recorded cause (termination reason, `codesign`/`spctl`, `syspolicyd`/`amfid`), not by which FP check it occurred at. "Cause not determinable" gives `inconclusive`, and B is not relied on for that candidate |
| PKG-R4 | **Confirmed** | FP-0 checks the first Authority; all 30 Mach-O are "Developer ID Application: OpenAI OpCo, LLC (2DC432GLL2)" in the rerun. `read_tree.py` records directories, links with their targets, and modes. The new TREE P6/P7/P8 cases pass |
| PKG-R5 | **Confirmed** | PK-R6, PK-R7 and PK-R8 are added. `role_set` is added and P-3 lists `roles.json`. §5.2 defines the manifest (byte order, final newline) and `read_tree.py --manifest` computes it. §5.3 states the placement |
| PKG-R6 | **Confirmed** | I-6 is now `not-run` with the package as missing input. FP-0, FP-1(a/b) and FP-3 are `first_package_checks` in the identity record, each with outcome, evidence and cause (cause required for `fail`/`blocked`). FP-2, FP-4, FP-5 and the witness are EXP records citing the identity record |
| PKG-R7 | **Confirmed** | I-4 requires the same team and bundle identifier across releases. G-8 is labelled general knowledge. SIGN-3 names the possible key-store entitlement and profile, and U-PKG-8 tracks it |
| PKG-R8 | **Confirmed** | U-PKG-3 is restated as "Decided by rule (R23-22)". FP-0 runs at the qualification pin |
| PKG-R9 | **Confirmed** | I-3 is "a build-time input to a package candidate". An absent item makes that candidate incomplete; the file says this "is a property of the candidate, not a production dependency", with no row in either direction |
| PKG-R10 | **Confirmed** | SIGN-1 cites R23-26. U-PKG-6 keeps OI-011's SWB part open |
| PKG-R11 | **Confirmed** | SIGN-1 reason 2 now reads "an inference in §2.2, not a recorded v3 failure" |

**PKG-R1 (confirmed).**

- §8 now opens with the quarantine requirement: "It starts as a person receives the App (G-7)", by a transfer that sets `com.apple.quarantine`, or with the attribute set and that recorded.
- The steps record it:
  - W-0 records `xattr -l` of the installer;
  - W-2 records `xattr -l` of the installed `.app` and checks that the first launch was "assessed and not refused";
  - W-5 records the first `codex` child launched "from inside the quarantined App", with its cdhash.
- "If quarantine cannot be produced, the witness is `blocked` …, never `pass`".
- FP-2 and FP-4 run "From a quarantined installer". The schema requires quarantine evidence whenever Gatekeeper is assessed.
- Gatekeeper's behaviour stays labelled as general knowledge. G-7 sits under §2.3 "(general knowledge; confirmed or refuted by §7)", is marked "*(Expected …)*", and is listed in U-PKG-1.

**PKG-R2 (confirmed).**

- **Signing sequence.**
  - PS-3/SP-1 runs `tauri build` with bundler signing disabled (CF-2).
  - PS-5/SP-2 signs P-0 and then the `.app` with `codesign --options runtime --timestamp`, "**without `--deep`**" (CF-4).
  - PS-7/SP-3 builds the installer and submits it with `notarytool --keychain-profile`. Only the profile's name is configured, and no credential enters a file or record (CF-7).
  - PS-8/SP-4 staples and runs `spctl`.
- **The double FP-1 comparison.**
  - FP-1(a) runs after SP-1 and settles G-5 for CF-2/CF-3.
  - FP-1(b) runs after SP-2 and settles that CF-4 does not re-sign nested code.
  - Each compares content, link targets and modes, and reports missing or extra entries. Any change found can therefore be attributed to the bundling step or the signing step.
- **The bound on "repairable by configuration".** CS-1…CS-4 are, in order:
  - placement after bundling;
  - signing strictly without `--deep`;
  - turning off any option found to re-sign;
  - the `Contents/Helpers` placement.

  The space is "exhausted when CS-1…CS-4 have each been tried and the failure persists with the same recorded cause". Only then is SIGN-2 proposed to HELP_HUMAN, and PK-R7 requires all four on any option-A record.
- **Other parts.** P-1 now includes `codex-package.json`, and the eight OUT-001 configuration elements CF-1…CF-8 are listed.

### PKG-R12 — MINOR (new) — §8 records a Gatekeeper refusal as `blocked`

- **Evidence.**
  - §8: "an attempt stopped at its start (no quarantine, or Gatekeeper refuses to open it) is `blocked` with that cause".
  - W-2 expects "first launch is assessed and not refused".
  - FP-4 passes when the "first launch not refused".
  - R23-20: `blocked` is for a stated precondition or dependency that stopped the case. EXP §3.1: `fail` is "evaluated on the actual subject and not met".
  - The same clause was in v0.1 and I missed it in round 1. Its effect is larger now that the witness exists to test this exact behaviour.
- **Consequence.** A Gatekeeper refusal is the observation W-2 and FP-4 test, and §7.3 already treats "Gatekeeper refusing nested code under quarantine" as a failure attributed to signatures. Recording it as `blocked` would show B's main risk as a precondition gap rather than a `fail`. Under EXP-R1 a `fail` outranks `blocked`, so this mislabels the witness rather than producing a false pass.
- **Repair.**
  - "No quarantine" stays `blocked`.
  - "Gatekeeper refuses to open it" becomes `fail` at W-2, classified by §7.3.

### PKG-R13 — NOTE — a `complete` option-B record does not need FP-1 or FP-3 to have passed (PK-R1)

- **Evidence.**
  - PK-R1 tests only that FP-1(a)/(b) "did not fail". Valid example PKG-EX-01 is `complete: true` with `fp1a`, `fp1b` and `fp3` all `not-run`.
  - My probe: setting `fp1b: not-run` on a complete B record is schema-valid and fires no rule.
- **Assessment.**
  - Manifest equality between the packaged and published trees still covers the files themselves.
  - §3 says B is not relied on until the first package answers FP-1 and FP-3, but a handed-over record does not show whether that has happened.
- **Repair (optional).** Either require `pass` for `fp1a`, `fp1b` and `fp3` on a record handed over under I-6 for the first package under B, or add an explicit "B not yet relied on" limit.

### PKG-R14 — NOTE — FP-0's label counts entries, not files

- **Evidence.** `check_pkg.py` now prints "FP-0 published tree read (52 files, 30 Mach-O)". The tree has 42 regular files and 10 directories (`find -type f`, `find -type d`), and §2.1 and the record's `files` say 42.
- **Repair.** Label it "52 entries (42 files)". This is cosmetic.

**Not checked in this round.** The schema and terms-record changes beyond the probes and the prototype run. No network was used and nothing was built or executed.

### Confirmation of PKG-R12…PKG-R14, at candidate commit `d150856784` (2026-10-03)

**Verdict: READY.** PKG-R12, PKG-R13 and PKG-R14 are adopted. There are no open findings.

**What I reviewed.** I reviewed the committed bytes (`git show d150856784:<path>`). For `projects/chirality-app-v4`, the working tree equals the commit (`git diff --quiet d150856784` returned clean).

**Hashes.** The six files O-B lists match at the commit: schema, the three example sets, `check_pkg.py`, and `read_tree.py` (unchanged). `PACKAGING_AND_DISTRIBUTION.md` at the commit is `0d8d14d2…42b4`, not O-B's `95722979…77fa`.

**Closeout changed only pin lines.**
- The closeout records the chain `95722979…` →C1→ `33aa12a5…` →C2→ `0d8d14d2…` (C1_INTEGRATION §7; C2 §1).
- I reversed the recorded edits in the committed file with my own script (`$TMPDIR/rv2/recon.py`):
  - the four C1 pins (HOSTING, EXP, WR, ROLE) and the C2 pin (ACCESS) set back to their old values;
  - the "(C1/C2 re-pin, R23-21 item 4)" markers removed.
- The result hashes to exactly `95722979…`. So the commit's bytes are O-B's repaired file plus those pin edits, and nothing else.
- Every pin in the committed file names current bytes, apart from:
  - the AAC-v0.2 commit pin (`31d65b0be3`, checked last round);
  - the VC-tree values;
  - the v0.1 self-reference.

**Prototype.** `python3 -B check_pkg.py --tree <VC 0.160.0 vendor dir>` gives **TOTAL 66, FAIL 0**. FP-0 now prints "42 files, 10 directories, 30 Mach-O". PKG-RV-12 is detected as PK-R9.

**Per finding.**

| Finding | State | Evidence |
|---|---|---|
| PKG-R12 | **Confirmed** | §8: "**Gatekeeper refusing to open the App, or refusing the `codex` child, is a `fail`**", classified under §7.3. Only "quarantine could not be produced" stays `blocked`. FP-4's pass column says the same. W-5 is now covered too, which goes beyond my finding |
| PKG-R13 | **Confirmed** | §3: "Option B is not relied on until FP-1(a), FP-1(b) and FP-3 pass on the first package". PK-R9 requires the limit "option B not yet relied on: FP-1/FP-3 not passed" whenever any of the three is not `pass` under B. Examples: PKG-EX-01 and -03 carry the limit; PKG-EX-04 has all three passing; PKG-RV-12 is my probe |
| PKG-R14 | **Confirmed** | The FP-0 label now reads "42 files, 10 directories, 30 Mach-O" |
