# Local source receipt and explicit notice inclusion

2026-11-02 update: the owner approved and packaging received the eleven exact
files. See [actual receipt and scope](approved-receipt-20261102/SCOPE.md).
For current source, pass the [rederived supplement](approved-receipt-20261102/rederived-4e942918/README.md)
to `--upstream-notices`; the original `supplement/` is bound to the superseded plan.
The subsequent [four-file receipt](approved-receipt-20261102-four/SCOPE.md)
resolved the rg/zsh release selectors. Neither receipt establishes full license
coverage or binary associations.

The executable intake is `app/packaging/notices/receipts.py`. It has no network
client, downloader, source executor or archive extractor. The maintained plan
is derived from `public-metadata.json`, `macos-runtime-license-metadata.json`
and the current direct-runtime notice index. The original eleven bodies total
130,005 bytes and are retained with their receipt. The five-component technical selection and its rederived supplement
are recorded at the links above.

For an independently authorized acquisition, the acquisition operator can
place each received body beneath a selected physical intake directory at its
plan `id` (for example `objc2/LICENSE.md` or `codex/scripts/codex_package/rg`).
These commands do not acquire anything:

```sh
python3 -B app/packaging/notices/receipts.py plan
python3 -B app/packaging/notices/receipts.py verify --intake /absolute/physical/intake
```

`verify` checks each expected size and Git blob SHA-1, records SHA-256, and
reports missing and conflicting inputs separately (exit 1 and 2 respectively;
0 means all planned receipts match). It reads only the eleven named files.
The intake directory must exist. Links, hardlinks and special inputs refuse. Source scripts remain inert bytes;
references found in their eventual contents do not authorize further acquisition.
The two already-retained Codex root texts remain under `supplier_notices/` and
are not counted as new requested receipts. Root-text correspondence does not
close the four binary/source/notice associations.

After inspecting the exact upstream license text and its scope, the responsible
packaging reviewer supplies a separate closed JSON selection:

```json
{
  "format": "upstream-notice-selection/1",
  "plan_sha256": "SHA256 of canonical receipts.encode(receipts.plan()) bytes",
  "components": ["objc2"],
  "basis": "Actual technical applicability rationale and review reference"
}
```

The example is a shape, not an actual selection. Only a nonempty subset of the
five maintained crate associations can be selected. No source/release recipe
can be selected as notice text. Staging checks the selected receipt directly;
it does not require unrelated Codex inspection files to exist.

```sh
python3 -B app/packaging/notices/receipts.py stage \
  --intake /absolute/physical/intake \
  --selection /absolute/private/selection.json \
  --output /absolute/separate/new-supplement
python3 -B app/packaging/notices/receipts.py check-stage \
  --output /absolute/separate/new-supplement
```

The output parent must already exist outside the repository, intake and private
selection directory. Staging refuses existing output, uses exclusive no-follow
writes, retains an initial incomplete marker on interruption, and publishes a
completion manifest last. The two bundled public files must have mode 0644;
the staging directory and completion marker remain private. Completion is valid only with matching files and no
incomplete marker. Preserve the private selection separately for review: its
canonical digest is public, its free-form rationale and paths are not bundled.
The public manifest names the exact Git source, archive/VCS/README associations,
selected component subset and limits. It explicitly does **not** label the
upstream text an archive member or alter the archive index's missing-text facts.
This is technical provenance and explicit inclusion, not license approval or
proof of full transitive coverage. Any edit to either maintained metadata file
changes the plan digest and requires renewed explicit selection/staging.

For a future coordinated build, add `--upstream-notices
/absolute/separate/new-supplement` to the existing production-input preparation
command. The helper revalidates the supplement against the selected frozen
export's metadata and current notice index and maps only `LICENSE.md` and
`manifest.json` beneath `third-party-notices/upstream/`. Its input account hashes
the mapped files and receipt helper. The existing `check_plan` interface and
three plan outputs remain unchanged. The supplement must remain immutable while
building, like every other mapped external resource. Neither a completion marker
nor a public selection hash is authentication or live authority.

Without the opt-in, no supplemental resources are included. Existing retained
12d26 unsigned bundle and its notice resource comparison remain historical and
unchanged. Current direct-runtime preparation remains 22 components / 30 texts;
the rederived supplement supplies one upstream overview for the five selected
components, not five complete missing archive texts. Four complete supplier
binary/source/notice associations and transitive coverage remain open.

The eleven-file and subsequent four-file receipts and their source findings are
recorded above. Remaining supplier associations and notice inputs are described in
[shipped notice coverage](../SHIPPED_NOTICE_COVERAGE.md). A newly discovered
upstream dependency is a separate exact input proposal, not automatic acquisition.
