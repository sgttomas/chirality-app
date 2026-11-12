# data-app-build: briefs for the builder and the suite author

A dispatched agent knows only its brief. State every field in full. Refer only to
files in the closure, this workflow's resources and host facts.

## Builder brief

| Field | Content |
|---|---|
| `Purpose` | Build the application in `<coverage>` for target `<target>` |
| `Role` | TASK; does not delegate |
| `Basis` | `appspec.json` and `appspec.lock` paths and SHA-256; the builder input contract version; the capability manifest path and SHA-256; the frozen suite path and `SUITE_MANIFEST.csv` SHA-256 |
| `Reads` | Only the closure, the contract, the capability manifest and the suite. Not the design record, reference apps or working notes |
| `Must not` | Edit the suite or the specification; re-implement a bound component; fetch at build time; make semantic choices the specification does not make; write code whose only purpose is to satisfy a test (report a suspected suite defect instead); publish or deploy anything |
| `On ambiguity` | Stop that element; report its path, the question and the options seen |
| `Write boundary` | `BUILD_ROOT/app/` and `BUILD_ROOT/ELEMENT_MAP.csv` |
| `Execution` | The permitted environment; commands that may run; no network except the package mirrors the capability manifest names; check for live test or app processes before each run, and stop those you start; the build tree hash method (contract) |
| `Return` | Build tree hash; element map; suite results; specification findings; presentation defaults applied; commands run |

## Suite author brief

| Field | Content |
|---|---|
| `Purpose` | Generate the conformance suite for `<coverage>` from the specification |
| `Role` | TASK; does not build and does not see the build |
| `Basis` | `appspec.json` and `appspec.lock` paths and SHA-256; the test kinds in method §2 |
| `Rules` | <ul><li>Derive every expected value from the specification or the closure's fixtures.</li><li>Record a specification finding where the specification is silent.</li><li>Seed generated fixtures and record the seed.</li><li>Run UI tests at the specification's viewport sizes, with visibility checks for declared content.</li><li>Add a shuffled-input test where order affects a result.</li><li>Record the mutation runs that show discriminating power.</li></ul> |
| `Write boundary` | `BUILD_ROOT/suite/` |
| `Return` | `SUITE_MANIFEST.csv` and its SHA-256, for examination before freezing; tests by kind and element; specification findings |
