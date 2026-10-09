# DEL-03-01 prototype — SH-1, the simulated host, and the schema checks

**Not product code.** A local prototype under R12-3 (run
APP-V4-DESIGN-PASS-2-20260930, node B3): Python 3 standard library only, no
package installed, no network. It shows that the PROPOSED formats of C-v0.8,
P-v0.8 and ADAPTER-v0.6 can be produced, parsed and checked, and it is the
one simulated host (test double) those files, and XT, cite (R12-4; C-v0.8
§10.8). Nothing it does is host evidence: its results carry the evidence label
*test-double* (C-v0.8 evidence-label mapping) and establish nothing about
SWBPIPE or any other host.

| File | What it shows |
|---|---|
| `simhost.py` | **SH-1**, the simulated host (C §10.8). One host state (a state file) reached by **both** native paths: the MCP-tool path (`mcp`: newline-delimited JSON-RPC 2.0 on stdio, `initialize`, `tools/list`, `tools/call`) and the command-line path (`cli`: one JSON host document on stdout, exit status 0 whenever a host document was produced). The person's acts and the host's own steps are separate controls (`person`, `host`) that no agent path reaches |
| `run_fixture.py` | Plays the App's Codex over both paths through the FX-PIPE-01 steps listed in C §10.8, records items shaped like the supplier's `mcpToolCall` / `commandExecution` thread items (an imitation of field names observed in generated types at pin 0.158.0, not an observation of Codex), prints the M3-CP basis comparison (C VC-C-04; P §11) and one PASS/FAIL line per check |
| `schema_subset.py` | A small JSON Schema 2020-12 validator for the keyword subset listed in its docstring. A schema that uses any other keyword is reported, so the subset claim is checked, not assumed |
| `validate_all.py` | Validates the eight PKG-03 schemas (three here, two in DEL-03-02, three in DEL-03-03), their valid and invalid example instances, and, with `--run`, every host document and change request of an SH-1 run. Since the RP-2 repair it also applies conformance rule CX-1 (C §3.5: a *from argument* declaration names an argument of its entry), which a JSON Schema cannot state, and the three catalog mutations of V18-3 R-7, each of which must be rejected |

Names. Property names in the documents are the PROPOSED Chirality semantic
labels of the schemas. The double's tool names (the fixture labels OP-C…),
its command words, its `_meta` key `sh1/catalog` and its identity method
`m-sh1` (a truncated sha256 over sorted JSON) are the double's own labels.
None of them selects a host wire field, a transport, or a hash or
canonicalization algorithm (C TBD-003; ADAPTER TBD-007).

## Run

```sh
cd "<this folder>"
python3 run_fixture.py --out "$TMPDIR/b3-sh1-run"
python3 validate_all.py --run "$TMPDIR/b3-sh1-run"
# then, from the sibling prototypes:
python3 "../../../DEL-03-03_Local external-agent receiving adapter/Design/prototype/observe_map.py" --run "$TMPDIR/b3-sh1-run"
python3 "../../../DEL-03-02_Proposal, validation and outcome contract/Design/prototype/proposal_states.py" --check "$TMPDIR/b3-sh1-run"
```

The observed output of the run of 2026-09-30 is recorded in
`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-2-20260930/WAVE_B/B3.md`, and that of
the RP-2 repair rerun (same date; 22 checks, R13-1 replacing the R12-9
options, explicit item-left events and capture times on the double's
recorded states) in `WAVE_B/RP-2.md`.

## Limits

- SH-1 holds a small part of FX-PIPE-01 (OP-C1…OP-C9, OP-C12; runs, supports,
  LC-1). OP-C10 (undo), OP-C11 and the checkpoint declarations are not
  implemented; checkpoint cases are exercised only as the observations the
  adapter passes on.
- The lost acknowledgement is injected by the driver (it discards a response
  the host sent); an endpoint stop is a host control. No timing, concurrency
  or restart of the double's state is simulated.
- R13-1 is printed as the one ruled rule (B3's option B); the run steps
  keep their B3 labels `R12-9-a` and `R12-9-b`.
- The Codex side is imitated, not run. What Codex actually reports for these
  items is OBS-1's (after round 2), not this prototype's.
