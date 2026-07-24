# TOOL POLICY — scope-change-packet

## Tool Posture

Reasoning-first packet production. No deterministic helper is required to author a packet.

## Preferred Validation

After packet creation, run:

```sh
python3 tools/validation/validate_scope_change_packet.py <packet-folder>
```

Do not claim validator PASS unless it actually ran and passed.

## Disallowed Tool Effects

- No writes outside `PACKET_PATH` and `_run_records/`.
- No mutation of product deliverables.
- No mutation of `Dependencies.csv`.
- No mutation of `_ScopeChange/`, `_Reconciliation/`, or decomposition authority.

