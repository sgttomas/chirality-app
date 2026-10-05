# DEL-01-03 prototype (NPTD-v0.3; CC-NPT-GEN)

Prototype only: not product code, not an App candidate, not an observation of
Codex. Python 3 standard library; no package installed; no network; the Codex
binary is not run.

| File | What it is |
|---|---|
| `npt_model.py` | Executable model of the rules in `../NATIVE_PLANS_TOOLS_DELEGATION.md`: plan revisions (RV-1…RV-6), tool rows (§6), goals (§6.4), descendants and availability (§7), run boundaries (§5.7), version line (§8), experimental surfaces (§4), truthful actor (§9). Its four transition tables must equal §13's |
| `scenarios.py` | Constructed native scenarios (fixture standing `constructed`, HOSTING §9.2): invented identities and material |
| `run_cases.py` | Cases PC-01…PC-22; writes `fixtures/native/*.jsonl` (deterministic) |
| `jsonschema_subset.py` | Byte-identical copy of DEL-01-01's validator (`DEL-01-01/Design/prototype/jsonschema_subset.py`, sha256 486e9286e5aa56888b5473f1c08493a115591255685a8a7bb88b93ff2cacffc0) |
| `fixtures/*.{valid,invalid}.json` | One valid and one invalid instance for each PROPOSED schema beside the Design file, as `{description, instance}` |
| `results/RUN_2026-10-02.txt` | Output of the v0.2 run recorded in the Design file (`RUN_2026-10-01.txt` is the v0.1 run, kept) |

Run: `python3 run_cases.py` in this folder. It reads, never writes, the
committed 0.158.0 bundle at
`../../../DEL-01-01_Stock Codex hosting and supplier contract/Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json`.

A passing case shows that the Design file's rules run as written against
constructed frames. It passes no VER criterion, and the constructed frames
say nothing about how Codex behaves: that is for recorded captures (HOSTING
§9.1) and OBS-2.

Values the Design file leaves open are marked TEST VALUE in the code: the
content-identity method (HOSTING U-08). The Codex feature names of round 1's
TEST VALUE are no longer used (R18-1 C-05: only plan mode is labelled
experimental; delegation availability is read at run time, C-04).


CC-NPT-GEN (2026-10-04) adopts full `{appSession, home, spawnCounter}` on
all lifecycle/frame inputs and checklist references; internal generation maps
use the complete immutable tuple. Scenario constructors accept a spawn counter
to construct this object, never a legacy scalar event/schema union. Each view
binds one session/home; every history response is delivered with source-home
context beside the native response, and missing/foreign context is refused.
Plan-item references retain native identities with no generation/receipt fields.
Their standalone references still need the receiving home context; see RV-2c.

Opaque revision key v2 uses lossless base64url UTF-8 components separated by
`.`; original native fields remain untouched. Shape schemas are successor
resources (plan-revision v0.2; item-anchor v0.3), and
`reference_identity_matches` checks key/component correspondence. The content
identity TEST VALUE is unchanged. Native item indexing includes the turn ID.

PC-19…PC-22 exercise sessions/homes sharing counters, native IDs and receipt
positions, Unicode/delimiters, caller mutation, closed/stale/foreign inputs,
receipt order, restart and same-home relaunch, wrong-home history refusal and
schema/key mismatch negatives. Current output is
`results/RUN_2026-10-04_CC-NPT-GEN.txt`. Historical results stay unchanged.
PC-22 additionally reads the actual reviewed 0.160.0 experimental v2 bundle
and validates 71 constructed frames/read shapes. The model's 0.158.0 constants
and existing PC-01 root are retained historical demonstration, not the current
product supplier; no live Codex run, network or qualification is claimed.
