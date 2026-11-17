# J1's input: an invented packing list

The input set for the counted J1 ("The counted J1", in `../README.md`): one
invented deliverable folder for the bundled `content-digest` workflow to read.
Authored for the App's examination in this repository, by an agent, from
nothing but this purpose. It describes no real project, site, person or
organisation, and no file in it is a copy of anything else. It is not a frozen
preparation fixture of `../../fixtures/` and is not listed by
`../../sources.terms-v1.json`.

`brief-note.txt` is a short UTF-8 brief, the file the operator selects as the
run's file input (J1-4). `execution/PKG-001/DEL-001-01_Packing-List/` holds `_CONTEXT.md`, the four
legacy documents (`Datasheet.md`, `Specification.md`, `Guidance.md`,
`Procedure.md`), `_REFERENCES.md` and the deliverable's `deliverable.yaml`,
kept here as `deliverable.yaml.in` and renamed when it is staged: this
repository's own deliverables tool reads every file named `deliverable.yaml`
in the checkout as one of the project's deliverables. Two things in it are
absent on purpose, and a useful digest reports each as absent rather than
inventing it:

- `_SEMANTIC.md`, which the workflow's read boundary lists;
- the carrier's crate guide, which `_REFERENCES.md` cites as not supplied.

It also carries what the workflow's quality observations look for: a TBD with
its resolution authority, an ASSUMPTION with its rationale, a placeholder
section, a conflict whose ruling is pending, an unknown need source, and an
outward obligation.

## Staging it (preparation outside the App's controls)

The examiner, not the operator, copies it into the kept folder's `project/`
before the phase that supplies inputs, makes the output's parent folder, which
the workflow requires to exist and never creates, and records the digest of
every staged file:

```sh
cp -R app/examination/standalone/operated/j1-content-digest/execution <kept folder>/project/
cp app/examination/standalone/operated/j1-content-digest/brief-note.txt <kept folder>/project/
mv <kept folder>/project/execution/PKG-001/DEL-001-01_Packing-List/deliverable.yaml.in \
   <kept folder>/project/execution/PKG-001/DEL-001-01_Packing-List/deliverable.yaml
mkdir -p <kept folder>/project/execution/_Evaluation/content-digests/PKG-001
( cd <kept folder>/project && find execution brief-note.txt -type f -print0 | sort -z | xargs -0 shasum -a 256 ) \
  > <evidence folder>/j1-staged.sha256
```

The step's record names this as preparation outside the controls, with the
revision of this repository the files were copied from. Nothing else is put in
the project. The run's inputs, as the workflow's contract names them, are then
`DELIVERABLE_PATH` = `<kept folder>/project/execution/PKG-001/DEL-001-01_Packing-List`
and `OUTPUT_PATH` =
`<kept folder>/project/execution/_Evaluation/content-digests/PKG-001/DEL-001-01.md`;
they are supplied through the App's controls, not by this staging.

For J1-4's second part the examiner, after the operator has selected
`brief-note.txt` and before it sends, appends one line to it (preparation
outside the controls, recorded with the time and the file's digest after the
change); the App is expected to hold that send and send nothing. The examiner
then copies the file back from this folder, checks its digest against
`j1-staged.sha256`, and the operator selects it again.

After the run, an independent observation outside the controls compares the
staged files with `j1-staged.sha256` (the workflow modifies none of them) and
reads the one file written at `OUTPUT_PATH`.
