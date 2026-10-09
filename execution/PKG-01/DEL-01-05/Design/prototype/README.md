# DEL-01-05 prototype — access model, custody scan, link dry run, schema checks

**This is a design prototype, not product code.** It belongs to
DEL-01-05/ACCESS-v0.2 (`../ACCOUNT_AND_PROVIDER_ACCESS.md` §16) and was written
by node D4 of run `APP-V4-DESIGN-PASS-3-20261001` under R17-1 and R12-3
(round 1, 2026-10-01; round 2, 2026-10-02). Supplier facts are at Codex 0.158.0.
Python 3 standard library only; nothing is installed; no network is used; no
Codex process or model is started; no sign-in, key or token exists anywhere
in it. Every value is invented. The custody canaries are deliberately not
shaped like any real key, token, URL or code.

| File | Role |
|---|---|
| `access_model.py` | The §5 transition tables (AE, KE, LE, CS, CL), a table-driven machine that refuses unlisted moves, the K-3 selection and K2-1 routing model, the CR-1…CR-10 recorder, the configuration, `AGENTS.md` and `skills/` link dry run (R18-6), the session flags and child environment (L-3, R18-3), and the K-12 network-view merge following the person's plugin setting |
| `run_cases.py` | Runs VC-A11…VC-A17, VC-A19 and VC-A20 of the design file and prints one line per case; exit 0 when all are as expected |
| `jsonschema_subset.py` | Byte-identical copy of DEL-01-01's validator (`DEL-01-01/Design/prototype/jsonschema_subset.py`, sha256 486e9286e5aa56888b5473f1c08493a115591255685a8a7bb88b93ff2cacffc0) |
| `fixtures/` | A valid and an invalid instance for each PROPOSED schema beside the design file (`../access.*.schema.json`); each file holds a `description` and the `instance` |
| `results/RUN_2026-10-02.txt` | The recorded v0.2 run, with the sha256 of every input |
| `results/RUN_2026-10-01.txt` | The v0.1 run (history) |

## How to run

```sh
cd "<this folder>"
PYTHONDONTWRITEBYTECODE=1 python3 run_cases.py
```

VC-A11 creates a temporary folder under `$TMPDIR` (prefix
`chirality-d4-link-`), works only inside it, checks that nothing under
`~/.codex` was touched, and removes it. A "pass (model)" means the rules ran
as written; it is never a VER pass.

CC-H independent-review repair: each App instance creates a unique app_session
(UUID; explicit fixture injection available). state_snapshot exports that
session. network_view requires app_session from its owning App; no fixed
prototype session is invented by the network record exporter.

SUP1: this prototype remains a historical 0.158.0 record/type model. Its
constants and expected rows are not the maintained product development pin;
HOSTING §7.0/generated/0.160.0 supplies that pin. Historical observations are
not silently relabelled at the adopted version. New product qualification
and connected consumer replay remain manager/receiving-owner work.

CC-ACCESS-EXPLICIT-PROJECT-CONTEXT: `new_conversation(None)` models genuine
project absence, with explicit choice/normal model-home guards and no0.2
project-bearing record/per-project offer/save. `view()` is a derived live
caption, not a new durable format or trusted production Root source. Known
context is frozen and remains its original reference when Root changes. Run
`python3 -B check_explicit_project_context.py` for the bounded controls.
