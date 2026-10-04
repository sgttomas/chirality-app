# Preserved history and coexistence account

- **Contribution:** DEL-11-01/CA-v0.1, the first Design file of DEL-11-01. Frozen with DEL-11-03 RP-v0.4 as unit **EU-F2**, because RP-v0.4 adopts this file's hand-over.
- **Status:** DRAFT DEFINITION — proposed, not accepted. Beside it is the PROPOSED schema `ca.continuity-account.schema.json`. The prototype is under `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-4-20261003/F/ca/` (RUN/F/ca): `build_ca.py`, `check_ca.py`, and the built account `records/CA-1.continuity-account.json` with its hand-over `records/CA-1.handoff.json`. The account's checks are **real**, run against this repository and the original checkout; only the lane obligations are absent, because their owners have not supplied them.
- **Run and owner:** `APP-V4-DESIGN-PASS-4-20261003`, tranche 2; owner O-F (Type 2, Claude Opus 5.5); 2026-10-04.
- **Serves:** OUT-001, OUT-002, OUT-003; REQ-001…REQ-006; designed cases for VER-001…VER-007 (§8).
- **Rulings (cited by ID):**
  - R23-32: F-R6 (a linked view over existing records), F-R7 (the thesis check method), F-R8 (SCC-006 treated by SCC-CASE-007 R1), F-R11 (consumers come from DEL-10-03), F-R14; and P-1, P-4 as the person's acts;
  - R23-43;
  - R23-44 (vendoring).
- **ScopeOfWork pin (R23-5):** `ScopeOfWork.md` sha256 `272f76221dd429a52143e51ef4898ce290669b7be1d773a8fba3476282f04309`. This is the INIT contract; no SCA-V4-001/002/003 block changed it. Its TBD-002 reads OI-017 and OI-018 as open. OI-017 is resolved for this definition run (CURRENT_EXECUTION_BASIS), and OI-018's App part is answered (K-9 as amended by L-2). The wording is carried to the next amendment (R23-11).
- **Basis pins** (`shasum -a 256`, 2026-10-04):
  - `docs/PRD.md` `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` (§6, §8, §9 OQ-12, §11);
  - `docs/OPERATING_METHOD.md` `98836b5240ed235ec2ad38b08a9525dc9f2b366145c0736f7c70d22c1c93c5dd` (§5 closing paragraph, V4-OPS-31/32);
  - `conceptual/DECISIONS.md` `abe26074667b77863c2d917331d4ffba3a6996189273c551e1cf722d84e0430a` (OD-09).
- **Linked records** (the account names each by its git identity at commit `22ed9383a45e788ade4718b9e78053e9ceb72d90`; the current sha256 of each file):
  - `reference/REFERENCES.md` `07fe44e0494634ee40ae57a0b112f6fed7ae0b937fd3e2502574cd5431b240fc`;
  - `reference/archives/ARCHIVES.md` `b791f8390b9423f59d5a7e5fbb43ec57d1c9f119be208c29b041a38c945e41a2`;
  - `archive_digests.json` `c73203c2fc13fe35954c75367947324b483f67533c8f2d3b6ab512418c5c9357`;
  - `archive_digests.py` `84ca3b480cba1a176a35c709cb319e904fdcb7babb80a9b8936e4e0d7c5cc816`;
  - `reference/SOURCE_INVENTORY.md` `4008921d7f826122f20c95861f9a3f15b474f37c4819bea715df60dcc910122a`.
- **Supplier input (R23-44):** DEL-10-03's RA-v0.1 draft (O-E, not frozen) is vendored at `RUN/F/ca/vendor/` (sha256 `531b65b7…8934`) for its X-1 consumer list.
- **Labels.** *States* means a file says it; *inference* marks this file's reading; PROPOSED marks a rule introduced here.

## 0. What the account is, and what it is not

**What it is.** The account is a **linked view** (AX-003; V4-OPS-31; F-R6). It does not copy or re-inventory what the project already keeps. Each preservation class links the primary records that already hold the material (REFERENCES, ARCHIVES and its digests, SOURCE_INVENTORY, git trees and tags, owner-decision records) by their identity at one commit. The account adds only what none of them carries: standing, current selector, recovery route, owner and point of need. It also adds the continuing-obligation rows and the replacement standing.

**What it is not.** It retires, migrates, freezes or deletes nothing, and it imports no v3 chat (REQ-005; PRD §6). It does not perform any of these acts:
- consumer adoption (DEL-11-02);
- the replacement decision (the owner; DEL-11-03 prepares the package);
- retirement (the owner with affected consumers, OI-024).

It does not open a whole-corpus archival audit.

## 1. Act boundary (REQ-005; CLM-002…CLM-006)

| Act | Who | Here |
|---|---|---|
| Keeping the fallback, old projects and archives | The owner's direction OD-09: "Preserve the old projects and archives until I decide v4 has replaced the fallback." | Recorded as an owner act (§5); every class is `retained` (schema `const`) |
| Replacing v3.0.1 | The owner (P-1; PRD §8) | Standing carried: "replacement pending; v3.0.1 retained" |
| Retiring any lane; ending coexistence; chat migration | The owner with affected consumers (P-4; OI-024; OQ-12) | Rows carried; no lane is eligible (§5) |
| A lane's continuing obligations | That lane's owner (DEP-006) | Status carried as *not supplied* |
| Consumer adoption | Each receiving loop (F-R10), recorded by DEL-11-02 | Status carried as *not supplied* until DEL-11-02's account exists |
| Shared responsibility and consumer map | DEL-10-03 (O-E) | X-1 consumed (§2) |

## 2. Interfaces

| ID | Input or output | Other end | Arc (DAG-004) | Point of need | If absent |
|---|---|---|---|---|---|
| I-1 | Consumer lanes (X-1: Root, Runtime, App v3, Piping), historical applicability, packaging and tool paths | DEL-10-03 RA (draft, vendored) | DEP-11-01-008, admitted | Before an obligation row is relied on | Rows are kept with the lanes named in DEP-006 and marked provisional |
| I-2 | Manual and method pins | DEL-10-01 (EB; CURRENT_EXECUTION_BASIS) | DEP-11-01-009, admitted | Before a selector cites a manual edition | No manual selector is written |
| I-3 | Adoption status | DEL-11-02 | DEP-11-01-010, admitted | Each account version | `not_supplied` |
| I-4 | Thesis tree identity | git; PRD §11 | DEP-11-01-012 (document) | Each account version | — |
| O-1 | Continuity hand-over `$defs/continuity_handoff` (CA-v0.1) | DEL-11-03 | DEP-11-03-008, held (SCC-006; F-R8, R1) | Each packet version | DEL-11-03 records it *not supplied* |
| O-2 | The owner's replacement disposition, returned | from DEL-11-03 | DEP-11-03-015, held | After an attributable owner act | Standing stays "pending; v3.0.1 retained" |

The hand-over (O-1) supersedes DEL-11-03's first-cut `$defs/continuity_input`. DEL-11-03 adopts it in RP-v0.4, which is frozen with this file. It carries the commit, the thesis check exactly as the account records it, the fallback identity standing, the archive verify result, the obligations' status, the adoption status and the replacement standing.

## 3. Preservation classes (OUT-001; REQ-001, REQ-002)

Seven classes are built from REQ-001's list and B-HTML d7's "What to carry" (F-R6). The account's identity check is in the last column, as run at `22ed9383a4`.

| ID | Class | Linked records | Standing | Current selector | Recovery route | Check |
|---|---|---|---|---|---|---|
| C-1 | Fallback release Chirality v3.0.1 | REFERENCES §2; source commit `485051eac9` | `current_fallback` | REFERENCES §2 | The published release; the source in git | **matches**. Local facts: package.json 3.0.1 at the source commit; the release-preparation commit is its ancestor; it is an ancestor of the account's commit; REFERENCES names it and the installer digest. The remote is not re-checked (no network) |
| C-2 | App v3 project lane | tree of `projects/chirality-app-dev`; its `AGENTS.md` | `active_lane` | The lane's own entry and `_Coordination` | git history | **passed**: tree `3fb53704…`; 225 commits touch it after the v3.0.1 source. Active: recorded at one commit, never frozen |
| C-3 | Git-ignored archives (19 locations) | ARCHIVES.md; `archive_digests.json`; `archive_digests.py` | `preserved_evidence` | ARCHIVES.md (with its hazard: never `git clean -x/-X` there) | Read-only access in the original checkout | **passed**: `archive_digests.py verify`, 19 of 19 locations OK, exit 0 (≈20 s). Only where the original checkout is present |
| C-4 | The complete thesis | tree `foundation/thesis`; PRD §11 | `preserved_basis` | PRD §11 | git | **matches** `47fc49e96c2931ba18090f1a82d56a49f230b3ee` (19 files) |
| C-5 | Investigation revision and source inventory | REFERENCES §1; SOURCE_INVENTORY; commit `2b0572fe04` | `preserved_basis` | REFERENCES §1, SOURCE_INVENTORY | `git show <commit>:<path>` | **passed**: the commit exists |
| C-6 | Archived agent-run records | tag `archive/agent-runs-2026-09-25`; REFERENCES §4 | `preserved_evidence` | The tag | `git show <tag>:<path>` | **matches** `8007c592…` |
| C-7 | External read-only archive named at the 30% gate | HANDOFF_30_PERCENT.md line 18 (its home path is not repeated) | `preserved_evidence` | That line | Read-only where it lives | **not_checked**: no digest record exists (U-CA-2) |

**Standing values (PROPOSED).** The values are `historical`, `current_fallback`, `active_lane`, `preserved_basis` and `preserved_evidence`. None is v4 authority (CLM-001); the schema refuses any other value. An active lane keeps its own scope. The account never imposes v4 rules on it, never erases it, and never treats new v4 files as its retirement (REQ-001).

## 4. Identity checks (OUT-002; REQ-003; VER-003, VER-004)

1. **Thesis (F-R7).**
   - The git tree id at the account's commit equals PRD §11's tree, and so does HEAD's.
   - The working tree under it is clean, with no modified, deleted or untracked file (`git status --porcelain --untracked-files=all`). Together these compare the complete file membership and bytes.
   - VER-003's negative cases run **in memory**: the detector compares the per-file listings and names an omitted, an added and a changed file. The thesis itself is never touched.
2. **Named material.**
   - C-1: local git facts.
   - C-3: the existing `verify` tool, whose committed digests are keyed by hashed subtree paths because the repository is public. The account records only the summary, never a path below a location or the archive root.
   - C-5, C-6: object existence and the tag target.
   - C-7: no check is possible yet.
3. **Attribution and standing.** PRD §11 states the thesis is kept "retaining attribution and its nonbinding stated standing", and: "Purpose-level citation does not convert its historical implementation choices into mandatory v4 requirements.". The account checks PRD's statement (`check_ca.py` K-7) and never edits the thesis to conform. Reading the thesis's own front matter for its attribution is left for VER-003's production run, as a limit; this unit does not claim it.

## 5. Continuing obligations, owner acts and replacement standing (OUT-003; REQ-004, REQ-006)

**Obligation rows (PROPOSED).** There is one row per DEP-006 consumer lane, checked against DEL-10-03's X-1 list (F-R11): App v3, Runtime, SWBPIPE and Root. Each row records:
- `retirement_intended` (false for every lane: none is intended or proposed);
- `continuing_obligations` (`not_supplied` for every lane);
- `disposition` (`null`);
- `retirement_eligible`, which is false;
- the decision's owner and point of need (OI-024: "Before each adoption/retirement decision").

**RE-1 (PROPOSED).** `retirement_eligible` can be true only with all of: retirement intended, obligations supplied, and an evidenced disposition by the lane's accountable owner (`by`, `record_ref`, `evidence`). The schema enforces this. The check's rule never consults the fallback replacement: a decided replacement makes no lane eligible (VER-005), and neither does an empty disposition.

**Owner acts, recorded faithfully (VER-006 positive).** Two real acts bear on preservation. Each is recorded with its exact text, which is found in its record at the commit, and with a recorder distinct from the actor:
- **OD-09** (conceptual/DECISIONS.md): "Preserve the old projects and archives until I decide v4 has replaced the fallback."
- **Direction item 2** of this run (OWNER_DECISIONS.md): "1 yes, 2 no rewrite, 3 go, 4 A+C", whose effect is that git history is not rewritten. History stays recoverable as recorded.

A fabricated act whose text is not in its record fails the rule, and an act recorded by its own actor is refused.

**Replacement standing (F-R8, SCC-CASE-007 R1).** The standing is "pending" and "v3.0.1 retained", with no disposition reference. When DEL-11-03 returns an attributable disposition, the next account version records it (`decided`, with its reference). Even then the account retires nothing: P-4's acts remain separate.

## 6. Records and sequence

- **Account record** (`ca.continuity-account.schema.json`): account id, version, date, `at_commit`, classes, obligations, owner acts, adoption status, replacement standing, the hand-over and limits.
- **Hand-over** `$defs/continuity_handoff` (format CA-v0.1): see §2 O-1.
- **Sequence.**
  1. Build the account at a named commit (`build_ca.py --at <commit> [--archives]`). Everything except the archive check is read from git at that commit, so a rebuild reproduces it exactly.
  2. Check it (`check_ca.py`).
  3. Hand the hand-over to DEL-11-03.
  4. On a change (a moved lane, a supplied obligation, adoption status, a returned disposition), write a new version. Earlier versions stay as history.

## 7. Failure behaviour

| # | What fails | Record left | Next |
|---|---|---|---|
| CF-1 | The archive tool cannot run (no original checkout, or an error) | C-3 `not_run`, with the tool's exit status; never reported as a change | Rerun where the checkout is present |
| CF-2 | `verify` reports a change | C-3 `changed`; the hand-over carries it | The owner is told: archives are the owner's (OD-09). The account never "repairs" archive content |
| CF-3 | The thesis tree differs, or its working tree is dirty | C-4 `differs`; `check_ca.py` K-5/K-6 fail | A discrepancy, exposed and not normalised (AC-003) |
| CF-4 | A lane owner supplies obligations | A new row version with a disposition only if evidenced; eligibility only under RE-1 | — |
| CF-5 | DEL-10-03's consumer list changes | V-1 prints a NOTICE (live moved since vendoring) | Re-pin deliberately (R23-21) |

## 8. Verification (designed; `check_ca.py` 21/21 at freeze)

| VER | Case | Held by |
|---|---|---|
| VER-001 | Every REQ-001 class is present, with its route, standing and retention; no lane is treated as replaced | K-1, K-4, N-6, N-8 |
| VER-002 | Selectors trace to DEL-10-03's consumer list; a historical pin never becomes current authority | K-10, N-8 |
| VER-003 | Complete thesis comparison; omitted, added and changed files detected in memory; thesis untouched | K-5, K-6, K-7, K-8 |
| VER-004 | Named material identities (C-1, C-3, C-5, C-6) with coverage limits (C-7 not checked) | K-4, K-3 (rebuild), C-3 live verify |
| VER-005 | Obligations to owners; a fallback-only replacement and an empty disposition never establish retirement | K-11, N-1, N-2, N-3 |
| VER-006 | Two real owner acts faithfully recorded; fabricated and self-recorded acts refused | K-9, N-4, N-5 |
| VER-007 | One-for-one act boundary (§1) | Review |

## 9. Open matters

| ID | Item | Owner | Point of need |
|---|---|---|---|
| U-CA-1 | Each lane's continuing obligations | The lane owners, with the owner (DEP-006; OI-024) | Before each adoption or retirement decision |
| U-CA-2 | C-7 has no inventory or digest record. Recording one would need `archive_digests.py`-style hashed keys and a write outside this unit's area | HELP_HUMAN to route (the owner's archive) | Before C-7's identity is relied on |
| U-CA-3 | Remote re-check of REFERENCES §2 | DEL-11-03 coordinator | When a real package is prepared for the owner |
| U-CA-4 | DEL-11-02's adoption status | O-F (DEL-11-02, next unit) | The next account version |
| U-CA-5 | Reading the thesis front matter for attribution (VER-003's production run) | O-F | Before the account is relied on as VER-003 evidence |

## 10. Changes

| Version | Change |
|---|---|
| CA-v0.1 (2026-10-04) | First Design file; unit EU-F2 with DEL-11-03 RP-v0.4 |
