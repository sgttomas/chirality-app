# DEL-01-05 prototype — access model, custody scan, link dry run, schema checks

**This is a design prototype, not product code.** It belongs to
DEL-01-05/ACCESS-v0.1 (`../ACCOUNT_AND_PROVIDER_ACCESS.md` §16) and was written
by node D4 of run `APP-V4-DESIGN-PASS-3-20261001` under R17-1 and R12-3.
Python 3 standard library only; nothing is installed; no network is used; no
Codex process or model is started; no sign-in, key or token exists anywhere
in it. Every value is invented. The custody canaries are deliberately not
shaped like any real key, token, URL or code.

| File | Role |
|---|---|
| `access_model.py` | The §5 transition tables (AE, KE, LE, CS, CL), a table-driven machine that refuses unlisted moves, the K-3 selection and K2-1 routing model, the CR-1…CR-10 recorder, the configuration-link dry run, and the K-12 network-view merge |
| `run_cases.py` | Runs VC-A11…VC-A17 of the design file and prints one line per case; exit 0 when all are as expected |
| `jsonschema_subset.py` | Byte-identical copy of DEL-01-01's validator (`DEL-01-01/Design/prototype/jsonschema_subset.py`, sha256 486e9286e5aa56888b5473f1c08493a115591255685a8a7bb88b93ff2cacffc0) |
| `fixtures/` | A valid and an invalid instance for each PROPOSED schema beside the design file (`../access.*.schema.json`); each file holds a `description` and the `instance` |
| `results/RUN_2026-10-01.txt` | The recorded run, with the sha256 of every input |

## How to run

```sh
cd "<this folder>"
PYTHONDONTWRITEBYTECODE=1 python3 run_cases.py
```

VC-A11 creates a temporary folder under `$TMPDIR` (prefix
`chirality-d4-link-`), works only inside it, checks that nothing under
`~/.codex` was touched, and removes it. A "pass (model)" means the rules ran
as written; it is never a VER pass.
