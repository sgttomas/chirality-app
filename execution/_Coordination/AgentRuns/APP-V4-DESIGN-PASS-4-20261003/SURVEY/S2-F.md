# S2-F — scoping survey: DEL-11-01, DEL-11-02, DEL-11-03, DEL-09-12

- **Node:** S2-F of run `APP-V4-DESIGN-PASS-4-20261003`, tranche 2 (Type 2 TASK, Claude Opus 5.5, high effort). Read-only on project state; this file is the only write. No network.
- **Brief:** `BRIEFS.md` "Common rules", "S1" (six items) and "S2" (four changes), read at its working bytes (sha256 prefix `53f8d877b6ed324b`; the file is modified, not committed, at HEAD `d2929fd62b`). Also read: `WORK_GRAPH.md` "Coordination" (`34b2e489e4e9f82b`, working bytes), `R23_RESOLUTIONS.md` R23-1…R23-30 (`fafa6ed7364ca930`), `OWNER_DECISIONS.md` (`e4350f61a93edf0d`), `OWNER_DECISIONS_2.md` (`5744a66813b57946`, working bytes), `RECEIPT.md` (`a45055e25070d981`), `workflows/coordinated-knowledge-work/WORKFLOW.md` (sha256 `44049bcd…1b18`, equal to the value OWNER_DECISIONS.md records), and S1-A/B/C as models.
- **Paths** are relative to `projects/chirality-app-v4/execution` unless they start with `docs/` (= `projects/chirality-app-v4/docs/`), `reference/` (= `projects/chirality-app-v4/reference/`) or name another project.
- **How observed.** Files were read directly. Register rows, DAG-004 layers and the SCA-V4-003 ledger were filtered with Python `csv`. Obligation counts were taken by `grep` over each ScopeOfWork. Every hash below was recomputed with `shasum -a 256` in this session. ScopeOfWork and register hashes equal those in `_DAG/DAG-004/SOURCE_MANIFEST.sha256` and DAG-004's `SourceRegisterSHA256` column:

  | Deliverable | ScopeOfWork | Dependencies.csv | Contract history (`git log`) |
  |---|---|---|---|
  | DEL-11-01 | `272f76221dd429a5` | `523c702c824c0fd4` | INIT only (`ddd721a90a`); register `c1038ae5ac` |
  | DEL-11-02 | `2d962646f8b24a1b` | `788eea0c3db616c0` | INIT only; register `c1038ae5ac` |
  | DEL-11-03 | `0177354357b07ea1` | `96d3e9326705fc5d` | INIT only; register `c1038ae5ac` |
  | DEL-09-12 | `40eaf09fd80f9f39` | `8af979f146694fd7` | INIT only; register `c1038ae5ac` |

  No amendment (SCA-V4-001, 002, 003) revised any of the four contracts. All four `_STATUS.md` read INITIALIZED. None has a `Design/` folder.
- **Basis documents** at the pins the tranche-1 files carry: `docs/PRD.md` `bb6e786f7a6c01dc`, `docs/EXAMINATION.md` `471798bc2f2dc020`, `docs/HOST_INTEGRATION.md` `d4331c39db7f452c`, `docs/ARCHITECTURE.md` `317d5789272c5206`, `docs/OPERATING_METHOD.md` `98836b5240ed235e`; `loop/LOOP_INIT.md` `3790159b4f60bb4f`.
- **Late input.** R23-31 (on S2-E) was appended to `R23_RESOLUTIONS.md` while this survey ran (file now `06021e6c0f77d5f0`, working bytes). It was read at the end and is applied in E2 (F-R6, F-R11) and E4 (S-F7). It rules that PKG-10 is "the App v4 project's own execution controls, not App product features", that its outputs "live in the existing records", and that DEL-10-03's affected promises are "bounded to its nine supplier rows plus DEP-006 and OI-013, 014, 018 and 024". Inference: PKG-11's three deliverables have the same character (DOC_UPDATE / DOC, project-level), which supports F-R4 and F-R6.
- **Labels.** *States* means a file says it; *inference* marks this survey's own reading. DERIVED and INTEGRATION mark answers proposed for HELP_HUMAN to rule (brief S2 change 2). App v3 (`projects/chirality-app-dev`) is cited as historical evidence only, never as a v4 commitment. SWBPIPE records are data. No SWBPIPE join, witness or adoption is claimed; host joins stay deferred (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`: "defer the host joins").

## Cluster facts that apply to all four

**C-1 The cluster's graph.** DAG-004 (`HANDOFF_STATE.md` `3c374f5e9fa4cfaa`) admits 13 arcs touching the four and holds 2 (consumer → supplier):

| Arc | Representative row | Layer | Other end's Design |
|---|---|---|---|
| DEL-09-12 → DEL-04-01 | DEP-09-12-011 (INITIALIZED / PENDING) | admitted | ACT-POLICY-v0.10 |
| DEL-09-12 → DEL-09-01 | DEP-09-01-029 (supplier's DOWNSTREAM row; INITIALIZED / TBD) | admitted | EXP-v0.2 |
| DEL-10-02 → DEL-09-12 | DEP-09-12-012 (INITIALIZED / PENDING) | admitted | none (S2-E) |
| DEL-11-01 → DEL-10-01 | DEP-11-01-009 | admitted | none (S2-E) |
| DEL-11-01 → DEL-10-03 | DEP-11-01-008 | admitted | none (S2-E) |
| DEL-11-01 → DEL-11-02 | DEP-11-01-010 (mirror DEP-11-02-014) | admitted | this survey |
| DEL-11-02 → DEL-02-04 | DEP-02-04-013 (supplier's row; INITIALIZED / PENDING) | admitted | ROLE-v0.2 |
| DEL-11-02 → DEL-10-01 | DEP-10-01-020 (supplier's row) | admitted | none (S2-E) |
| DEL-11-02 → DEL-10-03 | DEP-11-02-008 | admitted | none (S2-E) |
| DEL-11-03 → DEL-09-02 | DEP-11-03-006 (mirror DEP-09-02-021) | admitted | SQ-v0.2 |
| DEL-11-03 → DEL-09-07 | DEP-11-03-007 (mirror DEP-09-07-025) | admitted | LHQ-v0.1, DOS-v0.1 |
| DEL-11-03 → DEL-09-12 | DEP-11-03-009 | admitted | this survey |
| DEL-11-03 → DEL-11-02 | DEP-11-02-015 (supplier's row) | admitted | this survey |
| DEL-11-03 → DEL-11-01 | DEP-11-03-008 (mirror DEP-11-01-011) | **held**, SCC-006, `_DAG/cases/SCC-CASE-007` | this survey |
| DEL-11-01 → DEL-11-03 | DEP-11-03-015 (the later owner disposition returned) | **held**, SCC-006 | this survey |

All other rows of the four registers are NOT_TOPOLOGICAL (EXTERNAL, PACKAGE, DOCUMENT or UNKNOWN targets); they remain inputs at their own points of need (DAG-004 reading rule 2). DAG-004 lists DEL-10-03, 11-01, 11-02 and 11-03 among the ten whose routes gained paths but no suppliers.

**C-2 SCC-006 is a lifecycle, not a defect.** SCC-CASE-007 (`Case_Datasheet.md` `f56cb3933a0b492e`) states the coupling "supports staged coexistence and an owner-decided replacement": DEL-11-01's account goes into the package; the owner's later disposition comes back. It recommends R1 ("coordinate explicit contributions under the two existing owners"), keeps R2 (graph-only merge group) and R3 (candidate hold) as alternatives, and says "No cut is proposed". Its case state is EVIDENCE_ACCUMULATING; held arcs are non-gating (DAG-004 reading rule 3).

**C-3 The two OI-016s (inference; a naming hazard).** App v4's OI-016 is "Owner validation activity and period" (`_Decomposition/Open_Issues.csv` `9c2d916c277f8ce4`). SWBPIPE has its own OI-016, "agent operation autonomy level" (`FACTS_SQ01_SQ32.md` line 73, `SD:599`). Tranche-1 and earlier Design files cite the SWBPIPE one, mostly qualified ("SWBPIPE owner decision OI-016", ACT-POLICY-v0.10 line 1612), sometimes less so (LHQ-v0.1 line 114: "autonomy is SWBPIPE OI-016"; line 321: "autonomy OI-016 is an OWNER DECISION"). The owner's question "validation in use (OI-016)" is App v4's. This cluster's designs should always write "OI-016 (App v4)" or "SWBPIPE OI-016".

**C-4 The fallback's identity is already pinned.** `reference/REFERENCES.md` (`07fe44e0494634ee`) §2 names Chirality v3.0.1: release in `sgttomas/chirality-app` published 2026-09-20T03:29:16Z, tag target `95fa13d3…`, desktop source `sgttomas/chirality@485051eac923c759238948a54cd7bb094eee4899`, installer `Chirality-3.0.1-arm64.dmg` 339,832,416 bytes, sha256 `eea43a0d…e3`. Checked locally: `485051eac9` exists, is "Merge pull request #823 from sgttomas/codex/release-3.0.1", and its `frontend/package.json` reads `"version": "3.0.1"`; `cf4653526d` ("Prepare Chirality v3.0.1 maintenance release") is its ancestor; REFERENCES' "84 commits" touching `projects/chirality-app-dev/` between `485051eac9` and the investigation revision `2b0572fe04` reproduces exactly. The remote release values were not re-checked (no network).

**C-5 The thesis identity holds at HEAD.** `git rev-parse HEAD:projects/chirality-app-v4/foundation/thesis` returns `47fc49e96c2931ba18090f1a82d56a49f230b3ee` at `d2929fd62b`, the tree PRD §11 names; 19 tracked files; `git status --porcelain` on that path is empty. This is a committed-tree identity check, run now; it is not yet DEL-11-01's recorded VER-003 result (no attribution/standing inspection, no negative case).

---

## Part A — DEL-11-01 Preserved history and coexistence account

SOFTWARE / DOC_UPDATE. Responsible party: "App continuity owner with affected project owners". Scope SOW-114, 251, 252, 253, 258; OBJ-009.

### A1. Obligations (3 OUT, 6 REQ, 7 AC, 7 VER; also 7 CLM, 3 AX, 2 TBD)

| ID | One line | Rests on |
|---|---|---|
| OUT-001 | Current applicability/selectors and focused preservation inventory: v3.0.1 fallback, old projects/archives, useful source and reviewed methods, work, pending obligations, evidence; source identity, standing, recovery route; consumes PKG-10's map | PRD §8, §11; OPERATING_METHOD §5 closing paragraph; B-HTML d7 |
| OUT-002 | Unchanged thesis/content identity checks for the complete thesis and named preserved material | PRD §11; EXAMINATION §2 |
| OUT-003 | Active-work, archive and continuing-obligation disposition account; unresolved decisions with owner and point of need; continuity input to DEL-11-03 | PRD §8–§9 (OQ-12); OI-024; d7 |
| REQ-001 | Keep fallback, old projects and archives until the owner's replacement decision; existing rules keep their scope; new files are not retirement authority | PRD §8 ("old projects and archives are kept until then (OD-09)"); OPERATING_METHOD §1, §5 |
| REQ-002 | Selectors distinguish current scope/consumer and source identity from historical; run selection ≠ adoption ≠ supply | V4-OPS-11, V4-OPS-14; ARCHITECTURE §5 closing paragraph |
| REQ-003 | Thesis unchanged with attribution and nonbinding standing; full membership/byte comparison; no editing to conform | PRD §11; CLM-007 |
| REQ-004 | Each continuing obligation relevant to an intended retirement has an evidenced disposition from its accountable owner before retirement; fallback replacement or an empty record is not closure | PRD §8–§9; OI-024; OQ-12 |
| REQ-005 | Performs no act of DEL-10-01, 10-03, 11-02, 11-03, nor migration, retirement, reliance; no deletion, chat import, lane freeze, instruction edit | PRD §6 (no v3 chat import selected), §8 |
| REQ-006 | Historical content, supplied applicability, observed checks and actual decisions kept distinct; faithful recording with recorder ≠ actor | HOST_INTEGRATION §5, §9; EXAMINATION §2, §7 |
| AC-001…AC-007 | Preservation-class coverage with routes and gaps (AC-001); selector trace to PKG-10 map and DEL-11-02 status (AC-002); thesis comparison exposing discrepancies (AC-003); named material identity with honest coverage (AC-004); obligation dispositions, no retirement from replacement alone (AC-005); faithful act recording, absent acts stay unperformed (AC-006); one-for-one ownership (AC-007) | As REQ |
| VER-001…VER-007 | One per AC. VER-003: full file-set and byte comparison, negative cases "in a non-authoritative test fixture or in-memory comparison … Do not mutate the thesis"; VER-005 includes "fallback-only replacement cases, which must not establish retirement"; VER-006 "use existing records or clearly labelled fixtures, not fabricated live acts" | As above |

**Overtaken or lagging text** (inference):

- TBD-002 reads OI-017 and OI-018 as open. OI-017 now reads `RESOLVED_FOR_CURRENT_DEFINITION_RUN` (CURRENT_EXECUTION_BASIS.md `99d0800967fb16fd`, scoped to this definition run). OI-018's Consequence column says the App part is "answered by DECISION-K3 K-9 as amended by DECISION-L L-2"; "hosts and other instruction owners remain open". The wording is a candidate for the next amendment (R23-11); the design follows the current state (R23-7).
- CLM-002 calls the inputs "PKG-10 historical applicability and active-consumer maps". DEL-10-03 and DEL-10-01 have no Design yet (S2-E surveys them now), so the map's shape is not fixed.

### A2. Joins

Consumes (admitted): DEL-10-03 (DEP-11-01-008: "historical applicability, active-consumer, packaging and tool-path account"), DEL-10-01 (DEP-11-01-009: "actual manual/method pins … distinguishing this run selection from adoption or instruction supply"), DEL-11-02 (DEP-11-01-010: "absence or uncertainty remains visible rather than being inferred from publication, files or run selection"). Supplies (held, SCC-006): DEL-11-03 (DEP-11-01-011 / DEP-11-03-008). Receives later (held): the owner disposition from DEL-11-03 (DEP-11-03-015). Non-topological: DEP-11-01-012, the thesis tree `47fc49e…` as comparison basis (C-5).

What existing Design files assume of DEL-11-01: no first-increment, pass-3 or tranche-1 Design file names DEL-11-01 (grep over every `Design/*.md`). Tranche-1's DOS-v0.1 and SQ-v0.2 address DEL-11-03 only. DEL-10-01 CLM-005 and DEL-10-03 CLM-005 (ScopeOfWork text, not Design) assign "preserved-history/coexistence production" to DEL-11-01.

### A3. Proposed contract changes still open

None. The SCA-V4-003 ledger (`LEDGER.csv` `e28661cdf3375e15`) has no row naming DEL-11-01; the closure audit `ScopeClosure_SCA-V4-003_2026-10-03_2028` lists its files only in its input manifest. Candidates for the next amendment (inference): TBD-002's OI-017/OI-018 wording.

### A4. Open items, and who decides

| Item | Shapes design now? | What the files say; proposed answer | Who decides |
|---|---|---|---|
| **OI-024: first adopters, continuing obligations, end of coexistence** (TBD-001) | No for structure: OUT-003 is a record of obligations, dispositions and their owners whatever the answer | Register: Owner "Owner with affected consumers", point of need "Before each adoption/retirement decision". AX-002: "First adopters and end conditions remain actual owner decisions". | **Reserved to the person (with affected consumers). An act later, per decision; not a question now.** |
| **OQ-12: chat migration and ending coexistence** | No | PRD OQ-12: "No initial chat-import obligation or automatic retirement"; Owner "Owner with affected consumers"; needed "Before any migration/retirement act" | **Reserved. Act later.** |
| What the "identified coexistence scope" contains | **Yes** (OUT-001's classes, OUT-003's rows) | Proposed, DERIVED from REQ-001, d7's "What to carry" list and existing records: (a) the v3.0.1 fallback (C-4); (b) the App v3 lane `projects/chirality-app-dev`, still active (225 commits touching it after `485051eac9` up to HEAD, by `git rev-list --count`); (c) the 19 Git-ignored archive locations of `reference/archives/ARCHIVES.md` (`b791f8390b9423f5`); (d) the thesis; (e) the read-only external archive named in `HANDOFF_30_PERCENT.md` line 18 (its path is a home path and is not repeated here); (f) the consumers DEP-006 names (Root, Runtime, App, Piping) | HELP_HUMAN rules; the App continuity owner applies it |
| Form of the inventory: new inventory or linked view | **Yes** | AX-003: "reuses primary records and avoids a new whole-corpus archival audit or duplicate evidence system"; V4-OPS-31. Proposed, DERIVED: a linked view over REFERENCES §2, ARCHIVES.md with `archive_digests.py verify`, SOURCE_INVENTORY.md (`4008921d7f826122`), the thesis tree identity and the run records, adding only what none of them carries (standing, current selector, owner, point of need) | HELP_HUMAN rules |
| Thesis check method (VER-003) | Yes (the check's definition) | Proposed, DERIVED: the committed-tree identity against `47fc49e…` plus a clean working-tree check (C-5), with an in-memory negative (omitted, added, changed entry) as VER-003 requires; attribution/standing inspected against PRD §11 and the thesis front matter | Ordinary design decision of the owner of DEL-11-01 |
| Archive check under a public repository | Partly | ARCHIVES.md: committed digests name nothing below the 19 locations; `verify` recomputes locally. Proposed, INTEGRATION: OUT-002's "named preserved material" check reuses `verify` and records its result with the limit that the check runs only on the original checkout | O-F's ordinary decision |
| OI-017 / OI-018 status (TBD-002) | No | Carried as in A1 | Not the person now (OI-017's owner is the project-definition manager) |
| SCC-006 design treatment | Yes (where the disposition record lives and when DEL-11-01 updates) | Proposed, INTEGRATION: SCC-CASE-007's R1 for design purposes. DEL-11-01's account is versioned; it reads "replacement pending; v3.0.1 retained" until a disposition is returned, then records that disposition as received. No row change; graph treatment stays with the DAG process | HELP_HUMAN rules for design; the graph treatment is not needed now (held arcs are non-gating) |

### A5. What exists to build on

- **Already-built preservation records (v4 conceptual stage, states):** REFERENCES.md §1–§3 (investigation revision, the fallback, the original checkout); ARCHIVES.md with `archive_digests.py` (`84ca3b480cba1a17`; "19 locations, 57,073 files"; `verify` "names any location or subtree that changed"); SOURCE_INVENTORY.md §4 "Chirality App v3 (the fallback line)". The archive check was not run by this survey.
- **Root history mechanism:** annotated tag `archive/agent-runs-2026-09-25` holds closed agent run records moved out of the working tree (REFERENCES §4; the tag exists, `git tag -l`).
- **App v3 exemplar (evidence only):** `execution/_Coordination/_TaskManagement/APP_REMAINING_RETIREMENT_2026-09-22/` — an owner-directed retirement of v3's "App Remaining" task entries, with a finite decision packet, per-row dispositions (`ROWS.csv`) and a closeout. Inference: it is a worked precedent for OUT-003's "disposition before retirement" record, at a different subject (task entries, not a product).
- **DEL-01-01 facts, protocol types:** not relevant to this deliverable.

### A6. External parties

PEC and Domains: no role (neither is in DEP-006's consumer list). Affected project owners (App v3, Runtime, Piping, Root): they own their lanes' continuing obligations. **Designable now without them:** the account's structure; the fallback, thesis and archive identity checks (local); the coexistence scope; the obligation-row form with owner and point of need. **Waits for them:** each lane's actual obligation dispositions and any retirement intent (DEP-006, OI-024). Piping's part reaches it only through the human relay, and Piping-side retirement is not this App's to propose (inference from OPERATING_METHOD §6).

### A7. Design scope for this pass

1. `Design/CONTINUITY_ACCOUNT.md`: the preservation classes (REQ-001), the coexistence scope as ruled, each class's record as a linked view (source, identity, standing, current selector, recovery route, owner, point of need), and the versioning rule for SCC-006 (account version → package → disposition → next version).
2. A continuity-account schema with valid and invalid examples, including the DEL-11-03 handoff block (the first-cut interface the early unit tests).
3. The identity checks: the thesis tree check with its in-memory negatives, the archive `verify` reuse, the fallback identity record from REFERENCES §2 with its "not re-checked remotely" limit.
4. The continuing-obligation table (OUT-003): row form; how a disposition's evidence is cited; the "fallback replacement alone" negative (VER-005); faithful recording of an owner act (VER-006) using existing owner-decision records.
5. Failure behaviour: an input not supplied (PKG-10 map, DEL-11-02 status) stays *not supplied*; a changed archive subtree is a discrepancy, never normalized.

Leave out: any archival audit, migration, chat import, retirement proposal for another lane, and PKG-10's maps themselves.

---

## Part B — DEL-11-02 Consumer-specific renewed-basis adoption

DOC_UPDATE. Responsible party: the App adoption coordinator; "each receiving consumer owner decides and performs that consumer's adoption". Scope SOW-250, 254, 255, 256, 257; OBJ-009.

### B1. Obligations (3 OUT, 7 REQ, 6 AC, 6 VER; also 5 CLM, 3 AX, 6 TBD)

| ID | One line | Rests on |
|---|---|---|
| OUT-001 | Consumer/scope/source-identity/adoption-point account: renewed and prior basis, publication/supply/adoption evidence, notices, decisions, departures | d1, d7; V4-OPS-11…14 |
| OUT-002 | Current-source applicability account for Root/Runtime/App/Piping consumers, packaging, tool paths, dependencies, with later-mainline comparison against the research pin `e548d4c…` | d1, d7; ARCHITECTURE §5 |
| OUT-003 | Received SoW-change and verification account tracing technical promises through consumer owners' SoWs to returned changes, checks and remaining obligations | d7; DEP-006 |
| REQ-001 | Per consumer and scope: responsible owner, old and new basis, adoption point or unresolved; prepared notice, delivery, publication, resolved content, supply, provider adoption, observed behaviour and consumer adoption kept apart | CLM-005; V4-OPS-14 |
| REQ-002 | Supplied instructions traceable to source-qualified origin, edition, content identity and adoption point; prior identities preserved; run selection ≠ project adoption | V4-OPS-11…14 |
| REQ-003 | Affected Root material and consumers, packaging, tool paths, dependencies; compare later mainline before relying on the pinned research | d1, d7 (#sources); SOW-257 |
| REQ-004 | Technical changes traced into owners' SoWs with promise, scope, owner, verification, returned evidence or gap | CLM-002, CLM-003 |
| REQ-005 | Who decided or acted, subject, scope, evidence, recorder; faithful recording allowed; no fabricated decision; no blanket acceptance-before-checking | V4-OPS-21, 31, 33 |
| REQ-006 | TBD-001…TBD-006 carried with owners and points of need; missing adoption visible before a consumer relies | V4-OPS-22, 23, 33; DEP-006 |
| REQ-007 | Performs no act of DEL-10-03, PKG-02…05 owners, receiving consumers, SWBPIPE, DEL-11-01, DEL-11-03 or the owner | CLM-002…CLM-004 |
| AC-001…AC-006 | Coverage with owners and evidence (AC-001); separately warranted states and actor/recorder custody (AC-002); instruction identity and history (AC-003); currency comparison before reliance (AC-004); promise-to-change trace (AC-005); open owners kept, no invented architecture (AC-006) | As REQ |
| VER-001…VER-006 | One per AC. VER-002 names four unsupported-state cases ("publication with no supply evidence; resolved content with no provider-adoption evidence; provider adoption with no behavior witness; and App adoption with no other consumer adoption") and a faithful human-adoption case; "no fabricated case is a real adoption witness" | As above |

The SoW also says the outputs "do not require a new register, transport or storage schema" and the methods "do not add … a new distribution mechanism".

**Overtaken or lagging text** (inference): TBD-001 (OI-017) and TBD-002 (OI-018) as in A1. Since the SoW was written, a real renewed-basis change has happened (B5), so the account has actual material.

### B2. Joins

Consumes (admitted): DEL-10-03 (DEP-11-02-008), DEL-10-01 (DEP-10-01-020, the supplier's row only), DEL-02-04 (DEP-02-04-013, the supplier's row only). Supplies (admitted): DEL-11-01 (DEP-11-01-010 / DEP-11-02-014) and DEL-11-03 (DEP-11-02-015, supplier's row only). Package-level and external inputs (NOT_TOPOLOGICAL): PKG-02, 03, 04, 05 (DEP-11-02-009…012); DEP-006 (DEP-11-02-013); later mainline changes (DEP-11-02-016, target UNKNOWN); OI-017, 018, 019, 020, 024, 014 (DEP-11-02-017…022).

What the Design files assume of DEL-11-02:

- **DEL-02-04 ROLE-v0.2** (`c8474d919bceec7d`), the only Design file that names it. §1: "consumer adoption (DEL-11-02)" is outside ROLE. §6.4 "The five facts kept apart" (selection, source resolution, supply, provider adoption, observed behaviour) ends with "Consumer adoption | Not here. DEL-11-02 records the adopting consumer's actor and scope | … | never inferred from supply or publication". Provider adoption is `adoption: unknown` in every ROLE record. §7.2 O-3: "DEL-11-02: the same evidence, no adoption claim" via DEP-02-04-013. §11 VC-R5: "positive consumer adoption … AWAITING INPUT". U-R8: "Consumer adoption evidence (OI-024; DEP-006) | Owner with consumers | Before adoption". ROLE also defines the App's own guidance store: "shipped defaults, seeded editable copy, release upgrade".
- **DEL-03-04 GUIDE-v0.7** (`a656682e2584ea86`) does not name DEL-11-02, but its pin set (25 contracts, R23-29) is the App/shared contract set a host would adopt. Inference: for Piping, OUT-003's promise-to-change trace runs through GUIDE's pin set, under DEP-001 and DEP-006.
- No other Design file names DEL-11-02.

### B3. Proposed contract changes still open

One. `LEDGER.csv` row **R22-7-open**: "No row proposed: the consumer-side counterpart owed by DEL-11-02 stays open with DEL-11-02's owner" (Disposition DEFER, owner item Q-15; R22-7: "records them open with DEL-11-02's owner (DEL-11-02 is outside the design passes)"). Inference: the same pattern applies to DEP-10-01-020 (no consumer row in DEL-11-02's register). Both have no graph effect (each arc exists through the supplier's row).

### B4. Open items, and who decides

| Item | Shapes design now? | What the files say; proposed answer | Who decides |
|---|---|---|---|
| **OI-024 staged adoption of the renewed basis** (TBD-005) | No for structure | As in A4 | **Reserved (Owner with affected consumers). Act later.** |
| **OI-020 manual revision authorship and approval** (TBD-004) | No | Register Owner "Owner", point of need "Before revising manuals from feedback"; V4-OPS-23: "The human retains consequential direction and adoption; agents can prepare changes when separately authorized." No manual revision is proposed now | **Reserved. Act later, only if a revision is proposed.** |
| OI-019 consequential manual gaps (TBD-003) | No | "Owner with execution manager", "When consequential gap affects selected work"; Consequence: "Do not use uncertainty alone to add prompts or halt independent preparation" | Conditional; not a question now |
| OI-018 distribution arrangement (TBD-002) | **Yes** (what OUT-001 records as "supply") | App part answered (K-9 as amended by L-2); hosts and other instruction owners open. Root already has a working arrangement: instruction tranches with an `m6_notice` that routes notices, and AGENTS.md: "Notices communicate changes; each receiving loop decides its adoption and updates its own accepted basis." Proposed, DERIVED: OUT-001 records adoption through that existing arrangement and the App's own (ROLE §4) and designs none (the SoW forbids "a new distribution mechanism"). The host remainder waits for host joins | HELP_HUMAN rules; the host remainder is not a question now |
| Who performs a consumer's adoption | **Yes** (actor column) | CLM-003 and Root AGENTS.md: the receiving loop. Proposed, DERIVED: a routine adoption of a changed instruction is the receiving loop's act (for App v4 it was HELP_HUMAN's ruling R23-30), not reserved to the person unless that loop's instruments reserve it; OI-024's owner decision is the staged adoption and retirement of the renewed v4 basis, not every notice | HELP_HUMAN rules |
| OI-014 shared placement (TBD-006) | No | "App/shared contract owners"; carried | Not the person |
| OI-017 edition pins (TBD-001) | No | Resolved for this definition run (CURRENT_EXECUTION_BASIS.md) | Project-definition manager |
| "Affected consumers" inventory | **Yes** (OUT-001/002 rows) | Comes from DEL-10-03's responsibility account (not designed; S2-E). Proposed, INTEGRATION: DEL-11-02 consumes DEL-10-03's consumer list and does not build a second one; until it exists, DEP-006's four consumers plus the App's own guidance store are the rows, each marked as provisional | O-F with O-E; HELP_HUMAN if they disagree |
| Research-pin currency (REQ-003, SOW-257) | No for structure | Compare only when a consumer relies on the pinned research as an implementation map; record coverage | O-F's ordinary decision |

### B5. What exists to build on

- **A real renewed-basis change, end to end in files: D-GOV-52.** Root `AGENTS.md` changed from sha256 `c8ce87ef…` to `f96feb19d297c74e…` (current file hash recomputed: equal) in tranche `ROOT-DGOV52-APPLICATION-20261004` (manifest `559dcf4316d1e0e1`). The owner approved the change ("I approve A1 and B1, go ahead", OWNER_DECISIONS_2.md). The manifest's `m6_notice` routed notices to App v4 (`a643415cb3109edf`), App v3 and Runtime (`5f4fb4d995cdf7e8` each); "Piping and PEC hold no pin or copy of either passage and read Root AGENTS.md live." App v4's adoption is recorded as HELP_HUMAN's ruling R23-30 ("App v4 adopts the changed Root text"), with Design-file updates deferred to each file's next revision. What this shows for OUT-001 (inference): the owner approved the **Root change**; the **App v4 adoption** is a separate act by App v4's coordinator; for App v3 and Runtime only a **notice** exists. Each notice's "This loop:" paragraph ("No adoption work is expected") was written by the sending tranche, not by the receiving loop, so the receiving decision is *not recorded*. The App v3 and Runtime notices are byte-identical, and the Runtime copy speaks of "the v3 idle-boundary path and RB-SETTINGS" (inference: text written for App v3). These are exactly VER-002's "prepared notice ≠ adoption" cases, on real records.
- **ROLE-v0.2 §6.4** gives the five-fact separation DEL-11-02 extends with the sixth (consumer adoption).
- **CURRENT_EXECUTION_BASIS.md**: the selected manual editions with sha256 and source-qualified workflow identities, labelled "not broader program/consumer adoption".
- **App v3 exemplar (evidence only):** v3's instruction bundle and seeded editable copy (`projects/chirality-app-dev/instructions/`), and earlier Root notices in v3's `_Coordination` (for example `NOTICE_2026-09-22_ROOT_D-GOV-44_…`). Inference: v3 is itself one of DEL-11-02's consumers, not only an exemplar.

### B6. External parties

PEC: not a DEP-006 consumer; D-GOV-52 sent PEC no notice. Domains: none. Root, Runtime, App v3 and Piping loops: they decide and perform their adoptions. **Designable now without them:** the account form; the six-state separation; the D-GOV-52 trace as the first real entry; the currency-comparison method. **Waits for them:** every receiving decision. For Piping, notices go only by human relay and the host-side instruction arrangement waits for host joins (OI-018 host part; DECISION-3).

### B7. Design scope for this pass

1. `Design/ADOPTION_ACCOUNT.md`: the consumer/scope row (consumer, owner, prior basis, renewed basis, source identity, adoption point) with six separately warranted states (prepared notice, delivered, published/resolved, supplied, provider-adopted, consumer-adopted), each with its evidence kind and who can produce it; actor ≠ recorder.
2. The first real entry: D-GOV-52 for App v4 (adopted, actor and record named), App v3 and Runtime (notice delivered; receiving decision not recorded), Piping and PEC (no notice by design, with the manifest's reason).
3. The OUT-002 currency-comparison method (scope, revisions, result, coverage) and OUT-003's promise-to-change trace form, keyed to DEL-10-03's allocation.
4. The handoffs to DEL-11-01 (adoption status) and DEL-11-03 (adoption status relevant to replacement), with "not supplied" as a first-class value.
5. Failure behaviour: a notice without a receiving record stays *notice only*; a consumer whose owner is unknown is a named gap.

Leave out: any distribution mechanism, edits to another loop's instructions or basis, and the allocation of shared promises (DEL-10-03).

---

## Part C — DEL-11-03 Owner replacement evidence packet

DOC. Responsible party: the App replacement-evidence coordinator; "The owner alone decides fallback replacement after considering both obligations". Scope SOW-111, 112, 113; OBJ-009.

### C1. Obligations (3 OUT, 6 REQ, 6 AC, 6 VER; also 4 CLM, 3 AX, 3 TBD)

| ID | One line | Rests on |
|---|---|---|
| OUT-001 | Candidate-specific v3.0.1 core-loop comparison from the DEL-09-02 dossier: planning, execution, workflow saving, reuse, approvals, interruption, restart | PRD V4-REP-01; EXAMINATION §7, V4-EXM-10/11 |
| OUT-002 | Linked live local-model SWBPIPE request-to-acceptance evidence from the DEL-09-07 dossier | V4-REP-01; V4-EXM-20; EXAMINATION §7 |
| OUT-003 | Exact owner replacement decision package and actual disposition record, with practitioner observations and DEL-11-01's continuity account | PRD §8; EXAMINATION §7; d7 |
| REQ-001 | Compare the candidate against the named v3.0.1 baseline per element; no general claim stands for a missing element | V4-REP-01; EXAMINATION §7 |
| REQ-002 | One actual live local-model embedded journey from request to the person's acceptance, from the joined dossier; acceptance distinct from execution, checking, approval, reliance | V4-EXM-20; V4-AUT-03/05 |
| REQ-003 | Candidate, configuration, date, source route, outcome on all evidence; changed candidate needs applicability; nothing promoted into qualification; practitioner validation separate, "no unagreed validation period or favorable outcome is inserted" | V4-EXM-01, 03, 05; EXAMINATION §2 |
| REQ-004 | Both obligations and standing before the owner; exact scope and candidate; disposition only from an attributable owner act; "observed recording time from any unavailable act time"; "A favorable result is never a completion criterion" | PRD §8; CLM-001 |
| REQ-005 | Continuity account and open matters; no silent retirement; "Domains and PEC are not initial replacement prerequisites"; "without inventing a third fixed-duration replacement gate" | PRD §8; EXAMINATION §7; OPERATING_METHOD §5 |
| REQ-006 | Performs no act of DEL-09-02, 09-07, 11-01, 09-12, SWBPIPE, the person, the owner (replacement, validation choice, release), consumers, or the accountable professional | CLM-001…CLM-004 |
| AC-001…AC-006 | Baseline and candidate identified, every element evidenced or the obligation unmet (AC-001); journey established or reported incomplete (AC-002); standing for both obligations and practitioner validation (AC-003); exact subject, faithful disposition, pending keeps v3.0.1 (AC-004); continuity and open owners, no PEC/Domains gates, no invented period (AC-005); one-for-one ownership (AC-006) | As REQ |
| VER-001…VER-006 | One per AC. VER-001 rejects "at-least-v3.0.1 coverage when any required element lacks applicable evidence"; VER-003 negatives: "a historical pass, initialized contract, Git merge, source inspection and isolated first-host success"; VER-004: "No new human act is requested merely to run this check" | As above |

**Overtaken or lagging text** (inference): TBD-002 says OI-021 remains open and DEP-001 is required — still true, and DECISION-3 now defers the host joins, so OUT-002 cannot be evidenced in this pass. CLM-004 still reads OI-001 as unresolved; D2 ruled it for App/shared contracts (Open_Issues Consequence column). Carry to the next amendment (R23-11).

### C2. Joins

Consumes (admitted): DEL-09-02 (DEP-11-03-006), DEL-09-07 (DEP-11-03-007), DEL-09-12 (DEP-11-03-009), DEL-11-02 (DEP-11-02-015). Consumes (held): DEL-11-01 (DEP-11-03-008). Returns (held): the disposition to DEL-11-01 (DEP-11-03-015). Non-topological: the v3.0.1 baseline (DEP-11-03-010, target UNKNOWN), the accepted and current Open_Issues rows (-011, -012), the owner as decision maker (-013, -014), affected consumers (-016).

What the tranche-1 Design files already require of DEL-11-03, by section:

- **DEL-09-02 SQ-v0.2** (`3e5d0f12c6190710`). §1: "Replacement decision | The owner (DEL-11-03 prepares) | Not claimed (SQ-R5)". §2 O-1: "The dossier (§5) | → DEL-11-03 | … | After the run | DEL-11-03 has no standalone evidence". §8: the dossier supplies "scenario outcomes, evidence limits, input gaps, affected rechecks, the **core-loop mapping** and **v3 comparison inputs**"; each step carries `core_loop_element` and `v3_reference` (App v3 `JOURNEY_RESULTS.md` J02…J09, or "none recorded"); "The comparison itself is DEL-11-03's act; v3 evidence qualifies nothing in v4." Schema (`sq.dossier.schema.json` `16f7f2325e7d5142`): `handoff` has `to: "DEL-11-03"`, `supplies` (six values), `not_claimed` (six values: joined_host_witness, replacement, public_release, retirement, professional_reliance, practitioner_validation), `handed_over`, `reported_as_independent`; `core_loop_element` is a free string ("DEL-11-03 REQ-001 element this step bears on"); `check_sq.py` checks that the seven elements are covered.
- **DEL-09-07 DOS-v0.1** (`b2ffba7135652c9e`). §1: independent examination is "Required before the dossier is handed to DEL-11-03". §4: the handoff names dossier identity, the CIR, the P20-A result and outcome, whether P20-A counts, acceptance acts (actor, recorder), receipts with resolution status, limits, the review record. **DH-1**: "P20-A counts only when its EXP outcome is `pass`, its run basis is `candidate`, it has no open review finding, and it names a local model server". **DH-2**: "The owner decides replacement (V4-REP-01)". Schema `handoff_del_11_03` (`lhq.dossier-manifest.schema.json` `88cd994821c25422`) fixes the statement "Evidence for the owner's replacement judgment; not a replacement decision, release or professional reliance." DF-5: session-only receipts are handed over as *unresolvable*.
- **DEL-09-07 LHQ-v0.1** (`20361a0be76904d4`). §341: "Replacement packet; replacement decision | DEL-11-03; the owner". The CIR (LHQ §3) has an `app_candidate` element; its open row: "OI-013/OI-014: whether the minimal loop is shared code, and so what 'the identified App … candidate' contributes to an embedded journey … CIR records the App candidate whose contracts and workflow were used; its runtime role is *not supplied* until decided".
- **DEL-09-01 EXP-v0.2** (`ff0187dafd9e1f02`): the outcome vocabulary both dossiers use (`pass`, `fail`, `blocked`, `not-run`, `inconclusive`), the `candidate_subject` form {revision, build_identity, packaged, package_record}, and the change-impact record (`exam.change-impact.schema.json` `b8fcb4586aa8d844`) for a changed candidate.
- **DEL-09-06 CA-v0.7** §920: the "replacement packet" belongs to DEL-11-03, "Coordinated through §5 and §6; not performed".
- **DEL-01-06 PKG-v0.2** (`0d8d14d2ce08d859`) I-7: "Terms record | Here → the owner's distribution decision | … | Public release not possible; owner use unaffected"; U-PKG-7 (OI-007) "Before public release beyond owner use". Inference: PKG already separates owner use from public release, which the package's alternatives need (C4).

**Three identity forms for one App candidate** (states, compared by reading the schemas): EXP `candidate_subject` {revision, build_identity, packaged, package_record}; SQ `candidate` {revision, build_identity, codex_pin, package_record}; LHQ CIR `elements.app_candidate` (a generic element). DEL-11-03 VER-003 must reconcile them. See S-F1.

### C3. Proposed contract changes still open

No SCA-V4-003 row names DEL-11-03. Carried candidates (inference): CLM-004's OI-001 wording; consumer-side rows for DEP-11-02-015 (DEL-11-03 has no UPSTREAM row to DEL-11-02). No graph effect.

### C4. Open items, and who decides

| Item | Shapes design now? | What the files say; proposed answer | Who decides |
|---|---|---|---|
| **The replacement decision** | No (the package is designed for any answer, including none) | PRD §8: "The owner decides the replacement; the old projects and archives are kept until then (OD-09)." EXAMINATION §7: "The owner decides the replacement (V4-REP-01)." SOW-113: "Leave replacement of v3.0.1 to the owner after considering both obligations." | **Reserved to the person. An act later, when the evidence exists; not a question now.** |
| **Public release** (kept separate from replacement) | Partly (the alternatives must not merge the two) | PRD OQ-08: Owner, "Before public release". CLM-003: "The owner retains public-release decisions … None follows from replacement". | **Reserved. Act later, not this cluster's act.** |
| **OI-024 / OQ-12 retirement** | No | As A4 | **Reserved. Act later.** |
| **OI-021 connected activity** (TBD-002) | No for this deliverable | "Owner via outside SWB session and App/shared owner", "Before connected-activity SoW and execution"; deferred with host joins | **Reserved to the owner with the SWB session. Act later, at the host join.** |
| The v3.0.1 baseline locator (DEP-11-03-010) | **Yes** | SCC-CASE-007 Q3: "Replacement-evidence coordinator identifies the v3.0.1 reference". Proposed, DERIVED: REFERENCES.md §2 (C-4) is the baseline identity; its remote values are re-checked when the package is prepared | HELP_HUMAN rules; the coordinator applies |
| Whether v3.0.1 must be rerun side by side | **Yes** (OUT-001's shape) | EXAMINATION §7 defines the evidence: "V4-EXM-10 and V4-EXM-11 passed on the candidate App (the core loop at least at v3.0.1's level)". Proposed, DERIVED: no rerun; OUT-001 is a per-element account of the v4 results with the v3 reference as context. SQ's `v3_reference` cites JOURNEY_RESULTS (`cb2d6db922d17674`), whose later journeys ran on development candidate `266c121bb`; that commit is **not** an ancestor of the v3.0.1 source `485051eac9` (`git merge-base --is-ancestor`), while the baseline `26657ff90` and the v3.0.0 source `6f41f93e74` are. The v3 references therefore describe v3.0.0-era behaviour; OUT-001 states that limit (12 commits touching `projects/chirality-app-dev` lie between the v3.0.0 and v3.0.1 sources) | HELP_HUMAN rules |
| One candidate for both obligations | **Yes** (VER-003's reconciliation, the package subject) | EXAMINATION §7 says "the candidate App" in both clauses; V4-EXM-03: "A check that passed on an earlier candidate supports only that candidate". Proposed, DERIVED: the subject is one identified App candidate (plus the SWBPIPE candidate and local model server for OUT-002); a result on another App revision counts only with an EXP change-impact record showing the change does not touch it. The OI-013/OI-014 residue (what the App contributes to an embedded journey) is recorded as LHQ records it | HELP_HUMAN rules; OI-013/014 residue with the shared contract owner and SWB owner, at the host join |
| Practitioner validation as a condition | **Yes** (AC-003/AC-005 text) | PRD §8 lists two conditions; REQ-005 forbids "a third fixed-duration replacement gate"; EXAMINATION §7 names only V4-EXM-10/11/20. Proposed, DERIVED: not a condition; the package carries DEL-09-12's standing, including "not agreed" and "not started" | HELP_HUMAN rules |
| Package shape and how the owner's act is recorded | **Yes** (OUT-003's whole form) | R23-8 and R23-24 define a decision package file (`decisionPackageFile` in DEL-02-03's schema, `a5271857c8bf71f6`) and A16, whose subject is "an App file" decided through DEL-01-04's act control. The replacement decision is a project-level act about the product. The project already records such acts in OWNER_DECISIONS files: exact text, custody "the owner's chat messages … transcribed by the recorder … no platform timestamp" (DECISION-3's record), which meets REQ-004's custody and time terms. Proposed, INTEGRATION: (1) the package file uses the R23-24 shape (`actKind` A16, `reservedBy` PRD §8 / EXAMINATION §7, alternatives with consequences), with `subject` naming the candidate and the packet manifest by sha256 so a decision binds to the exact evidence; (2) the owner's act is recorded in the project's owner-decision form; if the owner instead decides through a candidate App's act control, that A16 record is cited as well. No ACT, RS, AAC or schema change | HELP_HUMAN rules |
| Replacement scope alternatives | Yes (the alternatives) | REFERENCES §2 calls v3.0.1 "The published product that remains the fallback"; v3's update check reads "its latest published stable release" (`projects/chirality-app-dev/docs/BUILD_AND_RELEASE.md` §12; v3 history), so a v4 published there as stable would be offered to v3.0.x users (inference). Proposed, DERIVED: the alternatives keep (a) the owner's own work moving to v4 with v3.0.1 still published, (b) v4 replacing v3.0.1 as the published product, which is also a public-release act, and (c) defer or decline, each with its consequences; the owner chooses at the act | Proposed by the coordinator; chosen by the owner at the act |
| Session-only host receipts (S1-C S-3) | Partly (OUT-002's receipt column) | DOS DF-5 hands them over as *unresolvable*. A basis-level tension, not a design choice | Not a question now; SWBPIPE owner decision when host joins resume |

### C5. What exists to build on

- **The two supplier handoffs**, each with schema and valid and invalid examples (C2): `sq.dossier.valid.examples.json` (`426165ba047ac7c5`), `lhq.dossier-manifest.valid.examples.json` (`4d659926675a5c7e`). These are test-double material; no candidate exists.
- **The early path E's tooling** (`RUN/E/`): `decision_view.py` (`6fae1738275cadf5`), `run_e.py` (`81c973de992de646`), the R23-24 package example `decision-package-file.example.valid.json` (`3ea08ff575698e76`), and the isolated-reader method of RR-E and RR-F (`DISPATCH_RECORD.md`, `SUPPLIED.sha256`, examiner comparison).
- **The fallback identity** (C-4) and the v3 release history: v3.0.0 publication record (`PUBLIC_RELEASE_20260913.md` `b2b0bab9b1af29da`) and v3's record of prior owner release authority (D-APP-131 P-03, cited in v3 `BUILD_AND_RELEASE.md`). Inference: v3's owner acts authorized exact-candidate releases; that is a precedent for binding the owner's act to an exact candidate, not a v4 commitment.
- **DEL-01-01 facts:** only the identity values (HOSTING-v0.9 §7.1, VERSION_ADVANCE_0.160.0 under R23-22) that the candidate records carry. The generated protocol types are not relevant here.

### C6. External parties

PEC and Domains: not prerequisites (PRD §8: "Domains is not a prerequisite to the initial V4-REP-01 journey … PEC is likewise not a v4 start gate"). SWBPIPE: OUT-002 waits for DEL-09-07's live journey, which waits for the host joins (DECISION-3) and OI-021. Practitioner: only DEL-09-12's standing is consumed. **Designable now without them:** the packet manifest, OUT-001's per-element table and OUT-002's journey table over the suppliers' example dossiers, candidate reconciliation, the package and its alternatives, the disposition record, all negatives of VER-001…VER-006. **Waits:** every actual result; the owner's act.

### C7. Design scope for this pass

1. `Design/REPLACEMENT_PACKET.md`: the packet manifest (candidate subject, the two obligation accounts, practitioner standing, continuity account, adoption status, open matters with owners and points of need), its versioning and its relation to the package file.
2. OUT-001: the seven-element table keyed to SQ's `core_loop_element` values (a closed list owned here), v3.0.1 reference per element with its limit, and the rule from VER-001.
3. OUT-002: the journey table from DOS's `handoff_del_11_03` with DH-1 applied as written; receipts with resolution status.
4. Candidate reconciliation (VER-003) across EXP, SQ and the CIR, with the change-impact rule.
5. OUT-003: the package file (R23-24 shape) with its alternatives and consequences; the disposition record (pending, deferred, negative, favourable; custody; act time vs recording time); the return to DEL-11-01 and to affected consumers.
6. A schema for the packet manifest and the disposition record, valid and invalid examples, and a prototype check of the packet rules.

Leave out: running or assembling any qualification, choosing OI-021, any release step, and retirement.

---

## Part D — DEL-09-12 Practitioner validation and feedback disposition

TEST_SUITE-like DOC in PKG-09. Responsible party: "Owner as practitioner; App validation coordinator routes observations to responsible owners." Scope SOW-207, 208, 209; OBJ-008, OBJ-010. SOW-264 (OI-016) is an open interface, not locally allocated scope.

### D1. Obligations (3 OUT, 6 REQ, 6 AC, 6 VER; also 5 CLM, 3 AX, 4 TBD)

| ID | One line | Rests on |
|---|---|---|
| OUT-001 | Documented agreement on App and SWBPIPE validation activities and period: the owner's selected work, material, candidates, agreement evidence; pending stays explicit | V4-EXM-40; OI-016 (App v4) |
| OUT-002 | Source-linked account of actual observations (confidence for attention, workarounds, perception gaps, missing or unused records), per expression, candidate, configuration, date, conditions, limits | V4-EXM-41; V4-EXM-01/03 |
| OUT-003 | Traceable dispositions to the owning requirement, workflow or method, with recipient, proposed treatment, actual decision; successor-basis (v5.0) proposals kept with their standing | V4-EXM-42; V4-OPS-20…23 |
| REQ-001 | Arrange and preserve the owner's actual agreement for both expressions; a coordinator's plan is neither agreement nor use | V4-EXM-40; OI-016 |
| REQ-002 | Actual observations and limits; "without numerical pass scores or an assumed favorable fitness conclusion"; absence of an issue does not prove unobserved use | V4-EXM-41; V4-EXM-01, 03 |
| REQ-003 | Acts attributable to their actual actors; faithful recording allowed; no fabricated act; consumes adopted policy without settling the reserved list | V4-AUT-01…04; V4-HI-30…33 |
| REQ-004 | Route each observation to its owner with source identity, conditions, recipient, disposition; method feedback cites the manual section and work-graph node | V4-EXM-42; V4-OPS-20…23, 31, 32 |
| REQ-005 | Carry OI-016 exactly; OI-001/002 and OI-021 where selected work depends on them; OI-024 for transition consequences | Open_Issues |
| REQ-006 | Performs no act of DEL-09-01, feature owners, DEL-10-01/10-02, SWBPIPE, DEL-04-01, the owner, DEL-11-01, consumers or the human | CLM-003…CLM-005 |
| AC-001…AC-006 | Agreement identified or the obligation unmet (AC-001); real observations for all four aims, no fixture pass, "no numeric score or positive outcome is required" (AC-002); act attribution (AC-003); observation-to-recipient trace (AC-004); open owners kept, no invented period (AC-005); one-for-one ownership (AC-006) | As REQ |
| VER-001…VER-006 | One per AC. VER-002 distinguishes "preparation, review, repair, integration, recovery and waiting by cause" when like work is compared; VER-003's illustrative cases "are not actual practitioner observations" | As above |

**Overtaken or lagging text** (inference): TBD-002 reads OI-001/OI-002 as open; D2/D3 ruled them for the App (Open_Issues Consequence columns). Carry to the next amendment (R23-11).

### D2. Joins

Consumes (admitted): DEL-04-01 (DEP-09-12-011), DEL-09-01 (DEP-09-01-029, supplier's row only). Consumed by (admitted): DEL-10-02 (DEP-09-12-012), DEL-11-03 (DEP-11-03-009). Non-topological: OI-016 agreement (-007), identified App candidate (-008, UNKNOWN), DEP-001 SWBPIPE (-009), the owner's use records (-010), feature-owner recipients (-013, UNKNOWN), OI-021 (-014).

What the Design files assume of DEL-09-12:

- **DEL-09-01 EXP-v0.2** §1: "Practitioner validation and its period | DEL-09-12 with the owner (OI-016) | Records `activity: validation` only for an actual practitioner's use (§3.3)". §3.3: "`validation` (a practitioner's actual use, DEL-09-12's activity; requires the practitioner and a candidate basis). Neither substitutes for the other". U-EXP-6: "OI-016 validation period and activities | Owner | Before validation in use". The result-record schema (`f7871c96cef25bb9`) requires `case`, `criterion`, `outcome` (pass/fail/blocked/not-run/inconclusive) for every record, and for `activity: validation` also `practitioner` and `run_basis: candidate`. See S-F3.
- **DEL-04-01 ACT-POLICY-v0.10** (`1bf0ce8e413d2b8f`) §10.3: "DEL-09-12 | DEP-09-12-011 | none | Not mapped in detail". ACT's §2.1 act kinds (A4…A16) are what the owner performs inside a candidate during use.
- **DEL-09-02 SQ-v0.2**: `not_claimed` includes `practitioner_validation`; agent-operated scenarios never stand for validation.
- No other Design file names DEL-09-12.

### D3. Proposed contract changes still open

None in the SCA-V4-003 ledger. Candidates (inference): TBD-002's OI-001/002 wording; a consumer-side row to DEL-09-01 and a mirror on DEL-10-02's side (no graph effect).

### D4. Open items, and who decides

| Item | Shapes design now? | What the files say; proposed answer | Who decides |
|---|---|---|---|
| **OI-016 (App v4): validation period and owner-selected activities** | No for structure (OUT-001 is a record of the agreement whatever it says) | Register: Owner "Owner", point of need "Before practitioner validation in use", resolution "Agree period and owner-selected activities." V4-EXM-40: "real design work of the owner's choosing over an agreed period, in both the Chirality App and SWBPIPE". SOW-264: "Agree the owner's validation period and selected realistic activities before validation in use." | **Reserved to the person. An act later, when candidates exist; not a question now.** |
| **The owner's use and fitness judgments** | No | CLM-002: "the owner is the principal v4.0 practitioner"; V4-EXM-41 names "the owner's measure" (`plans/evidence/2026-09-19_owner_words_four_graph_structures.md`, `886195b2e442f6bc`) | **The person's activity. Later.** |
| **Consequential method or basis changes from feedback** (OI-020; v5.0 proposals) | No | OI-020 as B4; V4-EXM-42: observations "may reopen affected commitments … including a future v5.0 basis"; V4-OPS-21: "Preserve who decided and what the decision actually covers" | **Reserved where consequential. Act later, conditional.** |
| Whether the two expressions share one period or are staged | No for structure | V4-EXM-40 says "an agreed period, in both". Proposed, DERIVED: the arrangement record allows one period or one per expression; the owner chooses at agreement. The App expression could start before SWBPIPE's (host joins deferred) only if the owner so agrees | The owner, inside the OI-016 act; not a separate question |
| The observation record (OUT-002) and EXP's `activity: validation` | **Yes** | EXP requires an `outcome` and a `criterion` on every record; REQ-002/AC-002 exclude scores and any assumed favourable result. Proposed, INTEGRATION: DEL-09-12 keeps its own observation record, reusing EXP's `candidate_subject`, configuration and evidence-provenance labels (`live_observation`, `person_act`), and does not write an EXP result record as a verdict on fitness. Whether EXP's `validation` value is then used at all goes to O-B as a finding, not a change | HELP_HUMAN rules; O-B for EXP |
| Routing recipients (DEP-09-12-013, UNKNOWN) | Yes (OUT-003's recipient column) | Proposed, DERIVED: the deliverable that owns the implicated requirement, found through `_Decomposition/ScopeLedger.csv` `DeliverableIDs` and that SoW; method observations go to DEL-10-02 at the work-graph node (V4-OPS-20) | O-F's ordinary decision |
| OI-001/002 residue; OI-021; OI-024 (TBD-002…004) | No | Carried with their owners | Not questions now |

### D5. What exists to build on

- EXP-v0.2's candidate identity, configuration and provenance vocabulary; ACT's act kinds; RS-v0.10's human-act records (`2e7afb1bb8b872c0`) for acts the owner performs inside a candidate.
- The project's own owner-decision records (custody form) for the OI-016 agreement (C4's proposal applies the same way).
- **App v3 exemplar:** a grep over v3 `docs/` and `_Coordination` finds no practitioner-validation arrangement. v3's "validation" is software and governance evidence ("Validation evidence is software and governance evidence only", `docs/VALIDATION_STRATEGY.md` line 13). v3's journeys were agent-run scenario profiles ("not claims of longitudinal observation of real customers", JOURNEY_RESULTS). Inference: v3 offers no precedent for V4-EXM-40; the term itself changed meaning.

### D6. External parties

Practitioner: the owner; every observation waits for the owner's use of identified candidates. SWBPIPE: its expression waits for a SWBPIPE candidate with the embedded agent, which waits for the host joins (DECISION-3) and OI-021. PEC, Domains: none. **Designable now without them:** the arrangement record and its proposed form, the observation record with the four aims as fields (not scores), the routing and disposition records, the fabrication negatives, the handoffs to DEL-10-02 and DEL-11-03 with "not agreed / not started" as valid standings. **Waits:** the agreement, any use, any observation.

### D7. Design scope for this pass

1. `Design/PRACTITIONER_VALIDATION.md`: the arrangement record (proposed vs agreed, both expressions, candidates, material, period or periods, agreement evidence and custody), its states (proposed → agreed → in use → ended, or not agreed), and the rule that nothing before "agreed" counts as validation.
2. The observation record (OUT-002): expression, candidate, configuration, date, activity, the four V4-EXM-41 aims as observations, conditions, limits, unobserved coverage; no outcome field; source links.
3. The disposition record (OUT-003): observation → owning commitment → recipient → proposed treatment → actual decision (actor, scope), including successor-basis proposals.
4. The handoffs: to DEL-10-02 (method observations), to feature owners, to DEL-11-03 (practitioner standing, the early unit's input).
5. Schemas with valid and invalid examples (fabricated agreement from a plan; a fixture pass offered as validation; a numeric score).

Leave out: choosing activities or a period, any use, and any change to feature requirements or manuals.

---

## Part E — Merged results

### E1. Items genuinely reserved to the person

None is a question for the owner now. Each is an act the person performs when its point of need arrives; the design's job now is to prepare what that act needs.

| # | Item | Basis that reserves it (quoted) | Question now or act later |
|---|---|---|---|
| P-1 | Replacing v3.0.1 with v4 | PRD §8: "The owner decides the replacement; the old projects and archives are kept until then (OD-09)." EXAMINATION §7: "The owner decides the replacement (V4-REP-01)." DEL-11-03 CLM-001: "The owner alone decides fallback replacement after considering both obligations". | Act later: after DEL-09-02's and DEL-09-07's witnesses exist; the second waits on deferred host joins |
| P-2 | Agreeing validation activities and period, OI-016 (App v4) | Open_Issues: Owner "Owner"; "Agree period and owner-selected activities." V4-EXM-40: "real design work of the owner's choosing over an agreed period". | Act later: "Before practitioner validation in use"; needs candidates |
| P-3 | Doing the validation work and judging fitness | DEL-09-12 CLM-002: "the owner is the principal v4.0 practitioner"; V4-EXM-41: "the owner's measure". | Act (activity) later |
| P-4 | Staged adoption and retirement of the renewed basis; ending coexistence; chat migration (OI-024, OQ-12) | OI-024: Owner "Owner with affected consumers", "Before each adoption/retirement decision". DEL-11-01 AX-002: "First adopters and end conditions remain actual owner decisions". OQ-12: "Before any migration/retirement act". | Act later, once per decision |
| P-5 | Public release | PRD OQ-08: Owner, "Before public release". DEL-11-03 CLM-003: "The owner retains public-release decisions". | Act later; outside this cluster, kept separate from P-1 |
| P-6 | Consequential method or basis changes from feedback; manual revision arrangement (OI-020) | OI-020: Owner "Owner", "Before revising manuals from feedback". V4-OPS-23: "The human retains consequential direction and adoption". | Act later, only if feedback proposes such a change |
| P-7 | The first connected activity (OI-021) | OI-021: "Owner via outside SWB session and App/shared owner", "Before connected-activity SoW and execution". | Act later, at the host join (DECISION-3); shared with S2-D and tranche-1 owners |

Professional reliance belongs to the accountable professional (V4-AUT-05; DEL-11-03 REQ-006); no deliverable here touches it. The person's acceptance inside the V4-EXM-20 journey is DEL-09-07's observed act, not a decision for this cluster.

### E2. Proposed for HELP_HUMAN to rule

| ID | Question | Proposed answer | Label |
|---|---|---|---|
| F-R1 | What is the replacement subject? | One identified App candidate (with the SWBPIPE candidate and local model server for OUT-002). A result on another App revision counts only with an EXP change-impact record. The OI-013/014 residue stays as LHQ records it | DERIVED (EXAMINATION §7, V4-EXM-03) |
| F-R2 | Must v3.0.1 be rerun beside v4? | No. The baseline identity is REFERENCES §2; OUT-001 is per element; v3 references carry their limit (v3.0.0-era candidates; `266c121bb` outside v3.0.1's ancestry) | DERIVED (EXAMINATION §7) |
| F-R3 | Is practitioner validation a replacement condition? | No. Its standing is presented, including "not agreed" | DERIVED (PRD §8; DEL-11-03 REQ-005) |
| F-R4 | Package shape and record of the owner's replacement act | R23-24 package file (A16, `reservedBy` PRD §8/EXAMINATION §7, subject naming candidate and packet manifest by sha256); the act recorded in the project's owner-decision form, plus any A16 record if taken in a candidate. No ACT/RS/AAC/schema change | INTEGRATION |
| F-R5 | Replacement scope alternatives | Own-use move, published-product replacement (also a release act), defer or decline, each with consequences; the owner chooses at the act | DERIVED (REFERENCES §2; CLM-003; OQ-08) |
| F-R6 | DEL-11-01's coexistence scope and form | Scope as A4; a linked view over REFERENCES, ARCHIVES (with `verify`), SOURCE_INVENTORY, the thesis tree and run records | DERIVED (AX-003; V4-OPS-31; d7) |
| F-R7 | Thesis check method | Committed-tree identity plus clean working tree; in-memory negatives; attribution and standing inspected | DERIVED (PRD §11; VER-003) |
| F-R8 | SCC-006 treatment for design | SCC-CASE-007 R1: versioned account → package → disposition → next version; "replacement pending" until then; no row change | INTEGRATION |
| F-R9 | DEL-11-02's distribution arrangement | Record adoption through Root's existing tranche-and-notice arrangement and ROLE §4; design none; the host part waits | DERIVED (SoW VER text; Root AGENTS.md; OI-018 Consequence) |
| F-R10 | Who adopts a routine instruction change | The receiving loop; OI-024 covers the staged adoption and retirement of the renewed basis, not every notice | DERIVED (Root AGENTS.md; CLM-003) |
| F-R11 | DEL-11-02's consumer inventory | Consume DEL-10-03's list, which R23-31 item 7 bounds to its nine supplier rows plus DEP-006 and OI-013/014/018/024; until DEL-10-03's thin Design file exists, provisional rows from DEP-006 | INTEGRATION (with O-E; R23-31) |
| F-R12 | DEL-09-12's observation record vs EXP | Own record reusing EXP's identity and provenance parts; no EXP outcome as a fitness verdict; EXP's `validation` value referred to O-B as a finding | INTEGRATION |
| F-R13 | Observation routing | By the requirement's owning deliverable (ScopeLedger); method feedback to DEL-10-02 at the node | DERIVED (V4-OPS-20; REQ-004) |
| F-R14 | The two OI-016s | Always qualify: "OI-016 (App v4)" or "SWBPIPE OI-016"; note to the owners of LHQ and others at their next revision | DERIVED |
| F-R15 | Missing consumer-side rows (R22-7-open; DEL-11-02 → DEL-10-01; DEL-11-03 → DEL-11-02; DEL-09-12 → DEL-09-01; DEL-10-02's mirror) | Carry to the next amendment (R23-11), each through the reach script first (R23-2); no graph effect | INTEGRATION |
| F-R16 | D-GOV-52 notices to App v3 and Runtime | Record as "notice delivered; receiving decision not recorded". The Runtime notice's v3-specific "This loop" text is an observation for HELP_HUMAN, not a repair here | DERIVED (DEL-11-02 REQ-001, VER-002) |

### E3. External parties, in one place

- **PEC, Domains, connectors:** no deliverable here needs them. PRD §8 and DEL-11-03 REQ-005 exclude them as replacement prerequisites; DEP-006 does not list PEC as a consumer.
- **SWBPIPE:** DEL-11-03 OUT-002 and DEL-09-12's SWBPIPE expression wait for the host joins (DECISION-3), DEP-001 and OI-021. Everything else in both is designable now.
- **Practitioner (the owner):** all of DEL-09-12's evidence and DEL-11-03's practitioner standing wait for P-2 and P-3; their records are designable now.
- **Root, Runtime, App v3, Piping loops:** their adoption decisions and continuing-obligation dispositions (DEP-006) wait for them; the account forms and the D-GOV-52 trace are designable now.

### E4. Structural questions that could force a later restructuring

- **S-F1 One App candidate, three identity forms.** EXP `candidate_subject`, SQ `candidate` and the LHQ CIR's `app_candidate` element differ, and LHQ leaves the App candidate's runtime role in V4-EXM-20 *not supplied* (OI-013/014). DEL-11-03 must reconcile them (VER-003). If the CIR element cannot carry revision and build identity in a comparable form, SQ, DOS or EXP would need an aligned identity element (most likely a row-level change, but in three tranche-1 files). The early unit tests this first.
- **S-F2 The package file has no evidence element.** R23-24's `decisionPackageFile` is closed (`additionalProperties: false`): subject, purpose, scope, `reservedBy`, alternatives. F-R4 puts the packet manifest's identity inside `subject`. If that proves inadequate, DEL-02-03's schema (a shared file under R23-21) would need an additive optional property and a new version label.
- **S-F3 EXP's validation records require an outcome.** EXP-v0.2 requires `outcome` and `criterion` on every record, including `activity: validation`. Under F-R12 DEL-09-12 does not use them, which leaves EXP's `validation` value without a user. Otherwise EXP would need a row change, and relaxing a required field is the kind of check change that needs a ruling.
- **S-F4 The v3 reference evidence.** SQ's `v3_reference` cites v3.0.0-era journeys. Under F-R2 that is a stated limit. If v3.0.1-specific evidence were required, SQ's step-map data would change (not its structure).
- **S-F5 SCC-006.** A later graph choice of R2 (merge group) or R3 would change no Design file under F-R8.
- **S-F6 Session-only receipts** (S1-C S-3) reach DEL-11-03 OUT-002 through DOS DF-5. This is a basis-level tension, not a file defect.
- **S-F7 PKG-10 is not designed.** DEL-11-01 and DEL-11-02 consume DEL-10-03 and DEL-10-01. R23-31 makes each of those one thin Design file mapping obligations to existing records (CURRENT_EXECUTION_BASIS, work graphs, run records, DAGs). Risk is low: DEL-11-01 and DEL-11-02 should cite those same records rather than define a consumer map of their own (F-R11). Their account forms can be built now; their row contents follow DEL-10-03's file.

### E5. Proposed early unit: **EU-F1, one replacement decision package, assembled from the suppliers' dossiers and read, with the decision pending**

**Why this unit.** DEL-11-03 is where the cluster meets: DEL-09-02, DEL-09-07, DEL-09-12, DEL-11-01 and DEL-11-02 all feed it. The premise most likely to invalidate dependent work is that the two tranche-1 dossier handoffs, a continuity input and a practitioner standing compose into one decision the owner can actually make: one candidate subject (S-F1), seven core-loop elements against a named v3.0.1 baseline (F-R2), the journey's DH-1 standing, and a package shape that fits a project-level reserved decision (S-F2, F-R4). If any of these fails, SQ, DOS, EXP or DEL-02-03's schema needs revision. That is better learned before four Design files are written.

**Path, from authoritative input to consumption.**

1. **Inputs, read only:** REFERENCES §2 (the baseline identity; real); the thesis tree check (C-5; real); `sq.dossier.valid.examples.json` and `lhq.dossier-manifest.valid.examples.json` (test-double standing, labelled); PRD §8 and EXAMINATION §7 (the reserving basis); a first-cut DEL-11-01 continuity handoff and a DEL-09-12 standing ("OI-016 (App v4) not agreed; no validation in use"), both written in the unit as the interfaces under test; DEL-11-02's adoption status "not supplied".
2. **Production:** a packet manifest (OUT-001 seven-element table, OUT-002 journey table, candidate reconciliation, standings, open matters with owners) and a package file in R23-24 shape whose `subject` names the candidate and the manifest by sha256, with the F-R5 alternatives and their consequences.
3. **Cheap checks where defects enter:** the package file validates against DEL-02-03's `decisionPackageFile`; the two examples validate against their own schemas; a prototype applies the packet rules: (a) no "core loop met" while any element lacks an applicable `candidate` `pass` (VER-001); (b) no joining of results from different App candidates without a change-impact record (VER-003); (c) DH-1 as written; (d) no claim of replacement qualification unless both obligations hold (AX-001); (e) practitioner standing shown and never used as a condition (F-R3). Each rule gets a negative case.
4. **Recording:** a recorder writes the `act_request` (CE-4) for the package, with no decision. The disposition record reads *pending* with "v3.0.1 remains the fallback". No owner act is requested (VER-004: "No new human act is requested merely to run this check").

**Consumption check.** An isolated reader (fresh `type2-opus-high`, dispatched as RR-E and RR-F were, given only the input-set manifest) answers fixed questions from the files alone:
- what is to be decided;
- on which candidate;
- which obligation holds, which does not, and why;
- what is missing, and who supplies it;
- what each alternative would change, including the release and retirement it would not make;
- that v3.0.1 remains until an attributable act exists.

An examiner compares the account with the expected answers, as in RR-F. The unit passes when every answer matches with nothing referred, all the schema and rule checks hold, and every negative is refused. Any mismatch is traced to its supplier interface (SQ, DOS, EXP, DEL-02-03 or the first-cut DEL-11-01 or DEL-09-12 handoff) before the four designs expand.

**Write area this would need** (for HELP_HUMAN to set): a prototype folder under the run (for example `RUN/F/`), and DEL-11-03's `Design/` for the first-cut schemas. Nothing in tranche-1 files is edited by the unit; findings against them return to O-A, O-B or O-C.

**The first independent branch, which can run alongside:** the DEL-11-02 D-GOV-52 trace (B5, F-R16). It uses only real records and does not depend on EU-F1.
