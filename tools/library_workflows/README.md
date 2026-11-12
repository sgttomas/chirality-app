---
name: chirality-app-library-workflow-bundle
description: Generate and check the App's bundled workflows from the selected Library release.
metadata:
  kind: instruction
  surface: tool
---
# Library workflow bundle

The App ships every workflow of the selected Chirality Library release
(DEL-02-02 AC-014). This tool writes them into
`app/src-tauri/resources/production_workflows/` and checks them. The tree and
its `MANIFEST.json` are generated: change them only by running the generator.

Run from the repository root with Python 3; no package beyond the standard
library is needed, and nothing is downloaded.

```sh
python3 -m tools.library_workflows generate --archive <release source .tar>
python3 -m tools.library_workflows compare  --archive <release source .tar>
python3 -m tools.library_workflows verify
```

- `generate` writes the tree from the archive, removing anything the release
  does not hold, and prints the manifest's SHA-256.
- `compare` writes nothing. It reports every file that is missing, extra or
  different between the committed tree and the archive. It is the inventory
  comparison of AC-014 on the source resources; no workflow is run.
- `verify` needs no archive. It checks the committed tree against its own
  manifest, and is what ordinary tests and CI run.

## What the source is

The only source is the release's source archive. The tool reads it whole and
refuses it unless its size and SHA-256 equal the ones recorded in the
project's reference record of the selected edition, named by `SELECTION` in
`bundle.py`. An extracted folder is never read. Changing the edition is a
deliberate App change: update the selection in `AGENTS.md` and the reference
record, point `SELECTION` at the new record, regenerate, and update the two
values the host is compiled with in `app/src-tauri/src/workflow_catalog.rs`:
`RELEASE_SUBJECT` and `SELECTED_BUNDLED_MANIFEST_SHA256`. The tests fail until
all of these agree.

## What a workflow is

The release's `workflows/index.json` decides. Every entry of kind `workflow`
is bundled as its whole package folder, byte for byte; the index's file list
for the package must equal the files in the archive, and the set of entries
must equal the folders under `workflows/` that hold a `WORKFLOW.md`, which is
the Library's own inventory rule. Entries of another kind (skills) are not
bundled and are listed in the manifest as `index_entries_not_bundled`, so
every index entry is accounted for. A package the App's own rules would
refuse (a link, an operating-system file, a name the App does not admit, more
than 1000 files or 16 MiB) stops the generator, and so does an index that
names no workflow.

A reading that cannot be made is a refusal, never a pass: an archive that is
not the selected one, a tree folder or file that cannot be read, a missing
tree, a manifest that names no workflow, and a folder holding no file are
each reported and make the command fail. Each command reads the tree in one
traversal and requires a stable tree: do not change it while a command runs,
because a file added after its folder was listed is not seen.

## What the manifest records

`MANIFEST.json` names the Library repository, tag, commit and archive digest,
and for each package:

- its name, its revision under the App's package method
  (`chirality.app.workflow-package.sha256/v1`, computed here without product
  code) and each file's size and SHA-256;
- the Library's own account of it from the index: description, navigation,
  compatible roles, and `library_execution`, the package's optional execution
  companion as the index states it, or `null` when the package has none;
- `library_paths_named`: the Library tool, skill and role paths that the
  package's files name. The App includes none of them.

Neither `library_execution` nor `library_paths_named` is the App's declared
part (DEL-02-01), and neither is given to the requirement check. An empty
tool list in `library_execution` does not mean the workflow needs no tools.

A path is counted in `library_paths_named` only when it is under `tools/`,
`.agents/skills/` or `agents/` and exists in the release archive, as a file
or a folder. It is read in two forms: a relative link, resolved from the file
that names it; and a path written from the Library's root, after any prefix
such as `$INSTRUCTION_ROOT/`. A path of the package itself is not counted. A
skill or tool named without a path is not counted, and neither is the rest of
a URL. A file that is not UTF-8 text is not scanned; this edition has none.
The list says what the text names, not what a run needs.

Document paths (`docs/`, the Library's `README.md`) are deliberately not
recorded. A workflow can name a path that it means in the person's own
project and that also exists in the release: two workflows name `docs/PRD.md`
as the project's file to write. No mechanical rule separates the two, and
telling a person that such a workflow depends on the Library's file would be
false. The field records matching tool, skill and role paths named in package
text; it does not establish that they are required.

## Checks

`python3 -m pytest -q tools/library_workflows` checks the committed tree
against its manifest, the manifest against the selected edition and the
host's compiled values, and the generator's rules on an invented archive.
The host's own tests (`app/src-tauri/src/p2_production_catalog_tests.rs`)
resolve every manifest package from the tree with the App's reader.
