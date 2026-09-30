# Mirror and same-arc assessment — DAG-003

`MirrorComparisons.csv` lists all 56 comparisons: 54 counterpart-register mirrors and 2 same-register rows. **None is new since DAG-002**: each of the four added arcs is carried by exactly one row, so no mirror or same-arc row was added, and no existing arc changed its representative. `MirrorAssessment.csv` restates every comparison with the standing assessed in DAG-001 (40) or DAG-002 (16), and flags which fields changed since DAG-002.

## Carried assessments

| Standing | Count | Carried from |
|---|---:|---|
| NO_MATERIAL_CONTRADICTION_IDENTIFIED_IN_BOUNDED_COMPARISON | 54 | DAG-001 (38), DAG-002 (16, less the two below) |
| MATURITY_DIFFERENCE_ROUTED_TO_BOTH_OWNERS | 2 | DAG-002 |

The two maturity differences are unchanged and remain routed to their owners as non-blocking findings:

| Arc | Representative | Counterpart | Difference |
|---|---|---|---|
| DEL-03-03 → DEL-04-01 (admitted) | DEP-03-03-008, UPSTREAM PREREQUISITE, RequiredMaturity **TBD** | DEP-04-01-023, DOWNSTREAM HANDOVER, **INITIALIZED** | Neither register changed its maturity value under SCA-V4-002 (DEP-03-03-008 changed SourceRef and Notes; DEP-04-01-023 was re-quoted) |
| DEL-09-06 → DEL-04-03 (admitted) | DEP-09-06-015, UPSTREAM INTERFACE, **TBD** | DEP-04-03-031, DOWNSTREAM INTERFACE, **INITIALIZED** | Unchanged (DEP-04-03-031 was re-quoted only) |

## Changed fields since DAG-002 (17 comparisons)

For every comparison the set of differing fields (`DifferentFields`: DependencyType, RequiredMaturity, ProposedMaturity, Statement, SatisfactionStatus) is identical to DAG-002's, so no assessment's basis moved. What changed is evidence text only:

- **15 comparisons** where one side's `EvidenceQuote` now reproduces the SoW's inline-code backticks exactly (ASC-ISS-008; V12 F1): the counterpart rows DEP-04-01-022, -023 (also SourceRef on the representative DEP-03-03-008), -024, -025, -026, -027, DEP-04-02-009, -019, -020, DEP-04-03-029, -030, -031, -032, and the representatives DEP-04-02-015, DEP-04-03-024, DEP-04-03-021, DEP-04-03-022 against DEP-03-02-018, DEP-03-02-019, DEP-04-01-016 and DEP-04-02-009.
- **1 comparison** where the representative's `SourceRef` changed (DEP-04-02-007 against DEP-04-01-015).
- **1 comparison** where both `SourceRef` and `EvidenceQuote` changed (DEP-03-03-008 against DEP-04-01-023).

Every quote is an exact substring of its current SoW (DX_SCC-CHECK: 820/820 ACTIVE rows). V12 F1 is therefore closed by the register owners' re-quoting, with no arc effect.

## Arcs carried only by a supplier-side row

Unchanged from DAG-002: N-05 (DEP-04-02-021), N-06 (DEP-04-02-022), N-07 (DEP-04-02-023) and N-20 (DEP-02-01-027) have no consumer UPSTREAM row. V12 §2 read the consumer SoWs and found each warranted on the supplier's explicit statement; V12 F6 noted that SCA-V4-002 could have given N-05 and N-07 consumer-side wording. ARC_EFFECT §5 left them out of SCA-V4-002 as outside its decided scope. They remain valid under SR-6 and are noted for the independent review's semantic check; adding consumer sentences later would change no arc.

## The four new arcs

N-18 (DEP-02-01-029), N-21 (DEP-02-03-025), N-24 (DEP-02-03-026) and X-1 (DEP-02-03-027) are consumer-side UPSTREAM INTERFACE rows, EXPLICIT / HIGH, each the sole row on its arc. Two of them form reciprocal pairs with existing supplier-consuming rows (N-18 with N-B3 DEP-03-02-027; N-24 with N-27 DEP-03-03-014). A reciprocal pair is two arcs, not a mirror; each direction carries a different contribution (ARC_EFFECT §1), and both sit held inside SCC-002.

This is not a full semantic certification of the source SoWs. A contradiction found by the independent review stays a finding routed to both endpoint owners.
