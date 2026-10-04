# F — EU-F1: one replacement decision package, assembled and read, decision pending (RP-v0.2)

**This is a bounded prototype, not product code.** Owner O-F, run `APP-V4-DESIGN-PASS-4-20261003`. Design text: DEL-11-03 `Design/REPLACEMENT_PACKET.md` (RP-v0.2). Rulings: R23-32, R23-33, R23-36.

Two input sets:
- **IS-FX-RP1-1**: fixture `FX-RP1`, key `EU-F1.answer-key.json`. Frozen under RP-v0.1 and read by the isolated reader RR-EUF1 (`../RR-EUF1/`). Kept unchanged as history. It is no longer regenerable or stageable after the RP-v0.2 repair: its legend schema changed, and `stage_is.py` detects that by hash.
- **IS-FX-RP1-2**: fixture `FX-RP1-2`, key `EU-F1-2.answer-key.json`, `READER_BRIEF.v2.md`, `rp.reader-account.v2.schema.json`. Built and keyed under RP-v0.2, before any reader.

Every supplier input is an illustrative schema example. No candidate exists. Nothing is presented to the owner, and no owner act is requested or implied. The prototype uses no network. It reads the repository; `git` is used read-only, only for the thesis tree at a fixed commit. It writes only `fixtures/FX-RP1/`, and `stage_is.py` writes into the folder you give it.

| File | What it is |
|---|---|
| `rplib.py` | Rules RP-R1…RP-R8 (REPLACEMENT_PACKET.md §4–§6) |
| `build_fx_rp1.py` | Writes fixture FX-RP1-2 deterministically (with `terms` and `packet/basis-excerpts.md`) from SQ-EX-05, DOS-EXAMPLE-INVENTED, the LHQ CIR example, REFERENCES §2, the thesis tree at `d2929fd62b`, and first-cut continuity and practitioner inputs |
| `fixtures/FX-RP1/` | Package file, packet manifest, disposition (`not_presented`), five supplied items, `MANIFEST.sha256` |
| `check_rp.py` | Part A (A-1…A-17): fixture FX-RP1-2 (integrity, schemas, copies equal sources, recomputation, thesis identity, terms, excerpts, receipts, points of need, evidence before status). Part B: 40 rule cases, positive and negative |
| `READER_BRIEF.md`, `rp.reader-account.schema.json` | What the isolated reader is given and must return |
| `IS-FX-RP1-1.input-set.sha256` | The exact input set for the reader: the fixture, the brief, the account schema, and the two RP schemas as a legend |
| `stage_is.py` | `python3 -B stage_is.py [--set 2] <empty folder>` copies exactly that input set and verifies every hash. The answer key is never staged |
| `EU-F1.answer-key.json` | **Withheld from the reader.** Frozen before any reader runs |
| `compare_rp.py` | `[--set 2] --self-check` (the key agrees with the fixture records), or `<account.json>` (the examiner comparison) |

```text
python3 -B build_fx_rp1.py     # same bytes on every run
python3 -B check_rp.py         # 57/57 at refreeze
python3 -B compare_rp.py --set 2 --self-check
python3 -B compare_rp.py ../RR-EUF1/account.json   # set 1: RR-EUF1 against the frozen key
```

Needs Python 3 and `jsonschema` (4.26.0 here).
