# Research Evidence Contract

## Evidence quality

| Level | Meaning |
|---|---|
| `R0` | unsupported claim, allowed only as a labeled hypothesis |
| `R1` | retrieval hit or inherited lead |
| `R2` | accepted ledger or register row |
| `R3` | accepted row plus source reference or source section |
| `R4` | multiple accepted sources or atoms converge |
| `R5` | an accepted snapshot or gate decision explicitly records the claim |

Prefer `R3` or better for final material claims. `READ` supports inspected artifacts; `RUN` supports an executed result. Do not describe a test, validator, query, or build as successful without `RUN` evidence.

Every evidence row records `VerificationSource` as `LIVE_TREE`, `RETRIEVAL_INDEX`, or `INHERITED_BRIEF`; `AssertionMode` as `READ` or `RUN`; and `LoadBearing` as `TRUE` or `FALSE`.

## CSV schemas

```text
Evidence_Map.csv:
EvidenceID,ClaimID,EvidenceLevel,SourceKind,ArtifactPath,SourceDocID,SourceRef,AtomicUnitID,SectionID,CategoryID,KnowledgeTypeID,SubjectID,RetrievalMode,Rank,Score,QuotedOrParaphrasedEvidence,Interpretation,Limitations,VerificationSource,AssertionMode,LoadBearing

Query_Log.csv:
QueryID,UTC,DomainRoot,Snapshot,Mode,Query,Filters,K,ResultCount,Notes

Conflicts.csv:
ConflictID,ClaimID,ConflictKind,Description,Contenders,SourceRefs,ProposedAuthority,HumanRuling,Limitations

Amendment_Candidates.csv:
AmendmentID,ClaimID,CandidateKind,TargetSurface,CurrentState,ProposedChange,EvidenceRefs,LoadBearing,VerificationSource,RecommendedRoute,HumanRuling,Limitations

Open_Questions.csv:
OpenQuestionID,ClaimID,Question,WhyItMatters,EvidenceNeeded,Status
```

Valid amendment candidate kinds are `NEW_ATOM`, `SCOPE_GAP`, `KTY_REMAP`, `CATEGORY_CONFLICT`, `SOURCE_UPDATE`, and `VOCAB`. Leave `HumanRuling` as `TBD` unless an accepted ruling is part of the supplied basis.

## Research note

`RESEARCH_NOTE.md` begins with `Status: DERIVATIVE_RESEARCH_PACKET` and contains Question, Accepted Basis, Short Answer, Evidence, Interpretation, Caveats, Open Questions, and Handoff / Next Action sections.

The handoff records packet status, accepted basis, retrieval snapshot and freshness, load-bearing claims, conflicts, amendment candidates, caveats, and explicit coverage gaps for a partial run.
