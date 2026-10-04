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

- **GC-5 When a Design-to-Design use counts as a dependency (RVG-ACT51
  ACT-M1). INTEGRATION.**
  Sources:
  - `loop/LOOP_INIT.md`: "keep the ScopeOfWork at the level of
    obligations, depended-on interfaces and examination";
  - DEL-10-04 ScopeOfWork: "A reference or ownership link becomes a
    production dependency only when the cited source establishes the
    specific required exchange or constraint";
  - DAG-004 edge semantics;
  - the owner's criterion: work proceeds "in parallel … without many or
    any conflicting outcomes".
  1. **A dependency.** A consumer's Design use of another deliverable's
     content is a dependency, whether or not any ScopeOfWork states it,
     when the consumer needs that content to define or produce its own
     part. These are G1 r3's K-2 and K-4 tests: rules, vocabularies,
     states, identity schemes or artifacts that the consumer's own rules
     or outputs depend on.
  2. **Not a dependency.** These are not dependencies:
     - an attribution, cross-reference or example;
     - an uninterpreted identifier under GC-3;
     - a citation of an integrator or owner ruling whose own text carries
       the content.

     A citation of a ruling that only directs where the content lives
     (for example R4-7 or R-7) does not count under this item. The use is
     then judged by item 1 against the Design that holds the content.
  3. **What happens to a dependency.** A use that is a dependency under
     item 1 is either removed by an accepted move (a rewording, invert,
     cut or merge), or carried into the consumer's ScopeOfWork as a
     depended-on interface (S1) and so into the register. Leaving it in
     the Design while absent from ScopeOfWork and register is not
     acceptable: the graph would change as soon as it was found.
  4. **Consequence for this run.** G2 matched by `DEL-` identifier and
     section labels. Its own limits note that abbreviation-only citations
     (for example "RS R3") could be missed, and ACT shows the gap is
     material. A complete, abbreviation-aware inventory of cross-
     deliverable Design uses (G2b) is therefore a closure condition. Each
     case's "no new row" conclusion is provisional until G2b reports.

- **GC-6 No narrowing to close a cycle (RVG2 C7-M2, C6-M1; recurring).
  INTEGRATION.**
  - **Sources.** The coordinated-knowledge-work workflow says: "If
    satisfying an expectation would require removing, narrowing, or
    bypassing an existing check, pause that affected change and expose the
    conflict … a newly passing result does not justify weakened assurance."
    The doctrine (§2 rule 3) adds that cut and merge are human-gated.
  - **Recurrence.** Two design agents analysing cycles in their own
    deliverables proposed rewordings that narrowed what their own Designs
    receive or check. In each case the cycle then closed on paper. RVG2
    caught both.
  - **Rule 1.** A move that removes or narrows an obligation, an input the
    Design needs, or a check is not an invert or a rewording. It is labelled
    NARROW, and it reaches the owner only as part of an SCA the owner
    accepts. Where the input is genuinely needed, the move records the
    residual and names the owner act that would close it (a cut, merge or
    decomposition).
  - **Rule 2.** When the rewordings are applied, each design agent states,
    for every change, that it narrows nothing. Its reviewer checks that
    statement.

- **GC-7 Recording relationships found after 60% (supersedes GC-5 item 3).
  INTEGRATION.**
  Source: the owner's directions under "Structure versus detail after 60%"
  in OWNER_DECISIONS.md, including "better to leave some things
  underdefined and seek human judgment in the moment".
  1. GC-5 items 1 and 2 stand: a Design use the consumer needs is a real
     relationship.
  2. **What a found relationship must be.** It must be recorded where
     everyone who depends on it will see it. It need not be added to the
     ScopeOfWork or register.
     - Within a group, the group's work graph is enough.
     - Across groups, record it in the shared list that every development
       loop reads.
  3. **Register and ScopeOfWork updates.** These are made when wording would
     otherwise mislead about what a deliverable must deliver or receive.
     They are decided by the human in batches, at natural boundaries, under
     SPEC §5.4's departure rule.
  4. **When to bring the human in at once.** The human is asked in the
     moment, not by threshold, about:
     - a relationship that seems to run against the accepted group order;
     - one that forms a cycle across groups, or changes the deliverable set;
     - one that would make another group's finished work wrong;
     - any sign that the grouping itself is wrong.

     In doubt, ask.
  5. **No fixed thresholds.** This ruling sets none. It rests on one
     project's experience and is to be revisited as loops report.

- **GC-8 Cross-group relationships go in the affected work graphs, not a
  new list (supersedes GC-7 item 2's "shared list"). INTEGRATION.**
  Source: the owner's words, "I don't want to create a new type of record
  that needs to be updated to maintain current state. … The present forms
  of governance presumed sufficient until shown otherwise."
  - A relationship found between two groups is recorded in the work graph of
    each affected loop: the one that found it, and the other group's.
    There, each loop sees it at entry.
  - Where the other group has no active work graph yet, the relationship is
    recorded in the finding loop's graph. It is carried into the other
    group's graph when that loop constructs it.
  - No `CROSS_GROUP_RELATIONSHIPS.md` or other new standing list is created.
  - GC-7's other items stand.

- **GC-9 Decisions for the LOOP_INIT revision (LI audit). INTEGRATION.**
  1. **Change control covers every deliverable.** It is not limited to
     group A. Agreed interfaces in any deliverable's Design are changed only
     through named, reviewed changes that are propagated to their consumers.
     This replaces LI's inference that "the contract core is group A". The
     owner's approval named the co-designed core, and the manuals already
     state "Agreed contracts frozen under change control" in general terms.
  2. **GROUPS.md stays in this run's folder**, as the record of the gate
     decision. LOOP_INIT points to it. A later regrouping decision is
     recorded by its own run, and LOOP_INIT's pointer is updated then. No
     standing current-state file is created; see the owner's "I don't want
     to create a new type of record".
  3. **Agent User Manual additions:**
     - adopted: A1 (receipt content, §13), A2 (App v4 entry, §14, plus the
       README description), A3 (gate sentence) and A5 (decision recording,
       §13);
     - not adopted: A4, a workflow change that is not needed because
       LOOP_INIT states App v4's adoption of the receipt location; and A6,
       because the principles paragraph stays in LOOP_INIT.
