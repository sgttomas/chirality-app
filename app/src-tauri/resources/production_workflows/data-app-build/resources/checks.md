# data-app-build: checks before the checkpoint

1. **Admission.** Every closure hash matched, the buildable-profile validation passed,
   and every element in the coverage is in the capability manifest; or the refusal is
   the result.
2. **Suite independence.**
   - The suite was generated from the specification by a contributor other than the
     builder.
   - A separate agent examined it before it was frozen.
   - Its manifest hash is unchanged, or each new version is recorded with the
     examiner's agreement and all results were re-run.
3. **Coverage.**
   - Every element in the coverage is in `ELEMENT_MAP.csv` with at least one test.
   - Unmapped code is listed as a finding.
4. **Conformance.**
   - The whole suite passed on the build tree whose hash is in the manifest.
   - The integration owner's own re-run produced `conformance.txt`.
   - The tree hash was recomputed by the contract's method.
   - No test or expected value changed during the build, except through a recorded
     suite version (item 2).
   - UI tests ran at the specification's viewport sizes.
   - The build contains no code whose only purpose is to satisfy a test.
5. **Components.** Each bound component is called through its bundle's entry point, at
   the pinned version.
6. **Disclosures.** Non-uses, caveats, data vintage and acceptance status appear as
   declared. Acceptance is shown only as recorded.
7. **Examination.**
   - A separate agent examined the build against the closure.
   - Its findings are repaired and backchecked, or presented unresolved.
8. **Specification findings.** Every ambiguity met in the build is reported for data-app-spec
   `revise`, with the element path. None was settled inside the build.
9. **No external effects.** Nothing was published, deployed or written outside
   `BUILD_ROOT`.

## Failure reporting

| Status | Use when |
|---|---|
| `REFUSED` | An admission precondition failed; the report names each element and rule |
| `SPEC_FINDINGS` | The build stopped at elements whose specification is ambiguous or defective |
| `NONCONFORMING` | Tests still fail after repair within authority |
| `READY_FOR_ACCEPTANCE` | All checks above pass; the owner decides |
