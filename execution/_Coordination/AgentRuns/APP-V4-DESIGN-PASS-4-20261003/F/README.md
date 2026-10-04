# F — EU-F1…EU-F3R, EU-F4: the replacement packet (RP-v0.6), the continuity account (CA-v0.3), the adoption account (AA-v0.2) and practitioner validation (PV-v0.2)

**This is a bounded prototype, not product code.** Owner O-F, run `APP-V4-DESIGN-PASS-4-20261003`. Design text: DEL-11-03 `Design/REPLACEMENT_PACKET.md` (RP-v0.6), DEL-11-01 `Design/CONTINUITY_ACCOUNT.md` (CA-v0.3, prototype in `ca/`), DEL-11-02 `Design/ADOPTION_ACCOUNT.md` (AA-v0.2, prototype in `aa/`) and DEL-09-12 `Design/PRACTITIONER_VALIDATION.md` (PV-v0.2, prototype in `pv/`). Every checker computes each claimed rule as a function and breaks it on the real record in memory; each Design file lists which claimed rules have such a negative case and which do not. Rulings: R23-32, R23-33, R23-36, R23-41, R23-43, R23-44.

Every supplier input is an illustrative schema example. No candidate exists. Nothing is presented to the owner, and no owner act is requested or implied. The prototype uses no network. It reads the repository; `git` is used read-only, only for the thesis tree at a fixed commit.

Three input sets; each is kept as history once a reader has read it:

| Set | Fixture | Key | Brief / account schema | Read by | State |
|---|---|---|---|---|---|
| IS-FX-RP1-1 | `FX-RP1` (RP-v0.1) | `EU-F1.answer-key.json` | `READER_BRIEF.md`, `rp.reader-account.schema.json` | RR-EUF1 (33/33) | History; cannot be restaged (its legend referenced live Design files) |
| IS-FX-RP1-2 | `FX-RP1-2` (RP-v0.2) | `EU-F1-2.answer-key.json` | `….v2…` | RR-EUF2 (33/33) | History; cannot be restaged, same reason |
| IS-FX-RP1-3 | `FX-RP1-3` (RP-v0.3) | `EU-F1-3.answer-key.json` | `….v3…` (Q-1…Q-13) | RR-EUF3 (36/36) | History; the legend is inside the fixture |
| — | `FX-RP1-4` (RP-v0.4) | — | — | — | History |
| — | `FX-RP1-5` (RP-v0.5) | — | — | — | History |
| — | `FX-RP1-6` (RP-v0.6) | — | — | — | Current; no reader (R23-49). Inputs include DEL-11-01's CA-1 v3 and DEL-11-02's AA-1 v2 status hand-overs |

`EU-F1.key-grounding.md` marks which key answers rest on supplier records, packet rules, O-F's own text, or O-F's first-cut inputs (RV3 EUF1-R3).

| File | What it is |
|---|---|
| `vendor/` + `VENDOR.json` | R23-44: exact supplier schemas and examples this unit relies on, with source path, sha256 and source commit |
| `rplib.py` | Rules RP-R1…RP-R8 (REPLACEMENT_PACKET.md §4–§6) |
| `build_fx_rp1.py` | Writes `fixtures/FX-RP1-6/` deterministically: package, packet manifest with `terms`, basis excerpts, disposition, supplier copies, first cuts, legend |
| `check_rp.py [--fixture NAME]` | Part A (A-1…A-22) on the named fixture (default FX-RP1-6); V-1 vendoring, plus a NOTICE if a live supplier file has moved; on the default fixture, C-1…C-21 (each Part A rule broken in memory) and Part B (B-1…B-52) rule cases |
| `ca/build_ca.py --at <commit> [--archives]`, `ca/check_ca.py` | DEL-11-01: build the continuity account CA-1 at a commit (archive check read-only, ≈20 s) and check it (36 expectations); `ca/vendor/` holds DEL-10-03's RA-v0.2 (R23-44) |
| `aa/build_aa.py --at <commit>`, `aa/check_aa.py` | DEL-11-02: build the adoption account AA-1 from git at a commit and check it (43 expectations) |
| `pv/pvlib.py --at <commit>`, `pv/check_pv.py` | DEL-09-12: build the practitioner-validation records at a commit and check them (27 expectations) |
| `stage_is.py [--set N] <empty folder>` / `--write-list` | Stage an input set exactly and verify every hash; the key is never staged |
| `compare_rp.py [--set N] --self-check` or `<account.json>` | Key against fixture; or the examiner comparison, with each set's own account schema |

```text
python3 -B build_fx_rp1.py                    # same bytes on every run
(cd aa && python3 -B build_aa.py --at 122c5abcf516f31ffdb1fdb17d9d5b0f96603154 && python3 -B check_aa.py)            # 43/43
(cd ca && python3 -B build_ca.py --at 122c5abcf516f31ffdb1fdb17d9d5b0f96603154 --archives && python3 -B check_ca.py) # 36/36
(cd pv && python3 -B pvlib.py --at b2fbfdbac84368c74a33e555815452fb8fcb199c && python3 -B check_pv.py)                  # 27/27
python3 -B check_rp.py                        # 99/99 at the RP-v0.6 freeze (build order: aa, ca, then build_fx_rp1.py)
python3 -B check_rp.py --fixture FX-RP1-3     # which current checks an earlier fixture fails
python3 -B compare_rp.py --set 3 --self-check
python3 -B compare_rp.py --set 2 ../RR-EUF2/account.json
```

Needs Python 3 and `jsonschema` (4.26.0 here).
