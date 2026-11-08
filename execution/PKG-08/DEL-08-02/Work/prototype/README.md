# RTD definition checker

The runnable checker lives outside the deliverable's declarative source tree.
From the repository root, run:

```sh
python3 -B tools/deliverable_prototypes/DEL-08-02/prototype/check_rtd.py
```

The frozen EU-D1 inputs remain in `fixtures/EU-D1/`. The checker reads them,
the standing schema and the research context account schema without writing
them. Its constructed accounts establish no actual Domains input or witness.

The relocation and historical source identity are recorded in
[`../CODE_LOCATION.md`](../CODE_LOCATION.md). The `prototype/check_rtd.py`
references in the RTD-v0.2 account identify the original rehearsal location.
