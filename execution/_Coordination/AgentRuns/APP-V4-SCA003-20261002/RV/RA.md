# RV return RA — DEL-01-01…DEL-01-05 (scope-of-work MODE=REVISE, closing MODE=VERIFY)

Run `APP-V4-SCA003-20261002`, node AK2 part 2, executor RA: Type 2 TASK,
Claude Opus 5.5, no delegation. It was dispatched by HELP_HUMAN as a
harness-native descendant. Basis commit: `eff378ffa2` (HEAD at the start;
clean tree). RB revised the other 14 Scopes of Work in parallel. Their
files are disjoint from these and RB's work is not covered here.

## Result

**PASS, 5 of 5.**
- All 63 blocks of `AMENDMENT_PACKET/SOW_REVISIONS_A.md` were applied exactly, in the listed order.
- Each prior hash was checked before writing.
- Each revised file equals the P2-A dry-run result once the snapshot name is substituted (see "Hashes").
- All three validators pass on every revised contract.
- The closing VERIFY passes.
- No wording was improvised, and no block failed or was dropped.

## Bound inputs

- **Route (Q-3):** `project-setup` INCREMENTAL Phase 5.5 routes each `SOW_V1` deliverable at IN_PROGRESS to `scope-of-work` `MODE=REVISE`, with `STATUS_POLICY=NO_STATUS_TOUCH`, closing with `MODE=VERIFY`. This node carries out only the five REVISE/VERIFY items. It writes no plan, setup-log line or run record for `project-setup`; those stay with the dispatcher.
- **AMENDMENT_REF**
  - Amendment: `SCA-V4-003`.
  - Accepted snapshot: `projects/chirality-app-v4/execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/`. `_ScopeChange/_LATEST.md` (sha256 `19cf31f1…e657`) reads `Latest: SCA-V4-003_2026-10-03_1827`.
  - Group 3 was accepted by DECISION-2 on 2026-10-03, recorded in `checkpoint_snapshots/SCA-V4-003_GROUP-3_2026-10-03/`, committed at `c8ae213134`. Its `DECISION.md` first line reads "accepted audited poststate".
  - Groups 1 and 2 were accepted by DECISION-1.
  - Action register: `checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/Amendment_Actions.csv`, sha256 `9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c`. The copy in the accepted snapshot is byte-identical.
  - Register rows 1–5 are `MODIFY` `DELIVERABLE` for DEL-01-01…DEL-01-05. `ScopeChanging` is NO on row 1 and YES on rows 2–5.
- **REVISION_SCOPE source:** `AMENDMENT_PACKET/SOW_REVISIONS_A.md`, sha256 `42c9167aadf8f0f88cc42b6e746af221140c2b7a00b7feaca552692e0cc7fc07`. The group-2 and group-3 manifests bind exactly this hash; it was checked before parsing. Each deliverable's REVISION_SCOPE is its section's `REVISION_SCOPE:` line, and is the same as the definitions its G-blocks change.
- **Conditional blocks:** DECISION-1 accepted every item as recommended, so every conditional block applies as written:
  - Q-2 and Q-4: all clauses; NR-03 has no text in these blocks.
  - Q-5: the act control, with REQ-008 as adjusted.
  - Q-11: the optional G-0101-03, G-0102-07, G-0102-09 and G-0105-09.
  - Q-15: G-0101-02 (P1-09).
  - Q-10: no token. The G-0105-08 text is fixed and independent of the status word.
- **Tokens:** `{AMENDMENT_ID}` = `SCA-V4-003` and `{AMENDMENT_SNAPSHOT}` = `SCA-V4-003_2026-10-03_1827`, as the brief directs and the pointer confirms. Each appears only in the new AX line, once per file. No other byte was supplied by this run, and no `{AMENDMENT_…}` token remains.
- **SOURCE_STATE:** `IN_PROGRESS` for all five, read from each `_STATUS.md` `**Current State:**` line. DEL-01-02…05 reached IN_PROGRESS by the Q-13 act. SOW_REVISIONS_A's lifecycle column still says INITIALIZED for them because it predates that act; REVISE admits both states.
- **Status policy:** `NO_STATUS_TOUCH`. No `_STATUS.md` was touched.
- **Instruction sources read:**

  | File | sha256 |
  |---|---|
  | `workflows/scope-of-work/WORKFLOW.md` | `84dadde4…bc2b` |
  | `resources/brief.md` | `1696cd9a…92bc` |
  | `resources/tools.md` | `fbd07771…e5cc7` |
  | `resources/checks.md` | `44ab41ac…f188` |
  | `workflows/project-setup/WORKFLOW.md` | `7aa4c30a…dd6d` |
  | `resources/method.md`, Function 5 | `febfecdd…26c9` |
  | `resources/contract.md`, INCREMENTAL | `e9f0d11b…218e` |
  | `RUN/BRIEFS.md` | `618f6a09…0e34` |
  | `RUN/OWNER_DECISIONS.md` | `29c0a07b…c28c2e` |

  The model is SCA-V4-002's `RV/RV_DEL-01-01.md` and its DISPATCH row "AK2 Part 2".

## Hashes

| Deliverable | Prior sha256 (= SOW_REVISIONS_A Summary = `HEAD`) | Revised sha256 | Dry-run revised sha256 (P2-A, dummy snapshot `SCA-V4-003_DRYRUN`) | Equal to dry-run? | `_STATUS.md` sha256 (unchanged) |
|---|---|---|---|---|---|
| DEL-01-01 | `9945e72b04b4f45c4c641a5248cca8bc2ac40bf4897d1018c5ab59eba307cc75` ✓ | `bbc81a8d31eeacab3497acf297c8c6eeac7b2f6febda5381f332ec14b8f65d02` | `3712a6e120b5131e41b31318b78aa3e8269dcddd15504059238c3ecab12c7967` | yes | `477c9a576400caf4…` |
| DEL-01-02 | `057ae2fdf4c3e98c961214739d2170a7c8ab29a530208f0c476af15125d6c6b4` ✓ | `6c62de1d749022a388d9a2c466655a35e06b0b9fa7779a7912f9df4424226a07` | `4a8f17d0f7c4dbbb1167c9222b19cb22cffa76558b4aa64d55b088923429f499` | yes | `00a87721b2803fd5…` |
| DEL-01-03 | `b5d533cb3dbea97b37950792ad2c68f42bf6023effa4ac894209a1ef3fc605f2` ✓ | `0056ec198e855080da740e2fb72a3e0a37fcd304c58cca537d4ad56a11c46069` | `dd5cad516bc9c7846c74a81356475246d088761d7e3736490ce1b8c5d6300e38` | yes | `0d60930353fd6a16…` |
| DEL-01-04 | `0cdb44e297010b70deb479ab647a165023846aa0943c3f9fc200407c708469cd` ✓ | `8434cc47ec28e1397e7dae548183543567f0b5fcfdefaebc0b44bc1f709aacf3` | `1d038a801e1c227ef4e78148ccedf32a5b15230b4d4486d1b4b1ac50ee005bb5` | yes | `440c16981c49c63b…` |
| DEL-01-05 | `baf68c79b5b8fdf01300fc255d7cf8e433975e6275daadf67b914b4e51eca4a6` ✓ | `2e134b572f2676ed4fe6daa892047e21e53a637f9901cba20f482a6637f7f3d3` | `e5169de4f168f7be27f111d00bb135d182c027dc98bc71154863c4c530f1eec9` | yes | `070c919079127dfe…` |

**Dry-run equality.**
- The P2-A dry-run (`sow_dryrun.py`, sha256 `d40d95a9…61a2b3`, line 58) filled `{AMENDMENT_SNAPSHOT}` with the dummy `SCA-V4-003_DRYRUN`. Its recorded revised hashes therefore cannot equal the real files byte for byte.
- The check: replace the accepted name `SCA-V4-003_2026-10-03_1827` with the dummy in each revised file and hash the result. All five hashes equal the full dry-run hashes in its `report_all.json`. The SOW_REVISIONS_A prefixes `3712a6e1`, `4a8f17d0`, `dd5cad51`, `1d038a80` and `e5169de4` also match, and V23 reproduced the same prefixes.
- So the revised files differ from the dry-run only in that one name, which appears once per file.

## Blocks applied (in listed order; `old` occurrences at application all exactly 1)

Line ranges are 1-based: the `old` text in the prior file, then the `new` text in the revised file.

| Block | Target | Prior lines | Revised lines | Occ. |
|---|---|---|---|---|
| G-0101-01 | CLM-005, new last sentence | 41 | 41 | 1 |
| G-0101-02 | CLM-004, new last sentence | 40 | 40 | 1 |
| G-0101-03 | TBD-002, first sentence | 69 | 69 | 1 |
| G-0101-04 | new AX-007 | 92 | 92–93 | 1 |
| G-0102-01 | CLM-001, interfaces sentence | 33 | 33 | 1 |
| G-0102-02 | CLM-002, first sentence | 34 | 34 | 1 |
| G-0102-03 | CLM-004, last sentence | 36 | 36 | 1 |
| G-0102-04 | OUT-004, last sentence | 42 | 42 | 1 |
| G-0102-05 | REQ-001, first sentence | 46 | 46 | 1 |
| G-0102-06 | REQ-002, first sentence | 47 | 47 | 1 |
| G-0102-07 | REQ-002, after G-0102-06's sentence | 47 | 47 | 1 |
| G-0102-08 | REQ-003, last sentence | 48 | 48 | 1 |
| G-0102-09 | REQ-004, after the first sentence | 49 | 49 | 1 |
| G-0102-10 | REQ-005, after the second sentence | 50 | 50 | 1 |
| G-0102-11 | REQ-006, first sentence | 51 | 51 | 1 |
| G-0102-12 | AC-002, first sentence | 57 | 57 | 1 |
| G-0102-13 | AC-006 | 61 | 61 | 1 |
| G-0102-14 | VER-002, first sentence | 73 | 73 | 1 |
| G-0102-15 | VER-006, first sentence | 77 | 77 | 1 |
| G-0102-16 | new AX-004 | 86 | 86–87 | 1 |
| G-0102-17 | TBD-001 (OI-012 sentence) | 87 | 88 | 1 |
| G-0102-18 | TBD-003, first sentence | 89 | 90 | 1 |
| G-0103-01 | CLM-003, after "…decision views." | 43 | 43 | 1 |
| G-0103-02 | CLM-004, last sentence | 44 | 44 | 1 |
| G-0103-03 | REQ-001, appended | 51 | 51 | 1 |
| G-0103-04 | REQ-003, appended | 53 | 53 | 1 |
| G-0103-05 | REQ-004, appended | 54 | 54 | 1 |
| G-0103-06 | REQ-005, appended | 55 | 55 | 1 |
| G-0103-07 | AC-001 | 60 | 60 | 1 |
| G-0103-08 | AX-002, third sentence | 85 | 85 | 1 |
| G-0103-09 | new AX-004 | 86 | 86–87 | 1 |
| G-0103-10 | TBD-001, appended after the first sentence | 87 | 88 | 1 |
| G-0103-11 | TBD-003, first sentence | 89 | 90 | 1 |
| G-0104-01 | CLM-001, after "…assigned to App `DEL-01-03`." | 41 | 41 | 1 |
| G-0104-02 | CLM-004, appended | 44 | 44 | 1 |
| G-0104-03 | OUT-002, appended clause | 49 | 49 | 1 |
| G-0104-04 | new OUT-005 | 51 | 51–52 | 1 |
| G-0104-05 | REQ-001, appended | 55 | 56 | 1 |
| G-0104-06 | REQ-002, appended | 56 | 57 | 1 |
| G-0104-07 | REQ-005, appended | 59 | 60 | 1 |
| G-0104-08 | REQ-006, `DEL-02-02` clause | 60 | 61 | 1 |
| G-0104-09 | new REQ-008 (App act control; adjusted wording, Q-5) | 61 | 62–63 | 1 |
| G-0104-10 | new AC-008 | 69 | 71–72 | 1 |
| G-0104-11 | VER-005, positive case | 79 | 82 | 1 |
| G-0104-12 | new VER-008 | 81 | 84–85 | 1 |
| G-0104-13 | new AX-005 | 90 | 94–95 | 1 |
| G-0104-14 | new matrix row for OUT-005 | 110 | 115–116 | 1 |
| G-0105-01 | CLM-001, last sentence | 37 | 37 | 1 |
| G-0105-02 | CLM-004, appended | 40 | 40 | 1 |
| G-0105-03 | OUT-002, appended | 42 | 42 | 1 |
| G-0105-04 | REQ-002, appended | 49 | 49 | 1 |
| G-0105-05 | REQ-004, appended | 51 | 51 | 1 |
| G-0105-06 | REQ-005, responsible participants | 52 | 52 | 1 |
| G-0105-07 | new REQ-010 | 56 | 56–57 | 1 |
| G-0105-08 | TBD-001 | 58 | 59 | 1 |
| G-0105-09 | TBD-002, appended | 59 | 60 | 1 |
| G-0105-10 | TBD-003, first two sentences | 60 | 61 | 1 |
| G-0105-11 | AC-004 | 65 | 66 | 1 |
| G-0105-12 | new AC-011 | 71 | 72–73 | 1 |
| G-0105-13 | VER-004, appended | 80 | 82 | 1 |
| G-0105-14 | new VER-011 | 86 | 88–89 | 1 |
| G-0105-15 | new AX-006 | 96 | 99–100 | 1 |
| G-0105-16 | new matrix row for REQ-010 | 111 | 115–116 | 1 |

There are 63 blocks (4 + 18 + 11 + 14 + 16) and 63 replacements. The parser
found 63 `#### G-` headings and 63 old/new pairs. Each block's `Target:`
agrees with its ID.

### Revised, added and removed IDs (each AX line compared with the actual definition changes, by script)

| Deliverable | Revised (= definitions whose line changed) | Added | Removed |
|---|---|---|---|
| DEL-01-01 | CLM-004, CLM-005, TBD-002 | AX-007 | none |
| DEL-01-02 | CLM-001, CLM-002, CLM-004, OUT-004, REQ-001…REQ-006, AC-002, AC-006, VER-002, VER-006, TBD-001, TBD-003 | AX-004 | none |
| DEL-01-03 | CLM-003, CLM-004, REQ-001, REQ-003, REQ-004, REQ-005, AC-001, AX-002, TBD-001, TBD-003 | AX-004 | none |
| DEL-01-04 | CLM-001, CLM-004, OUT-002, REQ-001, REQ-002, REQ-005, REQ-006, VER-005 | OUT-005, REQ-008, AC-008, VER-008, the OUT-005 matrix row, AX-005 | none |
| DEL-01-05 | CLM-001, CLM-004, OUT-002, REQ-002, REQ-004, REQ-005, TBD-001, TBD-002, TBD-003, AC-004, VER-004 | REQ-010, AC-011, VER-011, the REQ-010 matrix row, AX-006 | none |

- In every file, the AX line's Revised list equals the set of changed definitions, and its Added list equals the added definitions.
- No ID was removed, renumbered or reused.
- The only changed lines that are not definitions are the two new matrix rows (DEL-01-04 OUT-005 and DEL-01-05 REQ-010). Each was inserted after the existing last row, and no existing row changed.
- Frontmatter is byte-identical in all five files.

## Validation (`scope-of-work` resources/tools.md steps 2, 6, 7, 9)

| Deliverable | Prior: `validate_scope_of_work.py` (REVISE precondition) | Revised: `validate_scope_of_work.py --json` | `derive_review_checklist.py` (run twice; repeated byte-identical) | `check_boundary_owner_resolution.py --json` |
|---|---|---|---|---|
| DEL-01-01 | valid, `SOW_V1`, 0 issues | valid, `SOW_V1`, 0 issues (PASS) | 7 items AC-001…AC-007, contract order, bound to the revised hash; JSON `995fc012569c9162…` | OK; 0 findings; 2 checked, 0 not checkable, 0 without cited claim (report `a976bc4183c0ee49…`) |
| DEL-01-02 | valid, `SOW_V1`, 0 issues | valid, `SOW_V1`, 0 issues (PASS) | 9 items AC-001…AC-009; JSON `e6b964a292b164c0…` | OK; 0 findings; 1 / 0 / 0 (`0c05b9fbf3394a5f…`) |
| DEL-01-03 | valid, `SOW_V1`, 0 issues | valid, `SOW_V1`, 0 issues (PASS) | 7 items AC-001…AC-007; JSON `8fbec812272b4866…` | OK; 0 findings; 1 / 0 / 0 (`80673189ec1d6c11…`) |
| DEL-01-04 | valid, `SOW_V1`, 0 issues | valid, `SOW_V1`, 0 issues (PASS) | 8 items AC-001…AC-008 (+AC-008); JSON `ca84a5ca00f6253d…` | OK; 0 findings; 1 / 0 / 0 (`f38ffa1a3a53d12a…`) |
| DEL-01-05 | valid, `SOW_V1`, 0 issues | valid, `SOW_V1`, 0 issues (PASS) | 11 items AC-001…AC-011 (+AC-011); JSON `94bbc56337fb35c7…` | OK; 0 findings; 1 / 0 / 0 (`42a04ac9d1f10667…`) |

- Every boundary check found 0 `UNRESOLVED_OWNER`, 0 `UNDEFINED_CLAIM`, 0 `NOT_CHECKABLE` and 0 `NO_CITED_CLAIM`.
- The checklist counts match the dry-run (7, 9, 7, 8, 11).
- The tools were run three times on each file:
  1. once in the apply run, on the production paths;
  2. again, read-only, on the production paths;
  3. once on scratch copies before writing.

  All three passes gave the same checklist JSON bytes.
- The checklist and boundary JSON files are in the task scratch folder, outside the write fence. They are deterministic and can be regenerated from the revised contracts.

## MODE=VERIFY (read-only, on the five production files after writing)

| Check (checks.md) | Result |
|---|---|
| 3: `_STATUS.md` byte-identical to `HEAD`; state `IN_PROGRESS` unchanged (5/5) | PASS |
| 4: frontmatter, headings, IDs, references and matrix validate | PASS (5/5) |
| 8: every `OUT-*` maps to scope/objective refs. Validator; the new OUT-005 row and the REQ-010 row (under OUT-002) cite OBJ refs already in the frontmatter | PASS |
| 9: every `AC-*` maps to a `VER-*`. Checklist: AC-008 → VER-008, AC-011 → VER-011 | PASS |
| 13, 18: checklist has every `AC-*` once, in order, hash-bound; repeat byte-identical | PASS |
| 16: findings separated. Schema: none. Project content: none new. Execution substrate: none | PASS |
| 19: no bare upstream local ID added. Validator, plus reading the new text: upstream deliverables are named `DEL-NN-NN`, decisions by full identity | PASS |
| 20: matrix grouping. Each new row holds one AC verified only by its own VER; no existing row changed | PASS |
| 21: boundary-owner resolution, no `UNRESOLVED_OWNER` or `UNDEFINED_CLAIM` | PASS |
| 22: amendment accepted at group 3, and its register names each deliverable `MODIFY` (rows 1–5); state admitted and unchanged. Reverse-applying every filled `new` → `old` in reverse order reproduces the prior (`HEAD`) bytes exactly (5/5), so nothing outside the blocks changed. AX reference present, and the snapshot path exists | PASS |
| 1: pilot variance | Recorded. The validator resolves each contract as `SOW_V1` without a migration variance; a `SOW_V1` REVISE needs none |
| 2, 5–7, 10–12, 14, 17 | NOT_APPLICABLE (CONVERT only) |
| 15 | NOT_APPLICABLE (no HTML requested) |

**New deliverable names, compared with SOW_REVISIONS_A's "Extraction guards" table:**

| SoW | New names, by script |
|---|---|
| DEL-01-01 | DEL-02-03, 03-03, 03-04, 06-01, 09-01, 09-02, 09-06 |
| DEL-01-02 | DEL-01-03, 02-02, 02-03, 03-03, 09-02 |
| DEL-01-03 | DEL-06-01, 09-02, 09-05 |
| DEL-01-04 | DEL-01-05, 02-03, 02-04, 04-02, 09-02 |
| DEL-01-05 | DEL-09-02 |

- Each list equals the table's, and no name was removed.
- No register was re-extracted here. The extraction guards stay for the `dependency-extract` UPDATE.

**Write footprint (`git status --short`, after writing):** in PKG-01, only the five `ScopeOfWork.md` files are modified.
- `git diff --quiet HEAD` confirms that each deliverable's `_STATUS.md`, `Dependencies.csv` and `_DEPENDENCIES.md` are unchanged.
- `_DAG/` and `_Decomposition/` are also unchanged.
- The other 14 modified `ScopeOfWork.md` files in the tree are RB's (PKG-02, 03, 04, 05, 09); this node did not touch them.
- This node changed no register, `_DEPENDENCIES.md`, `_STATUS.md`, DAG or Design file. It made no git write and used no network.

## Diff, prior → revised (for the independent check)

`git diff HEAD -- "projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/"`
on the uncommitted tree (or between `eff378ffa2` and the commit that carries
these files) is exactly the 63 blocks in the table above: 62 lines added
and 48 removed per `git diff --numstat` (DEL-01-01 +4/−3, 01-02 +17/−16,
01-03 +11/−10, 01-04 +14/−8, 01-05 +16/−11). The
reverse-application check (VERIFY item 22) proves that the diff contains
nothing outside the blocks. The full diff is about 75 KB and is not copied
here.

## Method and evidence

- **Script:** `apply_ra.py` (sha256 `dd8f992e1bea684dafde3f71c7330c5c87432679142f83f42d3f745d4f0d1921`), in the task scratch folder and not in the repository. It does the following:
  1. checks the SOW_REVISIONS_A hash;
  2. parses the 63 blocks;
  3. checks each prior hash against the Summary table and against `HEAD`;
  4. validates the prior contract and reads the lifecycle state;
  5. applies the blocks in order, requiring exactly one occurrence of each `old` at application;
  6. fills the two tokens;
  7. compares with the dry-run under the dummy name;
  8. runs the three tools;
  9. checks reverse application, definitions, AX lists and frontmatter.
- **Runs:** it ran once on scratch copies (pre-flight, 5/5 ok), then with `--write` on the production files (5/5 ok).
- **Separate checks:** the read-only VERIFY rerun of the validators, and the line-range map of the blocks, were done separately.

## Open after this node (not in RA's fence)

- `dependency-extract` UPDATE for the five registers, under SOW_REVISIONS_A's "Extraction guards" and IMPACT §10.
- The `project-setup` INCREMENTAL record and the `SETUP_LOG.md` line.
- The `project-dag` currency audit and DAG-004.
- The Design re-pins.
