# Rulings — APP-V4-GRAPH-CLOSURE-20261004

These are HELP_HUMAN's rulings on shared premises for this run. The file is
append-only, and rulings are cited by ID. Each ruling quotes its source and
decides no more than that source settles.

- **GC-1 When a slot inversion (IV-S) removes a contract input (RVG-C2 M1).
  INTEGRATION.**
  Sources:
  - DAG-004 GRAPH_BASIS, edge semantics: "The consumer requires the
    supplier's stated contribution, at the stated maturity or condition,
    before the stated part of its work."
  - CYCLE_DRIVEN_RESOLUTION §2 rule 3: "**Invert** a dependency behind a
    contract/interface so the edge reverses."

  A consumer that carries a supplier's values "by reference" no longer
  requires the supplier's contribution before its own part only when both
  conditions hold:
  1. **(a) The reference is opaque to the consumer.** The consumer's Design
     uses no field, state value or identity scheme that the supplier
     defines.
  2. **(b) Conformance is checked outside the consumer's definition.** The
     supplier or a third party checks it, or the consumer's own check is
     recorded as a verification row (V), which stays a register obligation
     at its point of need.

  Where (a) fails, the row remains an interface row (I). The move is then an
  ownership-moving inversion (IV-O), a decomposition or a merge, unless the
  consumer's Design is reworded so that (a) holds. A rewording is a design
  change by the deliverable's design agent, and it is reviewed.

- **GC-2 Correction: "Q-5" does not say DEL-04-01 gains no supplier
  (RVG-C2 M2). INTEGRATION.**
  - **What Q-5 decided.** The owner's Q-5 (SCA-V4-003 OWNER_DECISIONS.md)
    accepted "the App act control in DEL-01-04, with REQ-008 as adjusted and
    the drafted OUT-005, AC-008 and VER-008, as worded".
  - **What it does not decide.** "DEL-04-01 gains no supplier" was the
    drafter's description of that one change, not an owner decision.
    HELP_HUMAN repeated it to the C2 agent and in a report to the owner. That
    was HELP_HUMAN's error, and it is corrected here.
  - **The open question.** Whether DEL-04-01 has suppliers is decided by
    its own ScopeOfWork and registers. ACT §5.1 takes grant state from
    DEL-04-02, and checkpoint state from DEL-02-01, DEL-02-03 and DEL-05-01.
    Whether those inputs are interface rows (I) or runtime evidence (E) under
    G1 r2's K-3 is open. It is analysed by C2 and checked by RVG, not
    assumed.

- **GC-3 An uninterpreted identifier is an opaque reference (RVG-C2
  Addendum A, B-M1). INTEGRATION.**
  Sources: GC-1 (a), "The consumer's Design uses no field, state value or
  identity scheme that the supplier defines", and the DAG-004 edge
  semantics.
  1. Carrying a supplier's identifier satisfies GC-1 (a) when all of these
     hold for the consumer:
     - it types the identifier as an uninterpreted string, with no pattern,
       format, enumeration or structure taken from the supplier;
     - it neither constructs, parses nor validates the identifier against
       the supplier's scheme. Equality comparison of the whole string is
       allowed;
     - its Design names who resolves the identifier, and that is the
       supplier or a third party, not the consumer.
  2. Each rewording that relies on this rule says so in its own text. It
     states that the identifier is uninterpreted and names its resolver.
  3. When a consumer needs any part of the identifier's structure (for
     example the kind, origin and revision of a workflow identity), the
     row stays I. A move must then come from elsewhere.

- **GC-4 Integrator rulings that the SCC-002 rewordings would amend
  (RVG-C2 Addendum A, B-M2). INTEGRATION.**
  1. The rewordings that rely on them would amend:
     - R-9: "workflow identity is carried everywhere as {kind, origin,
       source root, name, revision}";
     - R14-1: "Every CE kind gets an RS entry kind" and "RS states the
       mapping".
  2. These are HELP_HUMAN integrator rulings from earlier passes. Amending
     them is HELP_HUMAN's act, made when the rewordings are applied after
     checkpoint 1. Each amendment is listed in the owner-facing checkpoint,
     so the owner sees it. None is an owner decision.
  3. R-8, R2-6 and R-3 point 6 already allow P17's rewording, so no
     amendment is needed for them. R12-4 already allows the rewording that
     closes P10.
