# Chirality library 2.1.0 — App receiving source

This record identifies the shared Library edition that App development agents
use from 2026-11-07, and the partial source fixture retained for App's own
compatibility harness. The receiving account, limits and reserved migration
choices are in
[DEL-10-01 `LIBRARY_V2_1_RECEIVING.md`](../../execution/PKG-10/DEL-10-01/Work/LIBRARY_V2_1_RECEIVING.md).

## Selected source

| Item | Identity |
|---|---|
| Repository | `https://github.com/sgttomas/chirality-library` |
| Tag | `library-v2.1.0`, annotated tag object `f199d07eae679f775f09b4217cb145259dcfe5fc` |
| Commit | `c35b7bbc463f81c1fed566c744ea49d168d29eee` |
| Comparison basis | `library-v2.0.0`, commit `2f981163d76772d3779697d9def1a9e951d978e7` (prior App operational selection) |
| Publication notes | `execution/PKG-05/DEL-05-01/Work/PublicationNotes-2.1.0.md` at the commit, read in full |
| Method index | `workflows/index.json` at the commit, sha256 `9a3bf1d135a0d7f8b334aec8b13838c4ffbd08db67a74ce7899c52944a0bbd2d`: `chirality-method-index/v1`, 76 entries, none naming INTERLOCUTOR in `executionRoleIds`. At 2.0.0: sha256 `29e78d226c637678aa58d92672e1e5d0bb5b00054e3824f8ab2a02354cdcfdba`, 43 entries |
| Governing coordination method | `workflows/coordinated-knowledge-work/WORKFLOW.md`, blob `38201f9b451c51586adb52e1b5ce279f6c3b750c`, sha256 `0488a744eb163fc633e1ae356de1955a58e9ca1f6396ef6b028c2e8ffad75355`; identical at 2.0.0 and 2.1.0 |

Bytes were read from Git objects in the local Library checkout with
`git show`/`git cat-file` at the commit; the checkout itself was not advanced,
edited or reset. No release asset was downloaded, so the published archive
checksum is not re-derived here. The Library's supplied 972-pass, review,
hosted and publication verification are reused at their recorded subjects; that suite was not re-run. App's root
`LICENSE.md` is byte-identical to the c35 Library license (SHA256
`495c4cd17baafde07be4c358bd47237f259bb2e01914e94114efc97d7fa721da`)
and covers the retained source fixture.

## Partial test-source fixture

`source/` holds 11 exact files from the commit, at their Library paths. Each
was read in full. `MANIFEST.json` lists path, Git mode and blob, sha256, byte
count, whether the bytes equal 2.0.0, and the consumer use. The closure is what
the App harness executes and nothing more:

- `agents/registry.json` and the five `agents/AGENT_*.md` files it names. The
  unchanged validator requires the complete registered roster; the resolver
  fingerprints the selected role's instruction. The four original role files are
  byte-identical to 2.0.0.
- `tools/validation/validate_agent_instructions.py`: registry/role validator.
- `tools/validation/build_workflow_index.py`: execution-companion parser and role
  sets. It needs PyYAML, an existing repository-check dependency.
- `tools/validation/validate_workflow_metadata.py`: per-workflow metadata
  validator; imports the builder by bare name.
- `tools/validation/fixtures/method_discovery_v1.json`: unchanged discovery
  fixture; its role descriptors and execution cases drive App tests.
- `tools/workflow_runtime/resolve_workflow.py`: role/method resolver and write
  authority binding. Its `normalize_brief` import occurs only on the CLI
  `--brief` path, which the harness does not use, so that module is excluded.

This is a labelled test fixture, not a Library distribution, a copied Library
suite, a runtime dependency or packaged App product instructions. The catalog,
index, workflows and skills are not copied; constructed packages in the
harness are built in temporary directories. Ordinary tests read only these
files, never a sibling Library checkout, Git objects or the network.

Harness: `tools/validation/test_library_v2_1_operational_adoption.py`, run by
the governance harness repository checks.

To re-derive a file from a Library clone:

```sh
git -C <library-clone> cat-file blob c35b7bbc463f81c1fed566c744ea49d168d29eee:<path> | shasum -a 256
```

A later edition is received deliberately: a new directory and manifest, not
an in-place replacement of these bytes.
