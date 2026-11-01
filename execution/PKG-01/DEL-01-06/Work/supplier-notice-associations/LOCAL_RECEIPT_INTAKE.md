# Local source receipt and explicit notice inclusion

The executable intake is `app/packaging/notices/receipts.py`. It has no network
client, downloader, source executor or archive extractor. The maintained plan
is derived from `public-metadata.json`, `macos-runtime-license-metadata.json`
and the current direct-runtime notice index. The eleven requested bodies total
130,005 bytes; their download decision remains pending. No real receipt or
notice applicability selection is claimed by this implementation.

After the owner authorizes the exact acquisition, the acquisition operator can
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
Links, hardlinks and special inputs refuse. Source scripts remain inert bytes;
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
completion manifest last. Completion is valid only with matching files and no
incomplete marker. Preserve the private selection separately for review: its
canonical digest is public, its free-form rationale and paths are not bundled.
The public manifest names the exact Git source, archive/VCS/README associations,
selected component subset and limits. It explicitly does **not** label the
upstream text an archive member or alter the archive index's missing-text facts.
This is technical provenance and explicit inclusion, not license approval or
proof of full transitive coverage.

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
actual receipt and reviewed selection are needed before claiming the five
missing upstream texts supplied. Four complete supplier binary/source/notice
associations and transitive coverage remain open even after this supplement.

The next concrete input is the approved local receipt of the eleven exact
proposed files. After receipt, inspect assembly/source files to resolve the
host/rg/zsh edges, and review the shared upstream license's actual scope before
selecting components. A newly discovered upstream dependency is a separate
exact input proposal, not automatic acquisition.
