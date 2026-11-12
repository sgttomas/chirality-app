# Recordings at Codex 0.167.0

`st5` and `nv04`: exchanges recorded on 2026-11-12 from the stock Codex 0.167.0
App Server, with a scripted loopback provider standing in for a model. They are
evidence, kept as files. Each was made once; identifiers and times are those of
its run. A recording qualifies nothing.

## How they were made

By the capture harness as it stood at commit 696f8170 of this repository
(`app/supplier_checks/capture.py` and `stub_provider.py` at that commit), run
against the complete 0.167.0 vendor tree after it was compared with
`app/src-tauri/resources/supplier/0.167.0/CANONICAL_DISTRIBUTION.json`. The
harness is not in the maintained tree and is not maintained. Its refusals are
not relied on: four independent reviews each found a way for it to write a
recording after an observation had failed or had not finished, and it was taken
out instead of being repaired a fifth time.

## What these files establish, and what they do not

Checked from the files themselves by `supplier_checks/test_recordings.py`: every
frame is a JSON object; positions count without a gap in each generation and
direction; every request each script requires was answered with a result; the
recording names the pin, the supplier binary and the distribution record; and
the facts each scenario is kept for (below).

Not established by these files: what the supplier sent after the last required
reply of a generation, and whether a provider request arrived while the stub
provider was closing. The harness could lose either without saying so. The
socket sample each file reports is what was sampled, every 0.25 s; it is not
network isolation.

## What a reader must not take for the supplier's behaviour

- **The order of `nv04`'s notifications in generation 1, supplier positions 22
  to 28, is one of several the supplier produces.** The parent's and the
  child's threads emit concurrently there. Six healthy runs were made; five of
  them ordered those seven frames differently from the file kept here. This
  file was chosen among the six because its sequence of frames equals that of
  the recording it replaced, so that readers by position were not disturbed.
  Find a frame by its method and thread, not by its position; a test that
  relies on this order tests the choice of file, not the supplier.
- **Rollout file names are in UTC** because the harness gave the supplier
  `TZ=UTC`. The App starts Codex with the person's own environment.

## What each is kept for

- `st5`: the supplier raises a command approval; the process group is frozen
  before the answer is written and killed while frozen, so no acknowledgment
  can exist, and none does; after a restart and resume nothing is re-raised.
- `nv04`: a parent turn spawns one sub-agent and ends before the child does.
  The spawn item carries its prompt, sender and receiver live and on every
  history read of the parent (`thread/read`, `thread/turns/list`,
  `thread/items/list`), before and after a restart; the child's read names its
  parent.

A third scenario, `st5-race` (the answer written and the group killed at once),
is not kept: its outcome is a race, not a property of the supplier, and no test
reads it. Both outcomes were observed at 0.167.0 on that day: the acknowledgment
arrived before the kill in six runs on a loaded host and did not in an earlier
one. The earlier file is in this repository's history at commit e491f9ed and
the later at 696f8170.
