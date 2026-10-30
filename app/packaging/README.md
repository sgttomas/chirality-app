# Offline unsigned supplier preparation

This tool inventories the complete selected Codex vendor tree and prepares its
P-1 layout at `bundle/Contents/Resources/codex`. It never executes supplier code,
invokes Tauri, signs, notarises, generates a production bundle identity, or
launches an App. The preparation directory is **not an App package**.

Use Python 3.10+; only the standard library is required. From `app/`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 packaging/prepare.py inventory /absolute/vendor/tree
PYTHONDONTWRITEBYTECODE=1 python3 packaging/prepare.py inventory /absolute/vendor/tree --signature-display
PYTHONDONTWRITEBYTECODE=1 python3 packaging/prepare.py prepare --vendor /absolute/vendor/tree --expected-manifest <sha256> --pin 0.160.0 --candidate-revision <revision> --inputs /absolute/inputs.json --output /absolute/new-staging-directory
PYTHONDONTWRITEBYTECODE=1 python3 tests/group_b_packaging_test.py
```

`inputs.example.json` lists every accepted input field, initially null. Supply
actual values deliberately. `app_binary`, `workflows`, `shipped_revision_manifest`,
`guidance`, `role_files` and `role_set` are paths, interpreted from the process's
working directory (absolute paths are preferable). Supplied resources are read
and hashed **without being staged**; missing resources remain missing. No
production identity or content selection follows from supplying a path. Content
semantics, acceptance and production eligibility remain with the input owner.
A signing identity or notary profile is a name only; credentials are not inputs.
Unknown fields and duplicate JSON fields are rejected.

CF-1…8 and P-0…4 are represented in `preparation.json`. Only P-1 is copied;
P-0, P-2 and P-3 remain unstaged and P-4 is not generated, even if their source
files are inspected. Consequently `package_complete` is always false. The tool
neither changes `tauri.conf.json` nor treats its development identity as the
production identity. The output directory must be new, outside all inspected
inputs, with no symlink ancestry. On failure after creation it keeps an
`INCOMPLETE.txt` marker and publishes no success report. Successful reports are
published by renaming a temporary file after copy comparison.

Inventory records file hashes, modes, directory modes and link targets without
following links. The PKG §5.2 manifest hashes regular-file content/path lines in
UTF-8 byte order with the final newline. A separate complete comparison detects
mode/link/type/missing/extra differences (including the selected root's mode).
Preparation refuses all links and special files, inconsistent pin/layout/target
metadata, a non-executable or non-Mach-O entrypoint, and an expected-manifest
mismatch. File reads use no-follow descriptors, file mutation checks and
anchored directory traversal. The final copy and source are compared against
the original inventory. Run only against stable, caller-controlled input/output
directories; this is not a filesystem snapshot or a hostile concurrent-writer
isolation service. Extended attributes/ACLs, detached signatures and filesystem
metadata outside the PKG content/mode/link comparison are not copied or proved.

`--signature-display` calls only `/usr/bin/codesign -d`. It captures each return
code, raw display diagnostics and parsed entitlements. FP-0 is reported as pass
only when its supplier-team/authority/hardened-runtime/timestamp/no-get-task-allow
and no-link conditions are observed on all Mach-O files, with unchanged tree
bytes. Explicitly unsigned files fail. Unavailable authority, malformed or warned
entitlement output, or tool failures are inconclusive, not passing. Display is
not signature-validity verification, notarisation or a runtime entitlement test.
Host sandboxing may hide signature facts; repeat inspection with appropriate
read-only host access only when authorized, preserving the earlier limitation.

Exit 0 means the requested inventory/preparation completed; exit 1 means an
explicit signature inspection did not pass FP-0; exit 2 means invalid input or
an operation could not complete. A successful copy is a staging comparison,
**not FP-1(a) after Tauri bundling**. FP-1(b), FP-2/W-4, FP-3, FP-4 and FP-5
remain unrun. Preparation does not import another report's FP-0 result; an actual
signature inspection is a separate artifact. SIGN-1 Option B remains selected;
FP-1(a/b) and FP-3 must pass before reliance, and OI-011's SWB part remains open.

`sources.json` pins the canonical PKG design, scope and inventory prototype.
The maintained code does not execute that prototype or depend on a dated run.
Source drift requires reviewed adoption. Reports include source/tool hashes;
run evidence separately binds the actual source candidate and observations.

## Read-only checks on a received development candidate

Receive the exact candidate record, adjacent inventory/acquisition records,
bundle, source export and selected vendor directory from its build owner. Keep
the recorded source revision even when a merge commit has the same tree. Do
not re-record the candidate or inspect its account state to refresh it.

From the repository root, the existing candidate reader checks retained record
bindings and the live bundle without launching it or checking current App-data
absence (the record's absence observation stays historical):

```sh
PYTHONDONTWRITEBYTECODE=1 python3 app/examination/candidate_identity/identify.py check \
  --record /absolute/identified/candidate-identification.json \
  --app '/absolute/received.app'
```

For each received resource pair, use the maintained packaging inventory and
comparison functions. Substitute the exact agreed paths. This example checks
P1; repeat for bundled `workflows` against the exact source export's
`app/src-tauri/resources/production_workflows`, and `instructions` against
`app/src-tauri/resources/instructions`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 - <<'PY'
import json, sys
sys.path.insert(0, 'app/packaging')
from inventory import scan, compare
actual = scan('/absolute/received.app/Contents/Resources/codex')
expected = scan('/absolute/selected/vendor')
result = compare(actual, expected)
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['equal'] else 1)
PY
```

Retain the exact subject/tool identities, input paths, comparison output and
date with the owning Work/evidence. This comparison covers bytes, modes, types,
links and missing/extra entries; it does not prove signature validity, acquisition
authority or installed custody. Do not add `--signature-display` when signing
identity disclosure is outside the authorized scope. A later signed App/DMG is
a separately identified package: these commands neither create its package
record nor satisfy FP-1(b), FP-2/W-4, FP-3/4/5 or native examination.

The current candidate findings and concrete remaining decisions are in
[DEL-01-06 packaging Work](../../execution/PKG-01/DEL-01-06/Work/PACKAGING_AND_DISTRIBUTION.md#macos-publication-preparation-2026-10-30).
