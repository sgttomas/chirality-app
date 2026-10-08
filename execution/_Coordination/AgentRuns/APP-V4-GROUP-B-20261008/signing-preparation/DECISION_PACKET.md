# B4 signing and notarisation preparation — retained B2 candidate

**Prepared only; no signing/notary authorization requested or implied.** The
retained artifact is useful for an exact physical composition decision, but is
not currently sign-ready for a current-source or qualified package. This packet
supplies the concrete candidate, existing checks, missing inputs and proposed
operations. It does not grant a point-action or resolve an owner decision.

## Exact candidate and configuration

| Item | Bound value |
|---|---|
| Built App source | f79317be861bb63553512de3197b22d556268198 |
| Unsigned overlay author | 3269a2c288bdd3b34dbc7c3eb69f868e637a3cf6; subsequently merged in PR #1134 |
| This preparation source | 5d562a1f11bdad3f6794f6ff4ca25e665e9f5e06; it is **not** the artifact's source |
| Artifact | Retained `Chirality App v4 (development candidate).app`, arm64 debug |
| Full file manifest | cd0e8f7216d6c85b1b1cee96300e3b1f4aeaea15bbc6185214345290bdb83c15 |
| P0 executable SHA-256 | 54c3dcf305fc98159706fb21c029140e3a93c8ca71aeba0059b9115e7c5c4f1a |
| Default Tauri config SHA-256 at build | 5f848cc760814808e8013aac972c1ecf90251818b41f4358ee0f342359c4b3ec |
| Explicit unsigned overlay SHA-256 | c0a947f0e5db49e74d9a9a7559ba0d9656551c982ba37decd38fdb541d7288b8 |
| Exact historical build command/environment | ../complete-content/command.json; SHA-256 d89a290680dcad0910fd94743fd440f4402f742adabf12477a0c2bcb39662349 |
| Full historical source inputs | ../complete-content/BUILD_INPUTS.json; SHA-256 75cf327a0dd44bbb47768324e9ccfbcb0be66efc46abb08e3809426435906053 |
| Full physical inventory | ../complete-content/BUNDLE_INVENTORY.json; SHA-256 37a20b94a325e9d87bedaab0bddc5e730f780a9e6e9ef1a4f3f3fbd103abd79f |

The historical command used Tauri `build --debug --no-sign --bundles app
--features custom-protocol`, both explicit resource configurations, and Cargo
`--offline --locked`. The isolated clean environment and exact argument array
remain in the linked command record. No build was repeated. The vendor overlay
selects only the approved cached full development 0.160.0 tree; its path-neutral
mapping is retained alongside the historical command.

Rechecking all 74 physical entries (56 files) reproduced the prior full inventory,
including sizes, modes, link targets and read-only signature metadata. P1's
42 files/10 directories still equal the selected cached tree, manifest
327effb91a5854eccb388321b4b160e059795f0402c553f594e85365189d8d12.
P2/P3 still equal their source resources, including MANIFEST.json, roles.json and
ROLE_SET_SOURCE_BINDING.json. ARTIFACT_RECHECK.json and P2/P3_SOURCE_JOIN.json
record the rechecks. The actual P0 signature remains incidental linker ad-hoc;
Info.plist is not bound and resources are not sealed. This is no Developer ID
or signature-validity conclusion.

FP0_CACHED_VENDOR.json records all seven existing prototype checks passing on
that cached development tree: supplier-team Developer ID authority metadata,
hardened/timestamped Mach-O metadata, no get-task-allow, no symlinks and tree
manifest. This is current read-only cached-tree observation. It neither proves
archive acquisition provenance nor selects the R23-22 qualification pin. No
newer-version query was performed. FP1(a) was observed as exact physical equality
for this development candidate only. SIGN-1 Option B remains **not relied on:
FP-1/FP-3 not passed** at the required qualified-package level.

## Candidate boundary and prerequisites

STALE_SOURCE_BOUNDARY.json names and hashes ten changed compiled-source paths
between the artifact source and preparation source, including Cargo feature,
hosting/distribution and connector source/resources. Later H3B implementation
work, current support adoption, and any later source correction are not inside
this executable. Reading a newer checkout does not upgrade the retained artifact.
No current-main implementation or runtime-witness claim is made.

| Required input/decision | Present state | Consequence and owner |
|---|---|---|
| Candidate source/build for intended signing experiment | Only the older skeleton/debug candidate is retained | App/Group B owner selects the intended revision and build purpose; a changed choice requires a separately authorized build and rechecks. Do not silently sign this as a current/release build. |
| CF1 Developer ID Application identity name and team | **Absent; not inspected** | Owner supplies the intended non-secret name/team and account-act direction. No keychain or identity enumeration has occurred. |
| CF5 bundle identity/version/minimum OS | Actual `dev.chirality.app-v4.skeleton`, `0.0.0`, minimum `15.0` | App owner must select/confirm the intended values. Skeleton/debug defaults and proposed 15.0 are not release decisions; identity change also affects SEAL-2 continuity. |
| CF7 notary profile name | **Absent; not inspected** | Owner supplies the intended profile name and authority for submission when the candidate is ready; no credential enters evidence. |
| R23-22 qualified pin and applicable S3 reference | **Absent for this retained candidate** | Hosting/supplier owner supplies actual version-advance selection, identified distribution and qualified expected reference. Cached 0.160.0 is insufficient. |
| H3B actual runtime/witness | **Absent** | Hosting/examination owners supply the actual joined witness on the selected candidate. No helper implementation or this packet substitutes for it. |
| P2 LS5/LS8 runnable registration | Candidate content is physically present but remains non-runnable | Workflow owner/source decision and valid admission remain separate. Signing cannot change admission. |
| SIGN-3 App entitlements / SEAL-2 applicability | No needed App entitlement established; possible SEAL-2 dependency remains open | App/SEAL owner identifies required entitlements/profile, if applicable, before relying on signed continuity. Never transplant v3 entitlements. |
| FP3/notary and quarantine/installation route | Not executed; no installer exists | Only after concrete candidate/account prerequisites may owner-directed signing/notary and qualified native examination be proposed for action. |

No request to use an Apple account is ready merely because two non-secret names
are missing. Candidate intent, source, qualification and applicable entitlement
inputs must be settled and joined first. This packet asks for no point-action
approval, and supplies no release or package-complete standing.

## CF1–CF8 concrete disposition

| Configuration element | Candidate-specific preparation |
|---|---|
| CF1 | Missing Developer ID Application name/team above. Supplier team metadata in FP0 is not the App's signing identity. |
| CF2 | Existing build explicitly disabled signing with `--no-sign` and null signingIdentity; historical log confirms skip. Retain that rule for any new unsigned build. |
| CF3 | Current actual mapping: approved vendor → Contents/Resources/codex; production_workflows → workflows; instructions → instructions. Full content/mode/link comparisons pass on this artifact. |
| CF4 | Proposed owner-directed signing of P0 first, then outer .app with hardened runtime and timestamp, **without --deep**; entitlement file only after its exact bytes/purpose are selected. No command executed. |
| CF5 | Actual values above; no microphone usage key. Final choices are not silently supplied here. |
| CF6 | Proposed DMG from a subsequently signed identified .app, then sign DMG with the selected CF1 identity. No installer path, bytes or identity exists yet. |
| CF7 | Proposed `xcrun notarytool submit --wait --keychain-profile` for that identified installer; owner profile name missing. No service contacted. |
| CF8 | Proposed `xcrun stapler staple` after accepted notary result; retain ticket/assessment evidence. Not executed. |

## Ordered proposed operations and stop conditions

These are a reviewable sequence for later action, not executable authorization.
`APP` must resolve to the newly selected exact candidate, never follow a mutable
latest pointer. `APP_EXECUTABLE` is its Contents/MacOS/chirality-app-v4. `VENDOR`
is the selected published tree, not an inferred cache identity. `DEVELOPER_ID`,
`NOTARY_PROFILE` and `DMG` are intentionally unset; do not invent values.

1. **Resolve the prerequisites above and freeze the actual intended source,
   config and content identities.** Stop before signing if the record still
   names only this stale skeleton/debug candidate while the intended purpose
   requires current source or qualified behavior. A rebuild is a separate task,
   not authorized or performed here. Recheck P0–P4 and FP0 at the selected pin.
2. **SP1 / CF2–3 / FP1(a).** If a new build is required, use its reviewed explicit
   unsigned configuration and custom-protocol feature, then run the existing
   `read_tree.py "$APP/Contents/Resources/codex" --compare "$VENDOR"`.
   Stop on any content/mode/link/missing/extra mismatch; do not sign over it.
3. **SP2 / CF1, CF4.** After exact account-act direction exists, proposed commands:

   ```sh
   codesign --sign "$DEVELOPER_ID" --options runtime --timestamp "$APP_EXECUTABLE"
   codesign --sign "$DEVELOPER_ID" --options runtime --timestamp "$APP"
   ```

   These commands have no --deep and currently name no entitlement file. If a
   reviewed App entitlement file is required, record its hash and apply its
   selected use explicitly before execution. Stop for missing name/team,
   entitlement uncertainty affecting the selected purpose, signing error or
   unintended nested-code mutation; do not inspect credentials to fill a gap.
4. **FP1(b).** Repeat exact P1 comparison and run
   `codesign --verify --deep --strict "$APP"`; inspect resulting P0/outer metadata.
   Stop if supplier bytes/modes/links differ or verification fails. `--deep` is
   used only for verification, never signing. Preserve outcomes and exact new
   signed-artifact hashes; original unsigned evidence stays historical.
5. **SP3 / CF6–7 / FP3.** Prepare a reviewed DMG recipe from that signed App,
   bind its exact bytes, sign with CF1, then propose
   `xcrun notarytool submit "$DMG" --wait --keychain-profile "$NOTARY_PROFILE"`.
   Stop before submission for absent owner profile/direction or unbound installer.
   A rejected or incomplete result is not accepted; retain status/issues,
   especially supplier paths. This packet does not create a DMG or select an
   unreviewed installer recipe to hide the missing input.
6. **SP4 / CF8.** Only after notary acceptance, propose
   `xcrun stapler staple "$DMG"` and `spctl -a -vv "$APP"`. Stop if ticket or
   assessment does not establish the required notarized standing. Neither
   acceptance alone nor a cached assessment is a quarantine launch witness.
7. **PS-9 / package record.** Create the actual PKG identity record only with
   its candidate/config/signing/notary evidence and truthful incomplete checks.
   Apply PKG-v0.2 schema/PK-R rules; preserve Option B's reliance limit unless
   required FP1(a), FP1(b) and FP3 pass. Keep signing actor and recorder distinct.
8. **PS-10 / FP2, FP4, FP5 and W0–W6.** Separate later authorized native examination
   starts with a quarantined installer; retain quarantine, Gatekeeper and actual
   installed App/supplier verification/handshake. No quarantine at start means
   blocked, a Gatekeeper refusal means fail, and no package means not-run.
   Record installed entitlements and actual code-mode exercise or explicit
   not-run reason. M3 smoke is a separate result on the same package. Route
   qualification and human acts remain the examination owner's responsibility.

For any failed check, classify by recorded cause. Signature-attributed failures
lead through CS1–CS4 under their own bounded work; layout/launcher and stapling
faults are repaired at source. Unknown cause is inconclusive. Do not adopt
SIGN-2 re-signing of supplier code without the named escalation and HOSTING
interface treatment after configuration space is actually exhausted.

## Current support and B9 record

SUPPORT_BASIS.json verifies fixed canonical EXP-SUPPORT-BINDING-v1 pins selected
at this preparation revision. Its named adoption merge is PR #1138 / 5d562a1f11.
The prior complete-content build did not use this later method. No retrospective
producer-use claim, canonical EXP result, or PKG identity record is manufactured.
When the actual package/result/review/change cohort exists, retain exact records
and canonical sidecars, freeze the six-role selection, and run the maintained
canonical join. Historical correspondence never proves original producer use.
Legacy inventory checks remain partial; native/SQ/S4 receiving work stays separate.

The exact canonical DEL-01-06 Evidence/PKG/terms/OpenAI.json path was absent
before this assignment. It now records the supplied **unresolved** obligation,
**not_made** distribution decision and actual Codex TASK recorder/date. No response,
contact, owner act or legal conclusion is invented. TERMS_VALIDATION.json records
passing unchanged schema and PK-R4 checks. This terms record is outside the
canonical six-role EXP/PKG identity binding cohort. Owner use and independent
development remain unaffected; the written-response obligation belongs before
public release beyond owner use. No supplier communication was sent.

## Return and limits

B4 preparation is concrete and read-only; signing/notary execution remains
unperformed with the prerequisites above. B9's unresolved record is materialized,
not the supplier's answer. Physical artifact unchanged, package_complete false,
qualified false; FP1(b)/FP2/FP3/FP4/FP5, M2/M3, S3/H3B and release remain unsupplied
for this artifact. A current-source selection will require new candidate-specific
evidence. Independent review follows the sealed preparation commit. No additional
build, launch, supplier execution, signing, keychain/identity inspection, credential
use, notary submission, installer creation, download or newer-version lookup occurred.
