# F — EU-F1: one replacement decision package, assembled and read, decision pending (RP-v0.3)

**This is a bounded prototype, not product code.** Owner O-F, run `APP-V4-DESIGN-PASS-4-20261003`. Design text: DEL-11-03 `Design/REPLACEMENT_PACKET.md` (RP-v0.3). Rulings: R23-32, R23-33, R23-36, R23-41, R23-43, R23-44.

Every supplier input is an illustrative schema example. No candidate exists. Nothing is presented to the owner, and no owner act is requested or implied. The prototype uses no network. It reads the repository; `git` is used read-only, only for the thesis tree at a fixed commit.

Three input sets; each is kept as history once a reader has read it:

| Set | Fixture | Key | Brief / account schema | Read by | State |
|---|---|---|---|---|---|
| IS-FX-RP1-1 | `FX-RP1` (RP-v0.1) | `EU-F1.answer-key.json` | `READER_BRIEF.md`, `rp.reader-account.schema.json` | RR-EUF1 (33/33) | History; cannot be restaged (its legend referenced live Design files) |
| IS-FX-RP1-2 | `FX-RP1-2` (RP-v0.2) | `EU-F1-2.answer-key.json` | `….v2…` | RR-EUF2 (33/33) | History; cannot be restaged, same reason |
| IS-FX-RP1-3 | `FX-RP1-3` (RP-v0.3) | `EU-F1-3.answer-key.json` (withheld) | `….v3…` (Q-1…Q-13) | — | Current; the legend is inside the fixture |

`EU-F1.key-grounding.md` marks which key answers rest on supplier records, packet rules, O-F's own text, or O-F's first-cut inputs (RV3 EUF1-R3).

| File | What it is |
|---|---|
| `vendor/` + `VENDOR.json` | R23-44: exact supplier schemas and examples this unit relies on, with source path, sha256 and source commit |
| `rplib.py` | Rules RP-R1…RP-R8 (REPLACEMENT_PACKET.md §4–§6) |
| `build_fx_rp1.py` | Writes `fixtures/FX-RP1-3/` deterministically: package, packet manifest with `terms`, basis excerpts, disposition, supplier copies, first cuts, legend |
| `check_rp.py [--fixture NAME]` | Part A (A-1…A-19) on the named fixture (default FX-RP1-3); V-1 vendoring, plus a NOTICE if a live supplier file has moved; Part B (B-1…B-44) rule cases |
| `stage_is.py [--set N] <empty folder>` / `--write-list` | Stage an input set exactly and verify every hash; the key is never staged |
| `compare_rp.py [--set N] --self-check` or `<account.json>` | Key against fixture; or the examiner comparison, with each set's own account schema |

```text
python3 -B build_fx_rp1.py                    # same bytes on every run
python3 -B check_rp.py                        # 65/65 at the RP-v0.3 freeze
python3 -B check_rp.py --fixture FX-RP1-2     # which current checks the RP-v0.2 fixture fails
python3 -B compare_rp.py --set 3 --self-check
python3 -B compare_rp.py --set 2 ../RR-EUF2/account.json
```

Needs Python 3 and `jsonschema` (4.26.0 here).
