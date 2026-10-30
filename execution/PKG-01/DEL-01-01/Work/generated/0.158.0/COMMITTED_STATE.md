# Committed state of `generated/0.158.0/`

Recorded by HELP_HUMAN on 2026-09-28 (run APP-V4-FIRST-INCREMENT-20260928, IR1-C finding IR1C-04).

`MANIFEST.sha256` is left byte-unchanged (sha256 `42b95826…`, cited by the spike
record and HOSTING_BOUNDARY). It is the complete record of what the W11 spike
generated. Its `# COMMITTED` comment describes the spike's proposed commit form.
The parent then re-selected a smaller form (PIN_SPIKE_0.158.0.md §4), so that
comment is superseded as follows.

- **Committed:** `json-schema/experimental/codex_app_server_protocol.schemas.json`,
  `json-schema/experimental/codex_app_server_protocol.v2.schemas.json`,
  `MANIFEST.sha256`, `_spike/` and this note (about 1.9 MB).
- **Not committed:** both `ts/` trees (1,605 files), and every other JSON Schema
  file (752). All of them are regenerable with `_spike/generate.sh` at the pin.

Checks run by the parent:

| Check | Command | Result |
|---|---|---|
| Committed tree against manifest | `grep -v '^#' MANIFEST.sha256 \| shasum -a 256 -c` in this folder | 2 OK; 2,357 missing (not committed); 0 mismatched |
| Moved-out TS output against manifest | `grep '  ts/' MANIFEST.sha256 \| shasum -a 256 -c` over the spike's TS output kept in the session scratchpad | 1,605 OK; 0 mismatched |

The scratchpad copy is temporary. After it is deleted, TS verification
requires regeneration.
