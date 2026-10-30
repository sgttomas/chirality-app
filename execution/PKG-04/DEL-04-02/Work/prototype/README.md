# DEL-04-02 settings-in prototype (R12-3)

**This is a prototype, not product code.** It validates the PROPOSED
settings-in representation of AS-v0.8 §6 (`../AS_SETTINGS_IN.schema.json`)
against its example instances (`../AS_SETTINGS_IN.valid.examples.json`:
fixture ⟨set-1⟩, and ⟨set-2⟩ with a host agent's destination settings;
`../AS_SETTINGS_IN.invalid.examples.json`: four defects, INV-AS-4 added at
RP-4 for an always-off item shown on without an A12 reference). It also walks
the in-work destination-grant transitions of AS-v0.8 §3.1 as a small state
machine: eleven event sequences and nine forbidden transitions after RP-4
(DG-15 starts from no state and never passes through *requested*). It selects no
component placement (OI-014): AS-v0.8 §13 lists the options.

It uses the JSON Schema subset validator kept in DEL-04-03's prototype folder
(`minischema.py`; the subset is listed in that folder's README).

## Run

```text
cd "<this folder>"
python3 -B validate_settings_in.py
```

Python 3 standard library only (Python 3.13.7, macOS, 2026-09-30). The
output is recorded in `WAVE_B/B4.md` of run `APP-V4-DESIGN-PASS-2-20260930`.
The settings-in schema is also exercised through the RS record schema
(`settings_version` entries) by DEL-04-03's `run_prototype.py`.
