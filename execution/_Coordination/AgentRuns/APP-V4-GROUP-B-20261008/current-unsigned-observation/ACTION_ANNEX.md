# Proposed limited signing action — not executed or authorized

Artifact basis cc18e792f4ced071605bce9709c6d1397de36540; physical review
65ad37c8aecbc388c7021bfcc2fda048141186c6; signing-decision review
966a0d2a236baeffa29af47add588d298f8c98fc. SIGNING_DECISION.md supplies exact source,
P0/App/ZIP identities and temporary-custody limits. This annex proposes one
copy-only experiment; the original App and ZIP remain untouched.

**Choice for later owner consideration:** proceed with this limited experiment
on the reviewed debug candidate (dev.chirality.app-v4.skeleton, version0.0.0,
minimum macOS15.0, no extra App entitlements), or defer signing to a later selected
candidate. Neither choice is needed to accept the unsigned B2 contribution.
No question is sent and no choice is recorded by this annex.

Before execution, the owner supplies the actual non-secret Developer ID Application
name and team, explicitly directs this account act, and handles any keychain unlock,
private-key access or OS prompt personally. No agent identity enumeration, keychain
lookup, password/token/private-key collection, autoapproval or credential export.
The commands request a secure timestamp: owner direction must include the required
Apple timestamp-service contact. This is not an offline signing promise or a
notary submission. If owner handling or timestamping cannot complete, stop.

## Exact targets and initialization after authorization

Run in the reviewed repository checkout, with the two owner-supplied environment
variables already set. Their values are intentionally not invented here. Do not
paste the sequence as a way to bypass the decision and check gates.

```sh
set -eu
: "${CHIRALITY_DEVELOPER_ID:?Owner must supply the actual Developer ID Application name}"
: "${CHIRALITY_TEAM_ID:?Owner must supply the actual team identifier}"
export CHIRALITY_CHECKOUT="$(git rev-parse --show-toplevel)"
export CHIRALITY_UNSIGNED_APP='/private/tmp/chirality-b2-current-9a82cbcf/target/debug/bundle/macos/Chirality App v4 (development candidate).app'
export CHIRALITY_UNSIGNED_ZIP='/private/tmp/chirality-b2-current-9a82cbcf/artifacts/Chirality-App-v4-development-9a82cbcf.app.zip'
export CHIRALITY_SIGN_ROOT='/private/tmp/chirality-b2-signing-experiment-9a82cbcf-01'
export CHIRALITY_SIGN_APP="$CHIRALITY_SIGN_ROOT/Chirality App v4 (development candidate).app"
export CHIRALITY_SIGN_P0="$CHIRALITY_SIGN_APP/Contents/MacOS/chirality-app-v4"
```

Refuse if the experiment root already exists, including a dangling symlink. Do
not remove or reuse it. Confirm adequate free space for a full independent copy
and logs (at least1GiB available), no concurrent writer to these subjects, and
original roots are physical non-symlink paths. Resolve the approved vendor root
from the retained current build's supplier.development.conf.json; verify it is
physical and matches the P1 identity below. Source evidence must be read at exact
cc18, using git show, rather than trusting modified working evidence.

## Mandatory gates — failure ends this action

Use the existing pinned PKG Design prototype read_tree.py at cc18 (read only),
whose read(...,False), compare and manifest functions provide complete per-entry
checks. Compare root modes separately, because that prototype excludes the root.
Do not replace these gates with a manifest-only comparison. Retain each boolean,
entry difference, root mode and fresh inventory in the experiment logs.

1. **Originals before copy.** Read the actual unsigned App and compare its complete
   path/kind/mode/size/hash/link-target set with cc18 BUNDLE_INVENTORY.json, excluding
   only stored signature-metadata fields. Include its root mode. Require manifest
   5ee389191acb585483efbf1e54dde5034e1b44aa1bd22e2df4b70ff793d14bfd and P0 hash
   7fe364a05737f4f9696eb4fb9d6cf9671000c4c38a5ac5ca950bc1b0c637bca0. Hash actual ZIP:
   require a3ea8fba0045e1e9773dc7755bc613066c278a81e1432b6986e0b9619a5ac09f and
   145846066 bytes. Refuse unavailable, changed, linked-root or incomplete inputs.
2. **Create only the new copy**, after gate1 passes:

   ```sh
   test ! -e "$CHIRALITY_SIGN_ROOT" && test ! -L "$CHIRALITY_SIGN_ROOT"
   mkdir -m 700 "$CHIRALITY_SIGN_ROOT"
   mkdir -m 700 "$CHIRALITY_SIGN_ROOT/logs"
   /usr/bin/ditto "$CHIRALITY_UNSIGNED_APP" "$CHIRALITY_SIGN_APP"
   ```

   Require full copied App equality with the freshly checked original, including
   root/entry modes, kinds, hashes, sizes, links and exact member set. Confirm all
   corresponding regular files have different device/inode pairs from originals
   (no hard-link alias), and no copied root/ancestor symlink. Recheck originals
   against gate1 after copying. Preserve an immutable pre-sign copy inventory.
3. **P1 before signing.** Compare copy/Contents/Resources/codex against both the
   freshly read approved cached vendor tree and cc18 RESOURCE_COMPARISONS.json P1
   entries, with root modes. Require52 entries excluding root,42 files,10 nested
   directories, no links, manifest
   327effb91a5854eccb388321b4b160e059795f0402c553f594e85365189d8d12. Retain this actual
   pre-sign FP1(a) operation. Read P0 signature metadata on the copy: require the
   reviewed incidental adhoc,linker-signed state, no team and no ordinary App
   signature. Any changed state stops rather than adding another --force.
4. **Owner-directed signing, only after gates1–3 pass:**

   ```sh
   /usr/bin/codesign --sign "$CHIRALITY_DEVELOPER_ID" --options runtime --timestamp \
     "$CHIRALITY_SIGN_P0" >"$CHIRALITY_SIGN_ROOT/logs/sign-p0.txt" 2>&1
   /usr/bin/codesign --force --sign "$CHIRALITY_DEVELOPER_ID" --options runtime --timestamp \
     "$CHIRALITY_SIGN_APP" >"$CHIRALITY_SIGN_ROOT/logs/sign-app.txt" 2>&1
   ```

   First-command omission of --force relies specifically on codesign's linker-signed
   ad-hoc replacement exception, verified at gate3. It is not permission to replace
   another ordinary signature. The explicit outer App alone uses --force because
   P0 now carries an ordinary signature. Neither signing command uses --deep or an
   entitlement file; no supplier path is a signing target. A nonzero exit stops;
   do not retry with stronger flags or automatic keychain handling.
5. **Post-sign checks before any success claim:**

   ```sh
   /usr/bin/codesign --verify --deep --strict "$CHIRALITY_SIGN_APP" \
     >"$CHIRALITY_SIGN_ROOT/logs/verify-app.txt" 2>&1
   /usr/bin/codesign -dv --verbose=4 "$CHIRALITY_SIGN_P0" \
     >"$CHIRALITY_SIGN_ROOT/logs/p0-metadata.txt" 2>&1
   /usr/bin/codesign -dv --verbose=4 "$CHIRALITY_SIGN_APP" \
     >"$CHIRALITY_SIGN_ROOT/logs/app-metadata.txt" 2>&1
   /usr/bin/codesign -d --entitlements - --xml "$CHIRALITY_SIGN_P0" \
     >"$CHIRALITY_SIGN_ROOT/logs/p0-entitlements.xml" 2>"$CHIRALITY_SIGN_ROOT/logs/p0-entitlements.stderr"
   ```

   Require recorded team and Developer ID authority to equal the owner-supplied
   actual selection, hardened runtime and timestamp present, no get-task-allow
   or unexpected entitlements, and valid outer sealed resources. Repeat the full
   P1 comparison from gate3 after signing, including root modes and the unchanged
   selected vendor. This is the experiment's FP1(b) observation, not FP3. Rescan
   the entire signed copy: changes are confined to P0 signing bytes and outer
   Contents/_CodeSignature sealing records; all other existing content, members,
   modes and links remain equal. Stop on unexplained changes; never repair supplier
   bytes or broaden signing scope. Repeat gate1 on both preserved originals.

Record new P0 hash, full signed-App inventory/manifest, actual identity/team,
operations, outcomes and separate actor/recorder identities. Keep every failed
experiment and failure cause identified; do not overwrite the originals or label
a failure successful. No signed ZIP is created by this minimum action. Any later
archive is a new artifact with new hash and review; the current unsigned ZIP
cannot represent signed contents. No notarytool, stapler, Gatekeeper/native launch,
installer creation, supplier execution, credential discovery or release is part
of this authorization proposal. FP3 and applicable later qualification remain
missing; S4/S3/reference and LS5/LS8 holds are unchanged.

This annex is a candidate for independent review. All commands above are proposed;
none was executed while preparing it. The exact unsigned subjects remain temporary
and untouched under the custody conditions in SIGNING_DECISION.md.
