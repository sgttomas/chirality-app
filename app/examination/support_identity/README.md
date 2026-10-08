# Proposed EXP support identity bindings v1

This offline tool checks a frozen technical selection of EXP result, review,
change-impact and PKG records against complete EXP §4.4 identity: version,
three schema IDs and prototype SHA-256. It preserves existing record bytes and
schemas. CI-26 canonical publication and consumer adoption remain unresolved.
A passing report establishes supplied file consistency only.

`declaration.v1.json` freezes exact accepted source, rule and existing checker
bytes at the recorded repository basis. The checker pins its exact digest and
that of `binding.v1.schema.json`; neither is a caller-selectable argument.
It independently compares the declared schema IDs/version and prototype hash
with the pinned sources. Any source drift requires a reviewed successor;
changing a record or passing a new source manifest cannot republish support.
The declaration's `frozen_candidate_not_published` standing is mandatory.
EXP §4.4 publication remains the deliverable's freeze/merge, not a writer act.
Merging this proposed tooling does not adopt it as the canonical contract.

## Use offline

Use the same installed Python and `jsonschema` environment as the existing
examination checkers. Nothing is downloaded or launched natively.

```sh
python3 -B app/examination/support_identity/support_identity.py bind review review.json
python3 -B app/examination/support_identity/support_identity.py check selection.json \
  --selection-sha256 <previously-frozen-64-character-sha256>
```

`bind` emits an unpublished sidecar to standard output. It checks basic record
identity but makes no validity/pass claim. Save that output beside the exact
original record. Do not rewrite the original to add sidecar fields.
The complete `check` command requires all six record roles: `before`, `after`,
`rerun`, `review`, `change`, `package`. Before/after describe the same prior result
before and after its currency update; the package belongs to the rerun.
Historical package bytes, unselected evidence and omitted changes are outside
this bounded selection.

A `selection.json` object has exactly these fields:

| Field | Value |
| --- | --- |
| `format` | `exp-support-selection.v1` |
| `standing` | `frozen_candidate_not_published` |
| `declaration_sha256` | SHA-256 of the shipped declaration |
| `artifacts` | The six roles above, each with `record` and `binding` references |
| `package_selection` | Existing checker inputs `revision`, `build`, `pin`, `package_ref` |
| `review_selection` | Existing admission checker's complete review selection object |
| `change_selection` | Existing admission checker's complete change selection object |

Each reference is exactly `{ "path": "relative-file.json", "sha256": "…" }`.
Paths are relative to the selection's directory. Absolute paths, traversal,
duplicate paths, observed symlinks and nonregular files are refused. References
and sidecars bind exact original bytes, including whitespace. JSON duplicate
keys and nonfinite numbers are refused. Missing sidecars never fall back to a
legacy pass. Existing legacy tools remain independently usable unchanged.
The caller must freeze the selection's exact digest separately before checking;
this detects later selection changes and is not an authority credential.

Each sidecar binds a record kind/ID/digest, the full support identity and the
fixed declaration digest. The result's existing optional prototype field is
required on this stronger joined route. Review/change/PKG get their full identity
through the sidecar. No `published`, approval or override flag is accepted.

The checker captures the fixed sources and artifacts, then calls the unchanged
existing package-link, review-join and change-join commands from a temporary
project containing those exact bytes. Their results, rules and lock hashes are
preserved in `existing_checks`; transient input paths are omitted in favor of
the original immutable references. Review evidence and change affectedness must
resolve within this bounded pair. Unknown extra references fail this complete
join, while the original legacy checkers retain their narrower reporting.

Exit 0 means this supplied identity/relationship check passed; exit 1 means an
existing joined check failed; exit 2 means malformed, missing or mismatched
inputs/sources or a checker execution error. A pass can retain package
prerequisite gaps. Every check report sets publication, adoption and
qualification to false. The report cannot prove actual review independence,
observations, repair, signing, a native run or a human act.

This is a local offline file-consistency tool. Link checks are best effort,
not hostile concurrent filesystem isolation. Captured byte hashes do not
establish authenticated custody or immutability of the external filesystem.
The tool executes maintained Python checkers, never canonical prototypes or a
supplier binary. Temporary snapshots are removed after execution.

## Maintained verification

```sh
python3 -B -m unittest discover -s app/tests -p 'group_b_support_identity_test.py' -v
```

The suite composes maintained invented fixtures and exercises complete joins,
false source/record/sidecar digests, mixed versions, missing schema IDs,
publication impersonation, unresolved evidence, candidate/package differences,
review actor mismatch, history preservation and fixed-selection drift.
Tests have no dependency on dated run evidence.
