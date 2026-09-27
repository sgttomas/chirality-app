# T9: PEC and Domains as App connectors (read-only investigation)

**Refs read:** investigation revision `2b0572fe0`; `origin/main` = `d97fb75a9` plus later PEC commits up to `4dcc2c6a8`. Of the remote `origin/claude/pec-*` branches, only one is ahead of main: `origin/claude/pec-sca006-cp2-package` (`5799a559b`, 12 commits). I also read the pre-separation tree `1c5945c4c:domains/` and the ignored material in ORIG (`/Users/ryan/ai-env/projects/chirality`, on `main` at `06aff05a4`).

**Boundary kept:** nothing was written and no state-changing git command was run. SQLite catalogs were opened read-only (`mode=ro`). No content under `piping-design/_Sources` was opened; I only listed its structure and formats, plus the `_LATEST.md` pointer and the proof-case README from git history.

## Summary

1. **"Domains" is most probably the domain-pack effort** [agent inference]. These are knowledge corpora, each with a domain decomposition (atom ledger, then Category / Knowledge Type / Subject) and a derived BM25-plus-vector retrieval index. The corpora moved on 2026-08-20 to a separate private repository, `sgttomas/chirality-domains`. Three of the four packs index *project repositories*: the Chirality repo, `projects/chirality-app-dev` and `projects/chirality-piping`. This is already a working version of the thesis §4.3.5 "knowledge decomposition over the file directory plus BM25/vector search". The word "domain" has two other meanings in the repository, one of which includes PEC. **The owner should confirm which is meant.**
2. **PEC** prepares a read-only, rebuildable, non-authoritative projection of loop files, in two tiers:
   - **Record tier:** orientation, deltas, gate verdicts, the "Waiting on you" decision slate, work graphs, run records, drift findings.
   - **Presence tier:** sessions, worktrees, scope claims.

   It is designed for a local Unix socket, token-scoped. On `origin/main` only foundations exist: an API *envelope* schema, the loop registry v1, a SQLite store with a content guard, and a posture check. There is no reconciler, no server and no dashboard yet.
3. **Independence holds at the code and data level.** Neither side references the other, and no domain catalog indexes `projects/pec`. Coupling risk comes from three places: shared naming (PEC is registered as a "Domain Engine"), a shared substrate (both are derived projections over the same Git-tracked project files), and v4's PM features writing the very file grammars PEC parses.

---

## A. Domains

### A.1 Three meanings of "domain" in the evidence

| Meaning | Where | What it is | Status |
|---|---|---|---|
| **1. Domain packs (knowledge corpora)** | `domains/<name>/` until 2026-08-20; now the private repo `sgttomas/chirality-domains` | Source corpus, `_Decomposition` (ledger and registers), `_LocalIndexes` (retrieval) and `domain-pack.yaml` | Externalized; ignored in Chirality (`.gitignore@2b0572fe0` L63–64: "Domain corpora are maintained in the separate private chirality-domains repo") [implemented] |
| **2. Domain engines** | `_DomainEngines/` (Root, tracked) | Deterministic engine profiles: `open_pipe_stress` (OpenPipeStress, the SWBPIPE lineage) and **`pec`** | `pec` is ADOPTED / READ_ONLY (`_DomainEngines/DOMAIN_ENGINE_INDEX.md@origin/main` "Registered domain engines"); profile at `_DomainEngines/profiles/pec.yaml@origin/main` [accepted requirement] |
| **3. Host "domain truth"** | v4 conceptual D-07 | The engineering host's own project store (SWBPIPE) | `projects/chirality-app-v4/conceptual/DECISIONS.md@HEAD` row D-07 [owner words, accepted proposal] |

Meaning 2 includes PEC in several places:
- the App's code registers `pec` as a domain-engine profile (`projects/chirality-app-dev/frontend/src/lib/harness/mcp/domain-profile-registry.ts@origin/main` L1–13, L86–111) [implemented];
- PEC's own manifest lists it under `profiles.domain` (`projects/pec/chirality.project.json@origin/main`) [implemented].

**Reading** [agent inference]: the owner said "Neither depends on the other" (D-08, `DECISIONS.md@HEAD` L54). If "Domains" meant meaning 2, PEC would be one of the Domains, which contradicts treating them as two independent connectors. Meaning 1 fits the statement. It also matches the owner's 2026-09-19 words on knowledge decomposition and BM25/vector search (`plans/evidence/2026-09-19_owner_words_four_graph_structures.md@origin/main`, hash `dffb7629…`).

**Unresolved:**
- whether "Domains" also covers the domain *engines* for SWBPIPE (OpenPipeStress);
- whether the "Domains" being prepared now is the June-2026 pack format or a successor. Nothing in this repository shows Domains work after 2026-08-20; any such work would be in the inaccessible private repo.

**Flag for the owner.**

### A.2 What a domain pack is

- **Manifest** [implemented, historical]: `domain-pack.yaml` (`1c5945c4c:domains/*/domain-pack.yaml`) declares `local_roots` (sources, decomposition, coordination, vocabularies, indexes). Packs over repositories also declare `source_repo_root`, for example `../../projects/chirality-app-dev`, and cite sources as `@repo/<path>` rather than copying them.
- **The four packs** (pre-separation file counts from `git ls-tree -r 1c5945c4c`):

  | Pack | Files | Purpose, per its README or description |
  |---|---|---|
  | `chirality` | 2,606 | "retrieval-first self-knowledge"; README: "treats the live repository as the source of truth" |
  | `chirality-app-dev` | 1,823 | the App repository |
  | `chirality-piping` | 2,498 | the OpenPipeStress repository |
  | `piping-design` | 29,523 | external engineering handbooks |
- **Decomposition status** at separation [executed check (record)]:
  - `chirality` Gate 6 accepted 2026-06-15 (`1c5945c4c:domains/chirality/_Decomposition/gate_snapshots/_LATEST_GATE6.md`);
  - `chirality-app-dev` Gate 6 accepted 2026-06-16 (commit `e22321fe0`);
  - `chirality-piping` "COMPLETE (all 6 gates accepted)" 2026-06-17 (commit `e998e2888`);
  - `piping-design` has only an archived Gate-1 proof-case from 2026-05-16. Its README says "Not the start of the next decomposition… corpus is being expanded" (`1c5945c4c:domains/piping-design/_Decomposition/.proof-case/README.md`).
- **Externalization** [executed check (record)]:
  - tranche `ROOT-DOMAIN-REPOSITORY-SEPARATION-20260820` (`docs/governance_harness/tranche_manifests/…20260820.yaml@2b0572fe0`): 36,450 tracked files, 1.03 GB, snapshot-only history, destination `sgttomas/chirality-domains`;
  - validation (`execution/_Coordination/AgentRuns/ROOT_DOMAIN_REPOSITORY_SEPARATION_2026-08-20/VALIDATION.md@2b0572fe0`): private visibility, HEAD `5f4c6ffd…`, four `chirality.project/v2` manifests; "The private repository ignores future raw `_Sources` binaries, local indexes…";
  - commit `f99deaff0` added external domain working-root support to the Runtime project registry and the source-catalog tools [implemented].

### A.3 Inventory of `ORIG/domains/` (local ignored residue; read 2026-09-25)

| Folder | Local contents | Files | Size | Index snapshots and types |
|---|---|---|---|---|
| `chirality/` | `_LocalIndexes` only (no `_Sources`, no `_Decomposition`) | 142 | 528 MB | 12 snapshots, 2026-06-14. Latest `SRCIDX_20260614T204703Z`: 500 artifacts / 274 source docs / 29,843 chunks; SQLite catalog + CSVs + BM25 (`bm25s`) + dense (`bge-base-en-v1.5`, 768-d, NumPy); status READY |
| `chirality-app-dev/` | `_LocalIndexes`; `_Decomposition/_adapter/__pycache__/` (5 `.pyc`: gate3/4 assign and ratify, gate5 coverage) | 29 | 211 MB | 4 snapshots, 2026-06-16 (one empty, one catalog-only). Latest `…043733Z`: 660 / 547 / 20,398; BM25 + dense; READY |
| `chirality-piping/` | `_LocalIndexes`; empty `_Decomposition` | 16 | 299 MB | 2 snapshots, 2026-06-17 (one empty). Latest `…014930Z`: 1,210 / 995 / 36,263; BM25 + dense; `_index_build.log` records a 4-step build via fastembed |
| `piping-design/` | `_Sources` (6 source folders + 5 `*_pdf2md_work`) and `_LocalIndexes` | 7,442 | 5.9 GB (`_Sources` 5.7 GB) | 1 snapshot `…20260619T032014Z`: 29,506 artifacts / 6 source docs / 48,200 chunks / 357 audit rows. **BM25 only**: no embeddings, and `meta.json` has no `retrieval_index` block |

Additional notes on the local residue:
- `piping-design/_Sources` locally holds 7,434 files, almost all PNG (page renders, figures, tables, images, audit). The Markdown, JSON and XLSX that its index catalogs (for example `PAGE_MARKDOWN` 13,264 and `TABLE_XLSX` 1,268 per `QA_Report.md`) are not present locally.
- Every `_LATEST.md` states `Schema: chirality-source-db/v2`, `Derived-only: true`.
- **Indexes are stale and orphaned locally** [executed check (record), my read-only spot check]:
  - `meta.json` embeds absolute `domain_root` and `source_manifest` paths under `domains/*/_Sources/…`, which no longer exist;
  - the `chirality` snapshot's SHA-256 for `@repo/AGENTS.md` (`2bf5e0aa…`) differs from the current file (`c8ce87ef…`);
  - 220 of 467 `@repo/` artifacts in the app-dev snapshot are missing from ORIG's `projects/chirality-app-dev`.

### A.4 Index format, builders and query interface

- **Catalog** [implemented]: `tools/source_catalog/build_source_database.py@2b0572fe0` (843 lines) writes `catalog.sqlite` with the tables `source_docs`, `artifacts`, `audit_state`, `chunks`, `index_rows` and `index_builds`. Chunks carry `category_id`, `knowledge_type_id`, `subject_id` and `atomic_unit_id`, plus `source_ref` (for example `@repo/AGENTS.md:L0003|…SRC-AGENTS.html#SEC-RT001-0001`). Chunk types are `LEDGER_ATOM`, `SECTION_NODE`, `MARKDOWN_SECTION` and `AUDIT_SIDECAR`.
- **Retrieval** [implemented]: `tools/retrieval/build_source_index.py` (BM25 via `bm25s`, k1 1.5 / b 0.75; `fastembed` BAAI/bge-base-en-v1.5; NumPy cosine; `--no-embeddings` for lexical only).
- **Query** [implemented]: `tools/retrieval/query_source_index.py` (494 lines):
  - modes `hybrid` (reciprocal-rank fusion, `RRF_K = 60`, L48), `dense` and `bm25`;
  - filters on source doc, artifact role, chunk type, audit kind, category, knowledge type, subject and archive state;
  - `--json` output;
  - optional append to `Query_Log.csv` (L82–113).

  The public result contract is stable IDs and provenance (`chunk_id`, `artifact_id`, `source_doc_id`, `rel_path`, `source_ref`, structural IDs, ranks and scores, preview); row numbers are internal (`tools/retrieval/README.md@2b0572fe0` "Query") [described design].
- **Freshness** [implemented]: `tools/source_catalog/check_snapshot_freshness.py` re-hashes the indexed artifacts. It reports FRESH or STALE (exit 0 or 1) and does not rebuild. New, unindexed files are out of scope (docstring L1–29).
- **Tests** [test defined]: `tools/retrieval/test_query_source_index.py`, `tools/source_catalog/test_*.py`. At separation, 320 validation and source-catalog tests passed (VALIDATION.md) [executed check (record)].
- **Rebuild policy** [described design]: snapshots are immutable and `_LATEST.md` is a mutable pointer (README "Rebuild Policy").

### A.5 Workflows that produce and consume Domains

The pipeline, as far as it can be reconstructed [described design]:
1. `pdf2md*`, then per-kind source audit.
2. `domain-decomp` (WORKING_ITEMS): one pre-atomization checkpoint and three post-atomization checkpoint groups. It produces immutable `checkpoint_snapshots/` with `ACCEPTED_MANIFEST.csv`, `HANDOFF_STATE.md` and `_LATEST_ACCEPTED.md`. The Domain Ledger is "authoritative for atom truth" (`workflows/domain-decomp/resources/contract.md@2b0572fe0` invariants and glossary).
3. `domain-source-atomize` (per-slice TASK).
4. `domain-documents`: one `KA-*` Knowledge Artifact per Subject. KAs are "contextual enrichment for HBA-anchored retrieval" (`workflows/domain-documents/WORKFLOW.md` §Relationship).
5. `domain-hypergraph`: a derivative graph snapshot under `_Aggregation/Hypergraph`.
6. `researcher` and `research-orchestration` consume the index.

The consumer rules are in `workflows/research-orchestration/resources/contract.md@2b0572fe0` L44–50:
- accepted decomposition truth comes first;
- structure and similarity are kept separate ("Semantic similarity results are not membership proof");
- read-only by default;
- **no silent refresh**.

`tools.md` L5–8 orders the steps: freshness scout, then an immutable `RCH_*` packet, then logged queries. `domain-prose-validate` is a page-level extraction check. `content-digest` is a deliverable digest and is not domain-specific.

SPEC registers `_LocalIndexes/` as a tool root for "Derived source-catalog and retrieval snapshots (domain packs)" (`docs/SPEC.md@2b0572fe0` L170) and allows `{DECOMP_ROOT}` to be "a domain pack's `_Decomposition/`" (L86) [accepted requirement].

### A.6 Discrepancy with the thesis

Thesis §4.3.5 (`docs/thesis/04_architecture.md@2b0572fe0` L148) says of the knowledge decomposition, graph structuring and BM25/vector tool: "None of the three is built." The evidence shows two of the three existed in June 2026 for project-repository corpora [executed check (record)]:
- a decomposition over repository files;
- a BM25 + dense search tool called through `researcher` and `research-orchestration`.

What is missing:
- the graph structuring, beyond `domain-hypergraph`'s derivative snapshot;
- currency, because the indexes date from June 2026 and are orphaned;
- in-repository availability, because the corpora are external.

[agent inference; the thesis wording is the owner's and agent-drafted, so the owner should reconcile it.]

---

## B. PEC

### B.1 Product definition and tiers (`projects/pec/docs/PRD.md@origin/main`, v2.3, adopted 2026-09-25, D-PEC-92)

- **Thesis** [accepted requirement]: a "deterministic, rebuildable projection of governed file truth, plus an ephemeral presence layer", covering Step 0 and the deterministic parts of Step 1. It is "the coordination plane that does not need to exist" (§1.1).
- **Non-goals** [accepted requirement], §4.2:
  - not a system of record;
  - no ruling write path;
  - **"Not an orchestrator. No dispatch, no queues, no execution"** (L163);
  - **"Not a human project-management tool"** (L173);
  - not a Git actor.
- **Record tier** (§7.1, L234–249; citable with sources): Loop, Receipt, DecisionRow (identity and status only), Fence, Package/Deliverable census from `_STATUS.md`, DependencyEdge, RunRecord, CandidateBrief (the "work-selection queue"), OrientationSnapshot, DriftFinding, WorkGraph/WorkNode (from `execution/_Coordination/WorkGraphs/<undertaking>/WORK_GRAPH.md`, content-minimal).
- **Presence tier** (§7.2; TTL'd, never citable): Session, Worktree/GitRef, PresenceRecord, HierarchyEdge (deferred), ScopeClaim.
- **Invariants** [accepted requirement]:
  - K-01: graceful absence, plus a kill test at every release;
  - K-02: files govern;
  - K-03: pull-oriented, consumer-owned use;
  - K-04: every response carries the examined-through SHA and per-feed freshness;
  - K-05: the two tiers are never blurred;
  - K-10: content-minimal, meaning "Paths, counts, SHAs, states, hashes — never file or diff content" (L210–219).

### B.2 The consumer interface: chain of decisions

| Instrument | Effect | Label |
|---|---|---|
| **D-PEC-67** (2026-07-27), `_DECISIONS/D-PEC-67_od7_g3_boundary_dispositions.md@origin/main` | Adopts the exact PEC-K-03 (pull, consumer-owned; verify-before-rely *as then worded*) and PEC-K-11 (mode-capable, never forced) rows. Keeps Unix-only transport (ET-C). Defers the global feed, auth reuse and the event-contract home. Activates the L-A1 reliance-hold control | [accepted requirement] |
| **API v1 schema**, `projects/pec/v2/contracts/api/v1/schema.json@origin/main` (91 lines) | **Envelope only:** `CapabilityRequest {api_schema_version:1, capability, use_case, input:object}` and `CapabilityResponse {…, outcome: ok\|error, output:object}`. Actual shapes are "defined by a versioned capability contract", and none exists yet. Additive-evolution tests in `v2/tests/contracts/api/` (D-PEC-74; DEL-08-02 `CHECKING`) | [implemented] [test defined] |
| **D-PEC-90 R-A** (2026-09-25), `D-PEC-90_RULING_2026-09-25.md@origin/main` | Owner: "D-PEC-90: R-A." and "agents may eventually query PEC directly, yes. Through tool calls." Operational reliance on record-tier claims "as of the examined-through commit", within four bounds: pinned, coverage-honest, record tier only for correctness, file fallback. Authority unchanged. "Reliance begins at a PEC release whose gates prove the conditions… not now." The L-A1 hold is untouched | [owner words] [accepted requirement as direction] |
| **SCA-006 CP1** (2026-09-25), `_ScopeChange/checkpoint_snapshots/SCA-006_GROUP-1_2026-09-25/DECISION.md@origin/main` | Owner: "SCA-006 CP1: accept; DQ a; ENV a; BUD a; GATE a; INS a; R-C excluded". Selected: a new read-only **`agent` access class**; PEC-ORI-007 (the reliance envelope); PEC-API-006 (response size budgets); a standing §12 reliance-advertisement gate. It authorizes checkpoint-2 preparation only | [owner words] [accepted requirement at impact level] |
| **SCA-006 CP2 candidate**, branch `origin/claude/pec-sca006-cp2-package@5799a559b`, `…/CP2_CANDIDATE/docs/PRD.md` | PRD v2.4 **candidate** with the §8 "agent" bullet (L298–304). ORI-007 (L331): pin, per-feed coverage and freshness, per-claim tier, a file-fallback signal, and "No consumer may treat silence as a claim". API-006 (L384). **PEC-API-007** (L385): a read-only tool-call query interface under the `agent` class, which requires a tier-0 amendment of `pec.yaml` first. The reliance gate is at L451–460. Its status line is pre-written as "Adopted…"; it is **not accepted** (CP2 unruled) | [described design] |
| **D-PEC-95** (P + R) | Revision-1.5 metadata currency (119 paths); no interface change | [accepted requirement] |
| **D-PEC-96** (revision 3) | Loop-registry schema v2 with closed feed profiles (`shared-dev-loop` live, `remaining-items` live, `loop-receipts-ledger` and `agentruns-json` historical). **PROPOSAL / AWAITING_RULING** (`_REGISTER.md@origin/main` D-PEC-96 row) | [described design] |

Also relevant [described design]: PEC reads each loop's files through **feed profiles declared in PEC's own registry**, which are "PEC's reading hypothesis, never the loop's truth" (PRD §16.3). It does *not* read the App's `_harness/adapter.yaml` as a manifest; that file is read only as a parity peer (`projects/chirality-app-dev/execution/_Coordination/NOTICE_2026-09-25_PEC_SCA-005_ADAPTER_YAML_FEED_SURFACES.md@origin/main`).

### B.3 Transport

- **Designed** [accepted requirement]: "local-only, Unix socket by default, with token-scoped access; any loopback TCP listener is a §16 open decision" (PEC-API-001, L349). Also an SSE subscription for deltas and presence (API-005) and p95 ≤ 100 ms orientation reads (API-002). The token mechanism (§16 item 6) and the event-contract home (§16 item 9) are open.
- **Not implemented:** no socket server exists in `v2/`. `projects/pec/server` and `web` are the retired v0.4 prototype.
- **Stale App connector** [implemented (code path), historical]: `projects/chirality-app-dev/frontend/src/lib/harness/mcp/pec-bridge-client.ts@origin/main` is a D-APP-52 **HTTP loopback client on port 4810** to the v0.4 prototype's proposal endpoints (login, create/refresh/get proposal). It does not match the v2 design (Unix socket, read-only, no proposals).

### B.4 What an App connector would read (all designed, none served yet)

| Need | PEC source | Requirement |
|---|---|---|
| Orientation per loop, project or package | newest receipt, examined-through SHA, gate states, owner directions, open tranches and candidate briefs, parked lanes with the unparking act, terminal completion via PR merge reachability | PEC-ORI-001/-003/-004/-005 |
| Changes since commit X | deltas | PEC-ORI-002 |
| Coverage honesty | stated limitations for unparsed or stale feeds | PEC-ORI-006 (+ ORI-007 candidate) |
| "Waiting on you" | every AWAITING_RULING row and parked lane, linking to authored files | PEC-GAT-003, PEC-DSH-004 (L320, L362) |
| Gate verdicts | Explain-shaped, advisory | PEC-GAT-001/-002 |
| Work graphs | WorkGraph/WorkNode | §7.1 L249; RCN-002 |
| Run records | RunRecord joined on the run-identity token | §7.1 L245 |
| Drift | DriftFinding (snapshot-to-snapshot, and parity with the harness) | §7.1 L248; RCN-004/-005 |
| Lifecycle census and stuck-age | `_STATUS.md` | DSH-002 |
| Presence and collisions | sessions × worktrees × scope, heartbeat age, advisory overlaps | PRS-001..007 |

### B.5 Implementation status on `origin/main`

`projects/pec/v2/` holds 42 files [implemented]:
- the API envelope schema;
- the loop-registry adapter and port (schema v1, a single row `pec → projects/pec/loop/LOOP_INIT.md`, `v2/config/loops.json`);
- the SQLite `MetadataStore` at `.pec-v2/record_store.sqlite3` with a content-minimal guard (`v2/docs/STORE_LIFECYCLE_AND_GUARD.md`);
- the service-core posture checker.

Deliverable states (`docs/STATUS.md@origin/main` "Implementation"; README L27–42) [executed check (record)]:
- DEL-08-02 `CHECKING`; DEL-01-03 and DEL-01-05 `IN_PROGRESS`; DEL-01-06 `INITIALIZED` under HOLD;
- lifecycle census 30 `OPEN` / 26 `INITIALIZED` / 4 `CHECKING` / 2 `IN_PROGRESS` / 4 `RETIRED`, none `ISSUED`.

D-PEC-90 itself notes "no consumer surface exists yet". The current work graph (`execution/_Coordination/WorkGraphs/HELP-HUMAN-PEC-20260925-POST-SCA005/WORK_GRAPH.md@origin/main`) has G1 (registry v2) `ACTIVE` and R2–R4 (SCA-006 CP2/CP3, reliance notices) `PLANNED` [executed check (record)].

### B.6 PEC compared with v4's project-management capability [agent inference unless marked]

The v4 Q-08 option B (`projects/chirality-app-v4/conceptual/QUESTIONS.md@HEAD` L240–246) lists five features. The table matches each one against PEC.

| v4 PM feature | PEC coverage | Division of labour |
|---|---|---|
| Delegation with briefs | None. PEC is "Not an orchestrator… no dispatch" [accepted requirement]; it only *lists* CandidateBriefs | v4 (with the Runtime) authors and dispatches; PEC may display them |
| One current work graph per undertaking | Reads `WORK_GRAPH.md` content-minimally; node state is "declared activity, never a liveness assertion" | v4 writes the graph as a file; PEC projects it across loops |
| Queue of returns awaiting examination | No explicit entity. Receipts, RunRecords and presence come closest | A gap in PEC; v4 must derive it from files itself, or ask PEC for a capability |
| Decision packages naming the act | Decision slate "Waiting on you" (GAT-003) links to authored packets; no ruling write path | v4 authors packages and records acts in files; PEC renders the cross-loop slate |
| Status across sessions | Orientation, census, presence board | Strong overlap. PEC is the designed cross-session, cross-loop view |

The D-PEC-57 packet summarizes the owner as saying "As a human-used project-management tool it has no interest". This is agent framing, marked there as "NOT A VERBATIM TRANSCRIPT" [agent inference]. The division is consistent: PEC observes and v4 acts.

---

## C. Independence of PEC and Domains

**Evidence that they are independent** [executed check (record)]:
- `git grep` finds no reference to `_LocalIndexes`, `query_source_index`, `build_source_database` or `domains/…` in `projects/pec/v2`, `docs/PRD.md` or `AGENTS.md` @origin/main.
- It finds no `pec` token in `tools/retrieval` or `tools/source_catalog` @origin/main.
- The three repository-corpus catalogs contain no `projects/pec/` artifact (case-sensitive `GLOB`). Apparent hits were "SPEC" filenames.
- PEC's registry lists only the `pec` loop.
- Domain corpora live in a separate private repository.

**Shared substrate and coupling risks** [agent inference]:
1. **Same source files, different projections.** App-dev and piping packs index project repositories, including `execution/**` and `_Coordination` files. PEC reconciles the same kinds of files. Both are "derived, rebuildable, never authority" projections under D-GOV-01 (thesis L148; PRD K-02), and both use SQLite. The only lawful coupling point between them is the file tree itself.
2. **Naming collision.** PEC is a registered *Domain Engine* (`_DomainEngines/profiles/pec.yaml`). PEC's future agent tool surface (PEC-API-007 candidate) must first be amended into that tier-0 profile. This couples PEC to `_DomainEngines`, not to Domains corpora. An App that unifies "domains" under one connector would silently re-merge them.
3. **Functional overlap in the future.** The thesis's intended index over "the application's file directory" (Domains) would answer topic queries over the same records whose state PEC answers. Both must keep "similarity ≠ membership/authority" apart from "pinned derivation ≠ authority".
4. **Root reliance wording.** Root `AGENTS.md` ("Search results and derived graphs help locate evidence; reliance remains grounded in the source records") governs both. D-PEC-90 notes that Root must confirm compatibility with operational reliance.

---

## D. Connector implications for v4 [agent inference throughout]

**A Domains connector would consume:**
- the accepted decomposition pointer (`checkpoint_snapshots/_LATEST_ACCEPTED.md`, or legacy `gate_snapshots/_LATEST_GATE6.md`), with `ACCEPTED_MANIFEST.csv` hashes;
- the ledger and registers (authoritative within the pack);
- KA documents;
- `_LocalIndexes/_LATEST.md` plus `query_source_index.py --json` (derived);
- `check_snapshot_freshness.py` for FRESH or STALE;
- research packets (`RCH_*`, `Query_Log.csv`).

Standing: the ledger is authoritative at the accepted snapshot, while the index and search results are discovery only.

The App must not assume:
- that the pack is inside the repository or reachable (it is private and external; the Runtime registers it as an external v2 working root);
- that the index is fresh (the local indexes date from June 2026, and their source paths are gone);
- that embeddings exist (piping-design is lexical only);
- that paths in `meta.json` are portable (they are absolute);
- that a similarity hit proves membership.

**A PEC connector would consume:**
- `CapabilityRequest` / `CapabilityResponse` over a Unix socket with a token (mechanism open);
- per response: examined-through SHA, generation time, per-feed freshness, per-claim citation and tier, and a file-fallback signal (ORI-003/-004/-006, ORI-007 candidate);
- the decision slate, orientation, deltas, work graphs, run records and drift findings.

Standing: operational reliance within the envelope *after* a release passes the reliance gate; never authority.

The App must not assume:
- that PEC is present (K-01; the kill test);
- that it is usable before the reliance gate;
- that presence facts support correctness;
- that PEC parses v4's file grammars (feed profiles are PEC's hypothesis, and D-PEC-96 is unruled);
- that PEC dispatches or queues anything;
- that the existing App PEC bridge (HTTP :4810, v0.4) is reusable.

**Cross-cutting:**
- v4's PM features would *write* the files PEC reads: `WORK_GRAPH.md`, `RECEIPT.md`, `MEMORY.md` run index, decision registers. Their grammar is therefore a de facto contract with PEC and needs a registered feed profile.
- Both connectors need the App to show freshness and standing to the user, and to fall back to the files when a connector is absent.

### Open questions for the owner

1. Does "Domains" mean the domain packs (knowledge corpora in `sgttomas/chirality-domains`), the domain engines, or both? PEC is itself a registered domain engine.
2. Is the June-2026 pack format (the `domain-decomp` ledger, `chirality-source-db/v2`, bm25s plus bge-base) what "preparing Domains" continues, or is there a successor? Where does the current work live?
3. Should v4 consume Domains through the existing CLI tools (`query_source_index.py --json`) or through a service interface? Who owns rebuilding and freshness?
4. Is the thesis §4.3.5 index over "the application's file directory" a Domains pack over the v4 project, and does it overlap with PEC's orientation?
5. Should v4's work graph, returns queue and decision packages use grammars PEC already reads (`shared-dev-loop` profile), and should v4 be registered as a PEC loop?
6. Should the stale App PEC bridge (D-APP-51/52) be retired from v4's basis?
7. Does the "returns awaiting examination" queue belong in PEC, which has no such entity, or only in v4?

### Gaps

- The private `chirality-domains` repository could not be read: no network, and no local clone was found.
- The actual per-capability PEC response shapes do not exist.
- I did not run `check_snapshot_freshness` (no tool execution was authorized); my staleness finding rests on hash and presence spot checks.
- SCA-006 checkpoint 2 and D-PEC-96 are unruled.
- The status of the App-dev D-APP-51/52 code in v3 releases was not verified.
