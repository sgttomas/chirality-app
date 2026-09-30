# DEL-03-03 prototype — observation-to-record mapping on both native paths

**Not product code.** A local prototype under R12-3 (run
APP-V4-DESIGN-PASS-2-20260930, node B3): Python 3 standard library only; it
imports DEL-03-01's `schema_subset.py` by relative path.

`observe_map.py --run RUN` reads the items an SH-1 run recorded (C-v0.8
§10.8; DEL-03-01 `Design/prototype/run_fixture.py`) and applies ADAPTER-v0.6:

- **§4.6 OM-1…OM-10**: each `mcpToolCall`-shaped item (N-MCP) and each
  `commandExecution`-shaped item (N-CLI) becomes one external dispatch record
  (`external_dispatch_record.schema.json`), with the native reference, the
  catalog operation through the host-supplied mapping or *not established*,
  the transport facts, the outcome in C §4.1 / P §9 terms with its reporter,
  and the evidence limits;
- **§7.7 CO-1…CO-9**: the checkpoint observations passed to DEL-02-03
  (`checkpoint_observation.schema.json`), each naming the EXEC §4.4 event row
  it feeds;
- **§3.6 CT-1…CT-12**: the channel status after each channel event
  (`channel_status.schema.json`).

Every record is validated against its schema; `--write-examples` writes the
ADAPTER example instances beside the schemas.

The items are **imitations** of supplier item shapes (field names observed in
generated types at pin 0.158.0, ADAPTER §3.5), produced by the driver, not by
Codex. The mapping rules that need a live observation (what Codex really
reports, for example whether `aggregatedOutput` interleaves stderr) are marked
"OBS-1 pending" in ADAPTER §4.6; ADAPTER 7 (the live spike) is not part of
this prototype.

```sh
python3 observe_map.py --run "$TMPDIR/b3-sh1-run"
```

The observed output of the run of 2026-09-30 is recorded in `WAVE_B/B3.md`.
