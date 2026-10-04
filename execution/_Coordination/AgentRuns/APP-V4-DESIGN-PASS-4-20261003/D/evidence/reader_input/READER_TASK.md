# EU-D1 reader task

You are given only the files in this folder (see `MANIFEST.sha256`). Use
nothing else: no other repository file, no git history, no earlier
conversation. Every PEC and Domains input behind these records is
constructed for a rehearsal (`simulated: true`); the two work-graph files
under `sources/` are real.

`CONNECTOR_FALLBACK.md` §2 defines the standing vocabulary every record uses.

## The questions

- **Q1** (asked of PEC, records `records/PR-P1.json` … `PR-P6.json`; route
  account `records/RA-Q1.json`): for undertaking
  APP-V4-DESIGN-PASS-4-20261003 at revision e086dfff32, (a) which work-graph
  nodes are READY, ACTIVE or BLOCKED; (b) which other nodes are open (any
  state other than COMPLETE); (c) which nodes changed state or were added
  since revision e4a0c2c4c3?
- **QD** (asked of Domains, records `records/DR-DM-1.json`, `DR-DM-2.json`;
  route account `records/RA-QD.json`): which admitted source supports the
  statement "line EX-L1 support spacing is 3.0 m", and does that support
  hold for the source as it stands now?

## What to return

One JSON document, `ACCOUNT.json`, with one entry per case, in this form.
Write what you can conclude from the files and on what basis. Where you
cannot conclude something, say so; do not fill gaps.

```json
{
  "reader": "<your identity: model and session>",
  "cases": {
    "P1": {
      "standing": {"envelope": "...", "condition": "..."},
      "pec_claims_relied_on": ["claim ids you rely on, or none"],
      "answer": {
        "a": ["node and state, or empty"],
        "b": ["node and state, or empty"],
        "c": ["node: from -> to, or 'added as STATE'"]
      },
      "basis": {"a": "pec | files | both", "b": "...", "c": "..."},
      "cannot_conclude": ["each conclusion these files do not support, with why"],
      "notes": "optional"
    },
    "P2": {}, "P3": {}, "P4": {}, "P5": {}, "P6": {},
    "DM-1": {
      "standing": {"envelope": "...", "condition": "..."},
      "admitted_current_support_for_3_0_m": true,
      "what_the_source_states_now": "...",
      "cannot_conclude": ["..."]
    },
    "DM-2": {},
    "independence": "Does PEC's standing in a record change Domains' standing, or the reverse? Answer and say how you can tell."
  }
}
```

Also answer, for each PEC case, in `cannot_conclude` or `notes`: can you
conclude that no work remains, that any node is ready to start, or that
anything is permitted?
