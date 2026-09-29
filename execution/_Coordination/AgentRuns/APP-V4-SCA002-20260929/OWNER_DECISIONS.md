# Owner decisions — APP-V4-SCA002-20260929

## Direction to start (owner, exact, 2026-09-29)

**Question.** "Should you run a closure audit on SCA-V4-001 first or can we
run the audit after you complete SCA-V4-002 and determine if a DAG-003 is
required?"

**Recorder's proposal.** Run it now:

1. In parallel: the SCA-V4-001 closure audit, and preparation of
   SCA-V4-002's package, folding in any gaps the audit finds.
2. The SCA-V4-002 checkpoints.
3. REVISE the affected SoWs and re-extract.
4. DAG-003 for owner acceptance, if the new arcs are confirmed.
5. SCA-V4-002's closure audit.

**Owner:**

> "Proposal accepted.  Proceed accordingly."

## Scope of SCA-V4-002, as decided so far

The sources are APP-V4-BASIS-ALIGN-20260928 DECISION-8 and DECISION-10.

1. DEL-10-03 ScopeOfWork REQ-005: "the minimal local-first host loop".
2. "Consumes" sentences, where the dependency is real, for:
   - N-18: DEL-02-01 → DEL-03-02;
   - N-21: DEL-02-03 → DEL-03-02;
   - N-24: DEL-02-03 → DEL-03-03;
   - X-1: DEL-02-03 → DEL-01-04.
3. Carried text items:
   - the DEL-09-07, DEL-01-04 and DEL-02-02 SoW text on OI-001/002/012;
   - the DEL-03-03 CLM-002 tail;
   - the A17b line join in HOST_INTEGRATION.
4. **To be proposed at group 1, not assumed** (V13 F3): the Open_Issues
   OI-001/002 status.
5. Record fixes V13 raised:
   - F2: `_ScopeChange/_LATEST.md` needs `Latest:`/`Updated:` lines;
   - F1: the group-3 manifest label, disclosed but not rewritten.

The SWBPIPE handoff "local-first" note is carried with the next relay to
SWBPIPE. It is not part of this amendment.
