# Recordings at Codex 0.167.0

`st5`, `st5-race` and `nv04`, recorded on 2026-11-12 from the stock Codex 0.167.0
App Server by `supplier_checks/capture.py` with its scripted loopback provider.
Each was made once and is not regenerated; identifiers and times are those of
its run. A recording qualifies nothing.

What a reader of these files must not take for the supplier's behaviour:

- **The order of `nv04`'s notifications in generation 1, supplier positions 22
  to 28, is one of several the supplier produces.** The parent's and the
  child's threads emit concurrently there. Six healthy runs were made; five of
  them ordered those seven frames differently from the file kept here. This
  file was chosen among the six because its sequence of frames equals that of
  the recording it replaced, so that readers by position were not disturbed.
  Find a frame by its method and thread, not by its position; a test that
  relies on this order tests the choice of file, not the supplier.
- **`st5-race` records whichever way a race falls.** The answer is written and
  the process group killed at once. In this file `serverRequest/resolved`
  arrived before the kill, as it did in all six runs made that day on a loaded
  host. In the recording this file replaced (commit e491f9ed of this
  repository) and at 0.160.0 it did not arrive. Both outcomes are observed at
  0.167.0. `st5` freezes the process group before the answer is written, so
  there no acknowledgment can exist, and none does.
- **Rollout file names are in UTC** because the capture gives the supplier
  `TZ=UTC`. The App starts Codex with the person's own environment.
