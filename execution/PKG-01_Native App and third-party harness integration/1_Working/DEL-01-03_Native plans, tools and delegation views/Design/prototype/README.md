# DEL-01-03 prototype (NPTD-v0.1 §15.3)

Prototype only: not product code, not an App candidate, not an observation of
Codex. Python 3 standard library; no package installed; no network; the Codex
binary is not run.

| File | What it is |
|---|---|
| `npt_model.py` | Executable model of the rules in `../NATIVE_PLANS_TOOLS_DELEGATION.md`: plan revisions (RV-1…RV-6), tool rows (§6), descendants (§7), version line (§8), experimental surfaces (§4), truthful actor (§9). Its four transition tables must equal §13's |
| `scenarios.py` | Constructed native scenarios (fixture standing `constructed`, HOSTING §9.2): invented identities and material |
| `run_cases.py` | Cases PC-01…PC-15; writes `fixtures/native/*.jsonl` (deterministic) |
| `jsonschema_subset.py` | Byte-identical copy of DEL-01-01's validator (`DEL-01-01/Design/prototype/jsonschema_subset.py`, sha256 486e9286e5aa56888b5473f1c08493a115591255685a8a7bb88b93ff2cacffc0) |
| `fixtures/*.{valid,invalid}.json` | One valid and one invalid instance for each PROPOSED schema beside the Design file, as `{description, instance}` |
| `results/RUN_2026-10-01.txt` | Output of the run recorded in the Design file |

Run: `python3 run_cases.py` in this folder. It reads, never writes, the
committed 0.158.0 bundle at
`../../../DEL-01-01_Stock Codex hosting and supplier contract/Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json`.

A passing case shows that the Design file's rules run as written against
constructed frames. It passes no VER criterion, and the constructed frames
say nothing about how Codex behaves: that is for recorded captures (HOSTING
§9.1) and OBS-2.

Values the Design file leaves open are marked TEST VALUE in the code: the
content-identity method (HOSTING U-08) and the Codex feature names that gate
delegation and plan mode (OBS-2 pending; tests use a constructed name).
