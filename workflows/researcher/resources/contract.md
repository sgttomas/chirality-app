# researcher — contract

## Runtime parameters (provided by the dispatching agent; do not hard-code)

| Parameter | Meaning | Default / Notes |
|---|---|---|
| `MODE` | Literal `ORCHESTRATED` marker; echoed in the packet and return so the run is auditable as unattended | Required |
| `DOMAIN_ROOT` | Domain package to research | Required |
| `QUERY_STRING` / `BRIEF` | The bounded research question(s), plus any "established facts" the dispatcher supplies | Required. Brief-asserted facts are **leads, not warrants** (`VerificationSource = INHERITED_BRIEF`); see PROTOCOL Step 7 |
| `RESEARCH_MODE` | One of `inquiry.md` modes (`ONTOLOGY`, `SEMANTIC_DISCOVERY`, `LEXICAL_LOOKUP`, `EVIDENCE_MAP`, `CROSS_CATEGORY`, `AMENDMENT_CANDIDATE`, `EXTERNAL_AUGMENTED`) | Default `EVIDENCE_MAP` |
| `OUTPUT_DIR` | Packet destination | MUST resolve under `{RESEARCH_ROOT}`; otherwise STOP with `ERROR: OUTPUT_DIR_OUTSIDE_RESEARCH_ROOT` |
| `ACCEPTED_SNAPSHOT_PATH` | Gate snapshot to treat as the accepted basis | Required explicit accepted snapshot path from the caller |
| `RETRIEVAL_SNAPSHOT` | Source index pointer | Default `{DOMAIN_ROOT}/_LocalIndexes/_LATEST.md` |
| `LOAD_BEARING_HINTS` | Claims the dispatcher already flags as load-bearing | Optional |
| `K` / `RETRIEVAL_MODE` | Retrieval overrides | Optional |

> Use repo-relative paths where possible. Treat absolute paths as inputs. If a required
> parameter is missing, **report what is missing rather than inventing** — there is no chat
> surface in this mode.

---

## Non-negotiable invariants

- **One brief per invocation.** TASK completes one bounded research question.
- **Accepted decomposition truth comes first**, and the retrieval index is *discovery, not
  truth*. Verify against the live tree / accepted snapshot before a claim becomes a warrant
  as specified in `evidence.md`.
- **No invention.** Unsupported claims are `UNKNOWN`/`TBD`/`INFERENCE`, never asserted.
- **Recommend, never approve.** Amendment candidates and conflicts are *returned* for the
  dispatcher/human to route and rule on. TASK applies no change to accepted truth.
- **Write quarantine.** Writes go only under `{OUTPUT_DIR}` within `{RESEARCH_ROOT}`. No
  source, ledger, register, snapshot, or index is modified. Packets are writable within the assigned run and become immutable at finalization. The caller owns shared pointers.
- **No silent refresh.** TASK never rebuilds the source database or retrieval index;
  it reports the snapshot's freshness and proceeds or surfaces the staleness.
- **No silent failure.** On a transient error, return partial results with an explicit
  coverage-gaps statement (PROTOCOL Step 9).

---

## Validity

The evidence-quality rubric (`R0`–`R5`), the `:READ`/`:RUN` AssertionMode, the
`VerificationSource` enum, and the Load-Bearing Claims duties are defined in
`evidence.md` contract and apply unchanged. Summary of the load-bearing rule: a
load-bearing claim must carry an explicit `VerificationSource`, prefer `:RUN` for anything
executable/checkable, and MUST NOT reach `R3+` while its `VerificationSource` is
`INHERITED_BRIEF`.

### Valid TASK result

A valid result:
- writes an **immutable packet** under `OUTPUT_DIR` (within `{RESEARCH_ROOT}`) with canonical
  headers (the scaffolder guarantees the shape);
- logs queries via the retrieval tool, not from memory;
- records `VerificationSource`, `AssertionMode`, and `LoadBearing` on each evidence row;
- live-verifies every load-bearing claim (never inherited) before it reaches `R3+`;
- returns the structured object (STRUCTURE) with `STATUS ∈ {COMPLETE, PARTIAL, FAILED_INPUTS}`;
- when `PARTIAL`, states explicit coverage gaps rather than failing silently;
- recommends only — applies no change to accepted truth and approves nothing.

### Hard rules

- Write only under `{OUTPUT_DIR}` ⊂ `{RESEARCH_ROOT}`.
- Never rebuild/refresh the source database or retrieval index.
- Never edit accepted snapshots, ledgers, registers, decomposition files, source catalogs,
  indexes, or repository metadata.

---

## Artifacts and schemas

### Structured return object

TASK returns this object to its parent (field names align with the packet so the
return and packet agree):

```text
MODE                  # echoed ORCHESTRATED marker
STATUS                # COMPLETE | PARTIAL | FAILED_INPUTS
PacketDir             # path to the immutable RCH_<UTC>_<slug>/ packet
ShortAnswer           # 2–5 sentence conclusion
LoadBearingClaims[]   # the claims a downstream decision depends on, with R-level + AssertionMode + VerificationSource
AmendmentCandidatesRef# path to Amendment_Candidates.csv (when any rows exist)
CoverageGaps[]        # what was not covered and why (required when STATUS = PARTIAL)
Conflicts             # count + ref to Conflicts.csv
AcceptedBasis         # the accepted gate snapshot / decision basis used
RetrievalSnapshot     # the source index snapshot queried
FreshnessVerdict      # FRESH | STALE from the freshness scout
Caveats[]             # limitations, staleness notes, unresolved issues
```

### Packet members

The packet files and their CSV/markdown schemas are defined in `evidence.md`
STRUCTURE (Evidence_Map, Query_Log, Conflicts, Amendment_Candidate, Open_Questions columns;
Research Note sections) and emitted with canonical headers by
`tools/retrieval/scaffold_research_packet.py` (backed by `tools/source_catalog/research_packet.py`).
TASK populates them; it does not redefine them.

---
